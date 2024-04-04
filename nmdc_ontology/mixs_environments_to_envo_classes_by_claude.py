import os
import time

import click

from anthropic import Anthropic

from dotenv import load_dotenv

load_dotenv("local/.env")

api_key = os.environ["ANTHROPIC_API_KEY"]

client = Anthropic(api_key=api_key)


def get_completion(client, prompt, model, max_tokens, temperature):
    while True:
        try:
            return client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{
                    "role": 'user', "content": prompt
                }]
            ).content[0].text
        except Exception as e:
            print(f"{e}. Retrying in 5 seconds...")
            time.sleep(5)


@click.command()
@click.option('--mixs-file', required=True, help='Path to the MIxS extension report YAML file')
@click.option('--envo-file', required=True, help='Path to the EnvO class annotations YAML file')
@click.option('--mappings-file', required=True, help='Previously completed mappings in YAML format')
@click.option('--envo-description', required=True,
              help='Description of EnvO classes (e.g., "environmental materials", "biomes")')
@click.option('--suffix', required=True, help='What should we ask for after presenting the input data?')
@click.option('--temperature', default=0.5, help='Temperature for the API (0 to 1, where 1 is most creative)')
@click.option('--max-tokens', default=4096, help='Maximum number of tokens for the API response')
@click.option('--model', default='claude-3-opus-20240229', help='Model name for the Anthropic API')
@click.option('--print-message', is_flag=True, default=False)
def main(mixs_file, envo_file, envo_description, mappings_file, temperature, max_tokens, model, suffix, print_message):
    '''this script takes YAML representations of
- MIxS environments (called packages or extensions in various sources)
- EnvO classes (esp biomes or environmental materials)
- previously completed mappings between them
and generates more mappings or asks other QC questions
The creation of the MIxS and EnvO YAML files is illustrated in qc.Makefile
This script prints its results to the console
Manual review and reformatting is recommended
Please place the reviewed results in the assets directory'''

    with open(mixs_file, 'r') as file:
        mixs_environments = file.read()

    with open(envo_file, 'r') as file:
        envo_classes = file.read()

    with open(mappings_file, 'r') as file:
        mappings = file.read()

    message = f"""Here are the definitions of environments, according to MIxS: {mixs_environments}
    and the definitions of {envo_description}, according to EnvO: {envo_classes}.
    Here are some mappings that we determined in previous sessions: {mappings}.
    {suffix}
    """

    if print_message:
        print(message)

    completion = get_completion(client, message, model, max_tokens, temperature)

    print(completion)


if __name__ == '__main__':
    main()
