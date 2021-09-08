from io import open

def Leer_Archivos():
    archivos_texto = open('archivoEntrada.pxla', 'r')
    texto = archivos_texto.read()
    return texto

def Menu():
    print('\n1. Leer Archivo')
    print('2. Analizar')
    print('3. Obtener lista de tokens')
    print('4. Obtener errores')
    salida = int(input("Ingrese su opcion: "))
    return salida