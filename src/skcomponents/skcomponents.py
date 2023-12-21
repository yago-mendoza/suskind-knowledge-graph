import os
import random

class NodeSet(list):

    def __init__(self, nodes=None, alias=False):

        self._alias = alias  # private attribute (only used in the following line)        
        nodes_as_list = self._convert_to_list(nodes)  # converts the data structure to a list
        if not all(isinstance(node, Node) for node in nodes_as_list):
            # Validate that all elements are instances of Node
            raise ValueError("All elements must be instances of Node")
        
        super().__init__(nodes_as_list)  # initialize the parent list class

    def define_permissions(self):

        synset0, synset1, synset2 = False, True, False
        semset0, semset1, semset2 = False, True, False

        self.edge_permissions = {
            'synset0': synset0,
            'synset1': synset1,
            'synset2': synset2,
            'semset0': semset0,
            'semset1': semset1,
            'semset2': semset2
            }
        
        self.group_mappings = {
            'synset': ['synset0', 'synset1', 'synset2'],
            'semset': ['semset0', 'semset1', 'semset2']
        }

    def disable(self, *edge_types):
        if not edge_types:
            for edge in self.edge_permissions:
                self.edge_permissions[edge] = False
        else:
            for edge in edge_types:
                if edge in self.group_mappings:
                    for group_edge in self.group_mappings[edge]:
                        self.edge_permissions[group_edge] = False
                elif edge in self.edge_permissions:
                    self.edge_permissions[edge] = False

    def enable(self, *edge_types):
        if not edge_types:
            for edge in self.edge_permissions:
                self.edge_permissions[edge] = True
        else:
            for edge in edge_types:
                if edge in self.group_mappings:
                    for group_edge in self.group_mappings[edge]:
                        self.edge_permissions[group_edge] = True
                elif edge in self.edge_permissions:
                    self.edge_permissions[edge] = True

    def view_nodes(self): return [node for node in self]
    def view_langs(self): return [node.lang for node in self]
    def view_types(self): return [node.type for node in self]
    def view_names(self): return [node.name for node in self]
    def view_lemmas(self): return [node.lemma for node in self]

    def set_langs(self): return list(set([n.lang for n in self]))
    def set_types(self): return list(set([n.type for n in self]))

    def _convert_to_list(self, input_nodes):
        # If the input is a NodeSet, Graph, list, or set, convert it to a list
        if isinstance(input_nodes, Node):
            input_nodes = [input_nodes]
        if isinstance(input_nodes, (NodeSet, Graph, list, set)):
            return list(set([node if self._alias else node._copy() for node in input_nodes]))
        return input_nodes or []

    def _clean_edges(self):
        # Create a set of node identifiers for faster membership checks
        node_identifiers = {node.identify(format=True) for node in self}

        # Remove connections to nodes not present in the NodeSet
        for node in self:
            for attr in ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']:
                try:
                    valid_nodes = getattr(node, attr, [])
                except AttributeError:
                    raise AttributeError(f"Node does not have attribute '{attr}'")

                # Use set intersection for efficient filtering
                setattr(node, attr, [n for n in valid_nodes if n.identify(format=True) in node_identifiers])
    
    def __getitem__(self, index):
        # Redefine magic method so that it returns NodeSets
        result = super().__getitem__(index)
        if isinstance(result, list):
            return NodeSet(result)
        return result

    def append(self, node):
        # Ensure only Node instances can be added to the Graph
        if not isinstance(node, Node):
            raise ValueError("Only Node instances can be added to the Graph.")
        # Check if the node is unique based on its identifier
        if any(existing_node == node for existing_node in self):
            raise ValueError("A node with the same identifier already exists in the Graph.")

        super().append(node)  # Use super() to avoid recursion

        # Set the graph reference in the Node instance
        node.graph = self

    def find(self, *args):

        # Unpack arguments based on their number and type
        if len(args) == 1 and isinstance(args[0], Node):
            lang, type_, name, lemma = args[0].identify()
        elif len(args) in [3, 4]:
            lang, type_, name, *lemma = args
            lemma = lemma[0] if lemma else None
        else:
            raise ValueError("Invalid number of arguments for find_node")

        results = []
        for node in self:
            if lemma is None:
                if node.lang == lang and node.type == type_ and node.name == name:
                    results.append(node)
            else:
                if node.lang == lang and node.type == type_ and node.name == name and node.lemma == lemma:
                    results.append(node)

        return NodeSet(results)

    def random(self, k=None, alias=False):
        if not k and self: return random.choice(self)
        if not self or k < 1: return None
        if k == 1: return NodeSet(nodes=random.choice(self), alias=alias)
        if k <= len(self): return NodeSet(nodes=random.sample(self, k), alias=alias)
        raise ValueError(f"k must be less than or equal to the number of nodes, got {k} for {len(self)} nodes.")
    
    def edit(self, **attr_edits):
        # Iterate through the keyword arguments provided in 'changes'
        for node in self:
            node.edit(**attr_edits)

    def filter_lang(self, *langs, complement=False):
        return self._filter_nodes(lambda node: getattr(node, 'lang') in langs, complement)
    
    def filter_types(self, *types, complement=False):
        return self._filter_nodes(lambda node: getattr(node, 'type') in types, complement)

    def filter_lemma(self, lemma=True):
        return self._filter_nodes(lambda node: bool(node.lemma) == lemma)

    def filter_favorite(self, favorite=True):
        return self._filter_nodes(lambda node: bool(node.favorite) == favorite)

    def filter_char_count(self, *args, on_lemma=False):
        return self._filter_by_length('char_count', *args, on_lemma=on_lemma)

    def filter_word_count(self, *args, on_lemma=False):
        return self._filter_by_length('word_count', *args, on_lemma=on_lemma)

    def filter_contains_word(self, *args, on_lemma=False):
        return self._filter_by_string_occurrence('contains_word', *args, on_lemma=on_lemma)

    def filter_contains(self, *args, on_lemma=False):
        return self._filter_by_string_occurrence('contains', *args, on_lemma=on_lemma)

    def filter_starts_with(self, chain, on_lemma=False):
        return self._filter_nodes(lambda node: getattr(node, 'lemma' if on_lemma else 'name', "").lower().startswith(chain.lower()))

    def filter_ends_with(self, chain, on_lemma=False):
        return self._filter_nodes(lambda node: getattr(node, 'lemma' if on_lemma else 'name', "").lower().endswith(chain.lower()))

    def _filter_by_length(self, length_type, *args, on_lemma=False):
        def condition_func(node):
            target = getattr(node, 'lemma' if on_lemma else 'name', "").lower()
            length_func = len if length_type == 'char_count' else lambda t: len(t.split())
            target_length = length_func(target)
            return self._compare_length(target_length, *args)

        return self._filter_nodes(condition_func)

    def _filter_by_string_occurrence(self, occurrence_type, *args, on_lemma=False):
        def condition_func(node):
            target = getattr(node, 'lemma' if on_lemma else 'name', "").lower()
            if occurrence_type == 'contains':
                return self._compare_string_occurrence(target, *args)
            else:  # contains_word
                words = target.split()
                return any(self._compare_string_occurrence(word, *args) for word in words)

        return self._filter_nodes(condition_func)

    def _compare_length(self, target_length, *args):
        if len(args) == 1:
            return target_length == args[0]
        elif len(args) == 2:
            operator, value = args
            return self._compare(target_length, operator, value)
        else:
            raise ValueError("Invalid arguments for length comparison.")

    def _compare_string_occurrence(self, target, *args):
        if len(args) == 1:
            return args[0] in target
        elif len(args) == 2 and isinstance(args[1], int):
            return target.count(args[0]) == args[1]
        elif len(args) == 3:
            string, operator, value = args
            return self._compare(target.count(string), operator, value)
        else:
            raise ValueError("Invalid arguments for string occurrence comparison.")

    def _compare(self, target_value, operator, value):
        operations = {
            '>=': target_value >= value,
            '<=': target_value <= value,
            '>': target_value > value,
            '<': target_value < value,
            '=': target_value == value
        }
        return operations.get(operator, False)

    def _filter_by_attribute(self, attribute, operator, value):
        filtered_nodes = []

        for node in self:
            node_value = len(getattr(node, attribute, None))

            if operator == '=' and node_value == value:
                filtered_nodes.append(node)
            elif operator == '!=' and node_value != value:
                filtered_nodes.append(node)
            elif operator == '<' and node_value < value:
                filtered_nodes.append(node)
            elif operator == '<=' and node_value <= value:
                filtered_nodes.append(node)
            elif operator == '>' and node_value > value:
                filtered_nodes.append(node)
            elif operator == '>=' and node_value >= value:
                filtered_nodes.append(node)

        return NodeSet(nodes=filtered_nodes, alias=False)

    def filter_synset0(self, operator, value):
        return self._filter_by_attribute('synset0', operator, value)

    def filter_synset1(self, operator, value):
        return self._filter_by_attribute('synset1', operator, value)

    def filter_synset2(self, operator, value):
        return self._filter_by_attribute('synset2', operator, value)

    def filter_semset0(self, operator, value):
        return self._filter_by_attribute('semset0', operator, value)

    def filter_semset1(self, operator, value):
        return self._filter_by_attribute('semset1', operator, value)

    def filter_semset2(self, operator, value):
        return self._filter_by_attribute('semset2', operator, value)
    
    def __repr__(self):
        return f'NodeSet(size={len(self)})'
    
