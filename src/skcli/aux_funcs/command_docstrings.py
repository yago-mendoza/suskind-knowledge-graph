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

'ls': """\
| Desc. Refreshes the grabbed nodes list in screen.
| Signature : grabbed\
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
    del 1 62 6 95\
""",

'clear': """\
| Desc. Fully unbinds all nodes from the field.
| Signature : clear\
""",

'mv': """\
| Desc. Moves bindings to a different field.
| Signature : mv <*index> <name> <*field>
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
| Signature : cp <*index> <name> <*field>
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
| Signature : cross <*index> [y/e]
| Arguments :
    1. <*index>  Index(s) representing connections. Mandatory.
    2. [y/e]     If 'y', the connections will be set through 'synset1'. Otherwise, through 'semset1'.
| Usage examples :
    cross 4-12 e
    cross 4-12 y
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

COMMAND_DOCSTRINGS_VG : Dict[str, str] = {

'___': """\
| Desc. Adds an example for the node.
| Signature : ___\
""",

'del': """\
| Desc. Deletes the given examples.
| Signature : del <*index>
| Arguments :
    1. <*index>  Index(s) representing connections. Mandatory.
| Usage examples :
    del 1 3\
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
| Signature : r [-l <lang>] [-t <type>] [-s <lim>] [-f]
| Arguments :
    -l, --lang  Specify the language to narrow down the search.
    -t, --type  Specify the type to narrow down the search.
    -s, --sos   Specify the max number of connections a node can have to be considered.
    -f, --fav   Specify wether the output must be favorite or not.
| Usage examples :
    r
    r -l en -t n\
""",

'<name>': """\
| Desc. Makes a connection through the placeholder parameters.
| Signature : <name>
| Note : this is usually faster than the 'ls' approach.\
""",

'sug': """\
| Desc. Initiates a sugestor feature.
| Signature : sug
| Note : Instead of [Y/N], we can directly specify the field through which we want to connect the suggestion.\
""",

'ls': """\
| Desc. Lists the current node's neighbors within the field scope, allowing for edit if single.
| Signature : ls [<y/e_>] [-d] [-r]
|                         [-p <lim>] [-w <width=35>] [-a <lim>] [-c <ncol=4>]
|                         [-l <lang>] [-t <type>]
| Arguments :
    <y/e_>   Can automatically switch to a given field.
    -l, --lang      Restricts the search to results of the lang (persistent across comands).
    -t, --type      Restricts the search to results of the type (persistent across comands).
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
    ls -l es
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

'vg': """\
| Desc. Shows the examples for the node, hence accessing the VG pseudo-CLI.
| Signature : vg\
""",

'del': """\
| Desc. Removes the current node from the graph (will ask first).
| Signature : del\
""",

'new': """\
| Desc. Enters a new node to the graph..
| Signature : new [name]
| Arguments :
    1. Name : The complete name of the new entry.
| Usage examples :
    new Carlo Magno\
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

'grabbed': """\
| Desc. Enters a session for editing the grabbed nodes.
| Signature : grabbed
| Arguments : None
| Usage examples :
    grabbed\
""",

'run': """\
| Desc. Runs a density search on the grabbed nodes set.
| Signature : run [-f] [-d] [-r] [-p <lim>] [-w <width=35>] [-a <lim>] [-c <ncol=4>]
| Arguments :
    -f, --fielding  Restricts the search to results within the placeholder fielding.
    -l, --lang      Restricts the search to results of the lang (non-persistent).
    -t, --type      Restricts the search to results of the type (non-persistent).
    -d, --details   Single-column data & field sizes.
    -r, --shuffle   Randomize the display order (by default, alphabetical is applied).
    -p, --stop      Limit the number of results.
    (*) -w, --width     Max allowed width for column (absolute).
    (*) -a, --abbr      Max allowed character length for names.
    (*) -c, --ncol      Number of columns.
    Note : the starred flags (*) only apply if '--details' isn't flagged.
| Usage examples :
    run
    run -f
    run -d -t 15 -r
    run -w 50 -a 5 -c 1
    run -l es
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
