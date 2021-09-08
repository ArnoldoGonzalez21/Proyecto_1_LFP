from Token import Token
import re

class Analizador():
    
    lexema = ''
    estado = 0
    tokens = []
    columna = 1
    fila = 1
    generar = True
    i = 0
    tipos = Token("lexema", -1, -1, -1)
    
    def agregar_token(self, tipo):
        nuevo_token = Token(self.lexema, tipo, self.fila, self.columna)
        self.tokens.append(nuevo_token)
        self.lexema = ''
        self.estado = 0
        
    def analizador_estados(self, entrada):
        self.estado = 0
        self.lexema = ''
        self.tokens = []
        self.fila = 1
        self.columna = 1
        entrada = self.quitar_espacios(entrada)
        entrada = self.separar(entrada)
        entrada += '¬'
        print(entrada)
        actual = ''
        longitud = len(entrada)
        for contador in range(longitud):
            actual = entrada[contador]
            if self.estado == 0:
                if actual.isalpha():
                    self.estado = 1
                    self.columna += 1
                    self.lexema += actual
                     
                elif actual.isdigit():
                    self.estado = 2
                    self.columna += 1
                    self.lexema += actual
                
                elif actual == '"':
                    self.estado = 3
                    self.columna += 1                    
                    self.lexema += actual   
                     
                elif actual == '=':
                    self.estado = 4
                    self.columna += 1
                    self.lexema += actual                    
                    self.agregar_token(self.tipos.SIGNO)
                     
                elif actual == '[' or actual == ']' or actual == '{' or actual == '}' or actual == ',' or actual == ';':
                    self.estado = 4
                    self.columna += 1  
                    self.lexema += actual                    
                    self.agregar_token(self.tipos.SIGNO)
                     
                elif actual == '@':
                    self.estado = 4
                    self.columna += 1                    
                    self.lexema += actual
                
                elif actual == '#':
                    self.estado = 5
                    self.columna += 1                    
                    self.lexema += actual    
                     
                elif actual == ' ':
                    self.columna +=1
                    self.estado = 0
                     
                elif actual == '\n':
                    self.fila += 1
                    self.estado = 0
                    self.columna = 1
                     
                elif actual =='\r':
                    self.estado = 0
                     
                elif actual == '\t':
                    self.columna += 5
                    self.estado = 0
                     
                elif actual == '¬' and contador == longitud - 1:
                    print('Análisis terminado')
                    
                else:
                    self.lexema += actual
                    self.agregar_token(self.tipos.ERROR)
                    self.columna += 1
                    self.generar = False    
            
            elif self.estado == 1:
                if actual.isalpha():
                    self.estado = 1
                    self.columna += 1
                    self.lexema += actual
                else:
                    if self.es_palabra_reserva(self.lexema):
                        self.agregar_token(self.tipos.PALABRA_RESERVADA)
                    elif self.es_booleano(self.lexema):
                        self.agregar_token(self.tipos.BOOL)
                    else:
                        print('entre')
                        self.agregar_token(self.tipos.ERROR)
                        
            elif self.estado == 2:
                if actual.isdigit():
                    self.estado = 2
                    self.columna += 1
                    self.lexema += actual
                else:
                    self.agregar_token(self.tipos.NUMERO)
                    
            elif self.estado == 3:
                if actual != '"':
                    self.estado = 3
                    self.columna +=1
                    self.lexema += actual
                     
                elif actual == '"':
                    self.estado = 6
                    self.lexema += actual 
                    self.agregar_token(self.tipos.CADENA)                     
                    
            elif self.estado == 4:
                if actual == '@':
                    self.estado = 4
                    self.columna += 1
                    self.lexema += actual
                else:
                    self.agregar_token(self.tipos.ARROBA)                     
                                
            elif self.estado == 5:
                if actual.isalpha():
                    self.estado = 5
                    self.columna += 1
                    self.lexema += actual
                     
                elif actual.isdigit():
                    self.estado = 5
                    self.columna += 1
                    self.lexema += actual
                     
                else:
                    self.agregar_token(self.tipos.COLOR)  
                          
    def separar(self, entrada):
        patron = r'(\w)([= - , - ; - { - } - \[ - \] ])'
        return re.sub(patron, r'\1 \2 ', entrada)                           
    
    def quitar_espacios(self, entrada):
        patron = ' +'
        return re.sub(patron, '', entrada)
      
    def es_palabra_reserva(self, entrada):
        entrada = entrada.upper() 
        palabras_reservadas = ['TITULO', 'ANCHO', 'ALTO', 'FILAS', 'COLUMNAS', 'CELDAS', 'FILTROS', 'MIRRORX', 'MIRRORY', 'DOUBLEMIRROR']
        if entrada in palabras_reservadas:
            return True
        return False
    
    def es_booleano(self, entrada):
        entrada = entrada.upper() 
        booleanos = ['TRUE', 'FALSE']
        if entrada in booleanos:
            return True
        return False
    
    
    def Impr(self):
        print(len(self.tokens))
        for token in self.tokens:
            print(token.lexema_valido," --> ",token.get_tipo(),' --> ',token.get_fila(), ' --> ',token.get_columna())
    
    
    def Imprimir(self):
        for x in self.tokens:
            if x.tipo != self.tipos.ERROR:
                print(x.get_lexema()," --> ",x.get_tipo(),' --> ',x.get_fila(), ' --> ',x.get_columna())
    
    def ImprimirErrores(self):
        for x in self.tokens:
            if x.tipo == self.tipos.ERROR:
                print(x.get_lexema()," --> ",x.get_fila(), ' --> ',x.get_columna(),'--> Error Lexico')
    
    

                        
        