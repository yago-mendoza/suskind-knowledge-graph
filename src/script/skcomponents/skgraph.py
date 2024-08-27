from src.script.skcomponents.sknode import Node
from src.script.skcomponents.sknodeset import NodeSet
import src.script.sktools as sk
import os
import difflib

class Graph(NodeSet):
    EDGE_TYPES = ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']
    OPPOSED_FIELDS = {
        'synset0': 'synset2', 'synset1': 'synset1', 'synset2': 'synset0',
        'semset0': 'semset2', 'semset1': 'semset1', 'semset2': 'semset0',
    }

    def __init__(self, filename, encoding='utf8'):
        self.filename = filename
        self.encoding = encoding
        self._build_nodes(filename)

    def _build_nodes(self, filename):
        if not filename.endswith('.txt'):
            raise ValueError("Filename must end with '.txt'")
        nodes = self._load_data(filename)
        super().__init__(nodes)
        self._set_parent_at_nodes()

    def _load_data(self, filename):
        try:
            with open(filename, 'r', encoding=self.encoding) as file:
                nodes = [self._parse_line_to_node(line.strip(), i) for i, line in enumerate(file)]
            return self._update_node_relationships(nodes)
        except FileNotFoundError:
            print(f"The file {filename} has not been found.")
        except IOError:
            print(f"An error occurred while reading the file {filename}.")

    def _parse_line_to_node(self, line, line_number):
        parts = line.split('|')
        try:
            identifier_part, name_lemma_part = parts[0].split(':', 1)
            lang, type_ = identifier_part.split('-')
            name, lemma = name_lemma_part.rsplit('(', 1)
            lemma = lemma[:-1]  # Remove the trailing ')'
            favorite = parts[1] == 'T'
            synsets = [[item for item in part.split('/') if item] for part in parts[2:5]]
            semsets = [[item for item in part.split('/') if item] for part in parts[5:8]]
            examples = [item for item in parts[8].split('/') if item]
            return Node(lang=lang, type=type_, name=name, lemma=lemma,
                        favorite=favorite,
                        synset0=synsets[0], synset1=synsets[1], synset2=synsets[2],
                        semset0=semsets[0], semset1=semsets[1], semset2=semsets[2],
                        examples=examples)
        except Exception as e:
            print(f"\nError parsing line {line_number + 1}:\n{line}\n{e}")
            print("Recommended action: Manually copy and re-paste the whole line in data.txt.")
            return None

    def _update_node_relationships(self, nodes):
        node_dict = {node._convert_header_to_str_format(): node for node in nodes if node}
        for node in nodes:
            if node:
                for attr in ['synset0', 'synset1', 'synset2']:
                    setattr(node, attr, [node_dict.get(related_node_str) for related_node_str in getattr(node, attr) if node_dict.get(related_node_str)])
        return [node for node in nodes if node]

    def _set_parent_at_nodes(self):
        for node in self:
            node.graph = self

    def save(self, custom_filename, directory_path=None, integrity_check=True):
        if integrity_check:
            self._perform_integrity_checks()
        
        file_path = os.path.join(directory_path, custom_filename) if directory_path else custom_filename
        string_ids = {node: node._convert_header_to_str_format() for node in self}

        with open(file_path, 'w', encoding='utf8') as file:
            for node in self:
                try:
                    line = f"{node.lang}-{node.type}:{node.name}({node.lemma})|{'T' if node.favorite else 'F'}"
                    for attr in self.EDGE_TYPES:
                        if attr.startswith('syn'):  # Syntactic edges
                            edge_content = [string_ids[n] for n in getattr(node, attr, [])]
                        else:  # Semantic edges
                            edge_content = getattr(node, attr, [])
                        while ' ' in edge_content:
                            edge_content.remove(' ')
                        line += '|' + '/'.join(edge_content)
                    line += '|' + '/'.join(node.examples)
                    file.write(line + '\n')
                except Exception as e:
                    print(f"Error saving node {node}: {e}")

    def _perform_integrity_checks(self):
        self._check_spurious_edges()
        self._check_self_connections()
        self._check_edge_mutuality()
        self._check_redundant_containment()

    def _check_spurious_edges(self):
        print('| : Spurious edges check ...')
        existing_nodes = set(self)
        for node in self:
            for attr in ['synset0', 'synset1', 'synset2']:
                new_attrs = [neighbor for neighbor in getattr(node, attr) if neighbor in existing_nodes]
                if len(new_attrs) != len(getattr(node, attr)):
                    print(f"Removed spurious edges from {node.name} in {attr}")
                setattr(node, attr, new_attrs)
        print('OK')

    def _check_self_connections(self):
        print('| : Self-connections check ...')
        for node in self:
            for attr in ['synset0', 'synset1', 'synset2']:
                new_attrs = [neighbor for neighbor in getattr(node, attr) if neighbor != node]
                if len(new_attrs) != len(getattr(node, attr)):
                    print(f"Removed self-connection from {node.name} in {attr}")
                setattr(node, attr, new_attrs)
        print('OK')

    def _check_edge_mutuality(self):
        print('| : Edge mutuality check...')
        for node in self:
            for field, opposed in self.OPPOSED_FIELDS.items():
                if field in ['synset0', 'synset1', 'synset2']:
                    for neighbor in getattr(node, field, []):
                        if node not in getattr(neighbor, opposed, []):
                            print(f"Fixed dis-mutuality on {node.name} -> {neighbor.name} in {field}")
                            self.bind(node, neighbor, field)
                            self.bind(neighbor, node, opposed)
        print('OK')

    def _check_redundant_containment(self):
        print('| : Redundant containment check...')
        for node in self:
            for attr in self.EDGE_TYPES:
                attrs = getattr(node, attr, [])
                set_attrs = list(set(attrs))
                if len(attrs) != len(set_attrs):
                    print(f"Removed redundancy in {node.name} for {attr}")
                    setattr(node, attr, set_attrs)
        print('OK')

    def create_node(self, lang, type, name, lemma):
        node = self.find(lang=lang, type=type, name=name, lemma=lemma)
        if not node:
            node = Node(lang, type, name, lemma)
            self.append(node)
        return node

    def delete_node(self, target_node):
        self.remove(target_node)
        for node in self:
            for attr in self.EDGE_TYPES:
                if target_node in getattr(node, attr):
                    getattr(node, attr).remove(target_node)

    def merge_nodes(self, node_a, node_b):
        for edge_type in self.EDGE_TYPES:
            for neighbor in node_b.get_neighbors(edge_type):
                self.unbind(node_b, neighbor, edge_type)
                self.bind(node_a, neighbor, edge_type)
        self.delete_node(node_b)

    def _convert_edge_type(self, edge_type):
        """Convierte entre formatos de borde externos (e1, y1) e internos (semset1, synset1)."""
        if edge_type.startswith(('e', 'y')):
            return sk.parse_field(edge_type, long=True)[0]
        return edge_type  # Si ya está en formato interno, lo devuelve sin cambios

    def _is_syntactic_edge(self, edge_type):
        """Determina si un tipo de borde es sintáctico."""
        return self._convert_edge_type(edge_type).startswith('synset')

    def bind(self, target_node, append_value, target_edge_type):
        internal_edge_type = self._convert_edge_type(target_edge_type)
        
        if self._is_syntactic_edge(internal_edge_type):
            # Para campos sintácticos (y0, y1, y2)
            if isinstance(append_value, Node) and target_node != append_value and append_value not in getattr(target_node, internal_edge_type, []):
                self._update_reciprocal_edges(target_node, append_value, internal_edge_type, 'add')
        else:
            # Para campos semánticos (e0, e1, e2)
            current_values = getattr(target_node, internal_edge_type, [])
            if append_value not in current_values:
                setattr(target_node, internal_edge_type, current_values + [append_value])

    def unbind(self, target_node, remove_value, target_edge_type):
        internal_edge_type = self._convert_edge_type(target_edge_type)
        
        if self._is_syntactic_edge(internal_edge_type):
            # Para campos sintácticos (y0, y1, y2)
            if isinstance(remove_value, Node):
                self._update_reciprocal_edges(target_node, remove_value, internal_edge_type, 'remove')
        else:
            # Para campos semánticos (e0, e1, e2)
            current_values = getattr(target_node, internal_edge_type, [])
            if remove_value in current_values:
                setattr(target_node, internal_edge_type, [v for v in current_values if v != remove_value])

    def _update_reciprocal_edges(self, node_a, node_b, edge_type_a, operation):
        edge_type_b = self.OPPOSED_FIELDS[edge_type_a]
        
        edges_from_a = getattr(node_a, edge_type_a, [])
        edges_from_b = getattr(node_b, edge_type_b, [])
        
        if operation == 'add':
            if node_b not in edges_from_a:
                edges_from_a.append(node_b)
            if node_a not in edges_from_b:
                edges_from_b.append(node_a)
        elif operation == 'remove':
            if node_b in edges_from_a:
                edges_from_a.remove(node_b)
            if node_a in edges_from_b:
                edges_from_b.remove(node_a)
        
        setattr(node_a, edge_type_a, edges_from_a)
        setattr(node_b, edge_type_b, edges_from_b)

    def find(self, **kwargs):
        for node in self:
            if all(getattr(node, key) == value for key, value in kwargs.items()):
                return node
        return None

    def select(self, **kwargs):
        def match_criteria(node, criteria):
            for key, value in criteria.items():
                if value is not None and getattr(node, key, None) != value:
                    return False
            return True

        return [node for node in self if match_criteria(node, kwargs)]

    def random(self, **kwargs):
        import random
        candidates = self.select(**kwargs)
        return random.choice(candidates) if candidates else None

    def __repr__(self):
        return f'Graph(size={len(self)})'
    
