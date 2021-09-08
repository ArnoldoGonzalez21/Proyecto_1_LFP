from Analizador import Analizador
from Helpers import Menu, Leer_Archivos

def main():
    entrada = ""
    opcion = Menu()
    lexico = Analizador()
    while opcion != 0 :
        if opcion == 1:
           entrada = Leer_Archivos()
        elif opcion == 2:
            print('\nAnalisis')
            lexico.analizador_estados(entrada)
        elif opcion ==3:
            print("\nLista de tokens")
            lexico.Imprimir()
        elif opcion == 4:
            print('\nLista de errores')
            lexico.ImprimirErrores()
        opcion = Menu();

if __name__ == "__main__":
    main()