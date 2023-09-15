# suggest-labels
A GitHub Action that can be used to suggest labels for issues.

## Inputs

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
    api-key: ${{ secrets.API_KEY }}
    endpoint: 'https://americasopenai.azure-api.net'
    deployment-id: 'gpt-35-turbo-16k'
```

