import random


def random_path(graph, source, target):
    current = source
    path = [current]
    visited = {current}

    while current != target:
        candidates = [v for v, w in graph[current] if v not in visited]

        if not candidates:
            return None

        current = random.choice(candidates)
        path.append(current)
        visited.add(current)

    return path