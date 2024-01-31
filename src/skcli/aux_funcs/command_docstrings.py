from typing import Dict

COMMAND_DOCSTRINGS_GB : Dict[str, str] = {
'grab': """\
| Desc. Adds a new node.
| Signature : grab <name>
| Arguments :
    1. <name>  The name of the node to be grabbed.
| Usage examples :
    grab Augusto César\
""",

'rm': """\
| Desc. Removes the given nodes(s).
| Signature : rm <*index>
| Arguments :
    1. <*index>  As many indexes as connections to be unbinded.
| Usage examples :
    rm 1 2 3\
""",

'clear': """\
| Desc. Clears all node within the grabbed list.
| Signature : clear\
""",

'ls': """\
| Desc. Refreshes the grabbed nodes list in screen.
| Signature : grabbed\
""",

}

COMMAND_DOCSTRINGS_LS : Dict[str, str] = {
'cd': """\
| Desc. Enters a given node within the results.
| Signature : ls <index>
| Arguments : 
    1. <index>  A single index representing the target node to access as current
| Usage examples :
    cd 47\
""",

'add': """\
| Desc. Binds nodes to the current.
| Signature : add <name>
| Arguments :
    1. <name>  The name reference to find for a node to be binded.
    <!> If multiple coincidences are encountered, pops an interface for selection.
    <!> If no matching is encountered, allows for the creation (and binding) of the node.
| Usage examples :
    add Sensatez\
""",

'del': """\
| Desc. Unbinds the given nodes(s).
| Signature : del <*index>
| Arguments :
    1. <*index>  As many indexes as connections to be unbinded.
| Usage examples :
    del 1 62 6 95\
""",

'clear': """\
| Desc. Fully unbinds all nodes from the field.
| Signature : clear\
""",

'mv': """\
| Desc. Moves bindings to a different field.
| Signature : mv <*index> <*field>
| Arguments :
    1. <*index>  One or more indexes representing connections to be relocated.
    2. <*field>  The field(s) to which the connections are intended to be reconnected.
| Usage examples :
    mv 50 12 13 14 y0 y1 
""",

'tf': """\
| Desc. Transfers the selected contents to the choice fields of an other node.
| Signature : tf [<*index>] [node_name] [<*field>]
| Arguments :
    1. <*index> [opt] : The index(s) representing connections. If none, moves them all.
    2. <node_name>    : The node where the connections will be set.
    2. <*field> [opt] : The field(s) where to replicate. If none, selects the current.
| Usage examples :
    tf 18 19 25 55 Rodillo de amasar y0 y1
    tf Vergüenza e1
    tf Camino
""",

'cp': """\
| Desc. Copies bindings to a field.
| Signature : cp <*index> <*field>
| Arguments :
    1. <*index>  One or more indexes representing connections to be copied.
    2. <*field>  The field(s) to which the connections are intended to be copied.
| Usage examples :
    cp 50 12 13 14 y0 y1 
""",

'grab': """\
| Desc. Grabs the given nodes(s).
| Signature : grab <*index>
| Arguments :
    1. <*index>  As many indexes as connections to be grabbed.
| Usage examples :
    grab 1 22 13 55\
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

'unset': """\
| Desc. Removes properties or settings from the current node or environment.
| Signature : unset <*settings>
| Arguments :
  <!> Supports shorthand for groups and individual settings.
    1. <*settings>
              "y/e"  Add all 'y' or 'e' prefixed fields (e.g., y0, y1, y2).
            "y_/e_"  Add specific fields (e.g., y0 y1)
| Usage examples :
    unset e
    unset y e0 e2\
""",

'cd': """\
| Desc. Accesses a node and sets it as current.
| Signature : cd <ent>
| Arguments :
    1. <ent>  A single node name. Must match case.
| Usage examples :
    cd Augustus César\
""",

'r': """\
| Desc. Freely performs a random node search with optional language and type constraints.
| Signature : r [-l <lang>] [-t <type>] [-f]
| Arguments :
    -l, --lang  Specify the language to narrow down the search.
    -t, --type  Specify the type to narrow down the search.
    -f, --fav   Specify wether the output must be favorite or not.
| Usage examples :
    r
    r -l en -t n\
""",

'run': """\
| Desc. Runs a density search on the grabbed nodes set.
| Signature : run [-f] [-d] [-r] [-t <lim>] [-w <width=20>] [-a <lim>] [-c <ncol=3>]
| Arguments :
    -f, --fielding  Restricts the search to results within the placeholder fielding.
    -d, --details   Single-column data & field sizes.
    -r, --shuffle   Randomize the display order (by default, alphabetical is applied).
    -t, --stop      Limit the number of results.
    (*) -w, --width     Max allowed width for column (absolute).
    (*) -a, --abbr      Max allowed character length for names.
    (*) -c, --ncol      Number of columns.
    Note : the starred flags (*) only apply if '--details' isn't flagged.
| Usage examples :
    run
    run -f
    run -d -t 15 -r
    run -w 50 -a 5 -c 1
""",

'del': """\
| Desc. Removes the current node from the graph (will ask first).
| Signature : del\
""",

'ls': """\
| Desc. Lists the current node's neighbors within the field scope, allowing for edit if single.
| Signature : ls [-d] [-r] [-t <lim>] [-w <width=20>] [-a <lim>] [-c <ncol=3>]
| Arguments :
    -d, --details   Single-column data & field sizes.
    -r, --shuffle   Randomize the display order (by default, alphabetical is applied).
    -t, --stop      Limit the number of results.
    (*) -w, --width     Max allowed width for column (absolute).
    (*) -a, --abbr      Max allowed character length for names.
    (*) -c, --ncol      Number of columns.
    Note : the starred flags (*) only apply if '--details' isn't flagged.
| Usage examples :
    ls
    ls -d -t 15 -r
    ls -w 50 -a 5 -c 1
""",

'new': """\
| Desc. Enters a session for introducing new entries.
| Signature : new
| Arguments : None
| Usage examples :
    new\
""",

'grabbed': """\
| Desc. Enters a session for editing the grabbed nodes.
| Signature : grabbed
| Arguments : None
| Usage examples :
    grabbed\
""",

'grab': """\
| Desc. Grabs the current node or a given one.
| Signature : grab [name]
| Arguments :
    1. name [opt] : name of the node the function will try to grasp.
| Usage examples :
    grab
    grab Augusto César\
""",

'edit': """\
| Desc. Edit a hash attribute for the current node.
| Signature : edit [hash_attr] [new_value]\
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

'term': """\
| Desc. Starts a terminal within the SKCLI terminal.
| Signature : term\
""",

'save': """\
| Desc. Saves the actual version of the Graph in the current directory.
| Signature : save [filename='data.txt']
| Arguments :
    1. filename : file to where the graph will be saved (terminated with .txt)
| Usage examples :
    save
    save provisional_dat.txt\
""",

'clear': """\
| Desc. Clears the screen.
| Signature : clear
"""

}
