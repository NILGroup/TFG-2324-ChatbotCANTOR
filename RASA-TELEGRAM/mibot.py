from config import * 
import telebot

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.reply_to(message, "Hola ¿Puedes indicarme tu nombre?")


@bot.message_handler(content_types=["text"])
def bot_mesajes_text(message):
    if message.text.startswith("/"):
        bot.send_message(message.chat.id, "El comando no esta disponible")
    else:
        bot.send_message(message.chat.id, "Un mensaje cuando no es comando")

#MAIN
if __name__ == '__main__':
   print('Bot iniciado')
   bot.infinity_polling()
   print("Fin")

   from rasa.core.agent import Agent

# Cargar el modelo de Rasa previamente entrenado
agent = Agent.load("models")

def procesar_mensaje(mensaje):
    # Procesar el mensaje del usuario y obtener la respuesta del modelo de Rasa
    respuesta = agent.handle_text(mensaje)
    return respuesta

# Ejemplo de uso de la función
mensaje_usuario = "Hola, ¿cómo puedo ayudarte?"
respuesta_rasa = procesar_mensaje(mensaje_usuario)
print(respuesta_rasa)
