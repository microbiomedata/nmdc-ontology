import click
from rdflib import Graph, Namespace
import pandas as pd


@click.command()
@click.option("--id-ranges-ttl", "-i", default="downloads/envo-idranges.owl.ttl", help="Input file path")
@click.option("--output", "-o", default="envo_id_ranges_report.tsv", help="Output file path")
def generate_id_ranges(id_ranges_ttl, output):
    # Load the Turtle content into an RDF graph
    g = Graph()
    g.parse(id_ranges_ttl, format="turtle")

    # Define namespaces
    obo = Namespace("http://purl.obolibrary.org/obo/")
    ro = Namespace("http://purl.obolibrary.org/obo/ro/")
    iao = Namespace("http://purl.obolibrary.org/obo/IAO_")
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
    owl = Namespace("http://www.w3.org/2002/07/owl#")
    rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

    # Construct SPARQL query string
    query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX obo: <http://purl.obolibrary.org/obo/>
        SELECT ?range ?owner ?min ?max
        WHERE {
            ?range a rdfs:Datatype ;
                   owl:equivalentClass ?ec ;
                   obo:IAO_0000597 ?owner .
            ?ec owl:withRestrictions ?restrictions .
            ?restrictions rdf:first ?first ;
                          rdf:rest ?rest .
            ?first xsd:minInclusive ?min .
            ?rest rdf:first ?rest_first .
            ?rest_first xsd:maxInclusive ?max .
        }
    """

    # Execute the SPARQL query and convert results to DataFrame
    results = g.query(query)
    data = [(str(row.range), str(row.owner), str(row.min), str(row.max)) for row in results]
    data = [(str(row.range).replace("http://purl.obolibrary.org/obo/ro/idrange/", ""), str(row.owner), str(row.min),
             str(row.max)) for row in results]

    df = pd.DataFrame(data, columns=['range', 'owner', 'min', 'max'])

    # Save DataFrame as TSV
    df.to_csv(output, sep="\t", index=False)

    click.echo(f"ID ranges saved to {output}")


if __name__ == "__main__":
    generate_id_ranges()
