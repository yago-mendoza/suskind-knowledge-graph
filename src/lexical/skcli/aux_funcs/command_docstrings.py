from typing import Dict

COMMAND_DOCSTRINGS_GB : Dict[str, str] = {
'tag': """\
| Desc. Adds a new node.
| Signature : tag <name>
| Arguments :
    1. <name>  The name of the node to be tagged.
| Usage examples :
    tag Augusto César\
""",

'ls': """\
| Desc. Refreshes the tagged nodes list in screen.
| Signature : ls\
""",

'expand': """\
| Desc. Performs a deterministic adaptive search to find relevant nodes based on tagged nodes.
| Signature : expand <target_results> <sample_size> <max_depth> [fields] [--complete_depth] [--only_new_centrality]
| Arguments :
    <target_results>    Desired number of results (integer).
    <sample_size>       Number of top central nodes to consider in each iteration (integer).
    <max_depth>         Maximum depth for search (integer).
    [type]              Type of nodes to be returned as a set (--type, -t)
    [fields]            Optional. Comma-separated list of fields to consider (default: all fields).
    --complete_depth    Optional. If set, the search will complete all iterations up to max_depth before
                        returning results, even if target_results is reached.
    --only_new_centrality   Optional. If set, centrality will be calculated only for newly found nodes in
                            each iteration, not including previously found nodes.
| Usage examples :
    expand 20 5 3 (most preferable)
    expand 20 5 3 -t n
    expand 30 5 5 y, e
    expand 40 3 6 y --only_new_centrality
    expand 50 3 5 e --complete_depth --only_new_centrality
| Notes :
    - The search starts with the currently tagged nodes.
    - Results are sorted by centrality score in descending order.
    - The search may stop early if no new nodes are found or if target_results is reached
    (unless --complete_depth is used).
    - A detailed search report is provided, showing progress at each depth level.
    - [NEW] tags in the results indicate nodes that were not in the original tagged set.
| Output :
    - Displays a list of found nodes, their centrality scores, and a visual representation
    of their centrality.
    - Provides a search report detailing the number of new connections and added nodes
    at each depth level.
    - Shows the total number of results and new additions.\
""",

'del': """\
| Desc. Removes the given nodes(s).
| Signature : rm <*index>
| Arguments :
    1. <*index>  As many indexes as connections to be unbinded.
| Usage examples :
    del 4-15
    del 1 2 3\
""",

'clear': """\
| Desc. Clears all node within the tagged list.
| Signature : clear\
""",


}

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

'tag': """\
| Desc. Tags the given nodes(s).
| Signature : tag [<*index>]
| Arguments :
    1. <*index>  As many indexes as connections to be tagged. If none, tags them all.
| Usage examples :
    tag
    tag 1 22 13 55\
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

'rtag': """\
| Desc. Tags <n> random nodes to tagged.
| Signature : rtag <n>\
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
| Signature : ls [<y_/e_>] [-d] [-r]
|                         [-p <lim>] [-w <width=35>] [-a <lim>] [-c <ncol=4>]
|                         [-l <lang>] [-t <type>]
| Arguments :
    <name>   Can automatically switch to a given node.
    <y/e_>   Can automatically switch to a given field.
     |
    -l, --lang      Restricts the search to results of the lang (persistent across comands).
    -t, --type      Restricts the search to results of the type (persistent across comands).
     |
    -d, --details   Single-column data & field sizes.
    -r, --shuffle   Randomize 'X' given results.
    -p, --stop      Limit the number of results.
    (*) -w, --width     Max allowed width for column (absolute).
    (*) -a, --abbr      Max allowed character length for names.
    (*) -c, --ncol      Number of columns.
    Note : the starred flags (*) only apply if '--details' isn't flagged.
| Usage examples :
    ls Mano
    ls y0
    ls -r 5
    ls -t j
    ls -c 3
    ...\
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

'vg': """\
| Desc. Shows the examples for the node, hence accessing the VG pseudo-CLI.
| Signature : vg\
""",

'rvg': """\
| Desc. Prints a random introcued example.
| Signature : rvg <particle> --caps\
| Arguments :
    1. Particle : the string to be present.
    2. Caps : if we also want to match caps.
| Usage examples :
    rvg Año --caps
    rvg
    rvg Al
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

'tag': """\
| Desc. Tags the current node or a given one.
| Signature : tag [<name>]
| Arguments :
    1. name [opt] : name of the node the function will try to grasp.
| Usage examples :
    tag
    tag Augusto César\
""",

'tagged': """\
| Desc. Enters a session for editing the tagged nodes.
| Signature : tagged
| Arguments : None
| Usage examples :
    tagged\
""",

'run': """\
| Desc. Runs a density search on the tagged nodes set.
| Signature : run [-f] [-l <lang>] [-t <lang>] [-d] [-r] [-p <lim>] [-w <width=35>] [-a <lim>] [-c <ncol=4>]
| Arguments :
    -f, --fielding  Runs the search only traversing edges matching the current placeholder fielding.
     |
    -l, --lang      Restricts the search to results of the <lang> (non-persistent).
    -t, --type      Restricts the search to results of the <type> (non-persistent).
     |
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
