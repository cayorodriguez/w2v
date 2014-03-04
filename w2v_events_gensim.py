#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append('.')
#from optparse import OptionParser
import sys
#import ewnlex
#lex = ewnlex.Lexicon()
#lex.load('wn_es_utf8.pickle')
sys.path.append("./python_libs")
import parse_Apertiums
from gensim.models import *
import cPickle

#lista de sustantivos en ES generada a partir del lemario de casi un millón de formas
WRDS = cPickle.load(open('./pos/lemmas_es.xml.bin'))

#Carga del modelo vectorial
model = Word2Vec.load_word2vec_format("./models/all_es.vectors.bin", binary=True)


#Generación de un diccionario de sustantivos eventivos (con sus categorias) a partir de las listas de Jordi
events = {}
for x in open("./eventos/noun.formes.txt").readlines():
    if x.split()[1] != 'none':
        events[x.split()[0]] = x.split()[1]
noneventos = [x.split()[0] for x in open("./eventos/noun.lemes.txt").readlines() if (x.split()[1] == 'none')]

#Cogemos cada evento y buscamos expandir con aquellos que son similares en el modelo vectorial (Paso 1), que NO aparecen como non-events en nuestro corpus (Paso 2), y que aparecen en nuestra lista de sustantivos (Paso 3). Le asignamos la misma categoria que el original en el paso 4
expanded = {}

for e in events.keys():
    expanded[e] = {}
    newlist = []
    #paso 1
    m = model.most_similar(positive=[e],topn=20)
    for l in m:
        if l[0] in noneventos:#Paso 2
            pass
        if l[0] in WRDS:#Paso 3
            newlist.append(l)
        else:
            pass
    expanded[e] = (events[e],newlist)#Paso 4


# Dado el nivel de ruido que mete WordNet, quitamos esta expansión adicional
## for e in expanded.keys():
##     syns = lex.synonyms(e,partsos='n')
##     new_list = []
##     old_list = expanded[e][-1]
##     if syns:
##         ya_listado = [y[0] for y in old_list]
##         for w in syns:
##             if w[0] in ya_listado:
##                 pass
##             else:
##                 if w[1] == 'n':
##                     old_list.append((w[0],0.9999)) 
##         expanded[e] = (expanded[e][0],old_list)

for e in expanded.keys():
    try:
        print "*"*40
        lista = expanded[e]
        print e,'\t',lista[0]
        print "_"*40
        for v in lista[-1]:
            print v[0],'\t',lista[0],'\t',v[-1]
    except keyError:
        print "---->",e
