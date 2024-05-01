This may not be the best long term home for this document

Have also been using `llm` in berkeley-schema-fy24 main

See also mapping_problem_statement.md

See also
- https://www.futurepedia.io/
- https://artificialanalysis.ai/

## globally exporting environment variables like API keys

```shell
set -a  # This ensures all variables defined from now on are exported automatically
source local/.env
set +a  # Turn off auto-export
```

and/or

```shell
llm keys set openai
```

`llm` ssaves keys in `~/.config/io.datasette.llm/keys.json` by default. See also

```shell
llm keys path
```

However, if the keys were set in one project, running this in another project might not detect the authorized models
```shell
llm models
```

Maybe the plugins need to be installed int eh new project?

## Method for interleaving strings and files for llm

```shell
{
  echo -e "here is the initial text\n";
  cat CHANGELOG.md;
  echo -e "\nand some subsequent text\n";
  cat LICENSE;
} | llm -m gemini-1.5-pro-latest
```

## Ways to use the LLMs
- web interface
- programmatically, esp Python
- `llm` CLI

## Remote APIs for `llm`
### Under evaluation. @turbomam has keys through BBOP or as an individual
* llm-claude-3 supports Anthropic’s Claude 3 family of models.
* llm-gemini adds support for Google’s Gemini models.

Some local models are included too

### Perhaps...
* llm-perplexity by Alexandru Geana supports the Perplexity Labs API models, including sonar-medium-online which can search for things online and llama-3-70b-instruct.

### Skipping for now
* llm-anyscale-endpoints supports models hosted on the Anyscale Endpoints platform, including Llama 2 70B.
* llm-bedrock-anthropic by Sean Blakey adds support for Claude and Claude Instant by Anthropic via Amazon Bedrock.
* llm-bedrock-meta by Fabian Labat adds support for Llama 2 by Meta via Amazon Bedrock.
* llm-claude by Tom Viner adds support for Claude 2.1 and Claude Instant 2.1 by Anthropic.
* llm-cohere by Alistair Shepherd provides cohere-generate and cohere-summarize API models, powered by Cohere.
* llm-command-r supports Cohere’s Command R and Command R Plus API models.
* llm-fireworks supports models hosted by Fireworks AI.
* llm-groq by Moritz Angermann provides access to fast models hosted by Groq.
* llm-mistral adds support for Mistral AI’s language and embedding models.
* llm-openrouter provides access to models hosted on OpenRouter.
* llm-palm adds support for Google’s PaLM 2 model.
* llm-reka supports the Reka family of models via their API.
* llm-replicate adds support for remote models hosted on Replicate, including Llama 2 from Meta AI.
* llm-together adds support for the Together AI extensive family of hosted openly licensed models.

## Google Gemini through the Vertex API

Requires installing a client app. Once it is installed, a list of project codes can be retrieved with

```shell
gcloud projects list
```
