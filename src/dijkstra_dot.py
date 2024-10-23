# python simple Dijkstra
import pydot

def neighbors(graph: pydot.Dot, node: str):
    neighbors = []
    for edge in graph.get_edges():
        if edge.get_source() == node:
            neighbors.append({'node': edge.get_destination(), 'weight': int(edge.get('label').strip("\""))})
        elif edge.get_destination() == node:
            neighbors.append({'node': edge.get_source(), 'weight': int(edge.get('label').strip("\""))})
    return neighbors


def dijkstra_dot(graph: pydot.Dot, start: str):
    distances = {}
    for node in graph.get_nodes():
        distances[node.get_name()] = {
            'dist': float('infinity'),
            'path': []
        }
    distances[start]['dist'] = 0
    
    unvisited = graph.get_nodes()

    while unvisited:
        current_node = min(unvisited, key=lambda node: distances[node.get_name()]['dist'])

        for neighbor in neighbors(graph, current_node.get_name()):
            distance = distances[current_node.get_name()]['dist'] + neighbor['weight']

            if distance < distances[neighbor['node']]['dist']:
                distances[neighbor['node']]['dist'] = distance
                distances[neighbor['node']]['path'] = distances[current_node.get_name()]['path'] +\
                    ([current_node.get_name()] if current_node.get_name() != start else [])

        unvisited.remove(current_node)

    return distances


## Testing
if __name__ == '__main__':
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

    graph = pydot.graph_from_dot_file('graphs/graph1.dot')[0]

    graph, _ = add_all_nodes(graph)

    for node in graph.get_nodes():
        print(f'\033[94mNode {node.get_name()}:\033[0m')

        data = dijkstra_dot(graph, node)

        for key, value in data.items():
            print(f'\tNode {key}: {value}')

        
