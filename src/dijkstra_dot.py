# python simple Dijkstra
import pydot # type: ignore

class Node:
    def __init__(self, name: str, dist: float, path: list[str]) -> None:
        self.name = name
        self.dist = dist
        self.path = path

    def __str__(self) -> str:
        return f'{self.name}: {self.dist}, {self.path}'

    def __repr__(self) -> str:
        return self.__str__()


def neighbors(graph: pydot.Dot, node: str) -> list[Node]:
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

        