# LA VERSION DE ARRIBA HA SIDO GENERADA POR CLAUDE

# from src.skcomponents.sknode import Node
# from src.skcomponents.sknodeset import NodeSet

# import src.sktools as sk

# import difflib
# import os
# import re

# class Graph(NodeSet):

#     def __init__(self, filename, encoding='utf8'):
#         self.filename = filename
#         self.encoding = encoding
#         self._build_nodes(filename)
        
#     def _build_nodes(self, filename):
#         if isinstance(filename, str) and filename.endswith('.txt'):
#             nodes = self._load_data(filename) # works just fine
#             super().__init__(nodes)
#             self._set_parent_at_nodes()
#         else:
#             raise ValueError("Filename must end with '.txt'")
    
#     def _load_data(self, filename):

#         def _parse_line_to_node(line, i):

#             parts = line.strip().split('|')

#             try:
#                 # Extract the identifier, name, and lemma
#                 identifier_part = parts[0].split(':')[0]  

#                 # Extract the identifier, name, and lemma
#                 identifier_part = parts[0].split(':')[0]
#                 lang, type_ = identifier_part.split('-')         
            
#                 # Extract name and lemma by removing the identifier and splitting by '('
#                 name_lemma_part = parts[0][len(identifier_part) + 1:].rsplit(':', 1)[-1] # Handles cases where name contains ':'
#                 name, lemma = name_lemma_part.split('(')
#                 lemma = lemma[:-1]  # Remove the trailing ')'

