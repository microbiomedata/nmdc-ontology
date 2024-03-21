import csv
import io

import yaml
import sys
import requests

# input_file = 'assets/class_summary_results.tsv'
output_file = 'assets/extension_report.yaml'

# Define the URL of the TSV file
# hopefully this will get merged in soon
# https://github.com/GenomicsStandardsConsortium/mixs/pull/769

url = "https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/c196fef8d9864b15db1abc71e66c4c0ddd8bdcee/class_summary_results.tsv"

# or download mixs.yaml and build here?
# uses schemasheets and then runs that though a python filtering script.
# probably don't wat to have that filtering code in multiple places

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Read the content of the response as text
    data = response.text

    # Use a StringIo object to treat the text data as a file-like object
    file = io.StringIO(data)

    # Use csv.DictReader to read the data
    reader = csv.DictReader(file, delimiter='\t')

    # Filter rows where is_a = "Extension"
    extension_rows = [row for row in reader if row['is_a'] == 'Extension']

else:
    print(f"Error: Failed to retrieve data from {url}. Status code: {response.status_code}")

# Create a dictionary to store the YAML data
yaml_data = {}

# Extract the desired fields for each Extension row
for row in extension_rows:
    extension_key = row['class'].strip()

    yaml_data[extension_key] = {}

    for key in ['title', 'description', 'comments', 'use_cases']:
        value = row[key].strip()
        if '\u2019' in value:
            print(f"Replacing '\\u2019' with ''' in field '{key}' of extension '{extension_key}'", file=sys.stderr)
            value = value.replace('\u2019', "'")  # Replace \u2019 with ASCII equivalent of \u0027
        if value:
            yaml_data[extension_key][key] = value

# Write the YAML data to a file
with open(output_file, 'w') as file:
    yaml.dump(yaml_data, file, default_flow_style=False)

print(f"YAML data written to {output_file}")
