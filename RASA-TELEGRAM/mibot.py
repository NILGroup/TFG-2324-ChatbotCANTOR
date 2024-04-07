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
# -*- coding: utf-8 -*-

#pip install telebot
#pip install -q -U google-generativeai
#pip install google

#Configuración: cargamos la API KEY y instalamos el modelo 
#pip install google
#import tfg

bot = telebot.TeleBot(TELEGRAM_TOKEN)

    
@bot.message_handler(commands=["start"])
def cmd_start(message):
    tfg.cargar_preguntas()
    bot.reply_to(message, "Bienvenido al chatbot de ayuda a la terapia de reminiscencia. A continuación, le haré una serie de preguntas que me ayudarán a conocer más sobre usted para ayudarle a recordar y trabajar la mente. En primer lugar, ¿Cuál es su nombre?")


@bot.message_handler(content_types=["text"])
def bot_mesajes_text(message):
    if message.text.startswith("/"):
        bot.send_message(message.chat.id, "El comando no esta disponible")
    else:
        answer = siguientePregunta.siguientePregunta(message.text)
       
#MAIN
if __name__ == '__main__':
    bot.infinity_polling()



