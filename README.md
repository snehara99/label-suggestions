# label-suggestions
A GitHub Action that can be used to suggest labels for issues.

## Inputs

### `repo`

**Required** The repo with the issues that need label suggestions.

### `owner`

**Required** The repo owner's user ID.

### `token`

Access token that can access the issues on the repo. Default `'${{ github.token }}'`.

### `api-key`

**Required** "OpenAI API access key."

### `endpoint`

**Required** "OpenAI endpoint for accessing the model"

### `deployment-id`

**Required** "The deployment ID of the OpenAI model"


## Outputs

### `labels`

The issues and their corresponding labels.

## Example usage

```yaml
name: Suggest Labels
- uses: actions/suggest-bales@e76147da8e5c81eaf017dede5645551d4b94427b
  with:
    repo: 'vscode-cmake-tools'
    owner: 'microsoft'
    token: ${{ github.token }}
    api_key: 1111aaaa2222bbbb3333cccc4444dddd
    endpoint: 'https://americasopenai.azure-api.net'
    deployment-id: 'gpt-35-turbo-16k'
```

