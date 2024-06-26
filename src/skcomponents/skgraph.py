from src.skcomponents.sknode import Node
from src.skcomponents.sknodeset import NodeSet

import src.sktools as sk

import difflib
import os
import re

class Graph(NodeSet):

    def __init__(self, filename):
        self.filename = filename
        self._build_nodes(filename)
        
    def _build_nodes(self, filename):
        if isinstance(filename, str) and filename.endswith('.txt'):
            nodes = self._load_data(filename) # works just fine
            super().__init__(nodes)
            self._set_parent_at_nodes()
        else:
            raise ValueError("Filename must end with '.txt'")
    
    def _load_data(self, filename):

        def _parse_line_to_node(line, i):

            parts = line.strip().split('|')

            try:
                # Extract the identifier, name, and lemma
                identifier_part = parts[0].split(':')[0]  

                # Extract the identifier, name, and lemma
                identifier_part = parts[0].split(':')[0]
                lang, type_ = identifier_part.split('-')         
            
                # Extract name and lemma by removing the identifier and splitting by '('
                name_lemma_part = parts[0][len(identifier_part) + 1:].rsplit(':', 1)[-1] # Handles cases where name contains ':'
                name, lemma = name_lemma_part.split('(')
                lemma = lemma[:-1]  # Remove the trailing ')'

                # Determine if it's marked as favorite
                favorite = parts[1] == 'T'

                # Process synsets and semsets
                synsets = [parts[2].split('/'), parts[3].split('/'), parts[4].split('/')]
                semsets = [parts[5].split('/'), parts[6].split('/'), parts[7].split('/')]

                # Extract examples
                examples = parts[8].split('/')

                # Return the Node object with all the extracted information
                return Node(lang=lang, type=type_, name=name, lemma=lemma,
                            favorite=favorite,
                            synset0=synsets[0], synset1=synsets[1], synset2=synsets[2],
                            semset0=semsets[0], semset1=semsets[1], semset2=semsets[2],
                            examples=examples)
            except:
                print(f"\nThere has been an error parsing line {i+1}:\n")
                print(f"{line}")
                print(f"\nThe segmented parts are the following:\n")
                print(f"{parts}")
                print('\nRecommended actions:\n')
                print('- Manually copy and re-paste the whole line at data.txt.')

                
        
        def _update_node_relationships(nodes):
            """Update each string edge referential attributes to reference other nodes in the graph instead."""
            node_dict = {node._convert_header_to_str_format(): node for node in nodes}
            for node in nodes:
                for attr in ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']:
                    current_relations = getattr(node, attr)
                    updated_relations = []
                    for related_node_str in current_relations:
                        related_node = node_dict.get(related_node_str)
                        if related_node:
                            updated_relations.append(related_node)
                    setattr(node, attr, updated_relations)
            return nodes

        nodes_loaded_from_txt = []
        try:
            with open(filename, 'r', encoding='latin1') as file:
                for i, line in enumerate(file):
                    node = _parse_line_to_node(line.strip(), i)
                    nodes_loaded_from_txt.append(node)
            updated_nodes_from_txt = _update_node_relationships(nodes_loaded_from_txt)
            return updated_nodes_from_txt
        except FileNotFoundError:
            print(f"The file {filename} has not been found.")
        except IOError:
            print(f"An error occurred while reading the file {filename}.")
    
    def _set_parent_at_nodes(self):
        for node in self:
            node.graph = self

    def save(self, custom_filename, directory_path=None, integrity_check=True):


        if integrity_check:
            
            found_error = False
            print('| : Spurious edges check ...')
            existing_nodes = set(self)
            for node in self:
                for attr in ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']:
                    new_attrs = []
                    for neighbor in getattr(node, attr, []):
                        if neighbor not in existing_nodes:
                            found_error = True
                            print(f"Removed {neighbor.name} from {node.name}")
                        else:
                            new_attrs.append(neighbor)
                    setattr(node, attr, new_attrs)
            if not found_error:
                print('OK')

            found_error = False
            print('| : Self-connections check ...')
            existing_nodes = set(self)
            for node in self:
                for attr in ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']:
                    content = getattr(node, attr, [])
                    new_neighbors = []
                    for neighbor in content:
                        if neighbor == node:
                            found_error = True
                            print(f"Removed a self-connection at {neighbor.name} from '{attr}'.")
                        else:
                            new_neighbors.append(neighbor)
                    setattr(node, attr, new_neighbors)
            if not found_error:
                print('OK')

            found_error = False
            print('| : Edge mutuality check...')
            opposed_field = {
                'synset0': 'synset2', 'synset1': 'synset1', 'synset2': 'synset0',
                'semset0': 'semset2', 'semset1': 'semset1', 'semset2': 'semset0',
            }
            non_mutual = []
            for node in self:
                for field, opposed in opposed_field.items():
                    for neighbor in getattr(node, field, []):
                        if node not in getattr(neighbor, opposed, []):
                            non_mutual.append((node, neighbor,))
                            self.bind(node, neighbor, field)
                            self.bind(neighbor, node, opposed) # redundant yet unharmful
                            found_error=True
                            print(f"Fixed dis-mutuality on {node.name} -> {neighbor.name}.")
                        else:
                            pass
            if not found_error:
                print('OK')

            found_error = False
            print('| : Redundant containment check...')
            for node in self:
                for attr in ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']:
                    attrs = getattr(node, attr, [])
                    set_attrs = list(set(attrs))
                    if len(attrs) != len(set_attrs):
                        found_error=True
                        setattr(node, attr, set_attrs)
                        print(f"Had to set attrs at {node.name} due to redundancy.")
            if not found_error:
                print('OK')
        
        # Save itself

        filename = os.path.basename(custom_filename)
        file_path = os.path.join(directory_path, filename) if directory_path else filename

        string_ids = {}
        for node in self:
            string_ids[node] = node._convert_header_to_str_format()

        with open(file_path, 'w') as file:
            for node in self:
                try:
                    line = f"{node.lang}-{node.type}:{node.name}({node.lemma})|{'F' if not node.favorite else 'T'}"
                    for attr in ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']:
                        line += '|' + '/'.join([string_ids[node] for node in getattr(node, attr)])
                    line += '|' + '/'.join(node.examples)
                    file.write(line + '\n')  
                except:
                    print(node)

    # ---------------------
    # Editing Methods
    # ---------------------

    def create_node(self, lang, type, name, lemma):
        # Check if a node with the given attributes already exists
        node = self.find(lang=lang, type=type, name=name, lemma=lemma)
        if not node:
            # If not, create a new Node instance with the provided attributes
            node = Node(lang, type, name, lemma)
            # Append the new node to the graph
            self.append(node) # sets node.graph=graph
        return node

    def delete_node(self, target_node):
        # Remove the target node from the graph
        self.remove(target_node)
        # Iterate over all nodes in the graph
        for node in self:
            # For each node, remove any references to the deleted node in their relational attributes
            for attr in ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']:
                if target_node in getattr(node, attr):
                    getattr(node, attr).remove(target_node)

    def merge_nodes(self, node_a, node_b):

        # Step 1: Unbinding node_a from all connections (not necessary in all implementations, but shown for clarity)
        # This step might be skipped depending on the graph implementation, as deleting a node might automatically handle this.
        for edge_type in ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']:
            for neighbor in node_b.get_neighbors(edge_type):
                self.unbind(node_b, neighbor, edge_type)
                self.bind(node_a, neighbor, edge_type)
        # Step 3: Deleting node_a
        self.delete_node(node_b)

    def bind(self, target_node, append_node, target_edge_type):
        if target_node != append_node and target_node not in getattr(append_node, target_edge_type, []):
            self._update_reciprocal_edges(target_node, append_node, target_edge_type, 'add')

    def unbind(self, target_node, remove_node, target_edge_type):
        self._update_reciprocal_edges(target_node, remove_node, target_edge_type, 'remove')

    def _update_reciprocal_edges(self, node_a, node_b, edge_type_a, operation):

        edge_type_a = sk.parse_field(edge_type_a, long=True)[0] # make sure

        opposed_field = {'synset0':'synset2', 'synset1':'synset1', 'synset2':'synset0',
                         'semset0':'semset2', 'semset1':'semset1', 'semset2':'semset0'}
        
        edge_type_b = opposed_field[edge_type_a]
        
        # Recover or initialises the relationship lists
        edges_from_a = getattr(node_a, edge_type_a, [])
        edges_from_b = getattr(node_b, edge_type_b, [])
        
        # Adds or removes nodes to the lists, basing on the given operation
        if operation == 'add':
            edges_from_a.append(node_b)
            edges_from_b.append(node_a)
        elif operation == 'remove' and node_b in edges_from_a:
            edges_from_a.remove(node_b)
            edges_from_b.remove(node_a)
        
        # Actualiza las relaciones en los nodos.
        setattr(node_a, edge_type_a, edges_from_a)
        setattr(node_b, edge_type_b, edges_from_b)

    def __repr__(self):
        return f'Graph(size={len(self)})'
    
    #################################################
    
    # About forking [deprecated hence not documented]

    #################################################
            
    # def fork(self):
    #     subset = [node._copy() for node in self]
    #     return Graph(subset)

    # def _clean_spurious_edges(self):
    #     """Cleans connections to nodes not present in the structure."""
    #     node_identifiers = {node._convert_header_to_str_format() for node in self}
    #     attrs_to_check = ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']
    #     for node in self:
    #         for attr in attrs_to_check:
    #             valid_nodes = [n for n in getattr(node, attr, []) if n._convert_header_to_str_format() in node_identifiers]
    #             setattr(node, attr, valid_nodes)
    
    # def merge(self, other_graph, politics='trim'):
    #     if not isinstance(other_graph, Graph):
    #         raise TypeError("The 'other_graph' must be an instance of Graph.")

    #     for node in other_graph:
    #         if politics == 'blossom':
    #             self._merge_and_blossom_connections(node)
    #         elif politics == 'trim':
    #             self._merge_and_trim_connections(node)

    # def _merge_and_blossom_connections(self, node):
    #     if not self.find(*node.identify()):
    #         new_node = node._copy()
    #         self._add_node(new_node)
    #     for attr in self._relationship_attributes():
    #         for connected_node in getattr(node, attr):
    #             if not self.find(*connected_node.identify()):
    #                 missing_node = connected_node._copy()
    #                 self._add_node(missing_node)

    # def _merge_and_trim_connections(self, node):
    #     new_node = node._copy()
    #     for attr in self._relationship_attributes():
    #         connections = getattr(new_node, attr)
    #         trimmed_connections = [c for c in connections if self.find(*c.identify())]
    #         setattr(new_node, attr, trimmed_connections)
    #     self._add_node(new_node)
    
    # def _add_node(self, node):
    #     if not isinstance(node, Node):
    #         raise TypeError("Only Node instances can be added to the graph.")
    #     if not self.find(node.lang, node.type, node.name, node.lemma):
    #         super().append(node)

    # @staticmethod
    # def _relationship_attributes():
    #     return ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']

    # def _scan_spurious_edges(self, rebind=False, remove=False):

    #     c0 = sum([1 for node in self for _ in node.get_neighbors()])

    #     for node in self:

    #         for neighbor in node.get_neighbors('y1'):
    #             if node not in neighbor.get_neighbors('y1'):
    #                 if remove:
    #                     node.synset1.remove(neighbor)
    #                 elif rebind:
    #                     self.bind(neighbor,'synset1',node)

    #         for neighbor in node.get_neighbors('e1'):
    #             if node not in neighbor.get_neighbors('e1'):
    #                 if remove:
    #                     node.semset1.remove(neighbor)
    #                 elif rebind:
    #                     self.bind(neighbor,'semset1',node)     

    #     c1 = sum([1 for node in self for _ in node.get_neighbors()])