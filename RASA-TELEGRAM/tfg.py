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

def generate_json(p):
  try:
      pregunta = p.enunciado
      respuesta = p.respuesta
      datos = list(p.campos.keys())
     
      prompt = f"Podrías, a partir de esta respuesta {respuesta} y partiendo de la siguiente pregunta {pregunta}, rellenarme si es posible estos datos {datos}" + "Quiero que vengan en formato json donde la clave sea el nombre del dato y el valor la información que has podido obtener en la respuesta de ese campo, en formato de lista. Es decir una lista de strings, donde cada string sea una información obtenida asociada a ese campo."
      prompt = prompt + "Si no has podido encontrar una respuesta, rellena el json con el valor 'No Encontrado'"

      response = model.generate_content(prompt)
      
      while not response.candidates:
        response = model.generate_content(prompt)
      
      text = response.text
      text = re.search('{.*}', text, re.DOTALL).group()  # Quitar contenido fuera de los corchetes {}
      text = text.replace('\n', '').replace('\r', '')
    
      json_obj = cargar_json(text)
      return json.loads(str(json_obj))
  except AttributeError:
      print(f"generate_json error: json_obj es {response.text}")
      return "return"

def generate_question(clave):
  try: 
      prompt = f"Escribe preguntas dirigidas a una persona a la que estoy haciendo una entrevista personal. Quiero que las preguntas me ayuden a obtener información acerca del siguiente tema: {clave} "
      response = model.generate_content(prompt)
      while not response.candidates:
        response = model.generate_content(f"Generame varias preguntas que para hacer a alguien y saber más sobre él, quiero que las preguntas tengan que ver con {clave}")
      text = response.text
      patron = r'¿(.*?)\?'
      preguntas = re.findall(patron, text)
      return preguntas
  except KeyError:
      print(f"Error de clave al trbaajar con la clave {clave}")

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
    
    return json.loads(cargar_json(response.text))
  else:
    return []

def analizar_respuesta(pregunta):
  try:
    data = generate_json(pregunta)
    """
    if data == "return":
        return
    extra = analizar_extra(pregunta)
    if extra != []:
        for clave,valor in extra.items():
            pregunta.actualizar_campo(clave, valor)
    """    
    for clave,valor in data.items():
        pregunta.actualizar_campo(clave, valor)
        #Si ya había generado preguntas extra para ese campo paso
        if "No Encontrado" in valor:
            if not pregunta.extra[clave]:
                pregunta.marcarGeneradasExtra(clave)
                nuevasPregs = generate_question(clave)
                pregunta.añadirPreguntasExtra(nuevasPregs)
                return
    pregunta.pasarSiguiente()
  except KeyError:
      print(f"Ha habido un error al trabajar con la clave {clave} y la pregunta {pregunta.enunciado}")
      pregunta.pasarSiguiente()
        
preguntas = []

index = 0

def siguientePregunta(respuesta):
    
    global index
    
    if index == 0: #En el caso de que sea la primera vez que llamo a esta función todavía no he hecho ninguna pregunta, será el saludo
        index = index + 1
        return preguntas[1].enunciado 
    
    preguntas[index].actualizar_respuesta(respuesta)
    analizar_respuesta(preguntas[index])
    if preguntas[index].pasar or len(preguntas[index].preguntasExtra) == 0:
        if index != (len(preguntas)-1):
            index = index + 1
            return preguntas[index].enunciado
        else:
            with open("informacion.txt","w",encoding="utf-8") as archivo:
                for p in preguntas:
                    archivo.write(str(p.campos))
            return "Muchas gracias por la información."
    else:
        pregunta = preguntas[index].preguntasExtra[0]
        preguntas[index].eliminarPreguntasExtra()
        return "¿"+pregunta+"?"
    
    

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

