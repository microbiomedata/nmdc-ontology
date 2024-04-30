import vertexai
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import yaml
from rdflib import Graph

ENV_FILE_PATH = "../local/.env"
envo_mixs_guidance_url = "https://github.com/EnvironmentOntology/envo/wiki/Using-ENVO-with-MIxS"
envo_env_materials_path = "../local/biomes.ttl"
mixs_schema_url = "https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/main/src/mixs/schema/mixs.yaml"

gc_location = "us-east4"
vertex_model = "gemini-1.5-pro-preview-0409"

vertex_temp = 0.0
vertex_max_tokens_out = 8192

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

# ## Retrieve the ontology
# try:
#     response = requests.get(envo_ontology_url)
#     response.raise_for_status()  # Check for HTTP errors
# except requests.exceptions.RequestException as e:
#     print(f"Error retrieving page: {e}")
#     exit()  # Exit the script if there's an error
#
# # Parse into an rdflib Graph
# graph = Graph()
# graph.parse(data=response.text, format='xml')  # Assuming RDF/XML format
#
# # Now you can query the ontology using rdflib
# print(graph)  # Example: Print the graph structure

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

    # Convert the filtered classes back into YAML
    mixs_classes_yaml = yaml.dump(filtered_classes)

else:
    mixs_classes_yaml = None
    print("The 'classes' key was not found in the dictionary.")
    exit()

# print(mixs_classes_yaml)

load_dotenv(ENV_FILE_PATH)
VERTEX_PROJECT_ID = os.environ['VERTEX_PROJECT_ID']

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

built_prompt = [prompts[0], envo_mixs_guidance_text,
                prompts[1], envo_env_materials_text,
                prompts[2], mixs_classes_yaml,
                prompts[3]]

vertexai.init(project=VERTEX_PROJECT_ID, location=gc_location)

model = GenerativeModel(vertex_model)

generation_config = GenerationConfig(
    temperature=vertex_temp,
    max_output_tokens=vertex_max_tokens_out,
)

word_count = 0

# Iterate through each sentence in the list
for sentence in built_prompt:
  # Split the sentence into individual words
  words = sentence.split()
  # Add the number of words in the current sentence to the total count
  word_count += len(words)

# Print the total word count
print(f"Total word count: {word_count}")

# response = model.generate_content(
#     built_prompt,
#     generation_config=generation_config
# )
#
# print(response.text)


# before extracting biomes and extensions
# # google.api_core.exceptions.InvalidArgument: 400 Unable to submit request because the input token count is 3601938
# # but model only supports up to 1000000. Reduce the input token count and try again.
# # You can also use the CountTokens API to calculate prompt token count and billable characters.
# # Learn more: https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models
