## Setup Python Virtual Environment
```bash
cd ./python
# create virtual environment named "env"
py -m venv env
# activate virtual environment
.\env\Scripts\activate
# install dependencies in virtual environment
pip install -r requirements.txt
```
> When you are ready to leave the virtual environment enter `deactivate`.

## Setup Environment Variables
1. Create a file in `./python` named `.env`.
1. Add the following key / value pairs to `.env`:
    ```bash
    OPENAI_API_KEY=<your OpenAI API key>
    GITHUB_PAT=<your GitHub PAT>
    ```
    > You can create a GitHub PAT [here](https://github.com/settings/tokens?type=beta).

## Running the Python Script
With the [virtual environment](#setup-python-virtual-environment) activated, run `py main.py`. To exit the chat loop enter `exit`.