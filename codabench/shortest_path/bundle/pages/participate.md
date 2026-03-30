# How to participate

To participate, you should submit a Python file `model.py` containing a class `Model` with a method `solve`.

Your submitted code will be imported and executed on Codabench.

## Required interface

Your `model.py` file must define:

```python
class Model:
    def solve(self, graph_data):
        ...
```

The input `graph_data` is a tuple:

```python
(graph, source, target)
```

where:

- `graph` is a dictionary such that `graph[node] = [(neighbor, weight), ...]`
- `source` is the source node id
- `target` is the target node id


## Expected output

The method `solve(graph_data)` must return one path, represented as a list of node ids.

Example:

```
[0, 2, 1, 3, 4, 5]
```

## Starting kit

Download the starting kit in the Files tab to get started!

Inside the starting kit you'll find the following files:

- `README.md`
- `model.py`: an example algorithm
- `random_path.py`: utilities for random_path baseline
- `random_path.py`: utilities for Dijkstra baseline
- `random_path_submission.zip`: a ready-to-submit file containing Dijkstra baseline
- `dijkstra_submission.zip`: a ready-to-submit file containing Dijkstra baseline

## Public data

See the public data in the Files tab for:
- example graph files
