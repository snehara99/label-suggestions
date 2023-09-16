import openai
import time
import os
from github import Github, Auth
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Setup
openai.api_version = "2023-08-01-preview"
openai.api_base = "https://americasopenai.azure-api.net"
openai.api_type = "azure"
openai.api_key = os.environ["OPENAI_API_KEY"]

# GitHub API Setup
gh_pat = os.environ["GITHUB_PAT"]
gh = Github(auth=Auth.Token(gh_pat))

def get_gh_labels():
    labels = []
    repo = gh.get_repo("microsoft/vscode-cmake-tools")
    gh_labels = repo.get_labels()
    for label in gh_labels:
        labels.append(f"'{label.name}'")
    return ", ".join(labels)

def main():
    deployment_id = "gpt-35-turbo-16k"
    conversation=[{"role": "system", "content": f"You are a bot that matches one or more of the following labels to the provided text in a single line: {get_gh_labels()}."}]
    flag = True

    while(flag):
        user_input = input("user: ")
        if user_input == "exit":
            flag = False
            print("Goodbye!")
            continue
        conversation.append({"role": "user", "content": user_input})
        try:
            response = openai.ChatCompletion.create(
                deployment_id=deployment_id,
                messages=conversation,
                temperature=0,
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
        print(f"::set-output name=issue_labels::{response.choices[0].message.content}") # set output for GitHub Action


if __name__ == "__main__":
    main()