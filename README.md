# suggest-labels
A GitHub Action that can be used to suggest labels for issues.

## Inputs

### `repo`

The name of the repo with the issues that need label suggestions. Default `'${{ github.repository }}'`.

### `owner`

The repo owner's username. Default `'${{ github.repository_owner }}'`.

### `token`

Access token that can access the issues on the repo. Default `'${{ github.token }}'`.

### `api-key`

**Required** OpenAI API access key.

### `endpoint`

**Required** OpenAI endpoint for accessing the model.

### `deployment-id`

**Required** The deployment ID of the OpenAI model.


## Outputs

### `labels`

The issues and their corresponding labels.

## Example usage

```yaml
name: Suggest Labels
- uses: snehara99/label-suggestions@0.0.5
  with:
    token: ${{ github.token }}
    api_key: ${{ secrets.API_KEY }}
    endpoint: 'https://americasopenai.azure-api.net'
    deployment-id: 'gpt-35-turbo-16k'
```

