import sys
import re

def generate_unique_name(label):
    # Remove any non-alphanumeric characters and replace spaces with underscores
    clean_label = re.sub(r'[^a-zA-Z0-9 ]+', '', label).replace(' ', '_')
    # Add a prefix to ensure the name is valid in DOT language
    unique_name = 'node_' + clean_label
    return unique_name

def rename_nodes(dot_file):
    with open(dot_file, 'r') as f:
        lines = f.readlines()

    renamed_lines = []
    node_labels = {}

    for line in lines:
        if '->' in line:  # Edge definition
            # Check if either source or target node has a label
            match = re.search(r'(\w+)\s*->\s*(\w+)', line)
            if match:
                source_node, target_node = match.groups()
                if source_node in node_labels:
                    line = line.replace(source_node, node_labels[source_node])
                if target_node in node_labels:
                    line = line.replace(target_node, node_labels[target_node])

        elif '[' in line and 'label' in line:  # Node definition with label
            match = re.search(r'(\w+)\s*\[.*label\s*=\s*"(.*?)".*\]', line)
            if match:
                node, label = match.groups()
                if label:
                    unique_name = generate_unique_name(label)
                    line = line.replace(node, unique_name)
                    node_labels[node] = unique_name

        renamed_lines.append(line)

    # Iterate over the lines again and replace occurrences of node names with renamed versions
    renamed_lines_second_pass = []
    for line in renamed_lines:
        for node, renamed_node in node_labels.items():
            line = line.replace(node, renamed_node)
        renamed_lines_second_pass.append(line)

    renamed_dot_file = dot_file.replace('.dot', '_renamed.dot')

    with open(renamed_dot_file, 'w') as f:
        f.writelines(renamed_lines_second_pass)

    print(f"Renamed DOT file saved as {renamed_dot_file}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python merge_col_v1.py input1.dot input2.dot ...")
        return

    dot_files = sys.argv[1:]  # Paths to the input DOT files

    for dot_file in dot_files:
        rename_nodes(dot_file)

if __name__ == "__main__":
    main()

