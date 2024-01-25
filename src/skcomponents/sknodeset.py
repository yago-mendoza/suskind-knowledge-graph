import difflib
import random

class NodeSet(list):

    def __init__(self, nodes=None):

        # Parses data structures into a list
        if isinstance(nodes, (NodeSet, list, set, tuple)):
            nodes = list(set(nodes)) # uniformize + listify
        nodes_as_list = nodes or []
   
        super().__init__(nodes_as_list) # initialize the parent list class   

    ##########
    # Display
    ##########

    def get_set(self, property):
        # Gets a set list of either 'lang' or 'type (or 'name' or 'lemma')
        return list(set(getattr(node, property) for node in self))
    
    def look(self):
        # Displays it in the __repr__ format set for <Node>, for fast inspection.
        return [node for node in self]
    
    #########
    # Search
    #########

    def select(self, **kwargs):
       
        lang_req = kwargs.get('lang', [])
        type_req = kwargs.get('type', [])
        name_req = kwargs.get('name', [])
        lemma_req = kwargs.get('lemma', None)  # Can be a list, single value, or None
        favorite_req = kwargs.get('favorite', None)  # Can be a list, single value, or None

        # Ensure all criteria are in list form for uniformity.
        if not isinstance(lang_req, list): lang_req = [lang_req]
        if not isinstance(type_req, list): type_req = [type_req]
        if not isinstance(name_req, list): name_req = [name_req]
        if not isinstance(lemma_req, list) and lemma_req != None: lemma_req = [lemma_req]
        if not isinstance(favorite_req, list) and favorite_req != None: favorite_req = [favorite_req]

        results = []
        for node in self:
            # Check if the node matches the non-empty criteria.
            if ((not lang_req or node.lang in lang_req) and \
                (not type_req or node.type in type_req) and \
                (not name_req or node.name in name_req) and \
                (not lemma_req or ((node.lemma!='NA') in lemma_req) or node.lemma in lemma_req) and \
                (not favorite_req or node.favorite in favorite_req) and \
                    any([lang_req, type_req, name_req, lemma_req, favorite_req])):
                results.append(node)

        return NodeSet(results)

    def random(self, k=None, **kwargs):
        candidates = self.select(**kwargs) if kwargs else self
        
        num_candidates = len(candidates)
        if not candidates or k is not None and k < 1:
            return None
        if k is None or k == 1:
            return random.choice(candidates) if k is None else NodeSet(nodes=[random.choice(candidates)])
        if k <= num_candidates:
            return NodeSet(nodes=random.sample(candidates, k))
        raise ValueError(f"k must be less than or equal to the number of nodes, got {k} for {num_candidates} nodes.")

    def find_similars(self, target_name, k=1):
        k = min(k, len(self))  # Ensure k does not exceed the number of nodes
        scores = [(difflib.SequenceMatcher(None, target_name.lower(), node.name.lower()).ratio(), node) for node in self]
        top_scores = sorted(scores, key=lambda x: x[0], reverse=True)[:k]
        return [(round(ratio, 3), node) for ratio, node in top_scores]
    
    ############
    # Filtering
    ############

    # Filtering by syntax

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
    
    # Filtering by number of X connections

    def filter_synset(self, operator, value, level=None):
        # ndst.filter_synset('>',5,level=2)
        # ndst.filter_synset('>',5,level=(1,2))
        levels = (0, 1, 2) if level is None else (level,) if isinstance(level, int) else level
        return NodeSet([node for node in self
                        for i in levels 
                        if self.___compare(len(getattr(node, f'synset{i}', [])), operator, value)])
    
    def filter_semset(self, operator, value, level=None):
        # ndst.filter_semset('>',5,level=2)
        # ndst.filter_semset('>',5,level=(1,2))
        levels = (0, 1, 2) if level is None else (level,) if isinstance(level, int) else level
        return NodeSet([node for node in self
                        for i in levels 
                        if self.___compare(len(getattr(node, f'semset{i}', [])), operator, value)])
    
    ##############
    # Manteinance
    ##############

    def _clean_spurious_edges(self):
        """Cleans connections to nodes not present in the structure."""
        node_identifiers = {node._convert_header_to_str_format() for node in self}
        # Create a set of node identifiers for faster membership checks
        attrs_to_check = ['synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2']
        # Define attributes to check in each node
        for node in self:
            # Remove connections to nodes not present in the NodeSet
            for attr in attrs_to_check:
                valid_nodes = [n for n in getattr(node, attr, []) if n._convert_header_to_str_format() in node_identifiers]
                setattr(node, attr, valid_nodes)

    #######################################
    # Inner Workings (most of the unused) #
    #######################################

    def edit(self, **attr_edits):
        # Mass-edit is enabled.
        for node in self:
            node.edit(**attr_edits)

    def append(self, node):
        # Checks for node uniqueness before appending.
        if all(node != existing_node for existing_node in self):
            node.graph = self
            super().append(node) # Use super() to avoid recursion
    
    ### (inner workings for 'filter' functions from above)  ###
    
    def _filter_by_length(self, length_type, *args, on_lemma=False):

        def condition_func(node):

            target = getattr(node, 'lemma' if on_lemma else 'name', "").lower()
            length_func = len if length_type == 'char_count' else lambda t: len(t.split())
            target_length = length_func(target)

            if len(args) == 1:
                return target_length == args[0]
            elif len(args) == 2:
                operator, value = args
                return self.___compare(target_length, operator, value)

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

    def _compare_string_occurrence(self, target, *args):
        if len(args) == 1:
            return args[0] in target
        elif len(args) == 2 and isinstance(args[1], int):
            return target.count(args[0]) == args[1]
        elif len(args) == 3:
            string, operator, value = args
            return self.___compare(target.count(string), operator, value)
        else:
            raise ValueError("Invalid arguments for string occurrence comparison.")

    def ___compare(self, target_value, operator, value):
        operations = {
            '>=': target_value >= value,
            '<=': target_value <= value,
            '>': target_value > value,
            '<': target_value < value,
            '=': target_value == value,
            '!=': target_value != value
        }
        return operations.get(operator, False)
    
    ###
       
    def __repr__(self):
        return f'NodeSet(size={len(self)})'