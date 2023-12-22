from skcomponents import Graph
from skcomponents import Node
from collections import deque

from collections import deque

def find_shortest_path(graph, start, end):
    
    queue = deque([(start, [])])
    visited = set()
    
    while queue:
        current_node, path = queue.popleft()
        print(current_node, current_node.graph)
        if current_node == end:
            return path + [(current_node, None)]
        
        visited.add(current_node)
        neighbors = current_node.get_neighbors()
        if neighbors is None:
            continue  # or handle as needed
        
        for edge, neighbor_nodeset in neighbors.items():
            for neighbor in neighbor_nodeset:
                if neighbor in visited:
                    continue
                queue.append((neighbor, path + [(current_node, edge)]))
                visited.add(neighbor)
    
    return None


G = Graph('data.txt')
print(find_shortest_path(G, G.random(), G.random()))
