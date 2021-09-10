from Color import Color
from Token import Token
from Imagen import Imagen
import re
import webbrowser

reporteHTML = ''

class Analizador():
    
    imagenes = []
    lexema = ''
    estado = 0
    tokens = []
    columna = 1
    fila = 1
    generar = True
    i = 0
    tipos = Token("lexema", -1, -1, -1, -1)
    colores = Imagen('',-1,-1,-1,-1,False,False,False,-1)
    id = 0
    
    def agregar_token(self, tipo):
        nuevo_token = Token(self.lexema, tipo, self.fila, self.columna, self.id)
        self.tokens.append(nuevo_token)
        self.lexema = ''
        self.estado = 0
        if tipo != 9:
            self.id += 1
        
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
     
    def Imprimir(self):
        for x in self.tokens:
            if x.tipo != self.tipos.ERROR:
                print(x.get_lexema()," --> ",x.get_tipo(),' --> ',x.get_fila(), ' --> ',x.get_columna(), ' --> ',x.get_id())
    
    def ImprimirErrores(self):
        for x in self.tokens:
            if x.tipo == self.tipos.ERROR:
                print(x.get_lexema()," --> ",x.get_fila(), ' --> ',x.get_columna(),'--> Error Lexico')
                            
    # Original --> False False
    # Mirror_x --> True False
    # Mirror_y --> False True
    # Double_M --> True True       
   
    def graficar2(self, img, ancho, alto, mirror_x, mirror_y, nombre):
        global reporteHTML
        for image in self.imagenes: #validar el nombre de la que se desea 
            filas = int(image.filas)
            columnas = int(image.columnas)
            factor_x = ancho//filas
            factor_y = alto//columnas
            
            for contador in range(image.cantidad_colores):
                coordenada_x = int(image.colores[contador].x)
                coordenada_y = int(image.colores[contador].y)
                if mirror_y:
                    coordenada_y = int(columnas) - int(coordenada_y) + 1
                if mirror_x:
                    coordenada_x = int(filas) - int(coordenada_x) + 1
             
                coordenada_x *= int(factor_x)
                coordenada_y *= int(factor_y) 
                contador_f = 0
                contador_y = 0
                if image.colores[contador].pintar:
                                                #x, y, factor_x, factor_y contenido.fillRect(0,4,33,33); ctx.fillStyle = "#FF0000";
                    reporteHTML += 'contenido.fillStyle = \"'+image.colores[contador].codigo+'\";'
                    reporteHTML += 'contenido.fillRect('+str(coordenada_x)+','+str(coordenada_y)+','+str(factor_x)+','+str(factor_y)+');\n'
                    #print(impL)
                    for i in range(factor_x*factor_y): 
                        img.put(image.colores[contador].codigo,(coordenada_x+contador_f, coordenada_y+contador_y))
                        contador_f += 1
                        if contador_f == factor_x:
                            contador_y += 1
                            contador_f = 0
                            
    #-----------GRAFICAR CON LOS TOKENS-------------            
    def graficar(self, img, ancho, alto, mirror_x, mirror_y):
        pinta = True
        coordenada_x = -1
        coordenada_y = -1
        token_fila = -1
        filas = 0
        columnas = 0
        token_tamano_fila = -1
        token_tamano_columna = -1
        for token in self.tokens:
            if token.get_lexema() == 'FILAS':
                token_tamano_fila = token.get_fila() 
            elif token_tamano_fila == token.get_fila() and token.tipo == self.tipos.NUMERO: #aca
                filas = token.get_lexema() 
            elif token.get_lexema() == 'COLUMNAS': #aca
                token_tamano_columna = token.get_fila()
            elif token_tamano_columna == token.get_fila() and token.tipo == self.tipos.NUMERO:
                columnas = token.get_lexema()    
            if token_fila < token.get_fila(): #donde guardo el numero de la fila es menor al numero de fila actual   saber si ya pase a la siguiente fila
                coordenada_x = -1
                coordenada_y = -1
                token_fila = -1
            if token.tipo == self.tipos.NUMERO:
                if coordenada_x == -1:
                    coordenada_x = token.get_lexema()
                    token_fila = token.get_fila()
                elif coordenada_y == -1 and token_fila == token.get_fila():
                    coordenada_y = token.get_lexema()    
            if token.tipo == self.tipos.BOOL:
                if token.get_lexema() == 'TRUE':
                    pinta = True
                elif token.get_lexema() == 'FALSE':
                    pinta = False          
            if token.tipo == self.tipos.COLOR and token_fila == token.get_fila() and pinta: #si se encuentran en la misma fila el token color y el token numero y es True
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
    
    def guardar_imagen(self):
        cantidad_colores = 0
        titulo = ''
        filas = 0
        columnas = 0
        ancho = 0
        alto = 0
        token_fila = -1
        id_token = -1
        lexema = ''
        numero_fila = -1
        id_celdas = -1
        valor = False
        tamano = len(self.tokens)
        cont = 0
        mirrorx = False
        mirrory = False
        doublemirror = False
        for token in self.tokens:
            if token.get_lexema() == 'TITULO':
                token_fila = token.get_fila()
                id_token = token.get_id()
                
            elif token.tipo == self.tipos.CADENA and token_fila == token.get_fila() and id_token == int(token.get_id()) - 2:
                titulo = token.get_lexema()
                titulo = titulo.replace('"','')       
                token_fila = -1
                id_token = -1
                
            elif token.get_lexema() == 'ANCHO':
                lexema = token.get_lexema()
                token_fila = token.get_fila()
                id_token = token.get_id()
                
            elif token.tipo == self.tipos.NUMERO and token_fila == token.get_fila() and id_token == int(token.get_id()) - 2 and lexema == 'ANCHO':
                ancho = token.get_lexema()   
                token_fila = -1
                id_token = -1
                
            elif token.get_lexema() == 'ALTO':
                lexema = token.get_lexema()
                token_fila = token.get_fila()
                id_token = token.get_id()
                
            elif token.tipo == self.tipos.NUMERO and token_fila == token.get_fila() and id_token == int(token.get_id()) - 2 and lexema == 'ALTO':
                alto = token.get_lexema()   
                token_fila = -1
                id_token = -1
                    
            elif token.get_lexema() == 'FILAS':
                lexema = token.get_lexema()
                token_fila = token.get_fila()
                id_token = token.get_id()
                
            elif token.tipo == self.tipos.NUMERO and token_fila == token.get_fila() and id_token == int(token.get_id()) - 2 and lexema == 'FILAS':
                filas = token.get_lexema()     
                token_fila = -1
                id_token = -1
                
            elif token.get_lexema() == 'COLUMNAS':
                lexema = token.get_lexema()
                token_fila = token.get_fila()
                id_token = token.get_id()
                
            elif token.tipo == self.tipos.NUMERO and token_fila == token.get_fila() and id_token == int(token.get_id()) - 2 and lexema == 'COLUMNAS':
                columnas = token.get_lexema()     
                token_fila = -1
                id_token = -1
                
            elif token.get_lexema() == 'CELDAS':
                lexema = token.get_lexema()
            
            elif token.get_lexema() == 'FILTROS':
                lexema = token.get_lexema()
                token_fila = token.get_fila()
                id_token = token.get_id()    
            
            if numero_fila < token.get_fila(): #saber si ya pase a la siguiente fila y reset coordenadas
                coordenada_x = -1
                coordenada_y = -1
                numero_fila = -1
                
            if token.tipo == self.tipos.NUMERO and lexema == 'CELDAS':
                if coordenada_x == -1:
                    coordenada_x = token.get_lexema()
                    numero_fila = token.get_fila()
                    id_celdas = token.get_id()
                elif coordenada_y == -1 and numero_fila == token.get_fila() and id_celdas == int(token.get_id()) - 2:
                    coordenada_y = token.get_lexema()    
            elif token.tipo == self.tipos.BOOL and lexema == 'CELDAS':
                if token.get_lexema() == 'TRUE':
                    valor = True
                elif token.get_lexema() == 'FALSE':
                    valor = False     
            
            elif token.tipo == self.tipos.COLOR and numero_fila == token.get_fila() and lexema == 'CELDAS': #si se encuentran en la misma fila el token color y el token numero y es True
                codigo_color = token.get_lexema()
                nuevo_color = Color(coordenada_x, coordenada_y, valor, codigo_color)
                self.colores.agregar_colores(nuevo_color)
                cantidad_colores += 1
                #print(coordenada_x, coordenada_y,valor,codigo_color)
            
            if token.get_lexema() == 'MIRRORX': 
                mirrorx = True
            elif token.get_lexema() == 'MIRRORY':
                mirrory = True
            elif token.get_lexema() == 'DOUBLEMIRROR':
                doublemirror = True
                
            if token.get_lexema() == '@@@@' or cont == tamano - 1 :
                #print(titulo, ancho, alto, filas, columnas)
                nueva_imagen = Imagen(titulo, filas, columnas, ancho, alto, mirrorx, mirrory, doublemirror, cantidad_colores)
                self.imagenes.append(nueva_imagen)
                
            cont += 1    
    
    def impr(self):
        i = 0
        for img in self.imagenes:
            print(img.titulo, img.ancho, img.alto, img.filas, img.columnas, img.mirrorx, img.mirrory, img.doublemirror)
            for i in range(img.cantidad_colores): 
                print(img.colores[i].x, img.colores[i].y, img.colores[i].pintar, img.colores[i].codigo)    
                
    def crear_reporte(self):
        global reporteHTML
        try: 
            file = open('Reporte.html','w')
            css = '''<style>section{ \n
            width:550px;
            position:relative;
            margin:auto;} </style>'''
            head = '<head><title>Reporte</title>'+css+'</head>\n'
            body = "<body> <font FACE=\"times new roman\">\n<section id = \"dibujo\">"
            body += "<canvas id = \"lienzo\" width = \"550\" height = \"550\"></canvas></section><script>\n"
            body += "var c = document.getElementById(\"lienzo\"); var contenido = c.getContext(\"2d\");\n"
            body += reporteHTML + "</script></body>"
            html = '<html>\n' + head + body + '</html>'
            file.write(html)
            print('Reporte generado exitosamente')
        except OSError:
            print("Error al crear el Reporte")
        finally:         
            file.close()
            webbrowser.open_new_tab('Reporte.html')
    
    def crear_reporte2(self):
        global reporteHTML
        try: 
            file = open('Reporte.html','w')
            head = '<head><title>Reporte</title></head>\n'
            body = "<body bgcolor=\"#B6F49D\"> <font FACE=\"times new roman\">"
            body += "<table width=\"475\" bgcolor=#B6F49D align=left> <tr> <td><font color=\"black\" FACE=\"times new roman\">" 
            body += "<p align=\"left\">Arnoldo Luis Antonio González Camey &nbsp;—&nbsp; Carné: 201701548</p></font>"
            body += "</td> </tr></table></br></br>" +   reporteHTML + "</body>"
            html = '<html>\n' + head + body + '</html>'
            file.write(html)
            print('Reporte generado exitosamente')
        except OSError:
            print("Error al crear el Reporte")
        finally:         
            file.close()
            webbrowser.open_new_tab('Reporte.html')

    def agregar_texto(self, text, color):
        global reporteHTML 
        reporteHTML += '<table width=\"800\" bgcolor=CDF9BA align=center> <tr> <td>'
        reporteHTML += '<font color=\"'+color+'\" FACE=\"courier, courier new, arial\"><p align=\"left\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + text + '</p></font>'
        reporteHTML += '</td> </tr> </table>'