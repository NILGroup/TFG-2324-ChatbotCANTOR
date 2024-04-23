# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 16:28:49 2024

@author: Marta
"""

import nltk 
sentence = "La terapia de reminiscencia hace uso de eventos de la vida haciendo que los participantes recuerden vocalmente recuerdos episódicos de su pasado."
tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens)
tagged[0:6]
