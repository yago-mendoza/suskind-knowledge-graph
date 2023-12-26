def run(G):
    cli = PrimaryInterface(G)
    cli.cmdloop()

###

def create_graph():
    data_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'data.txt')
    data_file_path = os.path.normpath(data_file_path)
    return Graph(data_file_path)
    
if __name__ == '__main__':
    # Pasamos todas las ejecuciones por este punto de entrada
    # para evitar poner la línea de modificación del path
    # en cada archivo.
    import sys, os
    sys.path.append(r'G:\Mi unidad\GATEWAY\[03] Dev\[04] On-going projects\[03] Suskind\suskind-knowledge-graph')
    from src.skcomponents.sknode import Node
    from src.skcomponents.sknodeset import NodeSet
    from src.skcomponents.skgraph import Graph
    from src.skcomponents.search_algorithms import *
    from src.skcli.test_cli import *
    from src.skcli.command_docstrings import *
    G = create_graph()
    run(G)

