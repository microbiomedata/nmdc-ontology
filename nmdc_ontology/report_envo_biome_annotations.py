import requests
from collections import defaultdict
import pandas as pd

output_file = "assets/report_envo_biome_annotations.tsv"

endpoint = "http://3.236.215.220/repositories/nmdc-knowledgegraph"
# https://graphdb-dev.microbiomedata.org/repositories/nmdc-metadata
query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ENVO: <http://purl.obolibrary.org/obo/ENVO_>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>
PREFIX IAO: <http://purl.obolibrary.org/obo/IAO_>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?s ?p ?o
WHERE {
  VALUES ?p {
    IAO:0000115
    IAO:0000116
    oboInOwl:hasBroadSynonym
    oboInOwl:hasExactSynonym
    oboInOwl:hasNarrowSynonym
    oboInOwl:hasRelatedSynonym
    rdfs:comment
    rdfs:label
  }
  GRAPH <http://purl.obolibrary.org/obo/nmdco.owl> {
    ?s rdfs:subClassOf* ENVO:00000428 ;
       ?p ?o .
  }
  FILTER (datatype(?o) = rdf:langString || datatype(?o) = xsd:string)
}
"""

# Set the Content-Type header to application/sparql-query
headers = {
    "Content-Type": "application/sparql-query",
    "Accept": "application/sparql-results+json"
}

# Send the POST request to the SPARQL endpoint
response = requests.post(endpoint, data=query, headers=headers)

# Check the response status code
if response.status_code == 200:
    # Parse the JSON response
    results = response.json()

    # Create a dictionary to store the pivot table data
    pivot_data = defaultdict(lambda: defaultdict(list))

    # Process the query results and populate the pivot table data
    for result in results["results"]["bindings"]:
        s = result["s"]["value"]
        p = result["p"]["value"]
        o = result["o"]["value"]

        # Convert the subject and predicate IRIs to CURIEs
        s_curie = s.split("#")[-1] if "#" in s else s.split("/")[-1]
        p_curie = p.split("#")[-1] if "#" in p else p.split("/")[-1]

        pivot_data[s_curie][p_curie].append(o)

    # Convert the pivot table data to a Pandas DataFrame
    df = pd.DataFrame.from_dict(pivot_data, orient='index')

    # Fill empty cells with an empty string
    df.fillna('', inplace=True)

    # Save the DataFrame to a TSV file
    df.to_csv(output_file, sep="\t")

    print(f"DataFrame saved to {output_file}")

else:
    print(f"Query failed with status code: {response.status_code}")
