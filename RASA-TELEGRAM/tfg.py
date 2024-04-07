# -*- coding: utf-8 -*-

#!pip install -q -U google-generativeai
#pip install google

"""A continuación, importamos los paquetes necesarios."""

import pathlib
import textwrap
import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

import json
import sys

import re

from config import *
#Configuración: cargamos la API KEY y instalamos el modelo 
#pip install google
import pregunta

genai.configure(api_key=GEMINI_TOKEN)

model = genai.GenerativeModel('gemini-pro')

def cargar_json(d_json):
  try:
    while '{' in d_json:
      indice_inicio = d_json.find('{') + 1
      d_json = d_json[indice_inicio:]
    if '}' in d_json:
      indice_fin = d_json.find('}')
    d_json = d_json[:indice_fin]
    return "{"+d_json+"}"
    try: 
        return json.loads("{"+d_json+"}")
    except:
        lista = d_json.split(',')
    
        j = {}
        for par in lista:
          desglose = par.split(':')
          clave = desglose[0].strip().strip("''").strip('""')
          j[clave] = desglose[1].strip().strip("''").strip('""')
        return j
  except IndexError:
    print("cargar_json:Error al generar el json")

def generate_json(pregunta,respuesta,datos):
  try:
      prompt = f"He preguntado a un usuario {pregunta}, y me ha respondido {respuesta}. Quiero que me ayudes a rellenar un json con los siguientes datos: {datos}. Rellenados con los valores apropiados según la respuesta." 
      prompt += "Quiero que vengan en formato json donde la clave sea el nombre del dato y el valor la información que has podido obtener en la respuesta de ese campo, en formato de lista. Es decir una lista de strings, donde cada string sea una información obtenida asociada a ese campo. En caso de que no se haya podido obtener ninguna información de un campo quiero que el valor asociado a la clave de ese dato sea una lista con un único string que sea No Encontrado"
    
      response = model.generate_content(prompt)
      
      while not response.candidates:
        response = model.generate_content(prompt)
      
      text = response.text
      text = re.search('{.*}', text, re.DOTALL).group()  # Quitar contenido fuera de los corchetes {}
      text = text.replace('\n', '').replace('\r', '')
    
      json_obj = cargar_json(text)
      return json.loads(str(json_obj))
  except AttributeError:
      print("Error en generate_json")

def generate_question(clave):
  prompt = f"Escribe preguntas dirigidas a una persona a la que estoy haciendo una entrevista personal. Quiero que las preguntas me ayuden a obtener información acerca del siguiente tema: {clave} "
  response = model.generate_content(prompt)
  while not response.candidates:
    response = model.generate_content(f"Generame varias preguntas que para hacer a alguien y saber más sobre él, quiero que las preguntas tengan que ver con {clave}")
  text = response.text
  patron = r'¿(.*?)\?'
  preguntas = re.findall(patron, text)
  return preguntas

def analizar_respuestaAux(pregunta,respuesta,clave):
  prompt = f"Tras preguntar {pregunta} en relacion con {clave} me han respondido {respuesta}. "
  prompt = prompt + f"Dada esa información, quiero que devuelvas cualquier información válida sobre {clave} y en caso de que no se haya podido obtener ninguna información válida, devolver No Encontrado"
  response = model.generate_content(prompt)
  return response.text


def analizar_extra(respuesta):
  prompt = f"A partir de este texto {respuesta}"
  prompt = prompt + f"Dada esa información, quiero que devuelvas 'si' en caso de que en la respuesta aparezca información útil que me ayude a conocer a una persona"
  response = model.generate_content(prompt)

  if 'si' in response.text or 'Sí' in response.text or 'sí' in response.text or 'Si' in response.text:

    prompt2 = f"Generame un json con el formato campo:información asociada a ese campo con la información que puedas obtener de esta respuesta {respuesta}"
    response = model.generate_content(prompt2)

    return cargar_json(response.text)
  else:
    return []

def analizar_respuesta(pregunta):
  keys = pregunta.campos.keys()
  data = generate_json(pregunta.enunciado,pregunta.respuesta,keys)
  extra = analizar_extra(pregunta)
  for clave,valor in data.items():
      pregunta.actualizar_campo(clave, valor)
  if extra != []:
      for clave,valor in extra.items():
          pregunta.actualizar_campo(clave, valor)
  for clave, valor in data.items():
    if "No Encontrado" in valor and pregunta.extra[clave]:#Si ya había generado preguntas extra para ese campo paso
        pregunta.marcarGeneradasExtra(clave)
        pregunta.añadirPreguntasExtra(generate_question(clave))
        return
  pregunta.pasarSiguiente()
        
preguntas = []

index = 0

def siguientePregunta(respuesta):
    
    global index
    
    if index == 0: #En el caso de que sea la primera vez aue llamo a esta función todavía no he hecho ninguna pregunta, será el saludo
        index = index + 1
        return preguntas[1].enunciado 
    
    preguntas[index].actualizar_respuesta = respuesta
    analizar_respuesta(preguntas[index])
    if preguntas[index].pasar or len(preguntas[index].preguntasExtra) == 0:
        if index != (len(preguntas)-1):
            index = index + 1
            return preguntas[index].enunciado
        else:
            return "Muchas gracias por la información"
    else:
        pregunta = preguntas[index].preguntasExtra[0]
        preguntas[index].eliminarPreguntasExtra()
        return pregunta
    

def cargar_preguntas():
    global preguntas
    with open("preguntas.txt", "r",encoding="utf-8") as archivo:
        
        for linea in archivo:
           
            partes = linea.strip().split(" : ")
            if len(partes) == 2:
                enunciado = partes[0]
                campos = partes[1].strip('[]').split(",")
                p = pregunta.Pregunta(enunciado, campos)
                preguntas.append(p)
    return preguntas

