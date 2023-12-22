import os
from sknode import Node
from sknodeset import NodeSet

class Graph(NodeSet):

    def __init__(self, parent=None):
        self.parent = parent
        self._build_nodes(parent)
        self._clean_edges()

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
            super().__init__(nodes, alias=True)
            for node in self:
                node.graph = self
        else:
            raise ValueError("Filename must end with '.txt'")
    
    def _handle_data_structure_source(self, parent):
        super().__init__(parent)
    
    def _load_data(self, parent):

        parent = os.path.basename(parent)

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
            global temp_nodes # delete
            temp_nodes = {node.identify(format=True): node for node in nodes}
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

        global nodes_loaded_from_txt
        global updated_nodes_from_txt
        nodes_loaded_from_txt = []
        try:
            global updated_nodes_from_txt # delete
            with open(parent, 'r') as file:
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
            string_ids[node] = node.identify(format=True)
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
        if not self.find(lang, type_, name, lemma):
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
    
    def bind(self, target_node, edge_type, append_node):
        if isinstance(append_node, Node):
            self._update_relationship('append', target_node, edge_type, append_node)
        elif isinstance(append_node, (list, set, NodeSet)):
            for node in append_node:
                self._update_relationship('append', target_node, edge_type, node)

    def unbind(self, target_node, edge_type, append_node):
        if isinstance(append_node, Node):
            self._update_relationship('remove', target_node, edge_type, append_node)
        elif isinstance(append_node, (list, set, NodeSet)):
            for node in append_node:
                self._update_relationship('remove', target_node, edge_type, node)
    
    def _update_relationship(self, action, target_node, edge_type, append_node):

        def perform_action(node, edge, action_method, additional_node=None):
            if additional_node is not None:
                getattr(node, edge).__getattribute__(action_method)(additional_node)
            else:
                getattr(node, edge).__getattribute__(action_method)()

        # Handle synset and semset relationships, which require a level
        if edge_type.startswith('synset') or edge_type.startswith('semset'):
            target_edge_type = edge_type 
            append_edge_type = edge_type[:-1] + str(2 - int(edge_type[-1]))
            perform_action(target_node, target_edge_type, action, append_edge_type)
            perform_action(append_node, append_edge_type, action, target_edge_type)
    
    def __repr__(self):
        return f'Graph(size={len(self)})'
    

G = Graph('data2.txt')

n1 = G.find('es','b','n1','l1')[0]
n2 = G.find('es','b','n2','l2')[0]
nn1 = n2.synset1[0]
nn2 = n1.synset1[0]

assert n1 is nn1, 'Waa-waa; n1 is not nn1 yet'