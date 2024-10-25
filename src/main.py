import pydot # type: ignore
import os
import sys

from dijkstra_dot import dijkstra_dot
from utils import add_all_nodes, change_color_link

def error_handler(all_nodes_names: list[str], start: str, end: str):
    """
    Check if the start and end nodes are in the graph.
    Otherwise, print an error message and exit the program.
    """
    if start not in all_nodes_names:
        print(f'Node {start} not in graph')
        sys.exit(1)
    if end not in all_nodes_names:
        print(f'Node {end} not in graph')
        sys.exit(1)

if __name__ == '__main__':
    # if not arguments are passed, quit
    if len(sys.argv) < 4:
        print('Usage: python3 src/main.py <graph_path> <node_start> <node_end> [output_file]')
        sys.exit(1)
    
    graphs = pydot.graph_from_dot_file(sys.argv[1])
    start = sys.argv[2]
    end = sys.argv[3]
    output_file = 'graph.png' if len(sys.argv) < 5 else sys.argv[4]

    for graph in graphs:
        graph, all_nodes_names = add_all_nodes(graph)

        error_handler(all_nodes_names, start, end)

        data = dijkstra_dot(graph, start)

        last_node = start
        for node in data[end].path:
            change_color_link(graph, last_node, node, 'red')
            last_node = node
        change_color_link(graph, last_node, end, 'red')

        # add title to graph
        graph.set_label(f'Dijkstra from {start} to {end}\nDistance: {data[end].dist}')

        graph.write_png(output_file)
        print(f'Graph saved as {output_file}')

