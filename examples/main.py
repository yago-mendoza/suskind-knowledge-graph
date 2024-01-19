import datetime

# Little explanation
# The code run is the one in RUN(G) function.
# Flags below decide what snippet to run.
# > py -i main.py to run

test_CLI = True
test_skcomponents = False

#########################################################
import sys 
def run(G):
    if test_CLI:
        cli = PrimaryInterface(G)
        cli.cmdloop() # executes cmdqueue and leaves terminal ready
    if test_skcomponents:
        pass

#########################################################

def create_graph():
    data_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'data.txt')
    data_file_path = os.path.normpath(data_file_path)
    return Graph(data_file_path)
    
if __name__ == '__main__':
    # Pasamos todas las ejecuciones por este punto de entrada
    # para evitar poner la línea de modificación del path
    # en cada archivo.
    import sys, os
    sys.path.append(r'G:\Mi unidad\GATEWAY\[01] Dev\[01] Python\[01] Suskind\suskind-knowledge-graph')
    from src.skcomponents.sknode import Node
    from src.skcomponents.sknodeset import NodeSet
    from src.skcomponents.skgraph import Graph
    from src.skcomponents.search_algorithms import *
    from src.skcli.SKCLI import *
    from src.skcli.aux_funcs.command_docstrings import *
    G = create_graph()
    run(G)

