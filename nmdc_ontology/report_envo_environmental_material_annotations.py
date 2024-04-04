import click
import requests
from collections import defaultdict
import pandas as pd
import yaml
from typing import Dict, List, Union


@click.command()
@click.option('--endpoint', default="http://3.236.215.220/repositories/nmdc-knowledgegraph", help="SPARQL endpoint URL")
@click.option('--tsv-output', 'tsv_output_file', default="assets/report_envo_environmental_material_annotations.tsv",
              help="Output TSV file path")
@click.option('--yaml-output', 'yaml_output_file', default="assets/report_envo_environmental_material_annotations.yaml",
              help="Output YAML file path")
def main(endpoint: str, tsv_output_file: str, yaml_output_file: str):
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
        ?s rdfs:subClassOf* ENVO:00010483 ;
           ?p ?o .
      }

      FILTER (datatype(?o) = rdf:langString || datatype(?o) = xsd:string)
    }
    """

    headers = {
        "Content-Type": "application/sparql-query",
        "Accept": "application/sparql-results+json"
    }

    response = requests.post(endpoint, data=query, headers=headers)

    if response.status_code == 200:
        results = response.json()
        pivot_data: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))

        for result in results["results"]["bindings"]:
            s = result["s"]["value"]
            p = result["p"]["value"]
            o = result["o"]["value"]

            s_curie = s.split("#")[-1] if "#" in s else s.split("/")[-1]
            p_curie = p.split("#")[-1] if "#" in p else p.split("/")[-1]

            pivot_data[s_curie][p_curie].append(o)

        df = pd.DataFrame.from_dict(pivot_data, orient='index')
        df.fillna('', inplace=True)
        df.to_csv(tsv_output_file, sep="\t")
        click.echo(f"DataFrame saved to {tsv_output_file}")

        data_dict: Dict[str, Dict[str, Union[List[str], str]]] = df.to_dict(orient='index')

        for row_key in data_dict:
            data_dict[row_key] = {
                k: v for k, v in data_dict[row_key].items() if (
                                                                       isinstance(v, (list, tuple, pd.Series)) and any(
                                                                   x for x in v if pd.notnull(x))
                                                               ) or (
                                                                       not isinstance(v, (
                                                                           list, tuple, pd.Series)) and pd.notnull(
                                                                   v) and v != ''
                                                               )
            }

        with open(yaml_output_file, 'w') as file:
            yaml.dump(data_dict, file)
    else:
        click.echo(f"Query failed with status code: {response.status_code}")


if __name__ == "__main__":
    main()
