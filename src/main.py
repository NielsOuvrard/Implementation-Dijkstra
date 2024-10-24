import pydot # type: ignore
import os
import sys

from dijkstra_dot import dijkstra_dot


def change_color_link(graph: pydot.Dot, node1: str, node2: str, color: str):
    for edge in graph.get_edges():
        if edge.get_source() == node1 and edge.get_destination() == node2:
            edge.set_color(color)
            # remove "both" attribute to forward
            if edge.get('dir') == '"both"':
                edge.set('dir', 'forward')
        elif edge.get_source() == node2 and edge.get_destination() == node1:
            edge.set_color(color)
            # remove "both" attribute to back
            if edge.get('dir') == '"both"':
                edge.set('dir', 'back')
            
def add_all_nodes(graph: pydot.Dot) -> tuple[pydot.Dot, list[str]]:
    all_nodes_names: list[str] = []
    # Ensure all nodes are added to the graph, only once
    for edge in graph.get_edges():
        if edge.get_source() not in all_nodes_names:
            graph.add_node(pydot.Node(edge.get_source()))
            all_nodes_names.append(edge.get_source())
        if edge.get_destination() not in all_nodes_names:
            graph.add_node(pydot.Node(edge.get_destination()))
            all_nodes_names.append(edge.get_destination())
    return graph, all_nodes_names

def error_handler(all_nodes_names: list[str], start: str, end: str):
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