#                 # Determine if it's marked as favorite
#                 favorite = parts[1] == 'T'

#                 # Process synsets and semsets
#                 synsets = [parts[2].split('/'), parts[3].split('/'), parts[4].split('/')]
#                 semsets = [parts[5].split('/'), parts[6].split('/'), parts[7].split('/')]

#                 # Extract examples
#                 examples = parts[8].split('/')

#                 # Return the Node object with all the extracted information
#                 return Node(lang=lang, type=type_, name=name, lemma=lemma,
#                             favorite=favorite,
#                             synset0=synsets[0], synset1=synsets[1], synset2=synsets[2],
#                             semset0=semsets[0], semset1=semsets[1], semset2=semsets[2],
#                             examples=examples)
#             except:
#                 print(f"\nThere has been an error parsing line {i+1}:\n")
#                 print(f"{line}")
#                 print(f"\nThe segmented parts are the following:\n")
#                 print(f"{parts}")
#                 print('\nRecommended actions:\n')
#                 print('- Manually copy and re-paste the whole line at data.txt.')

                
        
#         def _update_node_relationships(nodes):
#             """Update each string edge referential attributes to reference other nodes in the graph instead."""
#             node_dict = {node._convert_header_to_str_format(): node for node in nodes}
#             for node in nodes:
#                 for attr in ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']:
#                     current_relations = getattr(node, attr)
#                     updated_relations = []
#                     for related_node_str in current_relations:
#                         related_node = node_dict.get(related_node_str)
#                         if related_node:
#                             updated_relations.append(related_node)
#                     setattr(node, attr, updated_relations)
#             return nodes

