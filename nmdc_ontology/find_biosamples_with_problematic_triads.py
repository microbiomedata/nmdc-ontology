import click
import yaml


@click.command()
@click.option('--biomes-file', '-b', default="../data-vs-ontology-reports/envo-biomes.txt",
              help='Path to the file containing valid biome terms.')
@click.option('--materials-file', '-m', default="../data-vs-ontology-reports/envo-environmental-materials.txt",
              help='Path to the file containing valid environmental materials.')
@click.option('--all-envo-classes-file', '-c', default="../data-vs-ontology-reports/envo-all-classes.txt",
              help='Path to the file containing all ENVO classes.')
@click.option('--biosamples-file', '-f', default="../data-vs-ontology-reports/biosample-triad-report.tsv",
              help='Path to the annotated biosamples table.')
@click.option('--output', '-o', default="problematic_triads.tsv", help='Path to the output file.')
@click.option('--output-summary', '-s', default="problem_summary.yaml", help='Path to the summary output YAML file.')
def validate_biosamples(biomes_file, materials_file, all_envo_classes_file, biosamples_file, output, output_summary):
    # Dictionary to store valid biome terms and their labels
    valid_biomes = {}
    with open(biomes_file, "r") as f:
        for line in f:
            term_id, label = line.strip().split(" ! ")
            valid_biomes[term_id] = label

    # Dictionary to store valid environmental materials and their labels
    valid_env_materials = {}
    with open(materials_file, "r") as f:
        for line in f:
            term_id, label = line.strip().split(" ! ")
            valid_env_materials[term_id] = label

    # Dictionary to store all ENVO classes and their labels
    envo_classes = {}
    with open(all_envo_classes_file, "r") as f:
        for line in f:
            term_id, label = line.strip().split(" ! ")
            envo_classes[term_id] = label

    # Function to get label for a term ID
    def get_label(term_id, valid_terms):
        return valid_terms.get(term_id, envo_classes.get(term_id, None))

    # Function to parse biosamples table and collect problematic terms
    def parse_biosamples_table(table_file):
        problematic_triads = []
        problematic_env_broad_scale = set()
        problematic_env_medium = set()
        with open(table_file, "r") as f:
            next(f)  # Skip header line
            for line in f:
                parts = line.strip().split("\t")
                biosample_id = parts[0]
                env_broad_scale_term_id = parts[1]
                env_medium_rm_id = parts[3]
                problematic_env_broad_scale_val = 'true' if env_broad_scale_term_id not in valid_biomes else 'false'
                problematic_env_medium_val = 'true' if env_medium_rm_id not in valid_env_materials else 'false'
                any_problem = 'true' if problematic_env_broad_scale_val == 'true' or problematic_env_medium_val == 'true' else 'false'
                problematic_triads.append(
                    "\t".join(parts + [problematic_env_broad_scale_val, problematic_env_medium_val, any_problem]))

                if problematic_env_broad_scale_val == 'true':
                    problematic_env_broad_scale.add(env_broad_scale_term_id)
                if problematic_env_medium_val == 'true':
                    problematic_env_medium.add(env_medium_rm_id)

        return problematic_triads, problematic_env_broad_scale, problematic_env_medium

    # Parse biosamples table and collect problematic terms
    problematic_triads, problematic_env_broad_scale, problematic_env_medium = parse_biosamples_table(biosamples_file)

    # Write problematic_triads.tsv file
    with open(output, "w") as f:
        f.write(
            "biosample_id\tenv_broad_scale_term_id\tenv_local_scale_term_id\tenv_medium_rm_id\tproblematic_env_broad_scale\tproblematic_env_medium\tany_problem\n")
        for line in problematic_triads:
            f.write(line + "\n")

    print(f"Validation results written to {output}")

    # Write summary to YAML file
    summary = {
        "problematic_env_local_scale_term_ids": [{"term": term_id, "label": get_label(term_id, valid_biomes)} for
                                                 term_id in problematic_env_broad_scale],
        "problematic_env_medium_rm_ids": [{"term": term_id, "label": get_label(term_id, valid_env_materials)} for
                                          term_id in problematic_env_medium]
    }
    with open(output_summary, "w") as f:
        yaml.dump(summary, f, default_flow_style=False)

    print(f"Validation summary written to {output_summary}")


if __name__ == "__main__":
    validate_biosamples()
