import pydot # type: ignore

class Node:
    """
    Node class to store the distance and path to a node.
    """
    def __init__(self, name: str, dist: float, path: list[str]) -> None:
        self.name = name
        self.dist = dist
        self.path = path

    def __str__(self) -> str:
        return f'{self.name}: {self.dist}, {self.path}'


def change_color_link(graph: pydot.Dot, node1: str, node2: str, color: str):
    """
    Change the color of a link between two nodes and remove the "both" attribute from the edge.

    This function iterates through the edges of the graph and changes the color of the edge between the specified nodes. If the edge has a "both" direction attribute, it changes it to "forward" or "back" depending on the direction of the edge.

    Args:
        graph (pydot.Dot): The graph object containing the edges.
        node1 (str): The source node of the edge.
        node2 (str): The destination node of the edge.
        color (str): The color to set for the edge.
    """
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
    """
    Ensure all nodes are added to the graph, only once, and return a list of all node names.

    Some nodes could be hidden if they are created directly as edges. This function ensures all nodes are added to the graph variable, only once. Furthermore, it returns a list with all node names.

    Args:
        graph (pydot.Dot): The graph object to which nodes will be added.

    Returns:
        tuple[pydot.Dot, list[str]]: A tuple containing the updated graph and a list of all node names.
    """
    all_nodes_names: list[str] = []

    for edge in graph.get_edges():
        if edge.get_source() not in all_nodes_names:
            graph.add_node(pydot.Node(edge.get_source()))
            all_nodes_names.append(edge.get_source())
        if edge.get_destination() not in all_nodes_names:
            graph.add_node(pydot.Node(edge.get_destination()))
            all_nodes_names.append(edge.get_destination())
    return graph, all_nodes_names
