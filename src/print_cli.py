from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import pydot


class LinkToPrint:
    def __init__(self, src, dest, weight_sd, weight_ds):
        self.src = src
        self.dest = dest
        self.weight_sd = weight_sd
        self.weight_ds = weight_ds
    
    def __str__(self):
        return f'{self.src}-{self.dest}'

    def __repr__(self):
        return self.__str__()


def print_cli(graph: pydot.Dot, shortest_path: list[str], output_file: str):

    def add_link(links: list[LinkToPrint], src: str, dest: str, weight: int | float) -> list[LinkToPrint]:
        for i, link in enumerate(links):
            if (link.src == src and link.dest == dest) or (link.src == dest and link.dest == src):
                links[i] = LinkToPrint(link.src, link.dest, link.weight_sd, weight)
                break
        else:
            links.append(LinkToPrint(src, dest, weight, "-"))
        return links

    def fill_links(graph: pydot.Dot) -> list[LinkToPrint]:
        links : list[LinkToPrint] = []
        for edge in graph.get_edges():
            src = edge.get_source()
            dest = edge.get_destination()
            weight = float(edge.get('label').strip("\""))
            links = add_link(links, src, dest, weight)
            if edge.get('dir') == '"both"':
                links = add_link(links, dest, src, weight)
        return links

    def create_table(links: list[LinkToPrint]) -> Table:
        table = Table(title="Graph Representation", show_header=True, header_style="bold magenta")
        table.add_column("Node", justify="center", style="cyan", no_wrap=True)
        table.add_column("Connected To", justify="left")
        table.add_column("Weight ->", justify="center")
        table.add_column("Weight <-", justify="center")
    
        for link in links:
            table.add_row(link.src, link.dest, str(link.weight_sd), str(link.weight_ds))
        
        return table

    def show_path(path: list[str]):
        if not path:
            console.print(Panel("No path found!", style="bold red"))
            return

        path_str = " -> ".join(path)
        panel = Panel(f"Path: {path_str}", title="Shortest Path", border_style="bold green")
        console.print(panel)

    def show_output(output_file: str):
        panel = Panel(f'Graph saved as {output_file}', title='Output', border_style='bold blue')
        console.print(panel)

    table = create_table(fill_links(graph))

    console = Console()

    show_output(output_file)
    console.print()
    console.print(table)
    console.print()
    show_path(shortest_path)
