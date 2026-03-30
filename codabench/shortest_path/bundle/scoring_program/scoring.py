import json
import os
import re
import matplotlib.pyplot as plt
import io
import base64


reference_dir = os.path.join('/app/input/', 'ref')  # Graph data
prediction_dir = os.path.join('/app/input/', 'res') # Input from ingestion program
score_dir = '/app/output/'                          # To write the scores
score_file = os.path.join(score_dir, 'scores.json')           # Scores
html_file = os.path.join(score_dir, 'detailed_results.html')  # Detailed feedback
INVALID_COST = 10**4 # penalty when the path is invalid

def load_graph(path):
    """ Load graph from file path.
    """
    with open(path, "r") as f:
        data = json.load(f)
    directed = data.get("directed", False)
    source = data["source"]
    target = data["target"]
    nodes = data["nodes"]
    edges = data["edges"]
    graph = {node: [] for node in nodes}
    for u, v, w in edges:
        graph[u].append((v, w))
        if not directed:
            graph[v].append((u, w))
    return graph, source, target


def get_data(input_dir):
    """ Get all graph data.
    """
    graphs = {}

    # Get graph files: graph-0.json, graph-1.json, etc.
    pattern = re.compile(r"^graph-(\d+)\.json$")
    graph_files = []
    for filename in os.listdir(input_dir):
        match = pattern.match(filename)
        if match:
            graph_index = int(match.group(1))
            graph_files.append((graph_index, filename))
    graph_files.sort()

    for i, filename in graph_files:
        graph_name = f'graph-{i}'
        graphs[graph_name] = load_graph(os.path.join(input_dir, filename))
    return graphs


def load_predictions(path):
    """ Load predictions made by the submitted algorithm.
    """
    with open(path, "r") as f:
        predictions = json.load(f)
    return predictions


def compute_path_cost(graph, source, target, path, invalid_cost=INVALID_COST):
    """Validate one path and compute its cost.
    """
    if path is None:
        print("Path is None")
        return invalid_cost
    if not isinstance(path, list):
        raise ValueError("Path must be a list of node ids")
    if len(path) == 0:
        print("Empty path")
        return invalid_cost
    if path[0] != source:
        print(f"Path must start at source {source}")
        return invalid_cost
    if path[-1] != target:
        print(f"Path must end at target {target}")
        return invalid_cost
    total_cost = 0
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        if u not in graph:
            print(f"Unknown node in path: {u}")
            return invalid_cost
        found = False
        for neighbor, weight in graph[u]:
            if neighbor == v:
                total_cost += weight
                found = True
                break
        if not found:
            print(f"Invalid edge in path: {u} -> {v}")
            return invalid_cost
    return total_cost


def compute_score(graphs, predictions):
    """Score all graphs depending on predicted paths.
    """
    total_cost = 0
    all_costs = {}
    for graph_name, graph_data in graphs.items():
        print(f'--- Scoring {graph_name}')
        if graph_name not in predictions:
            raise ValueError(f"Missing prediction for {graph_name}")
        graph, source, target = graph_data
        path = predictions[graph_name]
        cost = compute_path_cost(graph, source, target, path)
        total_cost += cost
        all_costs[graph_name] = cost
    mean_cost = total_cost / len(graphs)
    return mean_cost, all_costs


def save_scores(scores):
    """ Input: dictionnary containing scores.
        Output: scores.json
    """
    with open(score_file, 'w') as f:
        f.write(json.dumps(scores))


def write_file(file, content):
    """ Write content in file.
    """
    with open(file, 'a', encoding="utf-8") as f:
        f.write(content)


import matplotlib.pyplot as plt


def make_figure(all_costs):
    """ all_costs: dict like {"graph-0": 7, "graph-1": 12}
        returns: matplotlib figure
    """
    items = sorted(all_costs.items())
    graph_names = [k for k, v in items]
    raw_costs = [v for k, v in items]
    valid_costs = [c for c in raw_costs if c != INVALID_COST]
    if valid_costs:
        invalid_bar_height = max(valid_costs) * 1.2
        ymax = max(valid_costs) * 1.35
    else:
        invalid_bar_height = 1
        ymax = 2
    display_costs = []
    colors = []
    for cost in raw_costs:
        if cost == INVALID_COST:
            display_costs.append(invalid_bar_height)
            colors.append("red")
        else:
            display_costs.append(cost)
            colors.append("C0")
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(graph_names, display_costs, color=colors)
    for bar, raw_cost, shown_cost in zip(bars, raw_costs, display_costs):
        x = bar.get_x() + bar.get_width() / 2
        if raw_cost == INVALID_COST:
            ax.text(
                x,
                shown_cost - 0.05 * ymax,
                f"invalid\n({INVALID_COST})",
                ha="center",
                va="bottom",
                fontsize=9,
                rotation=0,
                color="black",
                fontweight="bold"
            )
        else:
            ax.text(
                x,
                shown_cost + 0.02 * ymax,
                str(raw_cost),
                ha="center",
                va="bottom",
                fontsize=9
            )
    ax.set_title("Path cost per graph")
    ax.set_xlabel("Graph")
    ax.set_ylabel("Cost")
    ax.set_ylim(0, ymax)
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()
    return fig


def fig_to_b64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    fig_b64 = base64.b64encode(buf.getvalue()).decode('ascii')
    return fig_b64


def main():
    # Initialized detailed results
    write_file(html_file, '<h1>Detailed results</h1>')
    print('Reading data')
    graphs = get_data(reference_dir)
    print('Reading prediction')
    predictions = load_predictions(os.path.join(prediction_dir, 'predictions.json'))

    with open(os.path.join(prediction_dir, 'metadata.json')) as f:
        duration = json.load(f).get('duration', -1)

    print('Checking path validity and computing cost')
    score, all_costs = compute_score(graphs, predictions)
    scores = {
        'score': score,
        'all_costs': all_costs,
        'duration': duration
    }
    print('Scores:')
    print(scores)

    # Save scores
    save_scores(scores)

    # Create a figure for detailed results
    figure = fig_to_b64(make_figure(all_costs))
    write_file(html_file, f'<img src="data:image/png;base64,{figure}">')


if __name__ == '__main__':
    main()
