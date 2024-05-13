from config import * 
import telebot

import pathlib
import textwrap
import google.generativeai as genai

from IPython.display import display
from IPython.display import Image
from IPython.core.display import HTML
from IPython.display import Markdown

import json
import sys

import re
import tfg
import imagenes
# -*- coding: utf-8 -*-

#pip install telebot
#pip install -q -U google-generativeai
#pip install google

#Configuración: cargamos la API KEY y instalamos el modelo 
#pip install google
#import tfg

bot = telebot.TeleBot(TELEGRAM_TOKEN)

i = 0

@bot.message_handler(commands=["start"])
def cmd_start(message):
    tfg.cargar_preguntas()
    bot.reply_to(message, "Bienvenido al chatbot de ayuda a la terapia de reminiscencia. A continuación, le haré una serie de preguntas que me ayudarán a conocer más sobre usted para ayudarle a recordar y trabajar la mente. En cualquier momento, puede adjuntar fotos que le ayuden a dar sus explicaciones o que le interese mostrarme.")


@bot.message_handler(content_types=["text"])
def bot_mesajes_text(message):
    if message.text.startswith("/"):
        bot.send_message(message.chat.id, "El comando no esta disponible")
    else:
        answer = tfg.siguientePregunta(message.text)
        bot.send_message(message.chat.id, answer)
        
@bot.message_handler(content_types=["photo"])
def photo(message):
    global i 
    
    fileID = message.photo[-1].file_id
    
    file_info = bot.get_file(fileID)
    
    downloaded_file = bot.download_file(file_info.file_path)

    with open(f"image{i}.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
        answer = imagenes.analizador_imagenes(f"image{i}.jpg")
        if(answer == []):
            answer = "¡Qué foto más chula! ¿Qué puedes contarme sobre ella?"
        i = i + 1
        bot.send_message(message.chat.id, answer)
        
#MAIN
if __name__ == '__main__':
    bot.infinity_polling()



