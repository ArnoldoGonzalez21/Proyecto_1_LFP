class Token():
    
    lexema_valido = ''
    tipo = 0
    fila = 0
    columna = 0
    
    PALABRA_RESERVADA = 1
    LETRA = 2
    NUMERO = 3
    RESTO = 4
    CADENA = 5
    SIGNO = 6
    ARROBA = 6.1
    COLOR = 7
    BOOL = 8
    ERROR = 9
    
    def __init__(self, lexema, tipo, fila, columna):
        self.lexema_valido = lexema
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        
    def get_tipo(self):
        if self.tipo == self.PALABRA_RESERVADA:
            return 'Palabra Reservada'
        elif self.tipo == self.LETRA:
            return 'Letra'
        elif self.tipo == self.NUMERO:
            return 'Número'
        elif self.tipo == self.CADENA:
            return 'Cadena'
        elif self.tipo == self.SIGNO:
            return 'Signo'
        elif self.tipo == self.ARROBA:
            return 'Arroba'
        elif self.tipo == self.COLOR:
            return 'Color'
        elif self.tipo == self.BOOL:
            return 'Booleano'
    
    def get_lexema(self):
        return self.lexema_valido 
       
    def get_fila(self):
        return self.fila   
    
    def get_columna(self):
        return self.columna   
        
            