# Data

Each graph is stored as a JSON file.

A graph file contains:
- whether the graph is directed or not
- the source node
- the target node
- the list of nodes
- the list of weighted edges

## Format

Example:

```json
{
  "directed": false,
  "source": 0,
  "target": 5,
  "nodes": [0, 1, 2, 3, 4, 5],
  "edges": [
    [0, 1, 4],
    [0, 2, 2],
    [1, 2, 1],
    [1, 3, 5],
    [2, 3, 8],
    [2, 4, 10],
    [3, 4, 2],
    [3, 5, 6],
    [4, 5, 3]
  ]
}
```

## Meaning of the fields

- `directed`: boolean indicating whether edges are directed
- `source`: id of the source node
- `target`: id of the target node
- `nodes`: list of node ids
- `edges`: list of edges of the form `[u, v, w]`

Here:

- `u` is the starting node of the edge
- `v` is the ending node of the edge
- `w` is the edge weight, that is, its cost

If `directed` is `false`, then an edge `[u, v, w]` can be used in both directions.