#         nodes_loaded_from_txt = []
#         try:
#             with open(filename, 'r', encoding=self.encoding) as file:
#                 for i, line in enumerate(file):
#                     node = _parse_line_to_node(line.strip(), i)
#                     nodes_loaded_from_txt.append(node)
#             updated_nodes_from_txt = _update_node_relationships(nodes_loaded_from_txt)
#             return updated_nodes_from_txt
#         except FileNotFoundError:
#             print(f"The file {filename} has not been found.")
#         except IOError:
#             print(f"An error occurred while reading the file {filename}.")
    
#     def _set_parent_at_nodes(self):
#         for node in self:
#             node.graph = self

#     def save(self, custom_filename, directory_path=None, integrity_check=True):

#         if integrity_check:
            
#             found_error = False
#             print('| : Spurious edges check ...')
#             existing_nodes = set(self)
#             for node in self:
#                 for attr in ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']:
#                     new_attrs = []
#                     for neighbor in getattr(node, attr, []):
#                         if neighbor not in existing_nodes:
#                             found_error = True
#                             print(f"Removed {neighbor.name} from {node.name}")
#                         else:
#                             new_attrs.append(neighbor)
#                     setattr(node, attr, new_attrs)
#             if not found_error:
#                 print('OK')

#             found_error = False
#             print('| : Self-connections check ...')
#             existing_nodes = set(self)
#             for node in self:
#                 for attr in ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']:
#                     content = getattr(node, attr, [])
#                     new_neighbors = []
#                     for neighbor in content:
#                         if neighbor == node:
#                             found_error = True
#                             print(f"Removed a self-connection at {neighbor.name} from '{attr}'.")
#                         else:
#                             new_neighbors.append(neighbor)
#                     setattr(node, attr, new_neighbors)
#             if not found_error:
#                 print('OK')

#             found_error = False
#             print('| : Edge mutuality check...')
#             opposed_field = {
#                 'synset0': 'synset2', 'synset1': 'synset1', 'synset2': 'synset0',
#                 'semset0': 'semset2', 'semset1': 'semset1', 'semset2': 'semset0',
#             }
#             non_mutual = []
#             for node in self:
#                 for field, opposed in opposed_field.items():
#                     for neighbor in getattr(node, field, []):
#                         if node not in getattr(neighbor, opposed, []):
#                             non_mutual.append((node, neighbor,))
#                             self.bind(node, neighbor, field)
#                             self.bind(neighbor, node, opposed) # redundant yet unharmful
#                             found_error=True
#                             print(f"Fixed dis-mutuality on {node.name} -> {neighbor.name}.")
#                         else:
#                             pass
#             if not found_error:
#                 print('OK')

