# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 19:22:50 2024

@author: Marta
"""

import pathlib
import textwrap
import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

import json
import sys

import re

from config import *

import PIL.Image

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


model = genai.GenerativeModel('gemini-pro-vision')

def analizador_imagenes(image):
    img = PIL.Image.open(image)
    response = model.generate_content(["Generame una descripción de esta imagen en español. Finalmente, genera una pregunta para obtener información sobre algo o alguien en la imagen. ", img])
    return response.text