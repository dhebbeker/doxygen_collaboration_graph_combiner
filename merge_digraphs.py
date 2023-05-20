import sys
import re

def combine_dot_files(input_files, output_file):
    nodes = {}
    edges = {}

    for file_name in input_files:
        with open(file_name, 'r') as file:
            for line in file:
                line = line.strip()
                if re.match(r'\b(node|edge)\b', line):
                    nodes[line] = line
                elif re.match(r'\bdigraph\b', line):
                    continue
                elif line.startswith(('}', '{')):
                    continue
                elif re.match(r'\b(subgraph|label)\b', line):
                    print(f'Warning: Ignoring unsupported statement: {line}')
                elif '->' in line:
                    source, rest = line.split('->', 1)
                    target = rest.split()[0]
                    edge_key = f'{source.strip()}->{target.strip()}'
                    edges[edge_key] = line.strip()
                else:
                    node_name = line.split()[0]
                    nodes[node_name] = line.strip()

    with open(output_file, 'w') as file:
        file.write('digraph combined {\n')
        for node_value in nodes.values():
            file.write(f'    {node_value}\n')
        for edge_value in edges.values():
            file.write(f'    {edge_value}\n')
        file.write('}\n')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python combine_dot_files.py [input_files] [output_file]')
        sys.exit(1)

    input_files = sys.argv[1:-1]
    output_file = sys.argv[-1]
    combine_dot_files(input_files, output_file)
    print(f'Combined DOT files written to {output_file}')

