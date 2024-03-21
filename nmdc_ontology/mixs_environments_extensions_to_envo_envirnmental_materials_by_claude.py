import os
import time

from anthropic import Anthropic

from dotenv import load_dotenv

load_dotenv("../local/.env")

api_key = os.environ["ANTHROPIC_API_KEY"]

# Set up the Anthropic API client
# api_key = os.environ["ANTHROPIC_API_KEY"]
MODEL_NAME = "claude-3-opus-20240229"

client = Anthropic(api_key=api_key)

with open('../assets/extension_report.yaml', 'r') as file:
    mixs_environments = file.read()

with open('../assets/report_envo_environmental_material_annotations.tsv', 'r') as file:
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
and the definitions of environmental materials, according to EnvO: {envo_materials}.
Generate an exhaustive YAML-formatted report of all environmental materials 
that could reasonably be found in the Soil environment.
When associating an environmental material with an environment, 
report both the environmental material id 
and the environmental material label for every associated environmental material.
"""
)

print(completion)
