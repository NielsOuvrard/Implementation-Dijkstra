import pydot
import os
import sys

from dijkstra_dot import dijkstra_dot


def change_color_link(graph, node1, node2, color):
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
            
def add_all_nodes(graph):
    all_nodes_names = []
    # Ensure all nodes are added to the graph, only once
    for edge in graph.get_edges():
        if edge.get_source() not in all_nodes_names:
            graph.add_node(pydot.Node(edge.get_source()))
            all_nodes_names.append(edge.get_source())
        if edge.get_destination() not in all_nodes_names:
            graph.add_node(pydot.Node(edge.get_destination()))
            all_nodes_names.append(edge.get_destination())
    return graph, all_nodes_names

def error_handler(all_nodes_names, start, end):
    if start not in all_nodes_names:
        print(f'Node {start} not in graph')
        sys.exit(1)
    if end not in all_nodes_names:
        print(f'Node {end} not in graph')
        sys.exit(1)

if __name__ == '__main__':
    # if not arguments are passed, quit
    if len(sys.argv) < 4:
        print('Usage: python3 src/main.py <graph_path> <node_start> <node_end>')
        sys.exit(1)
    
    graphs = pydot.graph_from_dot_file(sys.argv[1])
    start = sys.argv[2]
    end = sys.argv[3]

    for graph in graphs:
        graph, all_nodes_names = add_all_nodes(graph)

        error_handler(all_nodes_names, start, end)

        data = dijkstra_dot(graph, start)
        print(data[end])

        last_node = start
        for node in data[end]['path']:
            print(f'coloring {last_node} - {node} red')
            change_color_link(graph, last_node, node, 'red')
            last_node = node
        change_color_link(graph, last_node, end, 'red')

        graph.write_png(f'graph.png')
        print(f'graph.png saved')

