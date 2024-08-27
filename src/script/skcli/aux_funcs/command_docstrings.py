from typing import Dict

COMMAND_DOCSTRINGS_LS : Dict[str, str] = {
'cd': """\
| Desc. Enters a given node within the results.
| Signature : cd <index>
| Arguments : 
    1. <index>  A single index representing the target node to access as current
| Usage examples :
    cd 47\
""",

'<name>': """\
| Desc. Binds a given node to the current.
| Signature : <name>
| Arguments :
    1. <name>  The name reference to find for a node to be binded.
    <!> If multiple coincidences are encountered, pops an interface for selection.
    <!> If no matching is encountered, allows for the creation (and binding) of the node.
| Usage examples :
    Sensatez\
""",

'del': """\
| Desc. Unbinds the given nodes(s).
| Signature : del <*index>
| Arguments :
    1. <*index>  As many indexes as connections to be unbinded.
| Usage examples :
    del 1 62 6 95
    del 1-15\
""",

'clear': """\
| Desc. Fully unbinds all nodes from the field.
| Signature : clear\
""",

'mv': """\
| Desc. Moves bindings to a different field.
| Signature : mv <*index> [<name>] [<*field>]
| Arguments :
    1. <*index> [opt]  Index(s) representing connections. If none is entered, all are selected.
    2. <name>   [opt]  Name of the node to which we want to move. If none, placeholder node is selected.
    3. <*field> [opt]  The field(s) to which the connections are headed towards. If none, selects placeholder fields.
    Note. Either <name> or <*fields> need to be specified.
| Usage examples :
    mv y1
    mv 22-28 Liebre
    mv 48 49 e1
    mv 50 12-14 Caparazón y0 y1 
""",

'cp': """\
| Desc. Copies bindings to a field.
| Signature : cp <*index> [<name>] [<*field>]
| Arguments :
    1. <*index> [opt]  Index(s) representing connections. If none is entered, all are selected.
    2. <name>   [opt]  Name of the node to which we want to move. If none, placeholder node is selected.
    3. <*field> [opt]  The field(s) to which the connections are headed towards. If none, selects placeholder fields.
    Note. Either <name> or <*fields> need to be specified.
| Usage examples :
    cp y1
    cp 22-28 Liebre
    cp 48 49 e1
    cp 50 12-14 Caparazón y0 y1 
""",

'cross': """\
| Desc. Interconnects every node of a subset either via 'y1' or 'e1'.
| Signature : cross <*index> [<y/e>]
| Arguments :
    1. <*index>  Index(s) representing connections.
    2. [y/e]     If 'y', the connections will be set through 'synset1'. Otherwise, through 'semset1'.
| Usage examples :
    cross 4-12 e
    cross 4-12 y
""",

'align': """\
| Desc. Aligns the content from the given nodes.
| Signature : align <*index> [<*field>]
| Arguments :
    1. <*index>        Index(s) representing connections (if only 1 is inserted, will align it with the placeholder node).
    2. <*field>[opt]   If 'y', the connections will be set through 'synset1'. Otherwise, through 'semset1'. Placeholder is default.
    3. <p>[opt]        Also align with the current node of the placeholder.
| Usage examples :
    align 13
    align 13-16 . y
    align 13 y0
    align 1 2 5 
    align 1 2 5 y
""",

'ls': """\
| Desc. Refreshes the node contents by showing the stat within edits.
| Signature : ls
| Arguments : None\
""",

'<__>': """\
| Desc. Switches to any field of format (y/e)(0/1/2).
| Signature : __
| Arguments : None\
""",

}

