import tkinter as tk
from tkinter import messagebox

def responder_si():
    messagebox.showinfo("Respuesta", "Has seleccionado 'Sí'.")

def responder_no():
    messagebox.showinfo("Respuesta", "Has seleccionado 'No'.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Pregunta")

# Crear la etiqueta de la pregunta
etiqueta_pregunta = tk.Label(ventana, text="¿Estás de acuerdo?")
etiqueta_pregunta.pack()

# Crear los botones de respuesta
boton_si = tk.Button(ventana, text="Sí", command=responder_si)
boton_si.pack(side="left", padx=10)

boton_no = tk.Button(ventana, text="No", command=responder_no)
boton_no.pack(side="right", padx=10)

# Ejecutar el bucle principal de la ventana
ventana.mainloop()



