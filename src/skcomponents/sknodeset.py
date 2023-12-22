import random

class NodeSet(list):

    def __init__(self, nodes=None):

        nodes_as_list = self._convert_to_list(nodes)  # converts the data structure to a list        
        super().__init__(nodes_as_list)  # initialize the parent list class

        self.define_permissions()        

    def define_permissions(self):

        synset0, synset1, synset2 = True, True, True
        semset0, semset1, semset2 = True, True, True

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
        if isinstance(input_nodes, (NodeSet, list, set)):
            return list(set(input_nodes))
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
        # Check if the node is unique based on its identifier
        if any(existing_node == node for existing_node in self):
            raise ValueError("A node with the same identifier already exists in the Graph.")

        super().append(node)  # Use super() to avoid recursion

        # Set the graph reference in the Node instance
        node.graph = self

    def find(self, *args):

        # Unpack arguments based on their number and type
        if len(args) == 1 :
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

    def random(self, k=None):
        if not k and self: return random.choice(self)
        if not self or k < 1: return None
        if k == 1: return NodeSet(nodes=random.choice(self))
        if k <= len(self): return NodeSet(nodes=random.sample(self, k))
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

        return NodeSet(nodes=filtered_nodes)

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