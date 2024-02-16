import datetime

directory = 'data'
filename = 'data.txt'

# Little explanation
# The code run is the one in RUN(G) function.
# Flags below decide what snippet to run.
# > py -i main.py to run

test_CLI = False # True for CLI interaction
                # False for inserting nodes in batch from TXT/instructions(str) (line 24)

# [!] Saving DOES save at /gateway, but data.txt used to init SKCLI is that from /data.
# Need to move it at every 'save'.

#########################################################
database_expansion_mode = test_CLI==False
import sys 
def run(G):
    if test_CLI:
        SK_Interface(G).cmdloop()
    if database_expansion_mode:

        # print(sum([len(n._get_raw_content()) for n in G]))

        nodes = []

        already_visited = []
        c = 0
        for node in G:
            c+=1
            if c%300 == 0:
                print(c)
            if node not in already_visited:
                nodes.append('')
                nodes.append(node.name)
                already_visited.append(node)
                neighbors = node.get_neighbors('y')

                if node.examples:
                    for ex in node.examples:
                        if ex:
                            nodes.append('>>> '+ex)

                for neighbor in neighbors:
                    if neighbor not in already_visited:
                        nodes.append('    y: '+neighbor.name)

                        if neighbor.examples:
                            for ex in neighbor.examples:
                                if ex:
                                    nodes.append('    >>> '+ex)

                        already_visited.append(neighbor)
                neighbors = node.get_neighbors('e')
                for neighbor in neighbors:
                    if neighbor not in already_visited:
                        nodes.append('        e: '+neighbor.name)
                        already_visited.append(neighbor)

                        if neighbor.examples:
                            for ex in neighbor.examples:
                                if ex:
                                    nodes.append('        >>> '+ex)

        with open('amalgama.txt', 'w') as file:
            for node in G:
                file.write(node+'\n')

                


                





        # # Empellón 9   12
        # # Tripa 22   51
        # # Rojo 60 70
        # # Arañazo 11 28
        # # Cagar sangre 13 15
        # # Carne cruda 78 92
        # # Diástole 33 34

        # # Elimina el contenido 'e1' de los neighbors de 'target'
        # target = 'Sangre'
        # sangre = G.find(name=target)
        # L1 = sangre.semset1
        # L2 = {}
        # for n in L1:
        #     L2[n] = n.semset1
        
        # print([n.name for n in L1])

        # for i in L1:
        #     for j in L2[i]:
        #         G.unbind(i, j, 'semset1')
        # G.save(f'data_without_{target}_neighbors_content.txt')


        # print(sum([len(n._get_raw_content()) for n in G]))
            

        # Para eliminar conexiones repetidas
        # Per espurias


        pass

        # size_o = len(G)
        # n_conn_o = sum([len(n._get_raw_content()) for n in G]) / 2
        # print('#'*15)

        # instructions = """

        # """
        
        # lines = instructions.split('\n')
        # if lines[-1] == '':
        #     lines = lines[:-1]

        # # Initialize variables
        # nodes_to_create = []
        # bindings_to_process = []

        # for line in lines:

        #     line = line.strip()

        #     if not line:
        #         pass

        #     elif '/' in line or line.split(' ')[-1] in ['y0','y1','y2','e0','e1','e2']:
            
        #         targets, field = line.rsplit(' ', 1)
        #         target_names = targets.strip().split('/')
        #         bindings_to_process.append((node_name, target_names, field))

        #     elif ' ' in line and len(line.rsplit(' ',1)[-1]) == 1:  # Double space as a delimiter

        #         parts = line.rsplit(' ', 2)  # Split from the right to get the last two spaces as delimiters
        #         if len(parts) == 3:
        #             node_name, node_lang, node_type = parts
        #             nodes_to_create.append((node_lang, node_type, node_name))
        #         else:
        #             print(f"[!] Incorrect format for node creation: '{line}'")
        #             continue
            
        #     else:
        #         print(f"[!] Unrecognized or misplaced instruction: '{line}'.")
        

        # print()
        # print('Creation')
        # print()
        # # Assuming the existence of a graph object `G` and relevant methods for node creation and binding
        # for node_lang, node_type, node_name in nodes_to_create:
        #     # Create each node with its specified type
        #     G.create_node(node_lang, node_type, node_name, 'NA')  # Assuming 'NA' is a placeholder attribute
        #     print(f"Created node {node_lang}-{node_type}-{node_name}.")
        # print()
        # print('Binding')
        # print()
        # for principal_node_name, target_names, field in bindings_to_process:
        #     # Select the principal node
        #     principal_node_matches = G.select(name=principal_node_name)
        #     if len(principal_node_matches) == 1:
        #         principal_node = principal_node_matches[0]
        #         # Process each binding
        #         for target_name in target_names:
        #             target_matches = G.select(name=target_name)
        #             if len(target_matches) == 1:
        #                 target_node = target_matches[0]

        #                 if len(field) != 2:
        #                     print('[!] Uncorrect type set for {principal_node.name}')
        #                 else:
        #                     G.bind(principal_node, target_node, field)
        #                     print(f"'{target_node.name}' binded to '{principal_node.name}' through '{field}'.")
        #             else:
        #                 print(f"[!] Target node '{target_name}' has to be created first for binding.")
        #     else:
        #         print(f"[!] Principal node '{principal_node_name}' wasn't created or isn't unique.")
            
        # #     if n:
        # #         syns = parts[6].split('/')
        # #         if syns not in [[],['']]:
        # #             for syn in syns:
        # #                 syn = G.select(lang='es', name=syn)
        # #                 if len(syn)==1:
        # #                     syn = syn[0]
        # #                 else:
        # #                     continue
        # #                 G.bind(n, syn, 'y1')

        # size_f = len(G)
        # n_conn_f = sum([len(n._get_raw_content()) for n in G]) / 2
        # print()
        # print('#'*15)
        
        # print()
        # print(f'Node expansion: {round(100*(size_f-size_o)/size_o,6)}% ({size_o} to {size_f} nodes)')
        # print(f'Edge expansion: {round(100*(n_conn_f-n_conn_o)/n_conn_o,6)}% ({n_conn_o} to {n_conn_f} conn.)')

        # print()
        # G.save('data.txt')
        # print('[!] data.txt saved at /gateway.')
        # print('[!] Move to /data to update the database working at SKCLI.')

#########################################################

def create_graph():
    data_file_path = os.path.join(os.path.dirname(__file__), '..', directory, filename)
    data_file_path = os.path.normpath(data_file_path)
    return Graph(data_file_path)
    
if __name__ == '__main__':
    # Pasamos todas las ejecuciones por este punto de entrada
    # para evitar poner la línea de modificación del path
    # en cada archivo.
    import sys, os
    sys.path.append(r'G:\Mi unidad\[01] Dev\[01] Python\[01] Suskind\suskind-knowledge-graph')
    from src.skcomponents.sknode import Node
    from src.skcomponents.sknodeset import NodeSet
    from src.skcomponents.skgraph import Graph
    from src.skcomponents.search_algorithms import *
    from src.skcli.SKCLI import *
    import src.sktools as sk
    from src.skcli.aux_funcs.command_docstrings import *
    G = create_graph()
    run(G)