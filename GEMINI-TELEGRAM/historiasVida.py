# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 18:00:32 2024

@author: Marta
"""



def generacionHistoriaVida(json):
  prompt = f"Teniendo en cuenta estos datos {str(json)} generame una historia de la vida de esa persona con estos datos."
  response = model.generate_content(prompt)
  print(response.text)
  