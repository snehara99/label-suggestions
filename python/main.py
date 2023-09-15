import openai
import time
import os
from github import Github, Auth
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Setup
openai.api_version = "2023-08-01-preview"
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_type = "azure"
openai.api_key = os.environ["OPENAI_API_KEY"]

# GitHub API Setup
gh_pat = os.environ["GITHUB_PAT"]
gh = Github(auth=Auth.Token(gh_pat))

repo_name = "microsoft/vscode-cmake-tools"

def get_gh_labels(repo):
    labels = []
    gh_labels = repo.get_labels()
    for label in gh_labels:
        labels.append(f"'{label.name}'")
    return ", ".join(labels)

def get_gh_issues(repo):
    issues = []
    gh_issues = repo.get_issues()
    for issue in gh_issues:
        print(issue)
    print(gh_issues)


def main():
    deployment_id = "gpt-35-turbo-16k"
    # conversation=[{"role": "system", "content": "You are a helpful assistant."}]
    # conversation=[{"role": "system", "content": "You are a bot that generates short labels based on provided text."}]
    repo = gh.get_repo(repo_name)
    labels = get_gh_labels(repo)
    issues = get_gh_issues(repo)
    print(labels)
    conversation=[
        {
            "role": "system", 
            "content": f"The following is a conversation with an AI assistant for the {repo_name} public GitHub repository." +
                       f"The assistant is focused on assigning any of these labels: {labels}, to issues presented."
        }
    ]
    
    flag = True

    while(flag):
        user_input = input("user: ")
        if user_input == "exit":
            flag = False
            print("Goodbye!")
            continue
        conversation.append({"role": "user", "content": user_input + " Please liberally apply relevant labels to the provided text. Please provide results in a comma-separated list."})
        try:
            response = openai.ChatCompletion.create(
                engine=deployment_id,
                messages=conversation,
                temperature=0.5,
                top_p=0.95
                # max_tokens=3
            )
        except openai.APIError as exception:
            if 429 == exception.http_status:
                print("Too many requests, please wait a few seconds and try again.")
                message = exception.json_body["message"].split(" ")
                time_index = message.index("seconds.") - 1  # accommodate different time units
                time_seconds = int(message[time_index])
                for i in range(time_seconds, 0, -1):
                    print(i, end = " \r")
                    time.sleep(1)
                continue
            else:
                raise exception
        conversation.append({"role": "assistant", "content": response["choices"][0]["message"]["content"]})
        print(f"{response.choices[0].message.role}: {response.choices[0].message.content}")


if __name__ == "__main__":
    main()