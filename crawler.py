# -*- coding: utf-8 -*-
import sys, traceback
from robobrowser import RoboBrowser
from settings import *
from rdflib import Graph
from merge import *
from extrair import *
import time
import re 

vetor_links = [] #vetor dos links para visitas
visitados_links = [] #vetor dos links visitados
url_pagina_inicial = PAGINA_INICIAL
vetor_links.append(url_pagina_inicial)
grafo = Graph() #grafo para uso do rdflib

#verifica se a url é navegável (não é javascript ou "#" etc..)
def url_navegavel(url):
    global url_pagina_inicial

    if(not url.startswith("http")):
        return url_pagina_inicial+ "/" + url

    return url

#muda urls relativas para urls absolutas
def corrige_url(url,urlbase):
    posicoes = [m.start() for m in re.finditer('/', urlbase)] #pega todas as posições de '/' na url base
    root = urlbase[:posicoes[3]] #define a url root (até a terceira barra ex: http://ex.com/)
    
    if(url.startswith("http")): #se o link começa com http já é absoluto
        return url
    if(url.startswith("/")): #se começa com / é um link para o root
        return root + "/" + url

    return urlbase[:urlbase.rfind('/')]+"/" + url #scaso contrário é um link par ao mesmo diretório

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

def captura(url): #metodo para acessar uma url e capturar informações
    global vetor_links
    global visitados_links
    global grafo

    print('-----' + url + '-------')

    visitados_links.append(url) #adiciona a url atual no vetor de visitados
    vetor_links.remove(url) #remove a url do vetor de "para visitar"
    browser = RoboBrowser()
    
    try:
        browser.open(url_navegavel(url)) #abre a url
        print("++++" + url_navegavel(url) + "+++")
        if(browser.response.status_code != 200): #verifica se o servidor respondeu ok
            return
        
        
        
        g = extrair_rdfa(url)
        
        grafo = merge_graphs(grafo,g) #chama a função de junção de grafos
        links = browser.select('a') #seleciona as tags 'a' da página
        
        for link in links: #varre os links, corrige e adiciona ao vetor de 'para visitar'
            if(link.has_attr('href') and valida_url(link['href'])):
                if corrige_url(link['href'], url) not in vetor_links and corrige_url(link['href'], url) not in visitados_links:
                    vetor_links.append(corrige_url(link['href'], url))
                
    except:
        print("erro")
        e = sys.exc_info()[0]
        traceback.print_exc(file=sys.stdout)
        print(e)


def iniciar(url):
    global PAGINA_INICIAL
    PAGINA_INICIAL = url
    while len(vetor_links) != 0: #enquanto existirem urls no vetor de para visitar..
        captura(vetor_links[0])
    timestamp = (int)(time.time())
    f = open((str)(timestamp) + '.rdf', 'w')
    resultado =  grafo.serialize(format='xml') #transforma o grafo em rdf
    f.write(resultado)
    return f.name

if __name__ == "__main__":
    iniciar()

