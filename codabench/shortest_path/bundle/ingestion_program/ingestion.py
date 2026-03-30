import json
import os
import sys
import time
import re


input_dir = '/app/input_data/'
output_dir = '/app/output/'
program_dir = '/app/program'
submission_dir = '/app/ingested_program'
sys.path.append(program_dir)
sys.path.append(submission_dir)


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


def save_predictions(predictions):
    """ Input: dictionnary containing predicted path for each graph.
        Output: predictions.json
    """
    # Save scores
    with open(os.path.join(output_dir, 'predictions.json'), 'w') as prediction_file:
        prediction_file.write(json.dumps(predictions))


def main():
    # Import participant submitted model
    from model import Model
    print('Reading Data')
    graphs = get_data(input_dir)
    print('Starting')
    start = time.time()
    m = Model()
    print('Running optimization')
    predictions = {}
    for graph_name, graph_data in graphs.items():
        print(f'--- Solving {graph_name}')
        predictions[graph_name] = m.solve(graph_data)
    duration = time.time() - start
    print(f'Run completed. Total duration: {duration}')
    print('Saving predictions')
    save_predictions(predictions)
    with open(os.path.join(output_dir, 'metadata.json'), 'w+') as f:
        json.dump({'duration': duration}, f)
    print('Ingestion Program finished. Moving on to scoring')


if __name__ == '__main__':
    main()
