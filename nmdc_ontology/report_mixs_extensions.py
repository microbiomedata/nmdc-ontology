import csv
import io
import yaml
from typing import Dict, List, Union
import requests
import click


@click.command()
@click.option('--url',
              default='https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/main/assets/class_summary_results.tsv',
              help='URL of a MIxS class summary TSV file')  # see https://github.com/GenomicsStandardsConsortium/mixs/blob/a1ded1e23abfb9372c81cab50107929e5ceea0b8/project.Makefile#L40
@click.option('--output-file', default='assets/extension_report.yaml', help='Output YAML file path')
def main(url: str, output_file: str) -> None:
    # Send a GET request to the URL
    response = requests.get(url)

    extension_rows: List[Dict[str, str]] = []

    # Check if the request was successful
    if response.status_code == 200:
        # Read the content of the response as text
        data: str = response.text

        # Use a StringIo object to treat the text data as a file-like object
        file = io.StringIO(data)

        # Use csv.DictReader to read the data
        reader = csv.DictReader(file, delimiter='\t')

        # Filter rows where is_a = "Extension"
        extension_rows = [row for row in reader if row['is_a'] == 'Extension']  # type: ignore # todo: do not ignore!
    else:
        click.echo(f"Error: Failed to retrieve data from {url}. Status code: {response.status_code}", err=True)

    # Create a dictionary to store the YAML data
    yaml_data: Dict[str, Dict[str, Union[str, List[str]]]] = {}

    # Extract the desired fields for each Extension row
    for row in extension_rows:
        extension_key: str = row['class'].strip()
        yaml_data[extension_key] = {}

        for key in ['title', 'description', 'comments', 'use_cases']:
            value: str = row[key].strip()
            if '\u2019' in value:
                click.echo(f"Replacing '\\u2019' with ''' in field '{key}' of extension '{extension_key}'", err=True)
                value = value.replace('\u2019', "'")  # Replace \u2019 with ASCII equivalent of \u0027

            if value:
                yaml_data[extension_key][key] = value

    # Write the YAML data to a file
    with open(output_file, 'w') as file:
        yaml.dump(yaml_data, file, default_flow_style=False)

    click.echo(f"YAML data written to {output_file}")


if __name__ == '__main__':
    main()
