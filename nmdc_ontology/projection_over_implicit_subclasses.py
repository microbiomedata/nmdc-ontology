import pandas as pd
import networkx as nx


def infer_relationships(df):
    # Create a new dataframe to store the asserted relationships
    asserted_df = df.copy()
    asserted_df['origin'] = 'asserted'
    asserted_df.loc[
        asserted_df['predicate'] == 'http://www.w3.org/2000/01/rdf-schema#subClassOf', 'origin'] = 'asserted hierarchy'
    asserted_df.loc[asserted_df[
                        'predicate'] != 'http://www.w3.org/2000/01/rdf-schema#subClassOf', 'origin'] = 'asserted relationship'

    # Create a directed graph from the subClassOf relationships
    G = nx.DiGraph()
    for _, row in df[df['predicate'] == 'http://www.w3.org/2000/01/rdf-schema#subClassOf'].iterrows():
        G.add_edge(row['sls'], row['ols'])

    # Create a new dataframe to store the inferred relationships
    inferred_df = pd.DataFrame(columns=['sls', 'predicate', 'ols', 'origin'])

    # Infer subClassOf relationships based on transitivity
    for node in G.nodes():
        descendants = nx.descendants(G, node)
        for descendant in descendants:
            if descendant != node:
                inferred_df = pd.concat([inferred_df, pd.DataFrame(
                    {'sls': [descendant], 'predicate': ['http://www.w3.org/2000/01/rdf-schema#subClassOf'],
                     'ols': [node], 'origin': ['inferred hierarchy']})], ignore_index=True)

    # Infer relationships based on inheritance
    for _, row in df[df['predicate'] != 'http://www.w3.org/2000/01/rdf-schema#subClassOf'].iterrows():
        superclass = row['ols']
        predicate = row['predicate']
        ols = row['sls']
        if superclass in G:  # Check if the superclass exists in the graph
            descendants = nx.descendants(G, superclass)
            for descendant in descendants:
                inferred_df = pd.concat([inferred_df, pd.DataFrame(
                    {'sls': [descendant], 'predicate': [predicate], 'ols': [ols],
                     'origin': ['inferred relationship']})], ignore_index=True)
        else:
            print(f"Warning: The node {superclass} is not in the graph.")

    return asserted_df, inferred_df


# Example usage
data = {
    'sls': ['oak', 'plant', 'tree', 'cell', 'organism', 'plant'],
    'predicate': ['http://www.w3.org/2000/01/rdf-schema#subClassOf', 'http://www.w3.org/2000/01/rdf-schema#subClassOf',
                  'http://www.w3.org/2000/01/rdf-schema#subClassOf', 'part_of', 'made_of', 'has_color'],
    'ols': ['tree', 'organism', 'plant', 'organism', 'cell', 'green']
}
df = pd.DataFrame(data)

asserted_df, inferred_df = infer_relationships(df)

# Sort the asserted dataframe by 'sls', 'predicate', and 'ols'
asserted_df = asserted_df.sort_values(['sls', 'predicate', 'ols'])

# Sort the inferred dataframe by 'sls', 'predicate', and 'ols'
inferred_df = inferred_df.sort_values(['sls', 'predicate', 'ols'])

print("Asserted relationships:")
print(asserted_df)
print("\nInferred relationships:")
print(inferred_df)
