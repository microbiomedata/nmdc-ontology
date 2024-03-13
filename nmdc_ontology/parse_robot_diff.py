import re
import csv

input_file = "assets/robot_diff.txt"
output_file = "assets/parse_robot_diff.tsv"

# Read the "robot diff" output from a file
with open(input_file, 'r') as file:
    diff_output = file.read()

# Split the output into lines
lines = diff_output.strip().split('\n')

# Initialize an empty list to store the parsed data
table_data = []

# Regular expression pattern to match the axioms
axiom_pattern = re.compile(r'^([\+\-])\s+(\w+)\((\S+)\s+(\S+)\)$')

# Iterate over each line in the diff output
for line in lines:
    # Check if the line matches the axiom pattern
    match = axiom_pattern.match(line)
    if match:
        # Extract the relevant parts from the matching line
        in_right = match.group(1)
        relationship = match.group(2)
        left_uri = match.group(3)
        right_uri = match.group(4)

        # Create a dictionary with the parsed data
        row_dict = {
            'in_right': in_right,
            'Relationship': relationship,
            'Left URI': left_uri,
            'Right URI': right_uri
        }

        # Append the dictionary to the table_data list
        table_data.append(row_dict)
    else:
        # If the line doesn't match the pattern, print it out
        print(f"Line not following the pattern: {line}")

# Open the TSV file for writing
with open(output_file, 'w', newline='') as file:
    # Create the CSV DictWriter object
    fieldnames = ['in_right', 'Relationship', 'Left URI', 'Right URI']
    writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='\t')

    # Write the table header
    writer.writeheader()

    # Write the table rows
    writer.writerows(table_data)

print(f"Output written to {output_file}")
