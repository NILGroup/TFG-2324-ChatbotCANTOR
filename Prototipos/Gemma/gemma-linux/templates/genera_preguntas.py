# Load model directly
#from huggingface_hub import login
#login()

import spacy
import sys
nlp = spacy.load("es_core_news_sm")
def generar_preguntas(texto):
    # Cargar el modelo de spaCy en español
    

    # Analizar el texto
    doc = nlp(texto)

    # Lista para almacenar las preguntas generadas
    preguntas = []

    # Formular preguntas basadas en el análisis del texto
    for token in doc:
        if(token.is_alpha):
        	if(token.tag_ == 'NOUN'):
        		pregunta = f"¿Qué tal tu experiencia de {token.text}?"
        		pregunta.format(token.tag_)
        		preguntas.append(pregunta)
        	#print(token.text, token.lemma_, token.pos_, token.tag_,str (token.is_alpha))

    return preguntas
    
def extraer_aficiones(texto):
    # Procesar el texto con spaCy
    doc = nlp(texto)
    
    # Lista para almacenar las aficiones encontradas
    aficiones = []
    
    # Buscar entidades nombradas relacionadas con "aficiones"
    for ent in doc.ents:
        if ent.label_ == "AFICION":
            aficiones.append(ent.text)
    
    print(aficiones)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 genera_preguntas.py generar_preguntas <texto>")
        sys.exit(1)
    
    funcion = sys.argv[1]
    
    if funcion == "generar_preguntas":
    	valor = str(sys.argv[2])
    	generar_preguntas(valor)
    	
    if funcion == "extraer_aficiones":
    	valor = str(sys.argv[2])
    	extraer_aficiones(valor)
    else:
        print("Función no reconocida:", funcion)
