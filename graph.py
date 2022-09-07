from platform import node
from queue import Queue

class Graph():
    def __init__(self, adjacency_matrix=None):
        if adjacency_matrix:
            self.adjacency_matrix = adjacency_matrix
        else:
            self.adjacency_matrix = {}
        self.nvertex = 0
        self.nedges = 0

    def add_vertex(self, vertex, on_error='print'):
        if vertex in self.adjacency_matrix:
            if on_error == 'print':
                print(f'vértice {vertex} já existe!')
            elif on_error == 'pass':
                pass
        else:
            self.adjacency_matrix[vertex] = {}
            self.nvertex += 1

    def add_edge(self, vertex_a, vertex_b, weight, on_error='print'):
        if self.has_edge(vertex_a, vertex_b):
            if on_error == 'print':
                print(f'aresta {(vertex_a, vertex_b)} já existe!')
            elif on_error == 'pass':
                pass
        else:
            self.adjacency_matrix[vertex_a][vertex_b] = weight
            self.adjacency_matrix[vertex_b][vertex_a] = weight
            self.nedges += 1

    def remove_edge(self, vertex_a, vertex_b):
        neighbors = {}
        if self.has_edge(vertex_a, vertex_b):
            for neighbor, weight in zip(list(self.adjacency_matrix[vertex_a].keys()),
                                        list(self.adjacency_matrix[vertex_a].values())):
                if neighbor != vertex_b:
                    neighbors[neighbor] = weight
            self.adjacency_matrix[vertex_a] = neighbors
            self.nedges -= 1
        else:
            print(f'aresta {(vertex_a, vertex_b)} não existe!')

    def remove_vertex(self, vertex):
        if vertex not in self.adjacency_matrix:
            print(f'vértice {vertex} não existe!')
        else:
            del self.grafo[vertex]
            self.nvertex -= 1

    def has_edge(self, vertex_a, vertex_b):
        if vertex_a not in self.adjacency_matrix or vertex_b not in self.adjacency_matrix:
            return False
        for node in list(self.adjacency_matrix[vertex_a].keys()):
            if node == vertex_b:
                return True
        return False

    def weight(self, vertex_a, vertex_b):
        if self.has_edge(vertex_a, vertex_b):
            return self.adjacency_matrix[vertex_a][vertex_b]
        return f'aresta {(vertex_a, vertex_b)} não existe!'

    def degree(self, vertex):
        if vertex in self.adjacency_matrix:
            return len(self.adjacency_matrix[vertex])
        return f'vértice {vertex} não existe'

    def get_adjacency_matrix(self, pretty=False):
        if pretty:
            for node, neighbors in zip(list(self.adjacency_matrix.keys()),
                                       list(self.adjacency_matrix.values())):
                print(node, neighbors)
        else:
            return self.adjacency_matrix

    def depth_first_search(self, start, end='all'):
        visited = []
        stack = [start]

        if end == 'all':
            end = stack
        else:
            end = end not in visited

        while end:
            vertex = stack.pop()
            if vertex not in visited:
                visited.append(vertex)
                stack.extend(set(self.adjacency_matrix[vertex].keys()) - set(visited))
        return visited

    def breadth_first_search(self, start, end='all'):
        visited = [start]
        queue = Queue()
        queue.put(start)

        if end == 'all':
            end = not queue.empty()
        else:
            end = end not in visited

        while end:
            vertex = queue.get()
            for neighbor in self.adjacency_matrix[vertex]:
                if neighbor not in visited:
                    visited.append(neighbor)
                    queue.put(neighbor)
        return visited

    def dijkstra(self, start='A', end='C'):
        nodes = list(self.adjacency_matrix.keys())
        unvisited = {node: None for node in nodes}
        current_distance = 0
        unvisited[start] = current_distance
        visited = {}

        while end not in visited:
            for neighbour, distance in self.adjacency_matrix[start].items():
                if neighbour not in unvisited:
                    continue

                new_distance = current_distance + distance

                if unvisited[neighbour] is None or unvisited[neighbour] > new_distance:
                    unvisited[neighbour] = new_distance

            visited[start] = current_distance
            del unvisited[start]
            
            if not unvisited:
                break
            
            candidates = [node for node in unvisited.items() if node[1]]
            start, current_distance = sorted(candidates, key = lambda x: x[1])[0]

        path = list(visited.keys())
        cost = list(visited.values())[-1]
        return path, cost