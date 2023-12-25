from skgraph import Graph
from sknode import Node
from sknodeset import NodeSet
from graph_funcs import *

G = Graph('data.txt')

n1 = G.find('Persona')
n2 = G.find('Individuo')

for _ in range(100):
    print(intersect(*NodeSet([G.random(),G.random()])))
