const core = require("@actions/core");
const github = require("@actions/github");
const { template } = require("lodash");

const { OpenAIClient, AzureKeyCredential } = require("@azure/openai");

function get_gh_labels() {}
async function run() {
  try {
    // let token = core.getInput('token');
    const octokit = github.getOctokit("");

    const issues = (
      await octokit.paginate(octokit.rest.issues.listForRepo, {
        owner: "microsoft",
        repo: "vscode-cmake-tools",
        state: "open",
        per_page: 100,
      })
    ).filter((i) => i.pull_request === undefined && i.labels.length === 0);

    const owner = "microsoft";
    const repo = "vscode-cmake-tools";
    // TODO get all labels
    const labels = (
      await octokit.rest.issues.listLabelsForRepo({
        owner,
        repo,
      })
    ).data
      .map((i) => i.name)
      .join("', '");

    console.log(labels);

    let apiKey = ""; //core.getInput('api_key');
    const client = new OpenAIClient(
      "https://americasopenai.azure-api.net",
      new AzureKeyCredential(apiKey)
    );

    var issueLabel = {};

    // TODO: I think that the API library is failing because it's doing too many requests too fast, we'll need to add some delays. 
    // This allows us to test for now.
    const testIssues = [issues[0]];

    // iterate through issues to label
    testIssues.forEach(async (issue) => {
      // todo maybe play with how title and body are represented
      const issueText = issue.title + ". " + issue.body.replace(/\n/g, " ");
      const userMessageText = `${issueText}. Please liberally apply relevant labels to the provided text. Please provide results in a comma-separated list.`;
      const messages = [
        {
          role: "system",
          content: `The following is a conversation with an AI assistant for the ${owner}/${repo} public GitHub repository. The assistant is focused on assigning any of these labels: ${labels}, to issues presented.`,
        },
      ];
      messages.push({ role: "user", content: userMessageText });
      const completion = await client.getChatCompletions(
        "gpt-35-turbo-16k",
        messages,
        {
          temperature: 0.5,
          topP: 0.95,
          n: 1,
        }
      );

      for (const choice of completion.choices) {
        issueLabel[
          issue.number
        ] = `[ISSUE ${issue.number}][${issue.title}][${choice.message.content}]`;
        console.log(
          `[ISSUE ${issue.number}][${issue.title}][${choice.message.content}]`
        );
      }
    });
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
