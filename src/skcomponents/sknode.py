from src.skcomponents.sknodeset import NodeSet
import src.sktools as sk
import difflib

class Node:

    def __init__(self, lang: str, type: str, name: str, lemma: str,
                 favorite: bool = False,
                 synset0: list = None, synset1: list = None, synset2: list = None,
                 semset0: list = None, semset1: list = None, semset2: list = None,
                 examples: list = None) -> None:
        
        self.graph = None

        # 1. Hash

        self.lang, self.type, self.name = lang, type, name # str
        self.lemma = lemma if lemma is not None else "NA" # str ("NA" by default)
        
        # 2. Connections

        self.synset0 = synset0 if synset0 else [] # list
        self.synset1 = synset1 if synset1 else [] # list
        self.synset2 = synset2 if synset2 else [] # list

        self.semset0 = semset0 if semset0 else [] # list
        self.semset1 = semset1 if semset1 else [] # list
        self.semset2 = semset2 if semset2 else [] # list
        
        # 3. Additional   
            
        self.favorite = favorite == True # bool (False by default)
        self.examples = examples if examples is not None else [] # list

    def get_neighbors(self, *fielding):

        long_format_fields = sk.parse_field(*fielding, long=True)
        
        results = []
        for long_format_field in long_format_fields:
            edge_type, index = long_format_field[:-1], int(long_format_field[-1])
            results += getattr(self, f'get_{edge_type}')(index)

        return NodeSet(results)
    
    def get_synset(self, *levels):
        levels = (0, 1, 2) if not levels else (levels) if isinstance(levels, int) else levels
        return NodeSet([node for i in levels for node in getattr(self, f'synset{i}', [])])
    
    def get_semset(self, *levels):
        levels = (0, 1, 2) if not levels else (levels) if isinstance(levels, int) else levels
        return NodeSet([node for i in levels for node in getattr(self, f'semset{i}', [])])
    
    def get_sizes(self):
        return (len(self.synset0), len(self.synset1), len(self.synset2),
                len(self.semset0), len(self.semset1), len(self.semset2),)
    
    def edit(self, **attr_edits):
        # Edits either 'lang', 'type', 'name' or 'lemma'.
        for key, value in attr_edits.items():
            if hasattr(self, key):
                setattr(self, key, value)

    # Additional functions

    def identify(self, core_only=False):
        # Used to enhance accessibility to hash attributes
        if not core_only:
            return (self.lang, self.type, self.name, self.lemma)
        return (self.lang, self.type, self.name)
    
    def is_homologous(self, other):
        # Checks if the core is the same for both Nodes.
        if isinstance(other, Node):
            return self.identify(core_only=True) == other.identify(core_only=True)
        return False

    def is_connected(self, other):
        # Checks if it is connected in any way.
        return other in self.get_neighbors().set()
    
    def assess_similarity(self, node):
        name_to_compare = node if isinstance(node,str) else node.name
        return difflib.SequenceMatcher(None, self.name.lower(), name_to_compare.lower()).ratio()
    
    ###########################
    # Used by external Classes
    ###########################
    
    #[not-documented]
    def _convert_header_to_str_format(self):
        # Used at _update_node_relationships() when load_data() is run from Graph object.
        # Used at save() when we want to save the data from Graph object.
        return f'{self.lang}-{self.type}:{self.name}({self.lemma})'

    #[not-documented]
    def _copy(self):
        # Used during Graph "merging" functions.
        return Node(
            self.lang, self.type, self.name, self.lemma, self.favorite,
            self.synset0[:], self.synset1[:], self.synset2[:],
            self.semset0[:], self.semset1[:], self.semset2[:],
            self.examples[:]
        )   
    
    #[not-documented]
    def __hash__(self):
        # It is used at no point of the project.
        return hash((self.lang, self.type, self.name, self.lemma))
    
    #[not-documented]
    def __eq__(self, other):
        # Checks perfect equivalence for identifiers.
        if isinstance(other, Node):
            return self.lang == other.lang and self.type == other.type and self.name == other.name and self.lemma == other.lemma
        return False
    
    #################################
    # Flags (developer visualisation)
    #################################

    """
    Note for reviewers:
    - FLAGS are useless beyond developing.
    - They only set the way __repr__ set visualisatinon of <Node> objects for developers.
    - The class really starts at line ~150 (after the __repr__ method re-definition)"""

    #_FLAGS : keeps the relation between 'str' and 'binary' code.
    #_repr_flags : actual state of the flags
    #_back_labels : binary (1/0) that sets wether labels will be displayed
    #    Ej. en-n:Dog(semset0=9, synset0=14, ...) OR en-n:Dog(9, 14, ...)

    identifier_structs = {'lang', 'type', 'name', 'lemma'}
    descriptive_structs = {'favorite'}
    edge_structs = {'synset0', 'synset1', 'synset2', 'semset0', 'semset1', 'semset2'}
    front_structs = identifier_structs | descriptive_structs
    back_structs = edge_structs | {'examples'}
    all_structs = front_structs | back_structs

    # Generate the dictionary _FLAGS with binary values
    _FLAGS = {flag: 1 << i for i, flag in enumerate(sorted(all_structs))}

    # >>> _FLAGS = {
    # ...         'lang':       0b000000000001,  
    # ...         'type':       0b000000000010,  
    # ...         'name':       0b000000000100,  
    # ...         'lemma':      0b000000001000,  
    # ...         'favorite':   0b000000010000,  
    # ...         'synset0':    0b000000100000,  
    # ...         'synset1':    0b000001000000,  
    # ...         'synset2':    0b000010000000,  
    # ...         'semset0':    0b000100000000,  
    # ...         'semset1':    0b001000000000,  
    # ...         'semset2':    0b010000000000,  
    # ...         'examples':   0b100000000000   
    # ...     }

    # Initially enable all flags
    _repr_flags = 0b111111111111
    _back_labels = 1

    @classmethod
    def toggle_back_labels(cls, flag=None):
        if flag in {0,1}:
            cls._back_labels = flag
        cls._back_labels ^= 1
        return cls

    @classmethod
    def compress(cls, *edge_type):
        if not edge_type:
            cls.toggle(*cls.identifier_structs, 1)
            cls.toggle(*cls.descriptive_structs, 0)
            cls.toggle(*cls.edge_structs, 0)
        else:
            cls.toggle(*edge_type, 0)
        return cls

    @classmethod
    def expand(cls, *edge_type):
        if not edge_type:
            cls.toggle(*cls.identifier_structs, 1)
            cls.toggle(*cls.descriptive_structs, 1)
            cls.toggle(*cls.edge_structs, 1)
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
        type = self.type if (Node._repr_flags & Node._FLAGS['type']) else ''
        lang_type = '-'.join([lang, type]) if (lang and type) else lang+type
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
                label_prefix = f"synset{level}=" if Node._back_labels else ""
                parts.append(f"{label_prefix}{len(getattr(self, f'synset{level}', []))}")
            if Node._repr_flags & semset_flag:
                label_prefix = f"semset{level}=" if Node._back_labels else ""
                parts.append(f"{label_prefix}{len(getattr(self, f'semset{level}', []))}")

        if Node._repr_flags & Node._FLAGS['examples']:
            parts.append(f"{'examples=' if Node._back_labels else ''}{len(self.examples)}")
        parts = '['+', '.join(parts)+']' if parts else ''

        return f"Node({header}){parts}"



