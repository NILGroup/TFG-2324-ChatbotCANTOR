# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 18:55:55 2024

@author: Marta
"""

import json

class Pregunta:
    def __init__(self, enunciado, campos):
        self.enunciado = enunciado
        self.respuesta = ""
        self.campos = {key: False for key in campos}
        self.preguntasExtra = []
        self.extra = {key: False for key in campos}
        self.respuestasExtra = {}
        self.pasar = False
    
    def pasarSiguiente(self):
        self.pasarSiguiente = True

    def actualizar_respuesta(self, nueva_respuesta):
        self.respuesta = nueva_respuesta

    def actualizar_campo(self, nombre_campo, valor):
        self.campos[nombre_campo] = valor

    def eliminarPreguntasExtra(self, preguntas):
        self.preguntasExtra.pop(0)
    
    def agregar_respuesta_extra(self, pregunta_extra, respuesta_extra):
        self.respuestasExtra[pregunta_extra] = respuesta_extra

    def marcarGeneradasExtra(self,campo):
        self.extra[campo] = True
        
    def __str__(self):
        representacion = f"Enunciado: {self.enunciado}\n"
        representacion += f"Respuesta: {self.respuesta}\n"
        representacion += f"Campos: {self.campos}\n"
        representacion += f"Preguntas Extra: {self.preguntasExtra}\n"
        representacion += f"Extra: {self.extra}\n"
        representacion += f"Respuestas Extra: {self.respuestasExtra}\n"
        return representacion

