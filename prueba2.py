from tkinter.constants import TRUE
from Analizador import Analizador
from tkinter import Frame, ttk, filedialog

from tkinter import Tk, Canvas, PhotoImage, mainloop
lexico = Analizador()
width = 550
height = 550
window = Tk()
canvas = Canvas(window, width=width, height=height, bg='white')
canvas.pack()
#canvas.create_rectangle(4,33,37,0,width=0,fill = '#000000')
#canvas.create_rectangle(50, 0, 100, 50,width=0, fill='red')
#canvas.create_rectangle(4,0,132,0, width=0, fill = '#000000')
#img = PhotoImage(width=width, height=height)
#canvas.create_image((width//2, height//2), image=img, state="normal")

#lexico.analizador_estados(entrada)

def leer_archivo():
        try:
            ruta = filedialog.askopenfilename(title = "Abrir un archivo")
            with open(ruta, 'rt', encoding = 'utf-8') as f:
                print('Archivo cargado con éxito')
                data = f.read()
                lexico.analizador_estados(data)  
                lexico.guardar_imagen()               
        except OSError:
            print("<<< No se pudo leer el Archivo", ruta ,'>>>')
            return  

def graficar3( ancho, alto, mirror_x, mirror_y):
        for image in lexico.imagenes: 
            
            filas = int(image.filas)
            columnas = int(image.columnas)
            factor_x = ancho//filas
            factor_y = alto//columnas
            
            for contador in range(image.cantidad_colores):
                coordenada_x = int(image.colores[contador].x) * factor_x
                coordenada_y = int(image.colores[contador].y) * factor_y
                if mirror_y:
                    coordenada_y = int(columnas) - int(coordenada_y) + 1
                if mirror_x:
                    coordenada_x = int(filas) - int(coordenada_x) + 1
                y_arriba = coordenada_y + factor_y
                x_abajo = coordenada_x + factor_x
                if image.colores[contador].pintar:
                    print(coordenada_x, y_arriba, x_abajo, coordenada_y, image.colores[contador].codigo)
                    canvas.create_rectangle(coordenada_x, y_arriba, x_abajo, coordenada_y, width = 0, fill = image.colores[contador].codigo)
                        
leer_archivo()
graficar3(400, 400, False, False)                  
# Original --> False False
# Mirror_x --> True False
# Mirror_y --> False True
# Double_M --> True True                
#oi_x(False, True) 
mainloop()       