#             found_error = False
#             print('| : Redundant containment check...')
#             for node in self:
#                 for attr in ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']:
#                     attrs = getattr(node, attr, [])
#                     set_attrs = list(set(attrs))
#                     if len(attrs) != len(set_attrs):
#                         found_error=True
#                         setattr(node, attr, set_attrs)
#                         print(f"Had to set attrs at {node.name} due to redundancy.")
#             if not found_error:
#                 print('OK')
        
#         # Save itself

#         filename = os.path.basename(custom_filename)
#         file_path = os.path.join(directory_path, filename) if directory_path else filename

#         string_ids = {}
#         for node in self:
#             string_ids[node] = node._convert_header_to_str_format()

#         with open(file_path, 'w', encoding='utf8') as file:
#             for node in self:
#                 try:
#                     line = f"{node.lang}-{node.type}:{node.name}({node.lemma})|{'F' if not node.favorite else 'T'}"
#                     for attr in ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']:
#                         line += '|' + '/'.join([string_ids[node] for node in getattr(node, attr)])
#                     line += '|' + '/'.join(node.examples)
#                     file.write(line + '\n')  
#                 except:
#                     print(node)

#     # ---------------------
#     # Editing Methods
#     # ---------------------

#     def create_node(self, lang, type, name, lemma):
#         # Check if a node with the given attributes already exists
#         node = self.find(lang=lang, type=type, name=name, lemma=lemma)
#         if not node:
#             # If not, create a new Node instance with the provided attributes
#             node = Node(lang, type, name, lemma)
#             # Append the new node to the graph
#             self.append(node) # sets node.graph=graph
#         return node

#     def delete_node(self, target_node):
#         # Remove the target node from the graph
#         self.remove(target_node)
#         # Iterate over all nodes in the graph
#         for node in self:
#             # For each node, remove any references to the deleted node in their relational attributes
#             for attr in ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']:
#                 if target_node in getattr(node, attr):
#                     getattr(node, attr).remove(target_node)

#     def merge_nodes(self, node_a, node_b):

#         # Step 1: Unbinding node_a from all connections (not necessary in all implementations, but shown for clarity)
#         # This step might be skipped depending on the graph implementation, as deleting a node might automatically handle this.
#         for edge_type in ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']:
#             for neighbor in node_b.get_neighbors(edge_type):
#                 self.unbind(node_b, neighbor, edge_type)
#                 self.bind(node_a, neighbor, edge_type)
#         # Step 3: Deleting node_a
#         self.delete_node(node_b)

#     def bind(self, target_node, append_node, target_edge_type):
#         if target_node != append_node and target_node not in getattr(append_node, target_edge_type, []):
#             self._update_reciprocal_edges(target_node, append_node, target_edge_type, 'add')

#     def unbind(self, target_node, remove_node, target_edge_type):
#         self._update_reciprocal_edges(target_node, remove_node, target_edge_type, 'remove')

#     def _update_reciprocal_edges(self, node_a, node_b, edge_type_a, operation):

#         edge_type_a = sk.parse_field(edge_type_a, long=True)[0] # make sure

#         opposed_field = {'synset0':'synset2', 'synset1':'synset1', 'synset2':'synset0',
#                          'semset0':'semset2', 'semset1':'semset1', 'semset2':'semset0'}
        
#         edge_type_b = opposed_field[edge_type_a]
        
#         # Recover or initialises the relationship lists
#         edges_from_a = getattr(node_a, edge_type_a, [])
#         edges_from_b = getattr(node_b, edge_type_b, [])
        
#         # Adds or removes nodes to the lists, basing on the given operation
#         if operation == 'add':
#             edges_from_a.append(node_b)
#             edges_from_b.append(node_a)
#         elif operation == 'remove' and node_b in edges_from_a:
#             edges_from_a.remove(node_b)
#             edges_from_b.remove(node_a)
        
#         # Actualiza las relaciones en los nodos.
#         setattr(node_a, edge_type_a, edges_from_a)
#         setattr(node_b, edge_type_b, edges_from_b)

#     def __repr__(self):
#         return f'Graph(size={len(self)})'