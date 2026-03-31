import sparql_dataframe
import pandas as pd

min_col_sparsity = 2
max_object_usage = 100
raw_output = "../assets/from_envo_ubergraph_raw.tsv"
filtered_output = "../assets/from_envo_ubergraph_filtered.tsv"
predicate_usage_output = "../assets/from_envo_ubergraph_predicate_usage.tsv"
object_usage_output = "../assets/from_envo_ubergraph_object_usage.tsv"


# # Set Pandas display options to show all rows and columns
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)


# Function to remove columns with less than min_col_sparsity non-blank values
def remove_sparse_columns(df, n):
    column_counts = df.astype(bool).sum(axis=0)
    columns_to_keep = column_counts[column_counts >= n].index
    return df[columns_to_keep]


endpoint = "https://ubergraph.apps.renci.org/sparql"
sparql_query = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?s (REPLACE(STR(?s), "http://purl.obolibrary.org/obo/", "") AS ?class) ?sls ?predicate ?o ?ols
WHERE {
    VALUES ?parent {
        <http://purl.obolibrary.org/obo/BFO_0000024> # fiat object, a material entity 
        <http://purl.obolibrary.org/obo/ENVO_00003074> # manufactured product, a material entity
        <http://purl.obolibrary.org/obo/ENVO_00010483> # environmental material, a material entity
        <http://purl.obolibrary.org/obo/ENVO_01000281> # layer, a material entity
        <http://purl.obolibrary.org/obo/ENVO_01000813> # astronomical body part, a material entity
        <http://purl.obolibrary.org/obo/ENVO_01001813> # construction, a material entity
        <http://purl.obolibrary.org/obo/RO_0002577> # system, a material entity
    } 
    # add RO:0002577 system ?
    # already included ENVO:00000428 biome, a astronomical body part
    # skipping ENVO:03500005 anthropogenic litter, CHEBI:24431 chemical entity, 
    # UBERON:0000465 material anatomical entity, BFO:0000030 object, BFO:0000027 object aggregate, 
    # OBI:0100026 organism (with NCBI descendants)
    # PCO:0000031 organismal entity -> collection of organisms
    # PO:0025131 plant anatomical entity -> plant structure, portion of plant substance
    # OBI:0000047 processed material -> device -> container
    # NCBITaxon:1 root
    # CHEBI:36342 subatomic particle
    GRAPH <http://reasoner.renci.org/ontology> {
        ?s rdfs:subClassOf+ ?parent ;
           rdfs:isDefinedBy <http://purl.obolibrary.org/obo/envo.owl> .
    }
    GRAPH <http://reasoner.renci.org/redundant> {
        ?s ?p ?o
    }
    GRAPH <http://reasoner.renci.org/ontology> {
        ?o rdfs:isDefinedBy <http://purl.obolibrary.org/obo/envo.owl> .
    }
    OPTIONAL { ?s rdfs:label ?sl . BIND(STR(?sl) AS ?sls) }
    OPTIONAL { ?p rdfs:label ?pl . BIND(REPLACE(STR(?pl), "_", " ") AS ?pls) }
    BIND(IF(BOUND(?pl), ?pls, STR(?p)) AS ?predicate)
    OPTIONAL { ?o rdfs:label ?ol . BIND(STR(?ol) AS ?ols) }
}
"""

df = sparql_dataframe.get(endpoint, sparql_query, post=True)
df.to_csv(raw_output, sep="\t", index=False)

# Get the value counts of the specified column
value_counts_df = df["ols"].value_counts().to_frame().reset_index()
value_counts_df.columns = ['ols', 'count']

value_counts_df.to_csv(object_usage_output, sep="\t", index=True)

# Merge df with value_counts_df based on the "ols" column
merged_df = pd.merge(df, value_counts_df, on='ols')

print(merged_df)

# Filter the merged dataframe based on the "Count" column
object_filtered_df = merged_df[merged_df['count'] < max_object_usage]

print(object_filtered_df)

# Drop the "Count" column if it's not needed in the final result
object_filtered_df = object_filtered_df.drop('count', axis=1)

print(object_filtered_df)

# Pivot the DataFrame
pivot_df = pd.pivot_table(object_filtered_df, index='class', columns='predicate', values='ols',
                          aggfunc=lambda x: '|'.join(x.dropna().unique()))

# Replace NaN values with an empty string
pivot_df.fillna('', inplace=True)

# Generate a report of non-empty values in each column
column_counts = pivot_df.astype(bool).sum(axis=0)
report_df = pd.DataFrame({'predicate': column_counts.index, 'usage': column_counts.values})
report_df.to_csv(predicate_usage_output, sep="\t", index=False)

filtered_df = remove_sparse_columns(pivot_df, min_col_sparsity)

filtered_df.to_csv(filtered_output, sep="\t", index=True)
