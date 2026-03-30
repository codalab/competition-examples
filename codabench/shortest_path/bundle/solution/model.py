from dijkstra import dijkstra_shortest_path
#from random_path import random_path

class Model:
    def solve(self, graph_data):
        graph, source, target = graph_data
        path = dijkstra_shortest_path(graph, source, target)
        #path = random_path(graph, source, target)
        return path
