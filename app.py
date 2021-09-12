from tkinter import *
import tkinter
from tkinter import Frame, ttk, filedialog
from Analizador import Analizador

WIDTH = 800
HEIGHT = 700

class po():
    nombre = ''
    lexico = Analizador()
    ventana = tkinter.Tk()     
    ancho = 550
    alto = 550
    
    def __init__(self):
        self.configuracion_ventana()        
        lienzo = Canvas(self.ventana, width = self.ancho, height = self.alto, bg = 'white')
        lienzo.place(x = 150, y = 100)        
        combo_imagenes = ttk.Combobox(self.ventana, font = ('Courier', 11), state = "readonly") #buscar una forma que se actualice
        self.crear_botones(lienzo, combo_imagenes)
        self.ventana.mainloop()
        
    def configuracion_ventana(self):
        self.ventana.geometry(str(WIDTH)+"x"+str(HEIGHT))
        self.ventana.title('Bitxelart') 
    
    def crear_botones(self, lienzo, combo_imagenes):
        boton_cargar = tkinter.Button(self.ventana, text = 'Cargar', command = lambda: self.leer_archivo(combo_imagenes), width = 10, height = 2)
        boton_analizar = tkinter.Button(self.ventana, text = 'Analizar', command = lambda: self.nombre_imagen_seleccionada(combo_imagenes), width = 10, height = 2)
        boton_reportes = tkinter.Button(self.ventana, text = 'Reportes', command = self.lexico.crear_reporte,  width = 10, height = 2)
        boton_salir = tkinter.Button(self.ventana, text = 'Salir', command = lambda: exit(), width = 10, height = 2)
        
        boton_original = tkinter.Button(self.ventana, text = 'Original', command = lambda: self.dibujar_imagen(lienzo, False, False), width = 10, height = 3)
        boton_mirror_x = tkinter.Button(self.ventana, text = 'Mirror X', command = lambda: self.dibujar_imagen(lienzo, True, False), width = 10, height = 3)
        boton_mirror_y = tkinter.Button(self.ventana, text = 'Mirror Y', command = lambda: self.dibujar_imagen(lienzo, False, True), width = 10, height = 3)
        boton_double_mirror = tkinter.Button(self.ventana, text = 'Double Mirror', command = lambda: self.dibujar_imagen(lienzo, True, True), width = 10, height = 3)
        
        #boton_agregar_imagen = tkinter.Button(self.ventana, text = 'Seleccionar', command = lambda: self.nombre_imagen_seleccionada(combo_imagenes), width = 12 , height = 1, bg = '#A9EAFF')
        
        boton_cargar.place(x = 10, y = 10)
        boton_analizar.place(x = 100, y = 10)
        boton_reportes.place(x = 190, y = 10)
        boton_salir.place(x = 280, y = 10)
        boton_original.place(x = 50, y = 140)
        boton_mirror_x.place(x = 50, y = 200)
        boton_mirror_y.place(x = 50, y = 260)
        boton_double_mirror.place(x = 50, y = 320)
        #boton_agregar_imagen.place(x = 595, y = 30)
        
        label_imagenes = tkinter.Label(self.ventana, text = "Seleccione el nombre de la imagen a analizar:", font = ('Courier', 9))
        label_imagenes.place(x = 370, y = 10)
    
    def configuracion_combo(self, combo_imagenes):
        self.lexico.opciones_imagenes(combo_imagenes)
        combo_imagenes.place(x = 370, y = 30)
    
    def nombre_imagen_seleccionada(self, combo_imagenes):
        self.nombre = combo_imagenes.get()
        #self.dibujar_imagen(lienzo, False, False, nombre)            

    # Original --> False False
    # Mirror_x --> True False
    # Mirror_y --> False True
    # Double_M --> True True
    def dibujar_imagen(self, lienzo, mirror_x, mirror_y):
        #nombre = combo_imagenes.get()
        #self.lexico.impr()
        #if self.nombre != '':
        self.borrar_imagen(lienzo)
        self.lexico.graficar_imagen(lienzo, 400, 400, mirror_x, mirror_y, self.nombre) #cambiarlo al ancho de self los 400
            
            #verificar que la imagen que se le envía se pueda mirror_x, mi... etc  if image.mirror_x is True:  Y el True que venga del parámetro
                               
    def borrar_imagen(self, lienzo):
        lienzo.delete(tkinter.ALL)
    
    def crear_repo(self):
        self.lexico.crear_reporte()
              
    def analizar_archivo(self, data, combo_imagenes):
        self.lexico.analizador_estados(data)
        self.lexico.guardar_imagen()        
        self.configuracion_combo(combo_imagenes)
        #self.lexico.Imprimir()
        self.lexico.impr()
        
    def leer_archivo(self, combo_imagenes):
        try:
            ruta = filedialog.askopenfilename(title = "Abrir un archivo")
            with open(ruta, 'rt', encoding = 'utf-8') as f:
                print('Archivo cargado con éxito')
                data = f.read()   
                self.analizar_archivo(data, combo_imagenes)              
        except OSError:
            print("<<< No se pudo leer el Archivo", ruta ,'>>>')
            return   
    
if __name__ == '__main__':
    po()