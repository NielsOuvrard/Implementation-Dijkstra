# The dijkstra algorithm

## Initial setup

```shell
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

## Usage

```shell
Usage: python3 src/main.py <graph_path> <node_start> <node_end> [output_file]
```

## For example

```shell
python3 src/main.py graphs/graph1.dot A F examples/graph1_solved.png
```

In this case, the program will find the shortest path from node A to node D in the graph1.dot file.
It will create a `graph.png` file with the graph and the shortest path, in red.

### CLI output

![Screenshot_CLI.png.png](examples/Screenshot_CLI.png)

### Graph1 original

![graph1_original.png](examples/graph1_original.png)

### Graph1 solved

![graph1_solved.png](examples/graph1_solved.png)

## Team members

- [Raquel Magdalena Ochoa Martínez](https://github.com/raqueochoam)
- [Santiago Perez Ochoa](https://github.com/santi1025)
- [Niels Ouvrard](https://github.com/NielsOuvrard).
