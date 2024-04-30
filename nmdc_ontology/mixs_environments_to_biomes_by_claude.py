import time
import click

from anthropic import Anthropic

from dotenv import load_dotenv

import os
import requests
from bs4 import BeautifulSoup
import yaml

ENV_FILE_PATH = "../local/.env"
envo_mixs_guidance_url = "https://github.com/EnvironmentOntology/envo/wiki/Using-ENVO-with-MIxS"
envo_env_materials_path = "../local/biomes.ttl"
mixs_schema_url = "https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/main/src/mixs/schema/mixs.yaml"

load_dotenv(ENV_FILE_PATH)
api_key = os.environ["ANTHROPIC_API_KEY"]
client = Anthropic(api_key=api_key)

# Retrieve the envo/mixs guidance page
try:
    response = requests.get(envo_mixs_guidance_url)
    response.raise_for_status()  # Check for HTTP errors
except requests.exceptions.RequestException as e:
    print(f"Error retrieving page: {e}")
    exit()  # Exit the script if there's an error

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Get text from more specific tags (adjust selectors as needed)
# Extract plain text - Including tables, headings, and lists
# this is a little over inclusive
envo_mixs_guidance_text = ""
for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'td']):
    envo_mixs_guidance_text += element.get_text() + "\n"

with open(envo_env_materials_path, 'r') as file:
    envo_env_materials_text = file.read()

# Retrieve the mixs schema
try:
    response = requests.get(mixs_schema_url)
    response.raise_for_status()  # Check for HTTP errors
except requests.exceptions.RequestException as e:
    print(f"Error retrieving page: {e}")
    exit()  # Exit the script if there's an error

mixs_schema_dict = yaml.safe_load(response.text)

if 'classes' in mixs_schema_dict:
    classes_data = mixs_schema_dict['classes']

    # Filter classes based on 'is_a' value (keep as dictionaries)
    filtered_classes = {}  # Initialize as an empty dictionary
    for class_name, class_dict in classes_data.items():
        if class_dict.get('is_a') == 'Extension':
            filtered_classes[class_name] = class_dict

    # Remove 'slot_usage' from each class
    for class_name, class_dict in filtered_classes.items():
        if 'slot_usage' in class_dict:
            del class_dict['slot_usage']
        if 'slots' in class_dict:
            del class_dict['slots']

    # Convert the filtered classes back into YAML
    mixs_classes_yaml = yaml.dump(filtered_classes)

else:
    mixs_classes_yaml = None
    print("The 'classes' key was not found in the dictionary.")
    exit()

prompts = [
    """Here is a document from the authors of the Environment Ontology (EnvO)
    about how to choose EnvO terms to go with terms from the MIxS schema.
    I find it a great starting point,
    but it does not address the fact that MIxS defines several environmental Extensions
    and the EnvO terms that are reasonable for the env_broad_scale in one environment
    may not be reasonable for other environments.
    For example, agricultural soil is not a reasonable env_broad_scale for the water Extension.
    """,
    """Here are the biomes from the EnvO ontology, in OWL Turtle format""",
    """Here are the Extensions the MIxS schema, as a fragment of a YAML serialized LinkML schema""",
    """Please create a YAML file that uses the MIxS Extension as outer keys,
    and then lists the EnvO terms that are reasonable for env_broad_scale in each Extension.
    Please report both the EnvO term ID and the EnvO term label."""
]


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


message = f"""
{prompts[0]} {envo_mixs_guidance_text} {prompts[1]}  {envo_env_materials_text} {prompts[2]} {mixs_classes_yaml} {prompts[3]}
"""

# completion = get_completion(client, message, model="claude-3-opus-20240229", max_tokens=4096, temperature=0.1)
#
# print(completion)

with open("large_string.txt", "w") as file:
    file.write(message)
