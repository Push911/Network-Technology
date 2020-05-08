import networkx as nx
import matplotlib.pyplot as plt
import random
from functools import reduce

LOSS_CHANCE = 0.95
SAMPLE = 10000
matrix = []
path = nx.path_graph(29)

graphInput = int(input("Enter which graph you want to see:\n"
                       "1: To draw linear graph\n"
                       "2: To draw cycle graph\n"
                       "3: To draw multi-graph\n"))


def reliability(graphPath):
    tries = 0
    for rep in range(SAMPLE):
        graph = graphPath.copy()

        for edge in list(graph.edges()):
            if random.random() > graph[edge[0]][edge[1]]['reliability']:
                graph.remove_edge(edge[0], edge[1])

        if nx.is_connected(graph):
            tries += 1

    return tries / SAMPLE


# Linear graph
if graphInput == 1:
    nx.draw(path)
    plt.savefig("Linear graph")
    nx.set_edge_attributes(path, LOSS_CHANCE, 'reliability')
    print("Linear graph reliability:", reliability(path))

# Cycle graph
cycle = path.copy()
cycle.add_edge(0, 28, reliability=0.9)
if graphInput == 2:
    nx.draw(cycle)
    plt.savefig("Cycle graph")
    nx.set_edge_attributes(cycle, LOSS_CHANCE, 'reliability')
    print("Cycle graph reliability:", reliability(cycle))

# Multi-graph
multi = cycle.copy()
multi.add_edge(10, 20, reliability=0.88)
multi.add_edge(1, 13, reliability=0.84)
multi.add_edge(7, 28, reliability=0.92)
multi.add_edge(17, 25, reliability=0.99)
multi.add_edge(12, 23, reliability=0.92)
multi.add_edge(3, 27, reliability=0.95)
multi.add_edge(23, 27, reliability=0.9)
if graphInput == 3:
    nx.draw(multi)
    plt.savefig("Multi-graph")
    nx.set_edge_attributes(multi, LOSS_CHANCE, 'reliability')
    print("Multi-graph reliability:", reliability(multi))


def createMatrix():
    for i in range(20):
        matrix.append([])
        for j in range(20):
            if i == j:
                matrix[i].append(0)
            else:
                matrix[i].append(random.randint(1, 20))


createMatrix()

for graph in cycle, multi:
    for edge in graph.edges():
        graph[edge[0]][edge[1]]['reliability'] = 0.95
        graph[edge[0]][edge[1]]['capacity'] = 100
        graph[edge[0]][edge[1]]['empty'] = 0


def fillMatrix(graph, matr):
    nx.set_edge_attributes(graph, 0, 'empty')
    for i, row in enumerate(matr):
        for j, n in enumerate(row):
            path = nx.shortest_path(graph, i, j)
            for k in range(len(path) - 1):
                graph[path[k]][path[k + 1]]['empty'] += n


def delay(graph, matr):
    fillMatrix(graph, matr)
    # G = matr.sum()
    # return 1 / G * sum([graph.get_edge_data(*e).get("empty")/(graph.get_edge_data(*e).get("capacity") - graph.get_edge_data(*e).get("empty"))])
    G = sum(reduce(lambda x, y: x + y, matr))
    d = 1 / G * sum([graph[es][ee]['empty'] / (graph[es][ee]['capacity'] - graph[es][ee]['empty'])
                     if graph[es][ee]['capacity'] > graph[es][ee]['empty'] else -1 for es, ee in graph.edges()])
    return d


for name, graph in ("Cycle graph", cycle), ("Multi-graph", multi):
    averageDelay = delay(graph, matrix)
    if averageDelay < 0:
        print(name, "delay was too much")
    else:
        print(name, "delay is:", averageDelay)


def delayReliability(gr, matr, tmax, loss, intervals=100):
    nx.set_edge_attributes(gr, loss, 'reliability')
    tries = 0
    for _ in range(1000):
        graph = gr.copy()

        for _ in range(intervals):
            for ed in list(graph.edges()):
                if random.random() > graph[ed[0]][ed[1]]['reliability']:
                    graph.remove_edge(*ed)

            if not nx.is_connected(graph):
                break

            d = delay(graph, matr)
            if 0 < d < tmax:
                tries += 1
    return tries / (1000 * intervals)


s = delayReliability(multi, matrix, 0.01, 0.98)
print("Delay reliability:", s)
