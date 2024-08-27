class Path:
    def __init__(self, nodes, edges):
        self.nodes = nodes  # Tuple of nodes
        self.edges = edges  # Tuple of edges

    def __repr__(self):
        # Representation showing the length of the path (number of edges)
        return f"<Path(length={len(self.edges)})>"