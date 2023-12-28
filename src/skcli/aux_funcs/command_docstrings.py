from typing import Dict

COMMAND_DOCSTRINGS : Dict[str, str] = {
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

'r': """\
| Desc. Performs a random node search with optional language and type constraints.
| Signature : r [-l LANG] [-t TYPE] [-f FAVORITE]
| Arguments :
    -l, --lang LANG     Specify the language to narrow down the search.
    -t, --type TYPE     Specify the type to narrow down the search.
    -f, --fav FAVORITE  Specify wether the output must be favorite or not.
| Usage examples :
    r
    r -l en -t n\
""",

'summary': """\
| Desc. Provides a quick summary of the current node's connections.
| Signature : summary
""",

'ls': """\
| Desc. Lists detailed information about the current node, including its neighbors and relevant properties.
| Signature : ls
""",

'set': """\
| Desc. Sets or adds properties to the current node or environment.
| Signature : set <*settings>
| Arguments :
  <!> Supports shorthand for groups and individual settings.
    1. <*settings>
              "y/e"  Add all 'y' or 'e' prefixed fields (e.g., y0, y1, y2).
            "y_/e_"  Add specific fields (e.g., y0 y1)
        "es/fr/..."  Set the node language for the PlaceHolder.
        "n/j/v/..."  Set the node type for the PlaceHolder.
| Usage examples :
    set y
    set y0 e1
    set en j y0 e2\
"""
}
