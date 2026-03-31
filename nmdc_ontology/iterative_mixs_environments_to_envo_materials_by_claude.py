import os
import pprint
import time

import click

from anthropic import Anthropic

import yaml

from dotenv import load_dotenv

import json

from itertools import islice

load_dotenv("local/.env")

api_key = os.environ["ANTHROPIC_API_KEY"]

client = Anthropic(api_key=api_key)

# File to log failed parses
log_file = 'failed_parses.txt'
file = open(log_file, 'a')


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
            print(f"{e}. Retrying in 1 minute...")
            time.sleep(60)


def parse_llm_string(llm_string):
    try:
        data = json.loads(llm_string)
        return data
    except (json.JSONDecodeError, TypeError) as e:
        # Handle the parsing error here,
        #  e.g., log the error and return a default value
        print(f"Error parsing JSON: {e}")
        file.write('\n' + llm_string + '\n')
        return None


def yaml_string_to_dict(yaml_string):
    """Converts a YAML string into a Python dictionary.

    Args:
        yaml_string: The YAML string to be converted.

    Returns:
        A Python dictionary representing the parsed YAML data.

    Raises:
        yaml.YAMLError: If there are errors in the YAML syntax.
    """

    try:
        return yaml.safe_load(yaml_string)
    except yaml.YAMLError as exc:
        raise ValueError(f"Error parsing YAML string: {exc}")


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
        mixs_environments_dict = yaml_string_to_dict(mixs_environments)
        # print(yaml.dump(mixs_environments_dict))

    with open(envo_file, 'r') as file:
        envo_classes = file.read()

    with open(mappings_file, 'r') as file:
        mappings = file.read()

    results_dict = {}

    message_printed = False

    sorted_items = sorted(mixs_environments_dict.items())

    # max_items = len(sorted_items)+1
    max_items = 5

    # for ek, ev in mixs_environments_dict.items():
    for ek, ev in islice(sorted_items, max_items):

        message = f"""Here are the definitions of environments, according to MIxS: {mixs_environments}
            and the definitions of {envo_description}, according to EnvO: {envo_classes}.
            Here is an example JSON mapping file: {mappings}.
            Populate the section with the mixs_context_label of 'env_medium'
            and the mixs_environment_label of {ek}
            with all compatible EnvO environmental materials.
            Follow the example format exactly, 
            but do not generate any mappings that would have an accepted value of false.
            I only provided those to you as negative training.
            You can include comments at any level in the mapping file.
            The provided examples are incomplete, so fill in any additional compatible mappings.
            Do not include any introduction, summary or anything outside of the requested JSON structure.
            """

        if print_message and not message_printed:
            print(message)
            message_printed = True

        print(ek)

        completion = get_completion(client, message, model, max_tokens, temperature)

        print(completion)

        result_dict = parse_llm_string(completion)

        results_dict[ek] = result_dict

    # write dict and error files
    # Writing JSON data
    with open("results_dict.json", 'w') as file:
        json.dump(results_dict, file, indent=4)


if __name__ == '__main__':
    main()
    file.close()
