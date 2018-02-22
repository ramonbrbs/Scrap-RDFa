# -*- coding: utf-8 -*-
import sys
#import urllib.parse
from robobrowser import RoboBrowser
from settings import *

vetor_links = []
url_pagina_inicial = PAGINA_INICIAL

def url_navegavel(url):
    
    global url_pagina_inicial

    if(not url.startswith("http")):
        return url_pagina_inicial+ "/" + url

    return url

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
    browser = RoboBrowser()
    try:
        browser.open(url_navegavel(url))
        
        links = browser.select('a')
        
        for link in links:
           if(link.has_attr('href') and valida_url(link['href'])):
               vetor_links.append(link['href'])
    except:
        print("erro")
        e = sys.exc_info()[0]
        print(e)


captura(url_pagina_inicial)
