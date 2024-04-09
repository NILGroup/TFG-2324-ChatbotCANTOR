# Load model directly
#from huggingface_hub import login
#login()

from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import sys
import torch
from genera_preguntas import generar_preguntas

info_persona = {} 


def gemma(): 
    tokenizer = AutoTokenizer.from_pretrained("google/gemma-7b") 
    model = AutoModelForCausalLM.from_pretrained("google/gemma-7b")
    while(True):
    	input_text = input("Introduce your text")
    	input_ids = tokenizer(input_text, return_tensors="pt")

    	outputs = model.generate(**input_ids, max_length=50)
    	print(tokenizer.decode(outputs[0]))
"""   	
def analizar_respuesta(campos, respuesta): 
	for campo in respuesta.keys():
		"""

def chatbot():
    # Creamos un diccionario para almacenar la información recopilada
    
    print("Bienvenido al Chatbot de ayuda a la terapia de reminiscencia.")
    
    # Generamos la lista de preguntas predefinidas 
    lista_preguntas = {}
    
    # Abrir el archivo en modo lectura
    with open('preguntas', 'r') as archivo:
        # Leer cada línea del archivo
        for linea in archivo:
            # Separar la pregunta del JSON
            partes = linea.strip().split('{')
            pregunta = partes[0].strip()
            datos_json = partes[1].strip()
            # Agregar la pregunta y los datos a la lista
            lista_preguntas[pregunta] = "{" + datos_json
            
    for pregunta in lista_preguntas:
    	info_persona[pregunta] = input(pregunta + " : ")
    	analizar_respuesta(json.loads(lista_preguntas[pregunta]),info_persona[pregunta])
    	
    #extra = generar_preguntas(ocupacion)
   
    # Guardamos la información en un archivo JSON
    with open('info_persona.json', 'w') as archivo:
        json.dump(info_persona, archivo)

    print("¡Gracias por proporcionar la información!")

# Ejemplo de uso
#interactuar_y_guardar_info()


if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Uso: python3 gemma.py chatbot <valor>")
        sys.exit(1)
    
    funcion = sys.argv[1]
    
    if funcion == "chatbot":
    	chatbot()
    if funcion == "gemma":
    	gemma()
    else:
        print("Función no reconocida:", funcion)

