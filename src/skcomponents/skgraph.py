from src.skcomponents.sknode import Node
from src.skcomponents.sknodeset import NodeSet

import os

class Graph(NodeSet):

    def __init__(self, parent=None):
        self.parent = parent
        self._build_nodes(parent)
        self._clean_spurious_edges()

    def _build_nodes(self, parent):
        if isinstance(parent, str):
            self._handle_file_source(parent)
        elif isinstance(parent, (list, set, NodeSet)):
            self._handle_data_structure_source(parent)
        elif isinstance(parent, (Graph)):
            raise ValueError("To fork a Graph, use the specific 'fork' method.")
        else:
            raise ValueError("Source must be a filename, a list of nodes, a set of nodes, or a NodeSet.")
    
    def _handle_file_source(self, parent):
        if parent.endswith('.txt'):
            nodes = self._load_data(parent) # works just fine
            super().__init__(nodes)
            for node in self:
                node.graph = self
        else:
            raise ValueError("Filename must end with '.txt'")
    
    def _handle_data_structure_source(self, parent):
        super().__init__(parent)
    
    def _load_data(self, parent):

        def _parse_line_to_node(line):
            parts = line.strip().split('|')
            lang, type_ = parts[0].split(':')[0].split('-')[0], parts[0].split(':')[0].split('-')[1]
            name, lemma = parts[0][:-1].split(':')[1].split('(')
            favorite = True if parts[1] == 'T' else False
            sections = [part.split('/') for part in parts[2:]]
            return Node(lang, type_, name, lemma, favorite, *sections)
        
        def _update_node_relationships(nodes):
            """
            Update each node's attributes to reference other nodes in the graph.
            Removes connections to nodes not present in the graph (remember, only when from TXT)
            """
            temp_nodes = {node._convert_header_to_str_format(): node for node in nodes}
            for node in nodes:
                for attr in ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']:
                    updated_relations = [] #poised to be the Node list
                    current_relations = getattr(node, attr) # lst of string format nodes
                    for related_node in current_relations:
                        try:
                            if temp_nodes.get(related_node):
                                target_node = temp_nodes.get(related_node)
                                updated_relations.append(target_node)
                        except Exception as e:
                            print(f'The {related_node} node at {node} has no pressence in the Graph besides this occurrence.')
                    setattr(node, attr, updated_relations)
            return nodes

        nodes_loaded_from_txt = []
        try:
            with open(parent, 'r', encoding='latin1') as file:
                for line in file:
                    node = _parse_line_to_node(line.strip())
                    nodes_loaded_from_txt.append(node)
            
            updated_nodes_from_txt = _update_node_relationships(nodes_loaded_from_txt)
            
            return updated_nodes_from_txt
        except FileNotFoundError:
            print(f"The file {parent} has not been found.")
        except IOError:
            print(f"An error occurred while reading the file {parent}.")
    
    def fork(self):
        subset = [node._copy() for node in self]
        return Graph(subset)
    
    def merge(self, other_graph, politics='trim'):
        if not isinstance(other_graph, Graph):
            raise TypeError("The 'other_graph' must be an instance of Graph.")

        for node in other_graph:
            if politics == 'blossom':
                self._merge_and_blossom_connections(node)
            elif politics == 'trim':
                self._merge_and_trim_connections(node)

    def _merge_and_blossom_connections(self, node):
        if not self.find(*node.identify()):
            new_node = node._copy()
            self._add_node(new_node)
        for attr in self._relationship_attributes():
            for connected_node in getattr(node, attr):
                if not self.find(*connected_node.identify()):
                    missing_node = connected_node._copy()
                    self._add_node(missing_node)

    def _merge_and_trim_connections(self, node):
        new_node = node._copy()
        for attr in self._relationship_attributes():
            connections = getattr(new_node, attr)
            trimmed_connections = [c for c in connections if self.find(*c.identify())]
            setattr(new_node, attr, trimmed_connections)
        self._add_node(new_node)

    def _add_node(self, node):
        if not isinstance(node, Node):
            raise TypeError("Only Node instances can be added to the graph.")
        if not self.find(node.lang, node.type, node.name, node.lemma):
            super().append(node)

    @staticmethod
    def _relationship_attributes():
        return ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']

    def save(self, custom_filename):

        custom_filename = os.path.basename(custom_filename)

        # Open the file specified in 'filename' for writing
        string_ids = {}
        for node in self:
            string_ids[node] = node._convert_header_to_str_format()
        with open(custom_filename, 'w') as file:
            # Iterate over each node in the graph
            for node in self:
                # Convert each node's attributes to a string format suitable for file storage
                line = f"{node.lang}-{node.type}:{node.name}({node.lemma})|{'F' if not node.favorite else 'T'}"
                for attr in ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']:
                    line += '|' + '/'.join([string_ids[node] for node in getattr(node, attr)])
                # Write each formatted node string to the file
                line += '|' + '/'.join(node.examples)
                file.write(line + '\n')        

    # ---------------------
    # Editing Methods
    # ---------------------

    def create_node(self, lang, type_, name, lemma):
        # Check if a node with the given attributes already exists
        if not self.find(lang=lang, type_=type_, name=name, lemma=lemma):
            # If not, create a new Node instance with the provided attributes
            node = Node(lang, type_, name, lemma)
            # Append the new node to the graph
            self.append(node) # sets node.graph=graph

    def delete_node(self, target_node):
        # Remove the target node from the graph
        self.remove(target_node)
        # Iterate over all nodes in the graph
        for node in self:
            # For each node, remove any references to the deleted node in their relational attributes
            for attr in ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']:
                if target_node in getattr(node, attr):
                    getattr(node, attr).remove(target_node)

    def _update_reciprocal_edges(self, node_a, edge_type_a, node_b, operation):
        if isinstance(node_b, Node) and edge_type_a.startswith(('synset', 'semset')):
            # Calcula el tipo de relación inversa.
            edge_type_b = f"{edge_type_a[:-1]}{2 - int(edge_type_a[-1])}"
            
            # Recupera o inicializa las listas de relaciones.
            edges_from_a = getattr(node_a, edge_type_a, [])
            edges_from_b = getattr(node_b, edge_type_b, [])
            
            # Añade o elimina nodos de las listas basado en la operación.
            if operation == 'add':
                edges_from_a.append(node_b)
                edges_from_b.append(node_a)
            elif operation == 'remove' and node_b in edges_from_a:
                edges_from_a.remove(node_b)
                edges_from_b.remove(node_a)
            
            # Actualiza las relaciones en los nodos.
            setattr(node_a, edge_type_a, edges_from_a)
            setattr(node_b, edge_type_b, edges_from_b)

def bind(self, target_node, target_edge_type, append_node):
    self._update_reciprocal_edges(target_node, target_edge_type, append_node, 'add')

def unbind(self, target_node, target_edge_type, remove_node):
    self._update_reciprocal_edges(target_node, target_edge_type, remove_node, 'remove')

    
    def __repr__(self):
        return f'Graph(size={len(self)})'