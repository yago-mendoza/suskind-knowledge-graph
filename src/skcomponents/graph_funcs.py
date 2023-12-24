from skgraph import Graph
from collections import deque

class Path:
    def __init__(self, nodes, edges):
        self.nodes = nodes  # Tuple of nodes
        self.edges = edges  # Tuple of edges

    def __repr__(self):
        # Representation showing the length of the path (number of edges)
        return f"<Path(length={len(self.edges)})>"

def find_shortest_path(graph, start, end):
    queue = deque([(start, [], [])])
    visited = set()

    while queue:
        current_node, node_path, edge_path = queue.popleft()
        if current_node == end:
            # Create a Path instance with nodes and edges and return it
            return Path(tuple(node_path + [current_node]), tuple(edge_path))

        visited.add(current_node)
        neighbors = current_node.get_neighbors()
        if neighbors is None:
            continue

        for edge, neighbor_nodeset in neighbors.items():
            for neighbor in neighbor_nodeset:
                if neighbor in visited:
                    continue
                queue.append((neighbor, node_path + [current_node], edge_path + [edge]))
                visited.add(neighbor)

    return None  # Return None if no path is found

def calculate_similarity(graph, node1, node2):
    # Inicialización de variables
    direct_similarity = 0
    jaccard_similarity = 0
    neighbor_similarity = 0
    path_length_factor = 0
    centrality_factor = 0
    
    # 1. Coincidencia Directa (preponderante)
    if node1 in graph and node2 in graph and node1.is_connected(n2):
        direct_similarity = 1  # Un valor alto para reflejar su importancia
    
    print(direct_similarity)
    
    # 2. Jaccard Similarity para relaciones vecinas
    neighbors1 = set(node1.get_neighbors())
    neighbors2 = set(node2.get_neighbors())
    intersection = neighbors1.intersection(neighbors2)
    union = neighbors1.union(neighbors2)
    if union:
        jaccard_similarity = len(intersection) / len(union)
    print(jaccard_similarity)
    
    # 3. Estudio de relaciones vecinas
    neighbor_similarity = len(intersection)  # Cuantos más vecinos en común, mayor similaridad
    print(neighbor_similarity)
    
    # 4. Longitud del camino
    path_length = len(find_shortest_path(G, node1, node2).nodes)  # asume una función hipotética que encuentra la longitud del camino más corto
    if path_length:
        path_length_factor = 1 / path_length  # Un camino más corto aumenta la similaridad
    
    print(path_length)

    # 5. Centralidad de los nodos
    centrality_factor = (node1.centrality + node2.centrality) / 2  # asume que 'centrality' es una propiedad precalculada de los nodos
    print(centrality_factor)

    # Agregación de factores con ponderaciones
    similarity_score = (5 * direct_similarity +
                        3 * jaccard_similarity +
                        2 * neighbor_similarity +
                        2 * path_length_factor +
                        3 * centrality_factor) / 15  # Ponderaciones ajustables según la importancia relativa
    
    return similarity_score

G = Graph('data.txt')
n1, n2 = G.random(2)
print(n1, n2)
print(calculate_similarity(G, n1, n2))