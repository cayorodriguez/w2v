#!/usr/bin/env python
# -*- coding: utf-8 -*-

class CONTok:
    """Class to create tokens with CONLLX-compliant features a partir del fichero original"""
    def __init__(self, line=None):
        self.ETIQUETAS = [u'form', u'postag', u'lemma', u'cpostag',  u'vform', u'tense',u'aspect', u'mood', u'event']
        for _tag in self.ETIQUETAS:
            setattr(self,_tag,None)
        if line:
            for n in range(len(line)):
                #_tag = self.ETIQUETAS[n]
                setattr(self,self.ETIQUETAS[n],line[n].split("=")[-1])
    #def __repr__(self):
    #    return self.tabIT()
    def convert(self,line):
        for n in range(len(line)):
            setattr(self,self.ETIQUETAS[n],line[n])

#Para leer más pitónicamente el corpus:
filein = "/home/carlos.rodriguez/Dropbox/events/events.sst"

lista = [[CONTok(x.split(" ")) for x in y.split("\t")[1:]] for y in open(filein).readlines()]
#for x in lista[1]:
#	print x.lemma,x.postag,x.event
## Según cs REPORTING
## publica vmip3s0 REPORTING
## hoy rg NONE

#Creo que lo único que necesitas es:

from gensim.models import *
import cPickle

#lista de sustantivos en ES generada a partir del lemario de casi un millón de formas
WRDS = cPickle.load(open('./pos/lemmas_es.xml.bin'))

#Carga del modelo vectorial
model = Word2Vec.load_word2vec_format("./models/all_es.vectors.bin", binary=True)

#para palabra 'e'. SI quieres también negativas, añades una lista negative=[]:
m = model.most_similar(positive=[e],topn=20)
# m es una lista de tuplos de palabras y sus indices de similitud
