class Imagen():
    
    colores = []
    def __init__(self, titulo, filas, columnas, ancho, alto, mirrorx, mirrory, doublemirror, cantidad_colores):
        self.titulo = titulo
        self.filas = filas
        self.columnas = columnas
        self.ancho = ancho        
        self.alto = alto
        self.mirrorx = mirrorx
        self.mirrory = mirrory
        self.doublemirror = doublemirror
        self.cantidad_colores = cantidad_colores
        
    def agregar_colores(self, nuevo_color):
        self.colores.append(nuevo_color)