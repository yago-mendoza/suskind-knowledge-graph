import datetime

"""
This file was created because I accidentally introduced strange characters into the latest data version. Now, I need to compare the entries with those in a previous version, which still contains correct integer data, to check for and recover the correct spelling of names. This file can also be used as a launchpad for any other changes to the database that require multiple lines.
"""

def create_graph(directory, filename):
    data_file_path = os.path.join(os.path.dirname(__file__), directory, filename)
    data_file_path = os.path.normpath(data_file_path)
    return Graph(data_file_path)
    
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
    g = create_graph('.', 'data_1.txt')
    G = create_graph('.', 'data_2.txt')
    c = 0
    non_special_twins = []

    for node in G:
        if "ï¿½" in node.name:
            c += 1

            print(f"Corrupted entry name: {node.name}")
            name = node.name.replace("ï¿½", "")
            print(f"Lacerated entry name: {name}")
            twins = sk.find_similars(g, name, k=5)

            # Buscar el primer twin con un carácter especial
            twin = None
            for twin_candidate in twins:
                if any(ord(char) > 127 for char in twin_candidate.name):
                    twin = twin_candidate
                    break

            # Si no encuentra un twin con carácter especial, almacenar en la lista
            if twin is None:
                non_special_twins.append(node)
                print('#\n#\n#\nERROR. NO MATCH FOUND.#\n#\n#')
            else:
                print(f"Similar match found:  {twin.name}")
                print('_'*40)
                G.select(name=node.name)[0].edit(name=twin.name)

            # Guardar el archivo cada 400 iteraciones
            if c % 400 == 0:
                G.save(f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt")
        
    G.save(f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt")

    # Imprimir nodos que no encontraron un twin con carácter especial
    if non_special_twins:
        print("Nodes without special character matches:")
        for ns_twin in non_special_twins:
            print(ns_twin.name)




    