class Node:

    # Define FLAGS as a class variable
    _FLAGS = {
        'lang':       0b000000000001,
        'type':       0b000000000010,
        'name':       0b000000000100,
        'lemma':      0b000000001000,
        'favorite':   0b000000010000,
        'synset0':    0b000000100000,
        'synset1':    0b000001000000,
        'synset2':    0b000010000000,
        'semset0':    0b000100000000,
        'semset1':    0b001000000000,
        'semset2':    0b010000000000,
        'examples':   0b100000000000
    }

    _identifier_flags = {'lang', 'type', 'name', 'lemma'}
    _descriptive_flags = {'favorite'}
    _edge_flags = set(_FLAGS.keys()) - _identifier_flags - _descriptive_flags

    # Initially enable all flags
    _repr_flags = 0b000000011111

    labels = 1

    def __init__(self, lang: str, type_: str, name: str,
                 lemma: str,
                 favorite: bool = False,
                 synset0: list = None, synset1: list = None, synset2: list = None,
                 semset0: list = None, semset1: list = None, semset2: list = None,
                 examples: list = None) -> None:
        
        self.graph = None

        self.lang, self.type, self.name = lang, type_, name
        self.lemma = lemma if lemma is not None else ''
        self.favorite = favorite == True
        self.synset0, self.synset1, self.synset2 = [synset if synset is not None else [] for synset in [synset0, synset1, synset2]]
        self.semset0, self.semset1, self.semset2 = [semset if semset is not None else [] for semset in [semset0, semset1, semset2]]
        self.examples = examples if examples is not None else []
    
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.lang == other.lang and self.type == other.type and self.name == other.name and self.lemma == other.lemma
        return False
    
    def __hash__(self):
        return hash((self.lang, self.type, self.name, self.lemma))

    def edit(self, **attr_edits):
        # Iterate through the keyword arguments provided in 'changes'
        for key, value in attr_edits.items():
            if hasattr(self, key):
                # For each attribute to be changed, update the target node's corresponding attribute
                setattr(self, key, value)
    
    def add_edge(self, node, type_):
        # Ensure the node is not already in the specified connexion type
        if node not in self.__getattribute__(type_):
            self.__getattribute__(type_).append(node)

    def remove_edge(self, node, type_):
        # Remove the node from the specified connexion type if it exists
        try:
            self.__getattribute__(type_).remove(node)
        except ValueError:

            pass

    def identify(self, format=False):
        if not format:
            return (self.lang, self.type, self.name, self.lemma)
        return f'{self.lang}-{self.type}:{self.name}({self.lemma})'
    
    def _copy(self):
        # Creating a deep copy of the node to avoid aliasing issues when new Graph instances are created
        # This ensures that changes to the copied node in one Graph instance do not affect the node in another
        return Node(
            self.lang, self.type, self.name, self.lemma, self.favorite,
            self.synset0[:], self.synset1[:], self.synset2[:],
            self.semset0[:], self.semset1[:], self.semset2[:],
            self.examples[:]
        )

    def get_neighbors(self, edge_type=None):

        # Special handling for 'synset' and 'semset'
        if edge_type == 'synset':
            all_synsets = self.synset0 + self.synset1 + self.synset2
            return NodeSet(all_synsets)
        elif edge_type == 'semset':
            all_semsets = self.semset0 + self.semset1 + self.semset2
            return NodeSet(all_semsets)

        if hasattr(self, edge_type):
            return NodeSet(getattr(self, edge_type))

        if edge_type==None:
            return {
                'synset0': NodeSet(self.synset0),
                'synset1': NodeSet(self.synset1),
                'synset2': NodeSet(self.synset2),
                'semset0': NodeSet(self.semset0),
                'semset1': NodeSet(self.semset1),
                'semset2': NodeSet(self.semset2),
            }

    def get_synset(self, set_level=None):
        if set_level is None:
            return NodeSet(self.synset0 + self.synset1 + self.synset2)
        elif set_level in [0, 1, 2]:
            return NodeSet(getattr(self, f'synset{set_level}', []))
        else:
            raise ValueError(f"Invalid synset level: {set_level}")

    def get_semset(self, set_level=None):
        if set_level is None:
            return NodeSet(self.semset0 + self.semset1 + self.semset2)
        elif set_level in [0, 1, 2]:
            return NodeSet(getattr(self, f'semset{set_level}', []))
        else:
            raise ValueError(f"Invalid semset level: {set_level}")

    @classmethod
    def toggle_labels(cls, flag=None):
        if flag in {1,2}:
            cls.labels = flag
        cls.labels ^= 1
        return cls

    @classmethod
    def compress(cls, *edge_type):
        if not edge_type:
            cls.toggle(*cls._identifier_flags, 1)
            cls.toggle(*cls._descriptive_flags, 0)
            cls.toggle(*cls._edge_flags, 0)
        else:
            cls.toggle(*edge_type, 0)
        return cls

    @classmethod
    def expand(cls, *edge_type):
        if not edge_type:
            cls.toggle(*cls._identifier_flags, 1)
            cls.toggle(*cls._descriptive_flags, 1)
            cls.toggle(*cls._edge_flags, 1)
        else:
            cls.toggle(*edge_type, 1)
        return cls

    @classmethod
    def toggle(cls, *edge_type):
        edge_type = list(edge_type)
        flag_state = None

        # Determine if the last argument is flag_state (0 or 1)
        if len(edge_type) > 0 and isinstance(edge_type[-1], int) and edge_type[-1] in [0, 1]:
            flag_state = edge_type.pop()

        # Expand 'synset' and 'semset' to their individual levels
        for genre in ['synset', 'semset']:
            while genre in edge_type:
                edge_type.remove(genre)
                edge_type.extend([genre + str(i) for i in range(3)])

        # Process each flag
        for arg in edge_type:
            if arg == 'name':
                continue
            elif arg in cls._FLAGS:
                flag = cls._FLAGS[arg]
                if flag_state is not None:
                    # Explicit flag state provided, enable or disable accordingly
                    if flag_state == 1:
                        cls._repr_flags |= flag  # Enable the flag
                    elif flag_state == 0:
                        cls._repr_flags &= ~flag  # Disable the flag
                else:
                    # No flag state provided, toggle the current state
                    cls._repr_flags ^= flag  # Toggle the flag
            else:
                raise ValueError(f"Unknown attribute: {arg}")
        return cls

    def __repr__(self) -> str:

        lang = self.lang if (Node._repr_flags & Node._FLAGS['lang']) else ''
        type_ = self.type if (Node._repr_flags & Node._FLAGS['type']) else ''
        lang_type = '-'.join([lang, type_]) if (lang and type_) else lang+type_

        else_name = ':'.join([lang_type, self.name]) if lang_type else self.name

        lemma = f"({self.lemma})" if (Node._repr_flags & Node._FLAGS['lemma']) else ''
        favorite = '/m' if (Node._repr_flags & Node._FLAGS['favorite']) and self.favorite else ''

        header = else_name + lemma + favorite

        parts = []

        # Synsets and semsets
        for level in range(0, 3):
            synset_flag = Node._FLAGS[f'synset{level}']
            semset_flag = Node._FLAGS[f'semset{level}']
            if Node._repr_flags & synset_flag:
                label_prefix = f"synset{level}=" if Node.labels else ""
                parts.append(f"{label_prefix}{len(getattr(self, f'synset{level}', []))}")
            if Node._repr_flags & semset_flag:
                label_prefix = f"semset{level}=" if Node.labels else ""
                parts.append(f"{label_prefix}{len(getattr(self, f'semset{level}', []))}")

        if Node._repr_flags & Node._FLAGS['examples']:
            parts.append(f"{'examples=' if Node.labels else ''}{len(self.examples)}")

        parts = '['+', '.join(parts)+']' if parts else ''

        return f"Node({header}){parts}"

class Graph(NodeSet):

    def __init__(self, parent=None):
        self.parent = parent
        self._build_nodes(parent)
        self._set_graph_reference()
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
            super().__init__(nodes)
        else:
            raise ValueError("Filename must end with '.txt'")
    
    def _handle_data_structure_source(self, parent):
        super().__init__(parent)

    def _set_graph_reference(self):
        for node in self:
            node.graph = self
    
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
            temp_nodes = {node.identify(format=True): node for node in nodes}
            for node in nodes:
                for attr in ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']:
                    current_relations = getattr(node, attr)
                    updated_relations = [temp_nodes.get(rel) for rel in current_relations if temp_nodes.get(rel)]
                    setattr(node, attr, updated_relations)
                    current_relations.clear()
                    current_relations.extend(updated_relations)
            return nodes

        nodes_loaded_from_txt = []
        try:
            with open(parent, 'r') as file:
                for line in file:
                    node = _parse_line_to_node(line.strip())
                    nodes_loaded_from_txt.append(node)
            nodes_loaded_from_txt = _update_node_relationships(nodes_loaded_from_txt)
            return nodes_loaded_from_txt
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
            self.append(node)

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