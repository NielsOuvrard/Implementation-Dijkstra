import pydot # type: ignore
import sys

from dijkstra_dot import dijkstra_dot
from utils import Node, add_all_nodes, highlight_shortest_path
from print_cli import print_cli

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

        data: dict[str, Node] = dijkstra_dot(graph, start)

        print_cli(graph, [start] + data[end].path + [end], output_file, data[end].dist)
    
        last_node = start
        for node in data[end].path:
            highlight_shortest_path(graph, last_node, node, 'red')
            last_node = node
        highlight_shortest_path(graph, last_node, end, 'red')

        # add title to graph
        graph.set_label(f'Dijkstra from {start} to {end}\nDistance: {data[end].dist}')

        graph.write_png(output_file)
