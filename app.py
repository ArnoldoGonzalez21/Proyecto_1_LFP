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
    img = PhotoImage(width = ancho, height = alto)
    
    def __init__(self):
        self.configuracion_ventana()        
        lienzo = Canvas(self.ventana, width = self.ancho, height = self.alto, bg = 'white')#resetear para que este en blanco de nuevo
        lienzo.place(x = 150, y = 100)
        lienzo.create_image((self.ancho//2, self.alto//2), image = self.img, state = "normal")
        self.crear_botones(lienzo)
        self.ventana.mainloop()
        
    def configuracion_ventana(self):
        self.ventana.geometry(str(WIDTH)+"x"+str(HEIGHT))
        self.ventana.title('Bitxelart') 
    
    def crear_botones(self, lienzo):
        boton_cargar = tkinter.Button(self.ventana, text = 'Cargar', command = self.leer_archivo, width = 10, height = 2)
        boton_analizar = tkinter.Button(self.ventana, text = 'Analizar', command = self.analizar_archivo, width = 10, height = 2)
        boton_reportes = tkinter.Button(self.ventana, text = 'Reportes', width = 10, height = 2)
        boton_salir = tkinter.Button(self.ventana, text = 'Salir', command = lambda: exit(), width = 10, height = 2)
        
        boton_original = tkinter.Button(self.ventana, text = 'Original', command = lambda: self.pintar(False, False), width = 10, height = 3)
        boton_mirror_x = tkinter.Button(self.ventana, text = 'Mirror X', command = lambda: self.pintar(True, False), width = 10, height = 3)
        boton_mirror_y = tkinter.Button(self.ventana, text = 'Mirror Y', command = lambda: self.pintar(False, True), width = 10, height = 3)
        boton_double_mirror = tkinter.Button(self.ventana, text = 'Bouble Mirror', command = lambda: self.pintar(True, True), width = 10, height = 3)
        
        #boton_original = tkinter.Button(self.ventana, text = 'Original', command = lambda: self.pintar2(False, False), width = 10, height = 3)
        #boton_mirror_x = tkinter.Button(self.ventana, text = 'Mirror X', command = lambda: self.pintar2(True, False), width = 10, height = 3)
        #boton_mirror_y = tkinter.Button(self.ventana, text = 'Mirror Y', command = lambda: self.pintar2(False, True), width = 10, height = 3)
        #boton_double_mirror = tkinter.Button(self.ventana, text = 'Bouble Mirror', command = lambda: self.pintar2(True, True), width = 10, height = 3)
        
        boton_borrar = tkinter.Button(self.ventana, text = 'Borrar imagen', command = self.pintar_imagen, width = 12 , height = 1, bg = '#A9EAFF')
        
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
    
    def analizar_archivo(self):
        self.lexico.analizador_estados(self.data)
        self.lexico.guardar_imagen()
        #self.lexico.impr()

    # Original --> False False
    # Mirror_x --> True False
    # Mirror_y --> False True
    # Double_M --> True True
    
    def pintar(self, mirror_x, mirror_y):
        self.lexico.graficar2(self.img, 400, 400, mirror_x, mirror_y, '') #cambiarlo al ancho de self los 400
    
    def pintar2(self, mirror_x, mirror_y):
        self.lexico.graficar(self.img, 400, 400, mirror_x, mirror_y)
                       
    def borrar_imagen(self, lienzo):
        lienzo.delete(tkinter.ALL)
    
    def pintar_imagen(self):
        contador_f = 0
        contador_y = 0
        for i in range(self.ancho*self.alto):
            self.img.put('white',(contador_f,contador_y))
            contador_f += 1
            if contador_f == self.ancho:
                contador_y += 1
                contador_f = 0
    
if __name__ == '__main__':
    po()