# python simple Dijkstra
import pydot # type: ignore
from utils import Node, add_all_nodes


def neighbors(graph: pydot.Dot, node: str) -> list[Node]:
    """
    Get all neighbors of a node in the graph.
    
    This function returns a list of all neighbors of a node in the graph. It iterates through all edges of the graph and checks if the node is the source or destination of the edge. If the node is the source, it appends the destination node to the list of neighbors. If the node is the destination, it appends the source node to the list of neighbors.
    
    Args:
        graph (pydot.Dot): The graph object containing the edges.
        node (str): The node to get the neighbors for.
        
    Returns:
        list[Node]: A list of all neighbors of the node.
    """
    neighbors: list[Node] = []
    for edge in graph.get_edges():
        weight = edge.get('label').strip("\"")
        if float(weight) < 0:
            print(f'Error: negative weight found in edge {edge.get_source()} -> {edge.get_destination()}')
            exit(1)
        if edge.get_source() == node:
            neighbors.append(Node(edge.get_destination(), float(weight), []))
        elif edge.get_destination() == node:
            neighbors.append(Node(edge.get_source(), float(weight), []))
    return neighbors


def dijkstra_dot(graph: pydot.Dot, start: str) -> dict[str, Node]:
    """
    Apply Dijkstra's algorithm to a graph.

    This function applies Dijkstra's algorithm to a graph and returns a dictionary with the distances and paths from the start node to all other nodes in the graph.

    Args:
        graph (pydot.Dot): The graph object to apply Dijkstra's algorithm to.
        start (str): The name of the start node.

    Returns:
        dict[str, Node]: A dictionary containing the distances and paths from the start node to all other nodes in the graph.
    """
    distances = {node.get_name(): Node(node.get_name(), float('inf'), []) for node in graph.get_nodes()}
    distances[start] = Node(start, 0, [])
    
    unvisited: list[str] = [node.get_name() for node in graph.get_nodes()]

    while unvisited:
        current_node: str = min(unvisited, key=lambda node: distances[node].dist)

        for neighbor in neighbors(graph, current_node):
            distance = distances[current_node].dist + neighbor.dist

            if distance < distances[neighbor.name].dist:
                distances[neighbor.name].dist = distance
                distances[neighbor.name].path = distances[current_node].path +\
                    ([current_node] if current_node != start else [])

        unvisited.remove(current_node)

    return distances


## Testing
if __name__ == '__main__':
    """
    Test the dijkstra_dot function with the graph in graphs/graph1.dot, with all nodes as starting nodes.
    """
    graph = pydot.graph_from_dot_file('graphs/graph1.dot')[0]

    graph, nodes = add_all_nodes(graph)

    for node in nodes:
        print(f'\033[94mNode {node}:\033[0m')

        data = dijkstra_dot(graph, node)

        for key, value in data.items():
            if key != node:
                print(f'\tNode {value}')
