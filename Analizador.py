from Token import Token
from Imagen import Imagen
import re
import webbrowser
#import imgkit

class Analizador():
    reporteHTML_token = ''
    reporteHTML_errores = ''
    reporteHTML_imagen = ''
    imagenes = []
    lexema = ''
    estado = 0
    tokens = []
    columna = 1
    fila = 1
    generar = True
    id = 0
    tipos = Token("lexema", -1, -1, -1, -1)
    colores = Imagen('',-1,-1,-1,-1,False,False,False,-1,-1)  
    
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
     
    def obtener_tokens(self):
        font = '<font color=\"#000000\" face=\"Courier\">'
        for x in self.tokens:
            if x.tipo != self.tipos.ERROR:
                self.reporteHTML_token += '<tr><td align=center>'+ font + x.get_tipo() + '</td><td align=center>'+ font + x.get_lexema() + '</td><td align=center>'+ font + str(x.get_fila()) + '</td><td align=center>'+ font + str(x.get_columna()) + '</td></tr>'
                print(x.get_lexema()," --> ",x.get_tipo(),' --> ',x.get_fila(), ' --> ',x.get_columna(), ' --> ',x.get_id())
    
    def obtener_errores(self):
        font = '<font color=\"#000000\" face=\"Courier\">'
        for x in self.tokens:
            if x.tipo == self.tipos.ERROR:
                self.reporteHTML_errores += '<tr><td align=center>'+ font + x.get_lexema() + '</td><td align=center>'+ font + str(x.get_fila()) + '</td><td align=center>'+ font + str(x.get_columna()) + '</td></tr>'
                print(x.get_lexema()," --> ",x.get_fila(), ' --> ',x.get_columna(),'--> Error Lexico')
                            
    # Original --> False False True
    # Mirror_x --> True False False
    # Mirror_y --> False True False
    # Double_M --> False False True 
    #-----------GRAFICAR CON CLASES Y RECTANGULOS-------------
    def graficar_imagen(self, lienzo, ancho, alto, mirror_x, mirror_y, double_mirror, nombre, tkinter):
        contador = 0
        self.reporteHTML_imagen = ''
        for image in self.imagenes:
            while contador <= len(image.colores) - 1:
                if image.cantidad_colores == contador:
                    break
                if image.titulo == nombre:
                    if mirror_x:
                        if image.mirrorx is False:
                            tkinter.messagebox.showinfo(message = "El Filtro MIRRORX no se puede mostrar", title = "Alerta")   
                            return
                    if mirror_y:
                        if image.mirrory is False:
                            tkinter.messagebox.showinfo(message = "El Filtro MIRRORY no se puede mostrar", title = "Alerta")   
                            return 
                    if double_mirror:
                        if image.doublemirror is False:
                            tkinter.messagebox.showinfo(message = "El Filtro DOUBLEMIRROR no se puede mostrar", title = "Alerta")   
                            return     
                    filas = int(image.filas)
                    columnas = int(image.columnas)
                    factor_x = ancho//filas
                    factor_y = alto//columnas
                    if image.indice_imagen == image.colores[contador].indice_imagen:
                        aux_x = int(image.colores[contador].x) 
                        aux_y = int(image.colores[contador].y)
                        if mirror_x:
                            aux_x = int(filas) - int(aux_x) + 1
                        if mirror_y:
                            aux_y = int(columnas) - int(aux_y) + 1
                        if double_mirror:
                            aux_x = int(filas) - int(aux_x) + 1 
                            aux_y = int(columnas) - int(aux_y) + 1  
                        coordenada_x = aux_x * factor_x
                        coordenada_y = aux_y * factor_y
                        
                        y_arriba = coordenada_y + factor_y
                        x_abajo = coordenada_x + factor_x
                        if image.colores[contador].pintar:
                            self.reporteHTML_imagen += 'contenido.fillStyle = \"'+image.colores[contador].codigo+'\";'
                            self.reporteHTML_imagen += 'contenido.fillRect('+str(coordenada_x)+','+str(coordenada_y)+','+str(factor_x)+','+str(factor_y)+');\n'
                            #print(coordenada_x, y_arriba, x_abajo, coordenada_y, image.colores[contador].codigo)
                            lienzo.create_rectangle(coordenada_x, y_arriba, x_abajo, coordenada_y, width = 0, fill = image.colores[contador].codigo)
                contador += 1
     
    def guardar_imagen(self):
        titulo = ''
        filas = 0
        columnas = 0
        ancho = 0
        alto = 0
        cantidad_colores = 0
        mirrorx = False
        mirrory = False
        doublemirror = False
        valor = False        
        indice_imagen = 0
        tamano = len(self.tokens)
        counter = 0        
        id_token = -1    
        id_coordenada = -1
        lexema = ''
        entro_primera_coordenada = False   
        for token in self.tokens:
            if token.get_lexema() == 'TITULO':
                id_token = token.get_id()
                
            elif token.tipo == self.tipos.CADENA  and id_token == int(token.get_id()) - 2:
                titulo = token.get_lexema()
                titulo = titulo.replace('"','')      
                id_token = -1
                
            elif token.get_lexema() == 'ANCHO':
                lexema = token.get_lexema()
                id_token = token.get_id()
                
            elif token.tipo == self.tipos.NUMERO and id_token == int(token.get_id()) - 2 and lexema == 'ANCHO':
                ancho = token.get_lexema()   
                id_token = -1
                
            elif token.get_lexema() == 'ALTO':
                lexema = token.get_lexema()
                id_token = token.get_id()
                
            elif token.tipo == self.tipos.NUMERO and id_token == int(token.get_id()) - 2 and lexema == 'ALTO':
                alto = token.get_lexema()   
                id_token = -1
                    
            elif token.get_lexema() == 'FILAS':
                lexema = token.get_lexema()
                id_token = token.get_id()
                
            elif token.tipo == self.tipos.NUMERO and id_token == int(token.get_id()) - 2 and lexema == 'FILAS':
                filas = token.get_lexema()     
                id_token = -1
                
            elif token.get_lexema() == 'COLUMNAS':
                lexema = token.get_lexema()
                id_token = token.get_id()
                
            elif token.tipo == self.tipos.NUMERO and id_token == int(token.get_id()) - 2 and lexema == 'COLUMNAS':
                columnas = token.get_lexema()     
                id_token = -1
                
            elif token.get_lexema() == 'CELDAS':
                lexema = token.get_lexema()
                id_token = token.get_id()
            
            elif token.get_lexema() == 'FILTROS':
                lexema = token.get_lexema()
                id_token = token.get_id()    
            
            if id_coordenada == int(token.get_id()) - 9: #saber si ya toca otra linea de colores
                coordenada_x = -1
                coordenada_y = -1
                
            if token.tipo == self.tipos.NUMERO and lexema == 'CELDAS' :
                #LAS PRIMERAS COORDENADAS
                if coordenada_x == -1 and id_token == int(token.get_id()) - 4 and entro_primera_coordenada == False:
                    coordenada_x = token.get_lexema()
                    id_coordenada = token.get_id()
                    
                elif coordenada_y == -1 and id_token == int(token.get_id()) - 6 and entro_primera_coordenada == False:
                    coordenada_y = token.get_lexema() 
                    entro_primera_coordenada = True 
                    
                #SIGUIENTES CELDAS
                if coordenada_x == -1 and id_coordenada == int(token.get_id()) - 10:
                    coordenada_x = token.get_lexema()
                    id_coordenada = token.get_id()
                    
                elif coordenada_y == -1 and id_coordenada == int(token.get_id()) - 2:
                    coordenada_y = token.get_lexema() 
                    
            elif token.tipo == self.tipos.BOOL and lexema == 'CELDAS' and id_coordenada == int(token.get_id()) - 4:
                if token.get_lexema() == 'TRUE':
                    valor = True
                elif token.get_lexema() == 'FALSE':
                    valor = False     
            
            elif token.tipo == self.tipos.COLOR and lexema == 'CELDAS' and id_coordenada == int(token.get_id()) - 6:
                codigo_color = token.get_lexema()
                self.colores.agregar_color(coordenada_x, coordenada_y, valor, codigo_color, indice_imagen)
                cantidad_colores += 1
                #print(coordenada_x, coordenada_y,valor,codigo_color)
            
            if token.get_lexema() == 'MIRRORX': 
                mirrorx = True
            elif token.get_lexema() == 'MIRRORY':
                mirrory = True
            elif token.get_lexema() == 'DOUBLEMIRROR':
                doublemirror = True
                
            if token.get_lexema() == '@@@@' or counter == tamano - 1 :
                nueva_imagen = Imagen(titulo, filas, columnas, ancho, alto, mirrorx, mirrory, doublemirror ,cantidad_colores, indice_imagen)
                self.imagenes.append(nueva_imagen)
                indice_imagen += 1
                #REINICIO DE LAS VARIABLES
                id_token = -1    
                id_coordenada = -1
                lexema = ''
                entro_primera_coordenada = False   
                valor = False   
                cantidad_colores = 0
                #print(titulo, ancho, alto, filas, columnas)
                
            counter += 1    
    
    def opciones_imagenes(self, combo):
        nombres = []
        values = list(combo["values"])
        for img in self.imagenes:
            nombres.append(img.titulo) 
        combo["values"] = values + nombres
    
    def imprimir_imagen(self):
        i = 0
        for img in self.imagenes:
            print(img.titulo, img.ancho, img.alto, img.filas, img.columnas, img.mirrorx, img.mirrory, img.doublemirror, img.cantidad_colores, img.indice_imagen)
            while i <= len(img.colores) - 1:
                if img.cantidad_colores == i:
                    break
                if img.indice_imagen == img.colores[i].indice_imagen:
                    print(img.colores[i].x, img.colores[i].y, img.colores[i].pintar, img.colores[i].codigo, img.colores[i].indice_imagen)    
                i += 1
                    
    def crear_reporte_imagen(self):
        try: 
            file = open('Imagen.html','w')
            css = '''<style>section{ \n
                        width:550px;
                        position:relative;
                        margin:auto;} </style>'''
            head = '<head><title>Imagen</title>'+css+'</head>\n'
            body = "<body>\n<section id = \"dibujo\">"
            body += "<canvas id = \"lienzo\" width = \"550\" height = \"550\"></canvas></section><script>\n"
            body += "var c = document.getElementById(\"lienzo\"); var contenido = c.getContext(\"2d\");\n"
            body += self.reporteHTML_imagen + "</script></body>"
            html = '<html>\n' + head + body + '</html>'
            file.write(html)
            print('Imagen guardada exitosamente')
        except OSError:
            print("Error al guardar la imagen")
        finally:         
            file.close()
            webbrowser.open_new_tab('Imagen.html')
        #with open('Imagen.html') as f:
            #imgkit.from_file(f, 'out.jpg')
          
    def crear_reporte_token(self):
        try: 
            file = open('Reporte_Tokens.html','w')
            head = '<head><title>Reporte Token</title></head>\n'
            body = "<body bgcolor=\"#B6F49D\">"
            body += "<table width=\"600\" bgcolor=#B6F49D align=left> <tr> <td><font color=\"black\" FACE=\"Courier\">" 
            body += "<p align=\"left\">Arnoldo Luis Antonio González Camey &nbsp;—&nbsp; Carné: 201701548</p></font>"
            body += "</td> </tr></table></br></br>"
            body += ''' <h2 align=\"center\"><font color=\"black\" FACE=\"Courier\">Reporte de Tokens</h2>
                    <table width=\"1000\" bgcolor=#CDF9BA align=center style="border:5px dashed brown">
                    <tr>
                        <td align=center><font color=\"#000000\" face=\"Courier\"><strong>Token</strong></td>
                        <td align=center><font color=\"#000000\" face=\"Courier\"><strong>Lexema</strong></td>
                        <td align=center><font color=\"#000000\" face=\"Courier\"><strong>Fila</strong></td>                                            
                        <td align=center><font color=\"#000000\" face=\"Courier\"><strong>Columna</strong></td>
                    </tr>''' 
            body += self.reporteHTML_token +'</table></body>'
            html = '<html>\n' + head + body + '</html>'
            file.write(html)
            print('Reporte de Tokens generado exitosamente')
        except OSError:
            print("Error al crear el Reporte de Tokens")
        finally:         
            file.close()
            webbrowser.open_new_tab('Reporte_Tokens.html')
        
    def crear_reporte_errores(self):
        try: 
            file = open('Reporte_Errores.html','w')
            head = '<head><title>Reporte Errores</title></head>\n'
            body = "<body bgcolor=\"#B6F49D\">"
            body += "<table width=\"600\" bgcolor=#B6F49D align=left> <tr> <td><font color=\"black\" FACE=\"Courier\">" 
            body += "<p align=\"left\">Arnoldo Luis Antonio González Camey &nbsp;—&nbsp; Carné: 201701548</p></font>"
            body += "</td> </tr></table></br></br>"
            body += ''' <h2 align=\"center\"><font color=\"black\" FACE=\"Courier\">Reporte de Errores</h2>
                    <table width=\"800\" bgcolor=#CDF9BA align=center style="border:5px dashed brown">
                    <tr>
                        <td align=center><font color=\"#000000\" face=\"Courier\"><strong>Caracter</strong></td>
                        <td align=center><font color=\"#000000\" face=\"Courier\"><strong>Fila</strong></td>                                            
                        <td align=center><font color=\"#000000\" face=\"Courier\"><strong>Columna</strong></td>
                    </tr>''' 
            body += self.reporteHTML_errores +'</table></body>'
            html = '<html>\n' + head + body + '</html>'
            file.write(html)
            print('Reporte de Errores generado exitosamente')
        except OSError:
            print("Error al crear el Reporte de Errores")
        finally:         
            file.close()
            webbrowser.open_new_tab('Reporte_Errores.html')