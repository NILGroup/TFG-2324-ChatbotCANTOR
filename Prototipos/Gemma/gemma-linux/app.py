from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ejecutar_chatbot', methods=['POST'])
def ejecutar_chatbot():
    # Recibir los datos del formulario
    nombre = request.form['nombre']
    edad = request.form['edad']
    ciudad = request.form['ciudad']
    estado_civil = request.form['estado_civil']
    hijos = request.form['hijos']
    preguntas = ['Cómo te llamas','qué te gusta']
    i = 0
    for i in range(len(preguntas)):
    	answer[i] = request.form[i]
    	i = i + 1
    # Llamar a la función chatbot con los datos recibidos
    salida = chatbot(nombre, edad, ciudad, estado_civil, hijos)

    return render_template('resultado.html', salida=salida)

def chatbot(nombre, edad, ciudad, estado_civil, hijos):
    # Aquí puedes utilizar los datos recibidos para realizar el procesamiento necesario
    # y generar la salida del chatbot
    salida = f"Hola {nombre}, tienes {edad} años, vives en {ciudad}, estás {estado_civil} y {'tienes' if hijos.lower() == 'si' else 'no tienes'} hijos."
    return salida

if __name__ == '__main__':
    app.run(debug=True)

