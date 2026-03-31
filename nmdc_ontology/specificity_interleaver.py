import json
import pandas as pd

# Load the JSON data
with open('results_dict_plus_repaired_failures2.json', 'r') as file:
    json_data = json.load(file)

# Load the TSV data into a DataFrame
specificity_data = pd.read_csv('SPECIFICITY_CONFIDENCE.tsv', sep='\t')
specificity_data.set_index('ENVO_ID', inplace=True)

# Traverse the JSON data and add specificity scores and justifications
for context in json_data['context_mappings']:
    for env_map in context['environment_mappings']:
        mixs_environment_label = env_map['mixs_environment_label']
        for onto_map in env_map['onto_term_mappings']:
            if 'term_id' in onto_map:
                term_id = onto_map['term_id']
                # Check if the term_id exists in the specificity data
                if term_id in specificity_data.index:
                    # Filter the specificity_data for the matching MIxS_LABEL
                    filtered_data = specificity_data[(specificity_data.index == term_id) & (specificity_data['MIxS_LABEL'] == mixs_environment_label)]
                    if not filtered_data.empty:
                        onto_map['specificity_score'] = float(filtered_data.iloc[0]['SPECIFICITY_CONFIDENCE'])  # Convert to float
                        onto_map['specificity_justification'] = str(filtered_data.iloc[0]['JUSTIFICATION'])

# Save the updated JSON data
with open('results_dict_plus_repaired_failures_with_specificity.json', 'w') as file:
    json.dump(json_data, file, indent=4)

print("JSON data updated with specificity scores and justifications.")
