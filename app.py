from tkinter import *
import tkinter
from tkinter import Frame, ttk, filedialog, messagebox
from Analizador import Analizador

WIDTH = 800
HEIGHT = 700

class Interfaz():
    data = ''
    lexico = Analizador()
    ventana = tkinter.Tk()     
    ancho = 550
    alto = 550
    
    def __init__(self):
        self.configuracion_ventana()        
        lienzo = Canvas(self.ventana, width = self.ancho, height = self.alto, bg = 'white')
        lienzo.place(x = 150, y = 100)        
        combo_imagenes = ttk.Combobox(self.ventana, font = ('Courier', 11), state = "readonly")
        self.crear_botones(lienzo, combo_imagenes)
        self.ventana.mainloop()
        
    def configuracion_ventana(self):
        self.ventana.geometry(str(WIDTH)+"x"+str(HEIGHT))
        self.ventana.title('Bitxelart') 
    
    def crear_botones(self, lienzo, combo_imagenes):
        boton_cargar = tkinter.Button(self.ventana, text = 'Cargar', command = self.leer_archivo, width = 10, height = 2)
        boton_analizar = tkinter.Button(self.ventana, text = 'Analizar', command = lambda: self.analizar_archivo(combo_imagenes), width = 10, height = 2)
        boton_reportes = tkinter.Button(self.ventana, text = 'Reportes', command = self.crear_reportes,  width = 10, height = 2)
        boton_salir = tkinter.Button(self.ventana, text = 'Salir', command = lambda: exit(), width = 10, height = 2)
        
        boton_original = tkinter.Button(self.ventana, text = 'Original', command = lambda: self.dibujar_imagen(lienzo, combo_imagenes, False, False, False), width = 12, height = 3)
        boton_mirror_x = tkinter.Button(self.ventana, text = 'Mirror X', command = lambda: self.dibujar_imagen(lienzo, combo_imagenes, True, False, False), width = 12, height = 3)
        boton_mirror_y = tkinter.Button(self.ventana, text = 'Mirror Y', command = lambda: self.dibujar_imagen(lienzo, combo_imagenes, False, True, False), width = 12, height = 3)
        boton_double_mirror = tkinter.Button(self.ventana, text = 'Double Mirror', command = lambda: self.dibujar_imagen(lienzo, combo_imagenes, False, False, True), width = 12, height = 3)
        boton_guardar_imagen = tkinter.Button(self.ventana, text = 'Guardar Imagen', command = self.guardar_imagen, width = 12, height = 3)
        
        boton_cargar.place(x = 10, y = 10)
        boton_analizar.place(x = 100, y = 10)
        boton_reportes.place(x = 190, y = 10)
        boton_salir.place(x = 280, y = 10)
        boton_original.place(x = 40, y = 130)
        boton_mirror_x.place(x = 40, y = 200)
        boton_mirror_y.place(x = 40, y = 270)
        boton_double_mirror.place(x = 40, y = 340)
        boton_guardar_imagen.place(x = 40, y = 410)
        
        label_imagenes = tkinter.Label(self.ventana, text = "Seleccione el nombre de la imagen a procesar:", font = ('Courier', 9))
        label_imagenes.place(x = 370, y = 10)
            
    def analizar_archivo(self, combo_imagenes):
        self.lexico.analizador_estados(self.data)
        self.lexico.guardar_imagen()        
        self.configuracion_combo(combo_imagenes)
        #self.lexico.Imprimir()    
    
    def configuracion_combo(self, combo_imagenes):
        self.lexico.opciones_imagenes(combo_imagenes)
        combo_imagenes.place(x = 370, y = 30)
    
    # Original --> False False True
    # Mirror_x --> True False False
    # Mirror_y --> False True False
    # Double_M --> False False True 
    def dibujar_imagen(self, lienzo, combo_imagenes, mirror_x, mirror_y, double_mirror):
        #self.lexico.imprimir_imagen()
        nombre = combo_imagenes.get() 
        if nombre != '':
            self.borrar_imagen(lienzo)
            self.lexico.graficar_imagen(lienzo, 400, 400, mirror_x, mirror_y, double_mirror, nombre, tkinter)
        else:
            messagebox.showinfo(message = "Seleccione una imagen", title = "Alerta")   
            
    def borrar_imagen(self, lienzo):
        lienzo.delete(tkinter.ALL)
    
    def guardar_imagen(self):
        #self.lexico.crear_reporte_imagen()
        self.lexico.guardar_imagen_png()
        
    def crear_reportes(self):
        self.lexico.obtener_tokens()
        self.lexico.obtener_errores()
        self.lexico.crear_reporte_token()
        self.lexico.crear_reporte_errores()
     
    def leer_archivo(self):
        try:
            ruta = filedialog.askopenfilename(title = "Abrir un archivo")
            with open(ruta, 'rt', encoding = 'utf-8') as f:
                print('Archivo cargado con éxito')
                self.data = f.read()               
        except OSError:
            print("<<< No se pudo leer el Archivo", ruta ,'>>>')
            return   
    
if __name__ == '__main__':
    Interfaz()