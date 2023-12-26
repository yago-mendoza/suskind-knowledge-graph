from src.skcomponents.sknodeset import NodeSet

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
    
    def get_neighbors(self, permission_string=''):

        results = _WrapperDict()

        def _parse_permission(s):
            bits = [bool(int(b)) for b in s.zfill(6)]
            return {f'{type}{i}': bits[i + (3 if type == 'semset' else 0)]
                    for i in range(3) for type in ['synset', 'semset']}
        
        permission_dict = _parse_permission(permission_string)

        # Collect neighbors based on permissions and edge types
        for i in range(3):
            for edge_type in ['synset', 'semset']:
                permission_dict = self.graph.edge_permissions if not permission_string else permission_dict
                edge_key = f'{edge_type}{i}'
                if permission_dict.get(edge_key):
                    neighbors = getattr(self, f'get_{edge_type}')(i)
                    results[edge_key] = NodeSet(neighbors)

        return results

    def is_connected(self, node):
        return node in self.get_neighbors()

    def get_synset(self, *levels):
        levels = (0, 1, 2) if not levels else (levels) if isinstance(levels, int) else levels
        return NodeSet([node for i in levels for node in getattr(self, f'synset{i}', [])])
    
    def get_semset(self, *levels):
        levels = (0, 1, 2) if not levels else (levels) if isinstance(levels, int) else levels
        return NodeSet([node for i in levels for node in getattr(self, f'semset{i}', [])])

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
    
class _WrapperDict(dict):
    def nodeset(self):
        """Converts all the NodeSet values in the dictionary to a single set."""
        all_nodes = NodeSet()
        for nodeset in self.values():
            all_nodes.extend(nodeset)
        return all_nodes

    def set(self):
        all_nodes = set()
        for nodeset in self.values():
            all_nodes.update(nodeset)
        return all_nodes
    
    def count(self):
        """Returns a dictionary where the keys are the counts and the values are NodeSets of nodes that appear that many times."""
        node_count = {}
        for nodeset in self.values():
            for node in nodeset:
                node_count[node] = node_count.get(node, 0) + 1

        count_dict = {}
        for node, count in node_count.items():
            if count not in count_dict:
                count_dict[count] = NodeSet([])
            count_dict[count].append(node)

        return count_dict