import json
import csv
import click


@click.command()
@click.option('--id-range-tsv-input',
              default='data-vs-ontology-reports/report-id-ranges.tsv',
              help='Path to the TSV file containing ID ranges.')
@click.option('--nmdco-classes-json-input',
              default='nmdco-classes.json',
              help='Path to the JSON file containing class nodes.')
@click.option('--output',
              default='data-vs-ontology-reports/nmdco-envo-classes-with-id-owner.tsv',
              help='Path to the output TSV file.')
def filter_class_nodes(id_range_tsv_input, nmdco_classes_json_input, output):
    # Load ranges from TSV file, skipping the first row
    owner_ranges = {}
    with open(id_range_tsv_input, 'r') as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter='\t')
        next(tsvreader)  # Skip the first row
        for row in tsvreader:
            owner = row[1].strip('"')
            min_val = int(row[2])
            max_val = int(row[3])
            owner_ranges[owner] = (min_val, max_val)

    # Function to check if ID falls within the range for a specific owner
    def in_range_for_owner(id, min_val, max_val):
        return min_val <= id <= max_val

    # Load class nodes from JSON file
    with open(nmdco_classes_json_input, 'r') as jsonfile:
        data = json.load(jsonfile)

    # Filter and collect class nodes
    filtered_nodes = []
    for node in data['graphs'][0]['nodes']:
        node_id = node['id']
        node_owner = None
        for owner, (min_val, max_val) in owner_ranges.items():
            if node_id.startswith('http://purl.obolibrary.org/obo/ENVO_') and in_range_for_owner(
                    int(node_id.split('_')[-1]), min_val, max_val):
                node_owner = owner
                break
        if node_owner is not None:
            filtered_nodes.append({
                'ID': node_id,
                'LBL': node['lbl'],
                'Owner': node_owner
            })

    # Write filtered nodes to TSV file
    fieldnames = ['ID', 'LBL', 'Owner']
    with open(output, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(filtered_nodes)

    print("Filtered class nodes written to", output)


if __name__ == '__main__':
    filter_class_nodes()
