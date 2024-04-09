from gensim.models import KeyedVectors

# Descargar el modelo preentrenado de FastText en español
# Asegúrate de tener conexión a Internet para descargar el archivo
url_modelo = 'https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.es.vec'
modelo_guardado = 'modelo_fasttext_espanol.vec'
# Descargar el modelo
import urllib.request
urllib.request.urlretrieve(url_modelo, modelo_guardado)

# Cargar el modelo preentrenado de FastText en español
word2vec_model = KeyedVectors.load_word2vec_format(modelo_guardado, binary=False)

# Función para encontrar palabras similares a una palabra dada
def encontrar_palabras_similares(palabra, modelo, cantidad=5):
    try:
        palabras_similares = modelo.most_similar(positive=[palabra], topn=cantidad)
        return palabras_similares
    except KeyError:
        return f"No se encontraron palabras similares para '{palabra}'."

# Mostrar palabras similares encontradas
if isinstance(palabras_similares, str):
    print(palabras_similares)
else:
    print(f"Palabras similares a '{palabra_input}':")
    for palabra, similitud in palabras_similares:
        print(f"- {palabra}: {similitud}")
        
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity


# Función para encontrar la respuesta más relevante a partir de un texto de entrada
def generar_respuesta(texto_entrada, textos_base, modelo):
    # Tokenizar el texto de entrada
    tokens_entrada = texto_entrada.lower().split()

    # Calcular el vector promedio del texto de entrada
    vector_entrada = sum(modelo.get_vector(token) for token in tokens_entrada) / len(tokens_entrada)

    # Calcular la similitud de coseno entre el vector de entrada y cada vector en la base de textos
    similitudes = [cosine_similarity([vector_entrada], [modelo.get_vector(token.lower())])[0][0] for token in textos_base]

    # Encontrar el índice del texto con mayor similitud
    indice_max_similitud = similitudes.index(max(similitudes))

    # Devolver el texto base más similar como respuesta
    return textos_base[indice_max_similitud]

# Textos base para generar respuestas
textos_base = [
    "Hola, ¿cómo estás?",
    "¿En qué puedo ayudarte?",
    "Lo siento, no entiendo la pregunta.",
    "Por favor, sé más específico.",
    "¡Gracias por tu mensaje!"
]

# Loop para interactuar con el usuario y generar respuestas automáticas
while True:
    # Texto de entrada del usuario
    texto_entrada = input("Tú: ")

    # Generar y mostrar la respuesta automática
    respuesta = generar_respuesta(texto_entrada, textos_base, word2vec_model)
    print("Bot:", respuesta)

