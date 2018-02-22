# -*- coding: utf-8 -*-
import sys, traceback
import tempfile
#import urllib.parse
from robobrowser import RoboBrowser
from settings import *
from rdflib import Graph
from merge import *
from extrair import *
import urllib
import io
import os

vetor_links = []
visitados_links = []
url_pagina_inicial = PAGINA_INICIAL
vetor_links.append(url_pagina_inicial)
grafo = Graph()

def url_navegavel(url):
    
    global url_pagina_inicial

    if(not url.startswith("http")):
        return url_pagina_inicial+ "/" + url

    return url

def corrige_url(url,urlbase):
    if(url.startswith("http")):
        return url
    if(url.startswith("/")):
        return urlbase[:urlbase.rfind('/')] + url
    return urlbase + url

def valida_url(url):
    global vetor_links
    #verfica se começa com http.. se começa verifica se o endereço inicial é do proprio site
    if(url.startswith('http') ):
        if(not url.startswith(url_pagina_inicial)):
            return False
    #verifica se  não é arquivo
    if(url.endswith(".jpg") or url.endswith(".png") or url.endswith(".jpeg") or url.endswith(".bmp") or url.endswith(".pdf") or url.endswith(".gif")):
        return False

    #verifica se já não está no vetor de links
    if(url in vetor_links ):
        return False

    #verifica se não começa com hashtag
    if(url.startswith("#")):
        return False

    #verifica se não é uma ação javascrit
    if(url.startswith('javascript')):
        return False

    #verifica se não é link para email
    if(url.startswith('mailto:')):
        return False

    if(url == '/'):
        return False
    
    return True

def captura(url):
    global vetor_links
    global visitados_links
    global grafo
    print('-----' + url + '-------')
    visitados_links.append(url)
    vetor_links.remove(url)
    browser = RoboBrowser()
    
    try:
        browser.open(url_navegavel(url))
        print("++++" + url_navegavel(url) + "+++")
        if(browser.response.status_code != 200):
            return
        
        
        ff = open('r.html', 'w')
        ff.write(browser.parsed.encode('utf-8'))
        ff.close()
        g = extrair_rdfa(ff)
        os.remove(ff.name)
        grafo = merge_graphs(grafo,g)
        links = browser.select('a')
        
        for link in links:
            if(link.has_attr('href') and valida_url(link['href'])):
                if corrige_url(link['href'], url) not in vetor_links and corrige_url(link['href'], url) not in visitados_links:
                    vetor_links.append(corrige_url(link['href'], url))
                
    except:
        print("erro")
        e = sys.exc_info()[0]
        traceback.print_exc(file=sys.stdout)
        print(e)


while len(vetor_links) != 0:
    captura(vetor_links[0])

f = open('teste2.rdf', 'w')
resultado =  grafo.serialize(format='xml')
f.write(resultado)