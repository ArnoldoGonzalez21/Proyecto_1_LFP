from Color import Color
class Imagen():
    colores = []    
    def __init__(self, titulo, filas, columnas, ancho, alto, mirrorx, mirrory, doublemirror, cantidad_colores, indice_imagen):
        self.titulo = titulo
        self.filas = filas
        self.columnas = columnas
        self.ancho = ancho        
        self.alto = alto
        self.mirrorx = mirrorx
        self.mirrory = mirrory
        self.doublemirror = doublemirror
        self.cantidad_colores = cantidad_colores
        self.indice_imagen = indice_imagen
        #self.colores = []
        
    def agregar_color(self, x, y, pintar, codigo, indice_imagen):
        nuevo = Color(x, y, pintar, codigo, indice_imagen)
        self.colores.append(nuevo)