COMMAND_DOCSTRINGS_SK : Dict[str, str] = {
'set': """\
| Desc. Sets or adds properties to the current node or environment.
| Signature : set <*settings>
| Arguments :
  <!> Supports shorthand for groups and individual settings.
    1. <settings>
              "y/e"  Add all 'y' or 'e' prefixed fields (e.g., y0, y1, y2).
            "y_/e_"  Add specific fields (e.g., y0 y1)
        "es/fr/..."  Set the node language for the PlaceHolder.
        "n/j/v/..."  Set the node type for the PlaceHolder.
| Usage examples :
    set y
    set y0 e1
    set en j y0 e2\
""",

'<field>': """\
| Desc. Shorter field setting.
| Signature : <field>
| Arguments :
    <field> : Single-short format representation of a field.
| Usage examples :
    y0
    y1\
""",

'unset': """\
| Desc. Removes properties or settings from the current node or environment.
| Signature : unset [<*setting>]
| Arguments :
  <!> Supports shorthand for groups and individual settings.
    1. <*settings>
              "y/e"  Add all 'y' or 'e' prefixed fields (e.g., y0, y1, y2).
            "y_/e_"  Add specific fields (e.g., y0 y1)
| Usage examples :
    unset e
    unset y e0 e2\
""",

'tag': """\
| Desc. Sets a word as a tag.
| Signature : tag [<word>]
| Usage examples :
    tag Dedos\
""",

'tagged': """\
| Desc. Displays the tags (and enables deletion through 'del')
| Signature : tags
| Usage examples :
    tags
    Current tags:
    | 1. Dedos
    >> del 1
    | Tag 'Dedos' deleted succesfully.\
""",

'filter': """\
| Desc. Uses the tags as a semantic filter to display results.
| Signature : filter <threshold>
| Arguments :
    1. <threshold>  A match threshold for deciding to take a node as a result.
                    (must be between 0 and 1)
| Usage examples :
    filter 0.01 (soft, lots of results) 
    filter 1.00 (stringent, fewer results)\
""",

'pick': """\
| Desc. Suggests a list of elements to pick from and adds the selected element to the current field of the placeholder.
| Signature : pick [-c <choices>]
| Arguments :
    -c, --choices  Number of choices to display (default: 5)
| Usage examples :
    pick
    pick -c 10\
""",

'sug': """\
| Desc. Suggests nodes or semantic elements for binding based on semantic similarity or randomly.
| Signature : sug
| Arguments : None
| Usage examples :
    sug
| Input :
    - Y : Accept and bind the suggested node or semantic element.
    - N : Reject the suggestion and move to the next one (or just ENTER)
    - q : Quit the suggestion mode.
| Example interaction :
    | Found 5 nodes with semantic similarity.
    | [1/5] NodeName [Y/N] (q to quit) > y
    | Nodes successfully binded through y0
    | [2/5] AnotherNode [Y/N] (q to quit) > n
    | [3/5] ThirdNode [Y/N] (q to quit) > q
    | Exiting suggestion mode.\
""",

'cd': """\
| Desc. Accesses a node and sets it as current.
| Signature : cd <ent> <--n>
| Arguments :
    1. <ent>  A single node name. Must match case.
    2. <n>    The number of guesses if no exact match is found.
              Tip : This is very useful to find node names containing a certain content.
| Usage examples :
    cd Augustus César\
""",

'r': """\
| Desc. Freely performs a random node search with optional language and type constraints.
| Signature : r [-l <lang>] [-t <type>] [-s <lim>] [-f]
| Arguments :
    -l, --lang  Specify the language to narrow down the search (persistent across commands).
    -t, --type  Specify the type to narrow down the search (persistent across commands).
     |
    -s, --sos   Specify the max number of connections a node can have to be considered.
    -f, --fav   Specify wether the output must be favorite or not.
| Usage examples :
    r
    r -l en -t n
    r -l # to unset
    r -t # to unset\
""",

'<name>': """\
| Desc. Makes a connection through the placeholder parameters.
| Signature : <name>
| Note : this is usually faster than the 'ls' approach.\
""",

'ls': """\
| Desc. Lists the current node's neighbors within the field scope, allowing for edit if single.
| Signature : ls [<y_/e_>] [-d] [-r]
|                         [-p <lim>] [-w <width=35>] [-a <lim>] [-c <ncol=4>]
|                         [-l <lang>] [-t <type>]
| Arguments :
    <y/e_>   Can automatically switch to a given field.
     |
    -l, --lang      Restricts the search to results of the lang (persistent across comands).
    -t, --type      Restricts the search to results of the type (persistent across comands).
     |
    -d, --details   Single-column data & field sizes.
    -r, --shuffle   Randomize the display order (by default, alphabetical is applied).
    -p, --stop      Limit the number of results.
    (*) -w, --width     Max allowed width for column (absolute).
    (*) -a, --abbr      Max allowed character length for names.
    (*) -c, --ncol      Number of columns.
    Note : the starred flags (*) only apply if '--details' isn't flagged.
| Usage examples :
    ls
    ls y0
    ls -d -t 15 -r
    ls -w 50 -a 5 -c 1
    ls -l es\
""",

'edit': """\
| Desc. Edit a hash attribute for the current node.
| Signature : edit <hash_attr> <new_value>\
| Arguments :
    1. Hash Attribute : the attribute we want to edit.
    2. New Value : the new value the attribute will be assigned.
| Usage examples :
    edit lang rs
    edit type w
    edit name Tendencia
    edit lemma NA\
""",

'pin': """\
| Desc. Pins a node, which means it sets 'favorite' attr to True.
| Signature : pin\
""",

'unpin': """\
| Desc. Unpins a node, which means it sets 'favorite' attr to False.
| Signature : unpin\
""",

'del': """\
| Desc. Removes the current node from the graph (will ask first).
| Signature : del\
""",

'new': """\
| Desc. Enters a new node to the graph.
| Signature : new <name>
| Arguments :
    1. Name : The complete name of the new entry.
| Usage examples :
    new Carlo Magno\
""",

'term': """\
| Desc. Starts a terminal within the SKCLI terminal.
| Signature : term\
""",

'save': """\
| Desc. Saves the actual version of the Graph in the current directory.
| Signature : save [<filename='data.txt'>]
| Arguments :
    1. filename : file to where the graph will be saved (terminated with .txt)
| Usage examples :
    save
    save provisional_dat.txt\
""",

'back': """\
| Desc. Goes back to menu.
| Signature : back
| Usage examples :
    back\
""",

'clear': """\
| Desc. Clears the screen.
| Signature : clear
"""

}
