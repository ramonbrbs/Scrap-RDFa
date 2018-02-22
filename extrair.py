from pyRdfa import pyRdfa
from pyRdfa.options import Options
import requests
import io
from rdflib import Graph


def extrair_rdfa(url):
    options = Options(embedded_rdf=True)
    #r = requests.get(url)
    #print pyRdfa(options=options).rdf_from_source(url,outputFormat='pretty-xml')
    g1= pyRdfa(options=options).rdf_from_source(url,outputFormat='pretty-xml')
    #print g1#g2 = pyRdfa(options=options).rdf_from_source('http://rbarbosa.me/ex.html',outputFormat='pretty-xml')
    g = Graph()
    g.parse(io.BytesIO(g1))
    return g
    #g.parse(io.BytesIO(g2))
    #f = open('teste2.rdf', 'w')
    #resultado =  g.serialize(format='xml')
    #f.write(resultado)
