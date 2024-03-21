import os
import time

import yaml

from anthropic import Anthropic

from dotenv import load_dotenv

load_dotenv("local/.env")

mixs_extension_report_file = "assets/extension_report.yaml"
envo_class_annotations_file = "assets/report_envo_environmental_material_annotations.tsv"
envo_classes_description = "environmental materials"
output_file = "assets/mixs_environments_env_materials_subsets.yaml.txt"

api_key = os.environ["ANTHROPIC_API_KEY"]

# Set up the Anthropic API client
# api_key = os.environ["ANTHROPIC_API_KEY"]
MODEL_NAME = "claude-3-opus-20240229"

client = Anthropic(api_key=api_key)

with open(mixs_extension_report_file, 'r') as file:
    mixs_environments = file.read()

with open(envo_class_annotations_file, 'r') as file:
    envo_materials = file.read()


def get_completion(client, prompt):
    while True:
        try:
            return client.messages.create(
                model=MODEL_NAME,
                max_tokens=4096,
                temperature=0.1,  # 0 to 1
                messages=[{
                    "role": 'user', "content": prompt
                }]
            ).content[0].text
        except Exception as e:
            print(f"{e}. Retrying in 5 seconds...")
            time.sleep(5)


completion = get_completion(client,
                            f"""Here are the definitions of environments, according to MIxS: {mixs_environments} 
and the definitions of {envo_classes_description}, according to EnvO: {envo_materials}.
Generate an exhaustive YAML-formatted report of all environmental materials 
that could reasonably be found in the Soil environment.
When associating an environmental material with an environment, 
report both the environmental material id 
and the environmental material label for every associated environmental material.
""")

# print(completion)

# Open the output file in write mode ('w')
with open(output_file, 'w') as outfile:
    # Dump the YAML string to the file
    yaml.dump(completion, outfile)
