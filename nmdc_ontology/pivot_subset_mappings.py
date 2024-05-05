import yaml
import csv
import sys
from collections import defaultdict
from datetime import datetime


def convert_yaml_to_tsv(yaml_data):
    tsv_data = defaultdict(dict)

    for context_mapping in yaml_data['mixs_context_mappings']:
        mixs_context_label = context_mapping['mixs_context_label']
        for environment_mapping in context_mapping['environment_mappings']:
            mixs_environment_label = environment_mapping['mixs_environment_label']
            for mapping_batch in environment_mapping['mapping_batches']:
                agent = mapping_batch['agent']
                timestamp = mapping_batch['timestamp']
                if isinstance(timestamp, datetime):
                    timestamp = timestamp.strftime('%Y-%m-%dT%H:%M')  # Format timestamp up to minutes
                else:
                    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ').strftime(
                        '%Y-%m-%dT%H:%M')  # Parse and format timestamp
                for ontology_term in mapping_batch.get('ontology_terms', []):
                    ontology_term_id = ontology_term['ontology_term_id']
                    ontology_term_label = ontology_term['ontology_term_label']
                    confidence = ontology_term['confidence']
                    comments = [comment['comment_body'] for comment in ontology_term.get('comments', []) if
                                comment['agent'] == agent and (isinstance(comment['timestamp'], datetime) and comment[
                                    'timestamp'].strftime('%Y-%m-%dT%H:%M') == timestamp or isinstance(
                                    comment['timestamp'], str) and datetime.strptime(comment['timestamp'],
                                                                                     '%Y-%m-%dT%H:%M:%S.%fZ').strftime(
                                    '%Y-%m-%dT%H:%M') == timestamp)]
                    comment_body = comments[0] if comments else ''
                    key = (mixs_context_label, mixs_environment_label, ontology_term_id, ontology_term_label)
                    tsv_data[key][f"{agent} {timestamp}"] = f"confidence:{confidence}|comment:{comment_body}"

    return tsv_data


# Read the YAML data from stdin
yaml_data = yaml.safe_load(sys.stdin)

# Convert the YAML data to pivoted TSV format
tsv_data = convert_yaml_to_tsv(yaml_data)

# Get the unique agent-timestamp combinations and sort them alphabetically
agent_timestamp_columns = sorted(set(column for row in tsv_data.values() for column in row.keys()))

# Write the TSV data to stdout
fieldnames = [
                 'mixs_context_label',
                 'mixs_environment_label',
                 'ontology_term_id',
                 'ontology_term_label'
             ] + agent_timestamp_columns

writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, delimiter='\t')
writer.writeheader()

for key, row_data in tsv_data.items():
    tsv_row = {
        'mixs_context_label': key[0],
        'mixs_environment_label': key[1],
        'ontology_term_id': key[2],
        'ontology_term_label': key[3]
    }
    for agent_timestamp in agent_timestamp_columns:
        tsv_row[agent_timestamp] = row_data.get(agent_timestamp, '')
    writer.writerow(tsv_row)
