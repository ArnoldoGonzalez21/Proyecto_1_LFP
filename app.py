from tkinter import *
import tkinter

class po():
    def __init__(self):
        ventana = tkinter.Tk()
        self.configuracion_ventana(ventana)
        self.crear_botones(ventana)
        ventana.mainloop()
        
    def configuracion_ventana(self, ventana):
        ventana.geometry("800x500")
        ventana.title('Bitxelart')
    
    def crear_botones(self, ventana):
        boton_cargar = tkinter.Button(ventana, text = 'Cargar', width = 10, height = 2)
        boton_analizar = tkinter.Button(ventana, text = 'Analizar', width = 10, height = 2)
        boton_reportes = tkinter.Button(ventana, text = 'Reportes', width = 10, height = 2)
        boton_salir = tkinter.Button(ventana, text = 'Salir', command = lambda: exit(), width = 10, height = 2)
        boton_original = tkinter.Button(ventana, text = 'Original', width = 10, height = 3)
        boton_mirror_x = tkinter.Button(ventana, text = 'Mirror X', width = 10, height = 3)
        boton_mirror_y = tkinter.Button(ventana, text = 'Mirror Y', width = 10, height = 3)
        boton_double_mirror = tkinter.Button(ventana, text = 'Bouble Mirror', width = 10, height = 3)

        boton_cargar.place(x = 10, y = 10)
        boton_analizar.place(x = 100, y = 10)
        boton_reportes.place(x = 190, y = 10)
        boton_salir.place(x = 280, y = 10)
        boton_original.place(x = 50, y = 140)
        boton_mirror_x.place(x = 50, y = 200)
        boton_mirror_y.place(x = 50, y = 260)
        boton_double_mirror.place(x = 50, y = 320)
 
if __name__ == '__main__':
    po()