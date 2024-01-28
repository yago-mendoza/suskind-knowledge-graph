import datetime

# Little explanation
# The code run is the one in RUN(G) function.
# Flags below decide what snippet to run.
# > py -i main.py to run



# Tienes que poner bien el código, ver qué funciona, qué 
# enllestir, qué todavía no, etcetera. Buenas practicas, esas cosas.
# Te recomiendo que empieces generalizando la función get_neighbors
# tanto como puedas. Y luego pases nivel a nivel, hacia arriba,
# hasta ir optimizando cosas de las interfaces.
# Deacuerdo¿?
# Ah, y las funciones '?' funcionan bastante bien...
#   pero aveces pone ARGS y deberia poner FLAGS en docstrings, y esas cosas
# Asegurate de lograr un formato estandarizado de '|', '()', 'SYS:', 'nothin', 'warnigns, etc. 
# A veces para los do_X, poner flags raras los rompe. Es porque se tiene
# que parsear con una funcion distinta, creo que la uso bien en do_ls. Asi flags unknown
# no reomperán el hilo de ejecución.
# 
# Pidele ayuda a ChatGPT

# contexto.
# SKCLI es la top.
# Luego NEW_ y LS_ Interfaces se triggerean con 'new' y con 'ls'(with single field scoped)
# El Select está estandarizado, kinda, pero a lo mejor se puede estandarizar más.

# OH! AAAND dont worry about the sec copies being created at 'examples' when I run the code.
# Its just for security. The 'save' feature will be arranged the last of all,
# since will depend on the actual configuration of the files, and I'll probably need help for that yikes


test_CLI = False

#########################################################
test_skcomponents = test_CLI==False
import sys 
def run(G):
    if test_CLI:
        cli = SK_Interface(G)
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
    import src.sktools as sk
    from src.skcli.aux_funcs.command_docstrings import *
    G = create_graph()
    run(G)

