import difflib
import random

class NodeSet(list):

    def __init__(self, nodes=None):

        nodes_as_list = self._convert_to_list(nodes)  # converts the data structure to a list        
        super().__init__(nodes_as_list)  # initialize the parent list class

        self._define_permissions()        

    def _define_permissions(self):

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

    def scan_for_similar_nodes(self, name, k=1):
        scores = []
        if k > len(self): k = len(self)
        for node in self:
            ratio = difflib.SequenceMatcher(None, name.lower(), node.name.lower()).ratio()
            scores.append((ratio, node))
        return NodeSet([node for ratio, node in sorted(scores, key=lambda x: x[0], reverse=True)[:k]])

    def langs(self): return [node.lang for node in self]
    def types(self): return [node.type for node in self]
    def names(self): return [node.name for node in self]
    def lemmas(self): return [node.lemma for node in self]

    def set_langs(self): return list(set([n.lang for n in self]))
    def set_types(self): return list(set([n.type for n in self]))

    def _convert_to_list(self, input_nodes):
        # If the input is a NodeSet, Graph, list, or set, convert it to a list
        if isinstance(input_nodes, (NodeSet, list, set, tuple)):
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
        if all(existing_node != node for existing_node in self):
            super().append(node)  # Use super() to avoid recursion
            node.graph = self
    
    def extend(self, nodeset):
        for node in nodeset:
            self.append(node)
        return self

    def find(self, **kwargs):

        lang = kwargs.get('lang', '')
        type_ = kwargs.get('type', '')
        name = kwargs.get('name', '')
        lemma = kwargs.get('lemma', None)
        favorite = kwargs.get('favorite', None)

        # Initialize results list.
        results = []

        # Iterate over each node in the container.
        for node in self:
            # Check if the node matches the non-empty criteria.
            if (not lang or node.lang == lang) and \
               (not type_ or node.type == type_) and \
               (not name or node.name == name) and \
               (lemma is None or (isinstance(lemma, bool) and bool(node.lemma) == lemma) or node.lemma == lemma) and \
               (not None or node.favorite == favorite):
                results.append(node)

        # Always return the results wrapped in a NodeSet object.
        return NodeSet(results)

    def random(self, k=None, **kwargs):
        candidates = self.find(**kwargs)
        if not k and candidates: return random.choice(candidates)
        if not candidates or k < 1: return None
        if k == 1: return NodeSet(nodes=[random.choice(candidates)])
        if k <= len(candidates): return NodeSet(nodes=random.sample(candidates, k))
        raise ValueError(f"k must be less than or equal to the number of nodes, got {k} for {len(candidates)} nodes.")
    
    def edit(self, **attr_edits):
        # Iterate through the keyword arguments provided in 'changes'
        for node in self:
            node.edit(**attr_edits)

    def is_lang(self, *langs, complement=False):
        return self._filter_nodes(lambda node: getattr(node, 'lang') in langs, complement)
    
    def is_type(self, *types, complement=False):
        return self._filter_nodes(lambda node: getattr(node, 'type') in types, complement)

    def has_lemma(self, lemma=True):
        return self._filter_nodes(lambda node: bool(node.lemma) == lemma)

    def is_favorite(self, favorite=True):
        return self._filter_nodes(lambda node: bool(node.favorite) == favorite)

    def char_count(self, *args, on_lemma=False):
        return self._filter_by_length('char_count', *args, on_lemma=on_lemma)

    def word_count(self, *args, on_lemma=False):
        return self._filter_by_length('word_count', *args, on_lemma=on_lemma)

    def contains_word(self, *args, on_lemma=False):
        return self._filter_by_string_occurrence('contains_word', *args, on_lemma=on_lemma)

    def contains(self, *args, on_lemma=False):
        return self._filter_by_string_occurrence('contains', *args, on_lemma=on_lemma)

    def starts_with(self, chain, on_lemma=False):
        return self._filter_nodes(lambda node: getattr(node, 'lemma' if on_lemma else 'name', "").lower().startswith(chain.lower()))

    def ends_with(self, chain, on_lemma=False):
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
    
    def _filter_nodes(self, condition, complement=False):
        # Initialize an empty list to hold nodes that pass the filter.
        filtered_nodes = []

        # Iterate over all nodes in the current set.
        for node in self:
            # Check if the node meets the condition.
            if condition(node):
                # If complement is False, add nodes that meet the condition.
                if not complement:
                    filtered_nodes.append(node)
            else:
                # If complement is True, add nodes that do not meet the condition.
                if complement:
                    filtered_nodes.append(node)

        # Return a new instance of NodeSet containing the filtered nodes.
        return NodeSet(nodes=filtered_nodes)

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
    
    def filter_synset(self, operator, value, level=None):
        level = (0, 1, 2) if level is None else (level,) if isinstance(level, int) else level
        return [node for i in level for node in self._filter_by_attribute(f'synset{i}', operator, value)]
    
    def filter_semset(self, operator, value, level=None):
        level = (0, 1, 2) if level is None else (level,) if isinstance(level, int) else level
        return [node for i in level for node in self._filter_by_attribute(f'semset{i}', operator, value)]

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
    
    def has_synset(self, target_nodes, sections=(0, 1, 2), tolerance=1.0, complement=False):
        return self._filter_by_relationship_type('synset', target_nodes, sections, tolerance)
    
    def has_semset(self, target_nodes, sections=(0, 1, 2), tolerance=1.0, complement=False):
        return self._filter_by_relationship_type('semset', target_nodes, sections, tolerance)
    
    def _filter_by_relationship_type(self, relationship_base, target_nodes, sections, tolerance, complement):
        # Ensure target_nodes is a set for efficient lookup.
        if not isinstance(target_nodes, (list, tuple)): target_nodes = (target_nodes,)
        target_nodes_set = set(target_nodes)
        # Initialize an empty NodeSet to hold nodes that pass the filter.
        filtered_nodes = NodeSet()
        # Calculate the minimum number of connections needed based on tolerance.
        min_connections = max(1, round(tolerance * len(target_nodes_set)))

        # Iterate over all nodes in the current set.
        for node in self:
            connections_met = 0  # Track the number of connections met.

            # Check each specified section.
            for section in sections:
                related_nodes = getattr(node, f'{relationship_base}{section}', [])

                # Increment connections_met for each target node that's connected.
                connections_met += len(target_nodes_set.intersection(related_nodes))

                # If the connections met the required number, add the node to filtered_nodes.
                if connections_met >= min_connections:
                    if not complement:
                        filtered_nodes.append(node)
                    break  # No need to check further sections for this node.
                else:
                    if complement:
                        filtered_nodes.append(node)

        return filtered_nodes
       
    def __repr__(self):
        return f'NodeSet(size={len(self)})'