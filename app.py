from tkinter import *
import tkinter
from tkinter import Frame, ttk, filedialog
from Analizador import Analizador

WIDTH = 800
HEIGHT = 700

class po():
    
    data = ''
    lexico = Analizador()
    ventana = tkinter.Tk()     
    ancho = 550
    alto = 550
    
    def __init__(self):
        self.configuracion_ventana()        
        lienzo = Canvas(self.ventana, width = self.ancho, height = self.alto, bg = 'white')
        lienzo.place(x = 150, y = 100)
        self.crear_botones(lienzo)
        self.ventana.mainloop()
        
    def configuracion_ventana(self):
        self.ventana.geometry(str(WIDTH)+"x"+str(HEIGHT))
        self.ventana.title('Bitxelart') 
    
    def crear_botones(self, lienzo):
        boton_cargar = tkinter.Button(self.ventana, text = 'Cargar', command = self.leer_archivo, width = 10, height = 2)
        boton_analizar = tkinter.Button(self.ventana, text = 'Analizar', command = self.analizar_archivo, width = 10, height = 2)
        boton_reportes = tkinter.Button(self.ventana, text = 'Reportes', command = self.lexico.crear_reporte,  width = 10, height = 2)
        boton_salir = tkinter.Button(self.ventana, text = 'Salir', command = lambda: exit(), width = 10, height = 2)
        
        boton_original = tkinter.Button(self.ventana, text = 'Original', command = lambda: self.pintar3(lienzo, False, False), width = 10, height = 3)
        boton_mirror_x = tkinter.Button(self.ventana, text = 'Mirror X', command = lambda: self.pintar3(lienzo, True, False), width = 10, height = 3)
        boton_mirror_y = tkinter.Button(self.ventana, text = 'Mirror Y', command = lambda: self.pintar3(lienzo, False, True), width = 10, height = 3)
        boton_double_mirror = tkinter.Button(self.ventana, text = 'Bouble Mirror', command = lambda: self.pintar3 (lienzo, True, True), width = 10, height = 3)
        
        boton_borrar = tkinter.Button(self.ventana, text = 'Borrar imagen', command = lambda: self.borrar_imagen(lienzo), width = 12 , height = 1, bg = '#A9EAFF')
        
        boton_cargar.place(x = 10, y = 10)
        boton_analizar.place(x = 100, y = 10)
        boton_reportes.place(x = 190, y = 10)
        boton_salir.place(x = 280, y = 10)
        boton_original.place(x = 50, y = 140)
        boton_mirror_x.place(x = 50, y = 200)
        boton_mirror_y.place(x = 50, y = 260)
        boton_double_mirror.place(x = 50, y = 320)
        boton_borrar.place(x = 610, y = 65)
    
    def leer_archivo(self):
        try:
            ruta = filedialog.askopenfilename(title = "Abrir un archivo")
            with open(ruta, 'rt', encoding = 'utf-8') as f:
                print('Archivo cargado con éxito')
                self.data = f.read()                 
        except OSError:
            print("<<< No se pudo leer el Archivo", ruta ,'>>>')
            return   
    
    def crear_repo(self):
        self.lexico.crear_reporte()
    
    def analizar_archivo(self):
        self.lexico.analizador_estados(self.data)
        self.lexico.guardar_imagen()
        #self.lexico.impr()

    # Original --> False False
    # Mirror_x --> True False
    # Mirror_y --> False True
    # Double_M --> True True
    def pintar3(self, lienzo, mirror_x, mirror_y):
        self.lexico.graficar3(lienzo, 400, 400, mirror_x, mirror_y, '') #cambiarlo al ancho de self los 400
                               
    def borrar_imagen(self, lienzo):
        lienzo.delete(tkinter.ALL)
    
if __name__ == '__main__':
    po()