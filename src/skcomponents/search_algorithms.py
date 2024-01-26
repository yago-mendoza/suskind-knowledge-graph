from src.skcomponents.sknodeset import NodeSet
from src.skcomponents.skpath import Path

from collections import deque
from itertools import combinations

def shortest_path (start, end, permission_string=''):
    if start == end:
        return Path(NodeSet((start,)), ())
    
    queue = deque([(start, [], [])])  # Queue of tuples: (current_node, node_path, edge_path)
    visited = {start}  # Set of visited nodes to avoid revisiting

    while queue:
        current_node, node_path, edge_path = queue.popleft()
        
        # Iterate through each neighbor of the current node
        neighbors = current_node.get_neighbors(permission_string)
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

def centrality(*nodes, scaled=False, permission_string=''):
    if not nodes:
        return {}
    
    # Paso 1: Identificar Intersecciones
    intersection_weights = {}  # Guarda el peso de cada intersección
    for r in range(2, len(nodes) + 1):  # Desde intersecciones de 2 hasta todas
        for combo in combinations(nodes, r):
            intersection = set.intersection(*(node.get_neighbors(permission_string).set() for node in combo))
            if intersection:
                for element in intersection:
                    intersection_weights[element] = intersection_weights.get(element, 0) + r  # Ponderar por el número de nodos
    
    # Paso 2 y 3: Calcular Contribuciones de Nodos
    node_contributions = {node: 0 for node in nodes}
    for node in nodes:
        neighbors = node.get_neighbors(permission_string).set()
        for element in neighbors:
            if element in intersection_weights:
                node_contributions[node] += intersection_weights[element]

    total_contribution = sum(node_contributions.values())
    
    if not scaled:
        if total_contribution > 0: normalized_contributions = {node: contrib / total_contribution for node, contrib in node_contributions.items()}
        else: normalized_contributions = {node: 0 for node in nodes}
        return normalized_contributions
    else:
        ideal_contribution = total_contribution / len(nodes) if nodes else 0
        scaled_contributions = {node: (contrib / ideal_contribution) if ideal_contribution else 0 for node, contrib in node_contributions.items()}
        return scaled_contributions
    
def intersect(*nodes, permission_string=''):
    # is used as *NodeSet or directly, (node1, node2,)
    if not nodes:
        return set()
    # Base case: if only one node is provided, return its neighbors
    if len(nodes) == 1:
        return nodes[0].get_neighbors(permission_string).set()   
    # Recursive case: intersect the neighbors of the first node with the result of the recursive call on the rest of the nodes
    return nodes[0].get_neighbors(permission_string).set().intersection(intersect(*nodes[1:]))

def containment (node1, node2, depth=2, permission_string=''):
    return _calculate_similarity(node1, node2, depth,
                                 strategy='containment',
                                 permission_string=permission_string)

def overlapping(node1, node2, depth=2, permission_string=''):
    return _calculate_similarity(node1, node2, depth,
                                 strategy='coincidence',
                                 permission_string=permission_string)

def intersection(node1, node2, depth=2, permission_string=''):
    return _calculate_similarity(node1, node2, depth,
                                 strategy='intersection',
                                 permission_string=permission_string)

def _calculate_similarity(node1, node2, depth, strategy, permission_string=''):
    
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
            second_layer.update(neighbor.get_neighbors(permission_string).set())
        return second_layer

    # Firs & Second Layer Analysis
    nghb11, nghb21 = node1.get_neighbors(permission_string).set(), node2.get_neighbors(permission_string).set()
    nghb12, nghb22 = second_neighbors(nghb11), second_neighbors(nghb21)

    # Weighted Jaccard similarity (weights can be adjusted as needed)
    weighted_jaccard = (0.7 * jaccard_similarity(nghb11, nghb21) +
                        0.3 * jaccard_similarity(nghb12, nghb22))

    return weighted_jaccard














# ESTOS DE DEBAJO LOS SAQUÉ DE SKNODESET.PY

def density_search(self, interest_nodes, *args, complement=False):

        # I want tolerance, operator and threshold to be allowed to be inputed as kwargs

        # I want that when '=0.0' or '=0' or '0' it returns the whole database.

        # G.density_search(n, '=', 0) >> 8 ¿¿¿HOW COME??? If candidates are at least related to 1 node from n

        # document this

        interest_nodes = NodeSet(interest_nodes)

        if isinstance(args[0], float):
            tolerance = args[0]
            operator, threshold = '=', round(tolerance * len(interest_nodes))
            fielding = args[1:] if len(args)>1 else []

        elif isinstance(args[0], int):
            operator, threshold, fielding = '=', args[0], args[1:] if len(args)>1 else []

        elif isinstance(args[0], str):
            operator, threshold, fielding = args[0], args[1], args[2:] if len(args)>2 else []

        candidates = self.get_contour(interest_nodes, *fielding)

        complying_candidates = []
        for candidate in candidates:
            ratio = sum([1 for neighbor in candidate.get_neighbors(*fielding) if neighbor in interest_nodes])
            success = self.___compare(ratio, operator, threshold)
            if success != complement:
                complying_candidates.append(candidate)

        return NodeSet(complying_candidates)

