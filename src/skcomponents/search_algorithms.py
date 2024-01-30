from src.skcomponents.sknodeset import NodeSet
from src.skcomponents.sknode import Node
from src.skcomponents.skpath import Path

from collections import deque
from itertools import combinations

import src.sktools as sk

def centrality(nodes, *fielding,
               depth=2, soiling_weight=0.1,
               rel_decay=0.50):

    # Initialize dictionary to store frequency of each neighbor
    neighbor_frequency = {}
    
    # Retrieve neighbors for each node for performance optimization
    node_neighbors = {node: node.get_neighbors(*fielding) for node in nodes}

    # Compute frequency of first-level neighbors
    for neighbors in node_neighbors.values():
        for neighbor in neighbors:
            neighbor_frequency[neighbor] = neighbor_frequency.get(neighbor, 0) + 1
    
    neighbor_frequency = {key: value**2 for key, value in neighbor_frequency.items()}

    # Filter neighbors shared by more than one node (akka intersections)
    shared_neighbors_frequencies = {key: value for key, value in neighbor_frequency.items() if value > 1}

    standard_scoring = {node: sum(shared_neighbors_frequencies.get(neighbor, 0) for neighbor in neighbors) for node, neighbors in node_neighbors.items()}
    
    # Initialize dictionary for additional scores based on depth
    soil_scoring = {node: 0 for node in nodes}

    if depth > 1:
        # Traverse nodes to a specified depth, excluding the first two levels
        neighbors_by_depth = _traverse_nodes(nodes, max_depth=depth)
        del neighbors_by_depth[0], neighbors_by_depth[1]

        standard_weight = 1
        # Update neighbor frequencies for deeper levels
        for neighbors in neighbors_by_depth.values():
            standard_weight *= rel_decay
            for node in nodes:
                soil_scoring[node] += standard_weight * neighbors.count(node)

    
    max_score = max(standard_scoring.values())
    max_soil_score = max(soil_scoring.values())

    rf = max_score/max_soil_score if max_soil_score != 0 else 1
    rescaled_soil_scoring = {node: score*rf for node, score in soil_scoring.items()}

    # Calculate and normalize centrality scores
    centralities = {}
    for node, neighbors in node_neighbors.items():
        # Calculate score based on shared neighbors and depth score
        score = standard_scoring[node] + soiling_weight * rescaled_soil_scoring[node]

        # Normalize score by the number of neighbors
        centralities[node] = score / len(neighbors) if neighbors else 0

    # Scale the values so that the maximum is 1.0
    max_centrality = max(centralities.values(), default=1)  # Use default=1 to handle empty centralities
    if max_centrality != 0:
        for node in centralities:
            centralities[node] /= max_centrality

    return centralities

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