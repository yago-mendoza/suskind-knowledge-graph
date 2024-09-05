from src.skcomponents.sknodeset import NodeSet
from src.skcomponents.sknode import Node
from src.skcomponents.skpath import Path

from collections import deque
from itertools import combinations

import src.sktools as sk


def centrality(nodes, *fielding,
               depth=2, soiling_weight=0.1,
               rel_decay=0.50):
    
    # Pre-fetch neighbors for each node to optimize performance. 
    # Access pattern: "node_neighbors[node]"
    node_neighbors = {node: node.get_neighbors(*fielding) for node in nodes}

    # Initialize dictionary to count occurrences of each neighbor across all nodes.
    # This serves as a preliminary measure of a neighbor's relevance.
    neighbor_frequency = {}
    for neighbors in node_neighbors.values():
        for neighbor in neighbors:
            neighbor_frequency[neighbor] = neighbor_frequency.get(neighbor, 0) + 1
    # Adjust frequency to emphasize distant nodes by squaring counts. 
    neighbor_frequency = {n: count**2 for n, count in neighbor_frequency.items()}

    # Isolate neighbors that are shared (intersect) between nodes, discarding unique links.
    shared_neighbors_frequencies = {n: count for n, count in neighbor_frequency.items() if count > 1}

    # Aggregate adjusted frequencies of shared neighbors for each node. This forms the "standard score,"
    # a proxy for node centrality based on direct neighborhood overlap.
    standard_scoring = {node: sum(shared_neighbors_frequencies.get(neighbor, 0) for neighbor in neighbors) for node, neighbors in node_neighbors.items()}

    # Initiate depth-based scoring, augmenting centrality with distant neighbor influence.
    soil_scoring = {node: 0 for node in nodes}
    if depth > 1:
        # Deep dive beyond immediate neighbors, excluding the superficial layer.
        neighbors_by_depth = _traverse_nodes(nodes, max_depth=depth)

        if 0 in neighbors_by_depth:
            del neighbors_by_depth[0]
        elif 1 in neighbors_by_depth:
            del neighbors_by_depth[1]

        standard_weight = 1
        # Gradually diminish the influence of deeper neighbors to reflect decreasing relevance.
        for neighbors in neighbors_by_depth.values():
            standard_weight *= rel_decay
            for node in nodes:
                soil_scoring[node] += standard_weight * neighbors.count(node)

    # Benchmarks for depth influence scaling.
    max_score = max(standard_scoring.values()) if standard_scoring else 0
    max_soil_score = max(soil_scoring.values()) if soil_scoring else 0
 
    # Harmonize soil scoring with standard scoring, ensuring comparable magnitudes.
    rf = max_score/max_soil_score if max_soil_score else 1
    rescaled_soil_scoring = {node: score*rf for node, score in soil_scoring.items()}

    # Initialize dictionaries for node centrality and neighbor ratings.
    centralities, neighbor_ratings = {}, {}

    for node, neighbors in node_neighbors.items():
        # Calculate a composite score for each node. This score combines the significance of shared neighbors 
        # (reflected by 'standard_scoring') and the influence of network depth (through 'rescaled_soil_scoring'), 
        # normalized by the count of neighbors to ensure fairness across nodes with varying degrees of connectivity.
        score = standard_scoring[node] + soiling_weight * rescaled_soil_scoring[node]
        centralities[node] = score / len(neighbors) if neighbors else 0

        # Aggregate centrality contributions for each neighbor. This step cumulatively assesses the importance of each neighbor
        # based on the centrality scores of the nodes they connect to, providing a measure of their network influence.
        for neighbor in neighbors:
            neighbor_ratings[neighbor] = neighbor_ratings.setdefault(neighbor, 0) + centralities[node]

    # Normalize centrality scores to a [0, 1] scale, where 1 represents the highest centrality.
    max_centrality = max(centralities.values(), default=1) # Fallback to 1 for empty sets.
    if max_centrality != 0:
        for node in centralities:
            centralities[node] /= max_centrality
    
    # Similarly, normalize neighbor ratings
    max_neighbor_rating = max(neighbor_ratings.values(), default=1) # Ensures a non-zero divisor; defaults to 1.
    if max_neighbor_rating != 0:
        for neighbor in neighbor_ratings:
            neighbor_ratings[neighbor] /= max_neighbor_rating

    return centralities, neighbor_ratings

def _traverse_nodes(nodes, max_depth=5, depth=0, depth_dict=None):

    # Initialize depth_dict in the first call
    depth_dict = {} if depth_dict is None else depth_dict

    # Base case: stop if the maximum depth is reached
    if depth >= max_depth:
        return depth_dict

    # Avoid adding an empty list at the current depth if there are no nodes
    if nodes:
        # Add the current list of nodes to the depth dictionary
        depth_dict.setdefault(depth, []).extend(nodes)

    # Prepare the list of next nodes to visit
    next_nodes = []
    for node in nodes:
        # Extend the list with neighbors of each node
        next_nodes.extend(node.get_neighbors())

    # Recursive call with incremented depth and updated next_nodes
    return _traverse_nodes(next_nodes, max_depth, depth + 1, depth_dict)

def density_search(interest_nodes, n_coincidences, *fielding):

    interest_nodes = NodeSet(interest_nodes)

    interest_nodes_neighbors = {}
    for node in interest_nodes:
        interest_nodes_neighbors[node] = node.get_neighbors(*fielding)
    candidates = NodeSet([item for sublist in interest_nodes_neighbors.values() for item in sublist])

    complying_candidates = []
    for candidate in candidates:
        ratio = sum([1 for neighbor in candidate.get_neighbors(*fielding) if neighbor in interest_nodes])
        if ratio >= n_coincidences:
            complying_candidates.append(candidate)

    return NodeSet(complying_candidates)

def find_shortest_path(start_node, end_node, *fielding):
    long_format_fields = sk.parse_field(*fielding, long=True)

    if start_node == end_node:
        return Path(nodes=(start_node,), edges=())

    visited = set()  # To keep track of visited nodes
    queue = deque([(start_node, [], [])])  # Queue for BFS, storing tuples of (node, path, path_edges)

    while queue:
        current_node, path, path_edges = queue.popleft()
        if current_node in visited:
            continue
        visited.add(current_node)
        # Check if we have reached the end node
        if current_node == end_node:
            return Path(nodes=tuple(path + [end_node]), edges=tuple(path_edges))

        # Enqueue all adjacent nodes through allowed edges
        for edge_type in long_format_fields:
            neighbors = current_node.get_neighbors(edge_type)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, path + [current_node], path_edges + [edge_type]))

    return Path([], [])  # No path found