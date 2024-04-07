# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 18:00:32 2024

@author: Marta
"""


preguntas = ['¿Cómo te llamas?', '¿Cuántos años tienes?', '¿Cuándo es tu cumpleaños?']
i = 0

def siguientePregunta(AnteriorRespuesta):
    global i 
    siguiente_pregunta = preguntas[i]
    i = i + 1
    return siguiente_pregunta