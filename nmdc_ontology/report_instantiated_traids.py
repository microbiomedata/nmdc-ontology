import click
import pandas as pd
import requests
from collections import Counter


@click.command()
@click.option('--api-url',
              default="https://api.microbiomedata.org/nmdcschema/biosample_set?max_page_size=9999&projection=env_broad_scale%2Cenv_local_scale%2Cenv_medium",
              help='URL of the API endpoint')
@click.option('--output-file', default="biosample_triad_report.tsv", help='Output file name')
@click.option('--counts-output-file', default="triad_term_counts.tsv", help='Output file name for value counts')
def main(api_url, output_file, counts_output_file):
    # Send the GET request
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Convert the JSON response to a Python dictionary
        data = response.json()

        # Extract the resources from the response
        resources = data.get("resources", [])

        # Initialize a list to store rows
        rows = []

        # Iterate over each resource and construct rows as dictionaries
        for resource in resources:
            row = {
                "id": resource.get("id"),
                "env_broad_scale.term.id": resource.get("env_broad_scale", {}).get("term", {}).get("id"),
                "env_local_scale.term.id": resource.get("env_local_scale", {}).get("term", {}).get("id"),
                "env_medium.rm.id": resource.get("env_medium", {}).get("term", {}).get("id")
            }
            rows.append(row)

        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(rows)

        # Save the DataFrame to a TSV file
        df.to_csv(output_file, sep="\t", index=False)

        # Combine all values into a single list
        combined_values = []
        for index, row in df.iterrows():
            combined_values.extend([
                row['env_broad_scale.term.id'],
                row['env_local_scale.term.id'],
                row['env_medium.rm.id']
            ])

        # Count the appearance of each unique value
        value_counts = Counter(combined_values)

        # Convert counts to DataFrame
        counts_df = pd.DataFrame(value_counts.items(), columns=['Value', 'Count'])

        # Split the 'Value' column into two parts before and after the colon
        counts_df[['Before Colon', 'After Colon']] = counts_df['Value'].str.split(':', n=1, expand=True)

        # Save counts DataFrame to a TSV file
        counts_df.to_csv(counts_output_file, sep="\t", index=False)
    else:
        print("Failed to fetch data from the API:", response.status_code)


if __name__ == '__main__':
    main()
