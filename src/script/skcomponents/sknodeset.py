import src.script.sktools as sk
import random

class NodeSet(list):

    def __init__(self, nodes=None):

        # Parses data structures into a list
        if not isinstance(nodes, (NodeSet, list, set, tuple)):
            nodes = [nodes] # if its a single <Node> object
        nodes = list(set(nodes)) # uniformize + listify
        nodes_as_list = nodes or []

        self.nodes = nodes
   
        super().__init__(nodes_as_list) # initialize the parent list class   

    ##########
    # Display
    ##########

    def get_set(self, property):
        # Gets a set list of either 'lang' or 'type (or 'name' or 'lemma')
        return list(set(getattr(node, property) for node in self))
    
    def look(self):
        # Displays it in the __repr__ format set for <Node>, for fast inspection.
        return [node._convert_header_to_str_format() for node in self]
    
    #########
    # Search
    #########

    def find(self, **kwargs):
        ndst = self.select(**kwargs)
        return ndst[0] if len(ndst) == 1 else None

    def select(self, **kwargs):
        lang_req = kwargs.get('lang', None)
        type_req = kwargs.get('type', None)
        name_req = kwargs.get('name', None)
        lemma_req = kwargs.get('lemma', None)  # Can be a list, single value, or None
        favorite_req = kwargs.get('favorite', None)  # Can be a list, single value, or None

        # Ensure all criteria are in list form for uniformity.
        if lang_req is not None and not isinstance(lang_req, list): lang_req = [lang_req]
        if type_req is not None and not isinstance(type_req, list): type_req = [type_req]
        if name_req is not None and not isinstance(name_req, list): name_req = [name_req]
        if lemma_req is not None and not isinstance(lemma_req, list): lemma_req = [lemma_req]
        if favorite_req is not None and not isinstance(favorite_req, list): favorite_req = [favorite_req]

        results = []
        for node in self:
            # Check if the node matches the criteria, or include all nodes if no criteria are provided.
            if ((lang_req is None or node.lang in lang_req) and \
                (type_req is None or node.type in type_req) and \
                (name_req is None or node.name in name_req) and \
                (lemma_req is None or ((node.lemma!='NA') in lemma_req) or node.lemma in lemma_req) and \
                (favorite_req is None or node.favorite in favorite_req) and \
                    any([lang_req is not None, type_req is not None, name_req is not None, lemma_req is not None, favorite_req is not None])):
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

    ############
    # Filtering
    ############

    # Filtering by syntax

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

    # Filtering by amount of edges

    def edge_count(self, *args):
        operator, threshold = ('=', args[0]) if isinstance(args[0], int) else (args[0], args[1])
        fielding = args[2:] if isinstance(args[0], str) else args[1:]
        fielding = ['y','e'] if not fielding else fielding
        return NodeSet([node for node in self
                        if self.___compare(len(node.get_neighbors(*fielding)),operator, threshold)])
    
    #######
    # Edit
    #######

    def edit(self, **attr_edits):
        # Mass-edit is enabled.
        for node in self:
            node.edit(**attr_edits)

    #######################################
    # Inner Workings (most of the unused) #
    #######################################
    
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