import datetime

# Little explanation
# The code run is the one in RUN(G) function.
# Flags below decide what snippet to run.
# > py -i main.py to run

# [!] Si decides deployearlo y camibar direcotrios y cosas recuerda que el comando 'term' se alimenta de 
# los objetos G y Node, asegurate de que siga pudiendo tener acceso a ellos (que a lo mejor va implicito
# con el hecho de estar en ese fichero ya, claro)


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


test_CLI = True

#########################################################
test_skcomponents = test_CLI==False
import sys 
def run(G):
    if test_CLI:
        cli = SK_Interface(G)
        cli.cmdloop() # executes cmdqueue and leaves terminal ready
    if test_skcomponents:
        pass

        # size_o = len(G)
        # n_conn_o = sum([len(n._get_raw_content()) for n in G])
        # print(size_o, n_conn_o)

        # G_names = [n.name for n in G]
        # c = 0
        # for line in s.split('\n'):
        #     c +=1
        #     if c%400==0:
        #         G.save(f'data_{c}.txt')

        #     parts = line.split('|')
        #     name = parts[0]

        #     print(name)

        #     n = None

        #     if name not in G_names:
        #         # Si no está creado
        #         n = G.create_node('es', 'k', name, 'NA')
        #         print('¡¡¡¡¡Created new!!!!')
        #     elif name in G_names:
        #         ns = G.select(lang='es', name=name)
        #         if len(ns)==1:
        #             n = ns[0]
        #         else:
        #             continue
            
        #     if n:
        #         syns = parts[6].split('/')
        #         if syns not in [[],['']]:
        #             for syn in syns:
        #                 syn = G.select(lang='es', name=syn)
        #                 if len(syn)==1:
        #                     syn = syn[0]
        #                 else:
        #                     continue
        #                 G.bind(n, syn, 'y1')
     
                
        #         sems = parts[9].split('/')
        #         if sems not in [[],['']]:
        #             for sem in sems:
        #                 sem = G.select(lang='es', name=sem)
        #                 if len(sem)==1:
        #                     sem = sem[0]
        #                 else:
        #                     continue
        #                 G.bind(n, sem, 'e1')
        
        # file.close()

        # for line in s.split('\n'):
        #     bs = line.split('|')

        #     for i in range(len(bs)):
        #         for j in range(len(bs)):
        #             if j <= i:
        #                 continue
        #             name_a = bs[i]
        #             name_b = bs[j]
        #             na = G.create_node('es', 'b', name_a, 'NA')
        #             nb = G.create_node('es', 'b', name_b, 'NA')

        #             G.bind(na, nb, 'y1')

        # pairs = []
        # cache = []
        # for line in s.split('\n'):
        #     line = line.strip()
        #     if line:
        #         pos_space = line.find(' ')
        #         line = line[pos_space+1:]
        #         cache.append(line)
        #         if len(cache)==2:
        #             pairs.append((cache[0], cache[1]))
        #             cache = []
        # for pair in pairs:

        #     na_name, nb_name = pair # if does not exist, creates it (and gets it)

        #     na = G.create_node('es', 'r', na_name, 'NA') # if does not exist, creates it (and gets it)
        #     nb = G.create_node('es', 'r', nb_name, 'NA') # if does not exist, creates it (and gets it)

        #     G.bind(na, nb, 'y1')
        
        # class entry:
        #     def __init__(self, string):
        #         self.name = string[:-3]
        #         self.type = string[-3:]

        # for line in s.split('\n'):

        #     line = line.split('|')
        #     if line != ['']:
        #         id = entry(line[0])
        #         syns = [entry(n) for n in line[1].split('/')]
        #         sems = [entry(n) for n in line[2].split('/')]
        #         exs = line[3].split('/')   

        #         #print()
        #         #print(f'@id.name={id.name}|n_syns={len(syns)};n_sems={len(sems)}')
            
        #         matches = G.select(name=id.name)
        #         if len(matches)==0:
        #             G.create_node('es', id.type, id.name, 'NA')
        #             print('Created '+id.name)
        #             na = G.find(name=id.name)
        #         elif len(matches)==1:
        #             na = matches[0]

        #         for ex in exs:
        #             if ex not in na.examples and ex.strip() != '':
        #                 na.examples.append(ex)
        #                 print(f'Added {ex} to {na}')
   
        #         for syn in syns:
        #             nb = G.select(name=syn.name)
        #             #print(f"¿Is '{nb}' True or False? Lets see it...")
        #             if nb:
        #                 nb = nb[0]
        #                 if nb not in na.get_neighbors('y'):
        #                     G.bind(na, nb, 'y1')
        #                     print(f'Binded {na._convert_header_to_compact_format()} to {nb._convert_header_to_compact_format()}.')
        #                 else:
        #                     a = 0
        #                     #print(f"{nb} was already in {na}.")
        #             else:
        #                 a = 0
        #                 #print(f'{syn.name} arised no results at G :(')

        #         for sem in sems:
        #             nb = G.select(name=sem.name)
        #             if nb:
        #                 nb = nb[0]
        #                 if nb not in na.get_neighbors('e'):
        #                     G.bind(na, nb, 'e1')
        #                     print(f'Binded {na._convert_header_to_compact_format()} to {nb._convert_header_to_compact_format()}.')
        #                 else:
        #                     a = 0
        #                     #print(f"{nb} was already in {na}.")
        #             else:
        #                 a = 0
        #                 #print(f'{syn.name} arised no results at G :(')   




        # for line in s.split('\n'):
        #     line = line[8:]
        #     parts = line.split('|')
        #     name = parts[0]
        #     sems = parts[-1].split('/')
        #     if sems != ['']:

        #         G.create_node('es', 'r', name, 'NA')
        #         na = G.find(lang='es', type='r', name=name, lemma='NA')
        #         for sem in sems:
        #             try:
        #                 matches = G.select(name=sem)
        #                 if len(matches)==1:
        #                     nb = matches[0]
        #                     G.bind(na, nb, 'e1')
        #             except:
        #                 print(name, sem)

        # size_f = len(G)
        # n_conn_f = sum([len(n._get_raw_content()) for n in G])
        # print(size_f, n_conn_f)

        # G.save('data_f.txt')

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