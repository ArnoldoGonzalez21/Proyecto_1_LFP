from tkinter.constants import TRUE
from Analizador import Analizador

#import Helpers
from tkinter import Tk, Canvas, PhotoImage, mainloop
lexico = Analizador()
width = 1000
height = 600
window = Tk()
canvas = Canvas(window, width=width, height=height, bg='white')
canvas.pack()
img = PhotoImage(width=width, height=height)
canvas.create_image((width//2, height//2), image=img, state="normal")


#def gra():
 #   for col in colores:
  #      img.put(col.color,(col.x,col.y))
#entrada = Helpers.Leer_Archivos()
#lexico.analizador_estados(entrada)
def oi(img):
    print('entre')
    pinta = True
    ancho = 400
    alto = 400
    coordenada_x = -1
    coordenada_y = -1
    token_fila = -1
    filas = 0
    columnas = 0
    token_tamano_fila = -1
    token_tamano_columna = -1
    print(len(lexico.tokens))
    for token in lexico.tokens:
        if token.get_lexema() == 'FILAS':
            token_tamano_fila = token.get_fila()
        if token_tamano_fila == token.get_fila() and token.tipo == lexico.tipos.NUMERO:
            filas = token.get_lexema()
        if token.get_lexema() == 'COLUMNAS':
            token_tamano_columna = token.get_fila()
        if token_tamano_columna == token.get_fila() and token.tipo == lexico.tipos.NUMERO:
            columnas = token.get_lexema()    
        if token_fila < token.get_fila():
            coordenada_x = -1
            coordenada_y = -1
            token_fila = -1
        if token.tipo == lexico.tipos.NUMERO:
            if coordenada_x == -1:
                coordenada_x = token.get_lexema()
                token_fila = token.get_fila()
            elif coordenada_y == -1 and token_fila == token.get_fila():
                coordenada_y = token.get_lexema()    
        if token.tipo == lexico.tipos.BOOL:
            if token.get_lexema() == 'TRUE':
                pinta = True
            elif token.get_lexema() == 'FALSE':
                pinta = False            
        if token.tipo ==  lexico.tipos.COLOR and token_fila == token.get_fila() and pinta: #si se encuentran en la misma fila el token color y el token numero
            factor_x = ancho//int(filas)
            factor_y = alto//int(columnas)
            color = token.get_lexema()
            print(color,coordenada_x,coordenada_y)
            contador_f = 0
            contador_y = 0
            coordenada_x = int(coordenada_x) * int(factor_x)
            coordenada_y = int(coordenada_y) * int(factor_y)
            for i in range(factor_x*factor_y):
                img.put(color,(coordenada_x+contador_f,coordenada_y+contador_y))
                contador_f += 1
                if contador_f == factor_x:
                    contador_y += 1
                    contador_f = 0

def oi_x(mirror_x, mirror_y):
    print('entre')
    pinta = True
    ancho = 400
    alto = 400
    coordenada_x = -1
    coordenada_y = -1
    token_fila = -1
    filas = 0
    columnas = 0
    token_tamano_fila = -1
    token_tamano_columna = -1
    print(len(lexico.tokens))
    for token in lexico.tokens:
        if token.get_lexema() == 'FILAS':
            token_tamano_fila = token.get_fila()
        if token_tamano_fila == token.get_fila() and token.tipo == lexico.tipos.NUMERO:
            filas = token.get_lexema()
        if token.get_lexema() == 'COLUMNAS':
            token_tamano_columna = token.get_fila()
        if token_tamano_columna == token.get_fila() and token.tipo == lexico.tipos.NUMERO:
            columnas = token.get_lexema()    
        if token_fila < token.get_fila():
            coordenada_x = -1
            coordenada_y = -1
            token_fila = -1
        if token.tipo == lexico.tipos.NUMERO:
            if coordenada_x == -1:
                coordenada_x = token.get_lexema()
                token_fila = token.get_fila()
            elif coordenada_y == -1 and token_fila == token.get_fila():
                coordenada_y = token.get_lexema()    
        if token.tipo == lexico.tipos.BOOL:
            if token.get_lexema() == 'TRUE':
                pinta = True
            elif token.get_lexema() == 'FALSE':
                pinta = False            
        if token.tipo ==  lexico.tipos.COLOR and token_fila == token.get_fila() and pinta: #si se encuentran en la misma fila el token color y el token numero
            factor_x = ancho//int(filas)
            factor_y = alto//int(columnas)
            color = token.get_lexema()
            if mirror_y:
                coordenada_y = int(columnas) - int(coordenada_y) + 1
            if mirror_x:
                coordenada_x = int(filas) - int(coordenada_x) + 1
            print(color,coordenada_x,coordenada_y)
            contador_f = 0
            contador_y = 0
            coordenada_x = int(coordenada_x) * int(factor_x)
            coordenada_y = int(coordenada_y) * int(factor_y)
            for i in range(factor_x*factor_y):
                img.put(color,(coordenada_x+contador_f,coordenada_y+contador_y))
                contador_f += 1
                if contador_f == factor_x:
                    contador_y += 1
                    contador_f = 0
                    
# Original --> False False
# Mirror_x --> True False
# Mirror_y --> False True
# Double_M --> True True                
oi_x(False, True) 
mainloop()       