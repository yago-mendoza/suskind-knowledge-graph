import datetime

"""
Another launchpad.
"""

def create_graph(directory, filename, encoding):
    data_file_path = os.path.join(os.path.dirname(__file__), directory, filename)
    data_file_path = os.path.normpath(data_file_path)
    return Graph(data_file_path, encoding=encoding)
    
if __name__ == '__main__':
    # Pasamos todas las ejecuciones por este punto de entrada
    # para evitar poner la línea de modificación del path
    # en cada archivo.
    from src.sk.skcomponents.sknode import Node
    from src.sk.skcomponents.sknodeset import NodeSet
    from src.sk.skcomponents.skgraph import Graph
    from src.sk.skcomponents.search_algorithms import *
    from src.sk.skcli.SKCLI import *
    import sk.sktools as sk
    from src.sk.skcli.aux_funcs.command_docstrings import *
    g = create_graph('.', 'data_1.txt', 'latin1')
    G = create_graph('.', 'data.txt', 'utf8')
    i=0
    for node in G:
        i+=1
        if i%100==0:
            print(i)
        nodeset = g.select(name=node.name)
        if nodeset:
            node.examples = nodeset[0].examples
    G.save(f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt")

