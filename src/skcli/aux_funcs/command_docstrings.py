from typing import Dict

# I HAVE TO CREATE 4 DICTIONNARIES, EACH FOR CLI 
# - one for SCKLI
# 3 others for CreateNode, SelectNode, LS_on_node jajaja ok¿?
# Para que siempre puede implementarse el do_help de una forma u otra.
# Ya sea en comandos o en general para devolver un mensaje informativo.
# Y al dividir los comandos en diccionarios me aseguro de que no se pisan
# algunas definiciones, que hay comandos de mismo nombre pero con behaviors
# distintas entre CLIs.


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

'mv': """\
| Desc. Moves bindings to a different field.
| Signature : mv <*index> <*field>
| Arguments :
    1. <*index>  One or more indexes representing connections to be relocated.
    2. <*field>  The field(s) to which the connections are intended to be reconnected.
| Usage examples :
    mv 50 12 13 14 y0 y1 
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
| Technical notes :
    N1. If the node is not found on the current PlaceHolder scope, the method
    progressively  broadens the search criteria for nodes by first using the
    current language and type, then only the language, then only the type, and
    finally neither, if more specific searches yield no results.\
""",

'r': """\
| Desc. Performs a random node search with optional language and type constraints.
| Signature : r [-l <lang>] [-t <type>] [-f]
| Arguments :
    -l, --lang  Specify the language to narrow down the search.
    -t, --type  Specify the type to narrow down the search.
    -f, --fav   Specify wether the output must be favorite or not.
| Usage examples :
    r
    r -l en -t n\
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
