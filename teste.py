from extrair import *
import io
from rdflib import Graph
from merge import *

g1 = extrair_rdfa('http://rbarbosa.me/ex3.html')
g2 = extrair_rdfa('http://rbarbosa.me/ex.html')
g3 = merge_graphs(g1,g2)
print g3.serialize(format='xml')