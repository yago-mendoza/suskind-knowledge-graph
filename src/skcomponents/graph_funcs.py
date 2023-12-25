from sknodeset import NodeSet
from collections import deque

class Path:
    def __init__(self, nodes, edges):
        self.nodes = nodes  # Tuple of nodes
        self.edges = edges  # Tuple of edges

    def __repr__(self):
        # Representation showing the length of the path (number of edges)
        return f"<Path(length={len(self.edges)})>"

def shortest_path (start, end):
    if start == end:
        return Path(NodeSet((start,)), ())
    
    queue = deque([(start, [], [])])  # Queue of tuples: (current_node, node_path, edge_path)
    visited = {start}  # Set of visited nodes to avoid revisiting

    while queue:
        current_node, node_path, edge_path = queue.popleft()
        
        # Iterate through each neighbor of the current node
        neighbors = current_node.get_neighbors()
        if neighbors is None:
            continue

        for edge, neighbor_nodeset in neighbors.items():
            for neighbor in neighbor_nodeset:
                if neighbor == end:
                    # Return path immediately once the end is found
                    return Path(NodeSet(tuple(node_path + [current_node, neighbor])), tuple(edge_path + [edge]))
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, node_path + [current_node], edge_path + [edge]))

    # Return an empty path if no path is found
    return Path(NodeSet(), ())


def common(*nodes):
    # Proximamente, personalizar tipo de conexiones para cada nodo.
    output = intersect(*nodes)
    for node in nodes:
        neighbors = node.get_neighbors().set()
        #sigue programando la idea es hacer islitas lo de los antiguso suskind vamos!

def intersect(*nodes):
    # is used as *NodeSet or directly, (node1, node2,)
    if not nodes:
        return set()
    # Base case: if only one node is provided, return its neighbors
    if len(nodes) == 1:
        return nodes[0].get_neighbors().set()   
    # Recursive case: intersect the neighbors of the first node with the result of the recursive call on the rest of the nodes
    return nodes[0].get_neighbors().set().intersection(intersect(*nodes[1:]))

def containment (node1, node2, depth=2):
    return _calculate_similarity(node1, node2, depth,
                                 strategy='containment')

def overlapping(node1, node2, depth=2):
    return _calculate_similarity(node1, node2, depth,
                                 strategy='coincidence')

def intersection(node1, node2, depth=2):
    return _calculate_similarity(node1, node2, depth,
                                 strategy='intersection')

def _calculate_similarity(node1, node2, depth, strategy):
    
    def jaccard_similarity(set1, set2):
        intersection = set1.intersection(set2)
        if strategy == 'containment':
            union = min(len(set1), len(set2))
        elif strategy == 'coincidence':
            union = max(len(set1), len(set2))
        elif strategy == 'intersection':
            union = len(set1) + len(set2) - len(intersection)
        return len(intersection) / union if union else 0
    
    def second_neighbors(first_layer):
        second_layer = set()
        for neighbor in first_layer:
            second_layer.update(neighbor.get_neighbors().set())
        return second_layer

    # Firs & Second Layer Analysis
    nghb11, nghb21 = node1.get_neighbors().set(), node2.get_neighbors().set()
    nghb12, nghb22 = second_neighbors(nghb11), second_neighbors(nghb21)

    # Weighted Jaccard similarity (weights can be adjusted as needed)
    weighted_jaccard = (0.7 * jaccard_similarity(nghb11, nghb21) +
                        0.3 * jaccard_similarity(nghb12, nghb22))

    return weighted_jaccard

