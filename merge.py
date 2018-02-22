from rdflib import Graph
import io

def merge_graphs(g1,g2):
    g = Graph()
    xml1 = g1.serialize(format='xml')
    xml2 = g2.serialize(format='xml')
    g.parse(io.BytesIO(xml1))
    g.parse(io.BytesIO(xml2))
    #print g.serialize(format='xml')
    return g