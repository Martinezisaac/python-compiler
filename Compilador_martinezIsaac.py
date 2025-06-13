# Martinez Isaac
# Compilador | Ingenieria en computacion

# Analisis Sintactico
# Analsiis Semantico
# Analisis Lexico
# Generacion de codigo

# Libreria
import re  # Importamos el modulo de expresiones regulares

# Analizazdor Lexico
    # Analiza el codigo fuente y devuelve una lista de tokens validos, dicha lista es una tupla
    # la cual contiene tanto el tipo del token como su valor

def analizadorLexico(codigoFuente):

    tokens = [ # Definir los tipos de tokens y sus respectivas expresiones regulares
        ('NUMERO', r'\d+(\.\d*)?'),  # Numeros enteros o decimales
        ('CHAR', r'\'[^\']\''),  # Caracter individual, e.g., 'a'
        ('STRING', r'\'[^\']*\'|\"[^\"]*\"'),  # Cadenas entre comillas simples o dobles
        ('COMENTARIO', r'//[^\n]*|/\*[\s\S]*?\*/'),  # Comentarios de linea o bloque
        ('ID', r'[A-Za-z_]\w*'),  # Identificadores: letras o guiones bajos seguidos de letras, digitos o _
        ('OPERADOR', r'[+\-*/=<>!&|]|==|!=|<=|>=|&&|\|\|'),  # Operadores aritmeticos, logicos y relacionales
        ('PUNTO_COMA', r';'),  # Punto y coma
        ('PARENTESIS_IZQ', r'\('),  # Parentesis izquierdo
        ('PARENTESIS_DER', r'\)'),  # Parentesis derecho
        ('LLAVE_IZQ', r'\{'),  # Llave izquierda
        ('LLAVE_DER', r'\}'),  # Llave derecha
        ('COMA', r','),  # Coma
        ('ESPACIO', r'[ \t]+'),  # Espacios en blanco o tabulaciones (se ignoran)
        ('NUEVA_LINEA', r'\n'),  # Saltos de linea
        ('PREPROCESADOR_DEFINE', r'#define'),  # Directiva de preprocesador: #define
        ('PREPROCESADOR', r'#\s*include\s*<[\w\.]+>'),  # Inclusion de librerias con <>
        ('PREPROCESADOR_INCLUDE', r'#\s*include\s*\"[\w\.]+\"'),  # Inclusion de archivos con comillas
        ('MISMATCH', r'.'),  # Cualquier otro caracter no reconocido
    ]

    # Variables auxiliares
    tok_regex = '|'.join(f'(?P<{nombre}>{pattern})' for nombre, pattern in tokens) # Combinamos todas las expresiones regulares en una sola 
    obtenerToken = re.compile(tok_regex).match # Compilamos la expresion regular y obtenemos la funcion de coincidencia
    posicion = 0  # Posicion actual en el codigo fuente
    tokens = []  # Lista donde se almacenan los tokens encontrados
    numero_linea = 1  # Contador de lineas

    while posicion < len(codigoFuente): # Recorrer todo el codigo proporcionado a la funcion
        mo = obtenerToken(codigoFuente, posicion)  # Obtener un match de acuerdo a la posicion

        if not mo: # Validar si no existe un match
            posicion += 1 # Actualizar la posicion para ecitar un bucle infinito
            continue # Continuar con el analisis

        tipo = mo.lastgroup  # Tipo del token encontrado ( de acuerdo con la lista de tokens que se declaro antes )
        valor = mo.group()  # Valor del texto que coincide con el tipo del tokebn

        if tipo == 'NUEVA_LINEA': # Validar si existe una linea nueva
            # Si encontramos un salto de linea, aumentamos el contador de lineas
            numero_linea += 1 # Actualizar el contador de lineas
            posicion = mo.end() # Ignorar la linea nueva

        elif tipo == 'ESPACIO': # Validar si existen espacios en el codigo
            posicion = mo.end() # Ignorar el espacio

        elif tipo == 'MISMATCH': # Validar si existen tokens no validos

            # MISMATCH es un tipo de token auxiliar para almacenar todos aquellos tokens que no coincidan
            # con los tokens previamente declarados, funciona como un almacen
            
            print(f'Error: Token inesperado "{valor}" en linea {numero_linea}') # Mostrar mensaje de error
            break # Termianr el analisis

        else: # Entonces paso todas las pruebas y se filtraron tipos de tokens no deseados, por lo que quedan tokens validos en el codigo
            tokens.append((tipo, valor)) # Agregar los tokens validos a la lista
            posicion = mo.end()

    return tokens # Devoler la tupla de los tokens con su tipo y valor



# Analizador sintactico
    # Esta clase implementa un analizador sintactico que procesa una lista de tokens ( los cuales deben de ser procesados 
    # previamente por la funciona del analizador lexico, dicha funcion devuelve la tupla con el tipo y valor de cada token).
    # El objetivo es construir un arbol de sintaxis abstracta (AST) de un lenguaje C

class analizadorSintactico: # Constructor: recibe una lista de tokens generada por un analizador lexico
    
    def __init__(self, tokens):
        # Variables auxiliares
        self.tokens = tokens # Lista de tokens para analizar
        self.posicion = 0 # Posicion actual en la lista de tokens

    # Devuelve el token en la posicion actual, o (None, None) si estamos al final
    def tokenActual(self):
        return self.tokens[self.posicion] if self.posicion < len(self.tokens) else (None, None)

    # Obtiene el token que sigue al actual sin avanzar la posicion
    def obtenerSiguienteToken(self):
        return self.tokens[self.posicion + 1] if self.posicion + 1 < len(self.tokens) else (None, None)

    # Se verifica si el token actual coincide con el tipo esperado
        # Si coincide, entonces se avanza a la posicion y se devuelve el valor del token, yu sino, entonces devuelve None
    def match(self, expected_type, expected_valor=None):
        tipoToken, valorToken = self.tokenActual() # Obtener el tipo y el valor del token de la tupla
        if tipoToken == expected_type and (expected_valor is None or valorToken == expected_valor):
            self.posicion += 1 # Actualizar la posicion
            return valorToken # Devoler el valor del token
        
        return None # Si no es la salida esperada, entonces no se devuelve nada 

    # Este es el metodo principal, el cual inicia el analisis sintactico
    def analizarSintaxis(self):
        
        # Variable auxiliar
        parametros = [] # Lista auxiliar para gaurdar los paramtros encontrados

        while self.posicion < len(self.tokens):
            
            while self.posicion < len(self.tokens) and self.tokenActual()[0] in ('COMENTARIO', 'NUEVA_LINEA'): # Saltar comentarios y lineas nuevas
                self.posicion += 1 # Actualiza la posicion 
            if self.posicion >= len(self.tokens):
                break # Terminar
            
            declaracion = self.programa() # Obtener una declaracion
            if declaracion: # Validar si existe una declaracion
                parametros.append(declaracion) # Actualizar la lista de parametros, puesto que han sido encontados
            else:
                # Si no se pudo analizar correctamente, avanza para evitar un bucle infinito
                # y reporta un error de sintaxis
                curr_posicion = self.posicion # Actualiza la posicion actual
                self.posicion += 1 # Actualizaa la posicion
                if curr_posicion == self.posicion - 1: # 
                    print(f"Error de sintaxis en la posicion {curr_posicion}, token: {self.tokens[curr_posicion] if curr_posicion < len(self.tokens) else 'EOF'}") # mensaje de erore
        
        return parametros # Devolver los parametros encontrados

    # Funcion para analizar un programa
    def programa(self):
        # Variables auxiliares
        function = self.declaracionFuncion() # Obtener codigo para analizar
        if function: # Si existe un codigo
            return function # Devolver el codigo
        return self.declaracion()

    # Analizar la declaracion de una funcion
        # por ejemplo "int main() { "hola munod, aqui puede haber codigo" }"
    def declaracionFuncion(self):
        
        while self.posicion < len(self.tokens) and self.tokenActual()[0] in ('COMENTARIO', 'NUEVA_LINEA', 'PREPROCESADOR'): # Salta comentarios, lineas nuevas y directivas de preprocesador
            self.posicion += 1 # Actualizar la posicion
        
        if self.posicion >= len(self.tokens):
            return None
            
        tipoToken, valorToken = self.tokenActual() # Obtener el tipo y el valor del token

        # Verifica si es una declaracion de funcion (comienza con un tipo de dato)
        if tipoToken == 'ID' and valorToken in ['int', 'float', 'double', 'char', 'boolean', 'String', 'void']:
            # Variables auxiliares
            posicionInicial = self.posicion # obtener la posicion inicial
            tipoRetorno = self.match('ID') # Tipo de retorno de la funcion
            nombre = self.match('ID') # Nombre de la funcion

            if not self.match('PARENTESIS_IZQ'): # Verificar si existe un parentesis inicial (el parentesis izquierdo)
                self.posicion = posicionInicial  # Se restaura la posicion si no es funcion
                return None

            # Procesar los parametros de la funcion
            parametros = [] # Variable auxiliar para guardar los parametros dentro de la funcion

            if self.tokenActual()[0] != 'PARENTESIS_DER': # Validar si existe un parentesis derecho
                
                while self.posicion < len(self.tokens): # Si no hay parentesis derecho, entonces significa que hay parametros
                    tipoParametro = self.match('ID')  # Tipo del parametro
                    if not tipoParametro: # Si no pasa la expresion regular del token
                        break # Entonces termina
                    
                    param_nombre = self.match('ID') # Nombre del parametro
                    if not param_nombre: # Si no pasa la expresion regular del token
                        break # Entonces termina
                    
                    parametros.append((tipoParametro, param_nombre)) # Obtener parametros (IDs obtenidos dentro de los parentesis previamente validados)
                    
                    
                    if self.tokenActual()[0] != 'COMA': # Validar si no existe una coma
                        break # Terminar de procesar
                    else: # Entonces existe una coma
                        self.match('COMA')  # Consumir la coma y continuar

            
            if not self.match('PARENTESIS_DER'): # Verificar parentesis derecho de cierre
                print("Error: Se esperaba ')' en declaracion de funcion") # Imprimir mensaje de error
                return None # No devolver parametros

            if not self.match('LLAVE_IZQ'): # Verificar llave izquierda (inicio del cuerpo de la funcion)
                print("Error: Se esperaba '{' para iniciar el cuerpo de la funcion") # Imprimir mensaje de error
                return None # No devolver parametros

            cuerpo = [] # Lista auxiliar para guardar el cuerpo de la funcion
            contadorLlaves = 1  # Variable auxiliar para contar las llaves
            # Previamente se encontro una, la cual era la llave izquierda, se encontro posteriormente de encontrar el parentesis
            # derecho de la declaracion de la fucnon
            
            # Analizar el cuerpo de la funcion
                # Hasta ahora se ha encontrado e identificado los paramteros de la funcion, de igual manera se sabe que existe
                # una llave abierta lo cual indica que ahora es posible analizar el cuerpo de la funcion, esto hasta que se encuentre
                # un token de cierre de llave, antes de eso, todo se considera cuerpo de la funcion

            while contadorLlaves > 0 and self.posicion < len(self.tokens): # Proceso del cuerpo de la funcion, controlando el balance de llaves
                if self.tokenActual()[0] == 'LLAVE_IZQ': # Validar si el token actual es la llave izquierda
                    contadorLlaves += 1 #Aumentar el contador de llaves
                    self.posicion += 1 # Actualizar la posicion

                elif self.tokenActual()[0] == 'LLAVE_DER': # Validar si el token actual es la llave derecha
                    contadorLlaves -= 1 # Reducir el contador de llaves
                    if contadorLlaves == 0:  # Se encontro la llave de cierre que corresponde a la funcion
                        break # Terminar
                    self.posicion += 1 # Si no se encontro la llave, encontes actualizar la posicion
                
                else: # Entonces no se econtraron llaves, por lo que significa que se analiza el cuerpo de la funcion
                    
                    declaracion = self.declaracion() # Analizar una declaracion dentro del cuerpo de la funcion
                    if declaracion: # Validar si existe una declaracion
                        cuerpo.append(declaracion) # Agregar a la lista el cuerpo de la fucnion
                    else: # Si no existe una declaracion
                        self.posicion += 1  # Entonces avanzar para evitar bucle infinito

            
            if not self.match('LLAVE_DER'): # Verificar llave derecha para terminar de analizar
                print("Error: Se esperaba '}' para cerrar el cuerpo de la funcion") # Mostrar mensaje de error porque se esperaba la llave derecha
                return None # No devolver nada

            return ('declaracionFuncion', tipoRetorno, nombre, parametros, cuerpo) # Retornar la estructura de la funcion analizada

        return None

    # Analizar una declaracion
        # Una declaracion puede ser:
        # - Una variable
        # - Asignacion
        # - Llamada de funcion
        # - Estructuras de control, etc
    def declaracion(self):
        
        while self.posicion < len(self.tokens) and self.tokenActual()[0] in ('COMENTARIO', 'NUEVA_LINEA'): # Salta comentarios y lineas nuevas
            self.posicion += 1 # Actualizar la posicion
        
        if self.posicion >= len(self.tokens):
            return None
            
        tipoToken, valorToken = self.tokenActual() # Obtener el tipo y el valor del token actual

        if tipoToken == 'ID' and valorToken in ['int', 'float', 'double', 'char', 'boolean', 'String']: #Validar una declaracion de variable
            tipo = self.match('ID') # Tipo de la variable
            nombre = self.match('ID') # Nombre de la variable

            # Verificar si hay inicializacion 
                # por ejemplo: int x = 5;
            if self.tokenActual() == ('OPERADOR', '='):
                self.match('OPERADOR', '=')
                valor_inicial = self.expresion()  # Obtener el valor de inicializacion
                self.match('PUNTO_COMA')
                return ('declaracionInicializacion', tipo, nombre, valor_inicial) # Devolver la declaracion
            else: # Entonces solo es una declaracion, sin inicializacion, es decir que no se le asigna un valor, por ejemplo: int x;
                self.match('PUNTO_COMA')
                return ('declaracion', tipo, nombre)

        elif tipoToken == 'ID' and self.obtenerSiguienteToken()[0] == 'OPERADOR' and self.obtenerSiguienteToken()[1] == '=': # Validar una asignacion de variable (por ejemplo un x = 10)
            nombre = self.match('ID') # Nombre de la variable
            self.match('OPERADOR', '=')
            expr = self.expresion() # Valor a asignar
            self.match('PUNTO_COMA')
            return ('asignacion', nombre, expr) 

        elif tipoToken == 'ID' and self.obtenerSiguienteToken()[0] == 'PARENTESIS_IZQ': # Validar una llamada a una funcion como declaracion 
            func_nombre = self.match('ID') # Nombre de la funcion
            self.match('PARENTESIS_IZQ')
            
            argumentos = [] # Variable auxiliar para guiardar los argumentos obtenidos

            if self.tokenActual()[0] != 'PARENTESIS_DER': # Validar que el token actual sea diferente del parentesis de cierre
                arg = self.expresion() # Obtener la expresion antes de encontrar el parentesis de cierre
                if arg: # Validar si existe un argumento
                    argumentos.append(arg) # Agregaar argumentos
                while self.tokenActual()[0] == 'COMA': # Validar si se encuentra una coma
                    self.match('COMA')
                    arg = self.expresion()
                    if arg:
                        argumentos.append(arg)
            self.match('PARENTESIS_DER')
            self.match('PUNTO_COMA')
            return ('llamadaFuncion_declaracion', func_nombre, argumentos) # Devolver una llamada de funcion

        elif tipoToken == 'ID' and valorToken == 'if': # Validar el IF
            self.match('ID', 'if')
            if not self.match('PARENTESIS_IZQ'): # Validar si existe un parentesis de inciio
                print("Error: Se esperaba '(' despues de 'if'") # Mostrar mensaje de error porque no existe parentesis izquierdo
                return None

            condition = self.expresion() # Analizar la condicion del if

            if not self.match('PARENTESIS_DER'):
                print("Error: Se esperaba ')' despues de la condicion") # Mostrar mensaje de error porque se esperaba el parentesis de cierre
                return None

            if not self.match('LLAVE_IZQ'):
                print("Error: Se esperaba '{' para iniciar el bloque if") # Mostrar mensaje de error porque se esperaba la llave de inicio del if
                return None

            if_cuerpo = [] # Variable auxiliar para guardar el contenido de un IF

            while self.tokenActual()[0] != 'LLAVE_DER' and self.posicion < len(self.tokens): # Analizar el cuerpo del if hasta encontrar la llave de cierre
                declaracion = self.declaracion() # Obtener la declaracion
                if declaracion: # Validar si existe una delcaracion
                    if_cuerpo.append(declaracion) # Entonces el if tiene contenido, se guarda en la lista
                else: # Entonces no existe un cuerpo dentro del if
                    self.posicion += 1  # Avanzar para evitar bucle infinito

            if not self.match('LLAVE_DER'): # Si no se encontro la llave de cierre
                print("Error: Se esperaba '}' para cerrar el bloque if") # Mostrar mensjae de error
                return None # No devolver nada

            if self.tokenActual() == ('ID', 'else'): # Verificar si hay un bloque else
                self.match('ID', 'else') # Buscar match

                if not self.match('LLAVE_IZQ'): # Verificar si existe la llave de inicio
                    print("Error: Se esperaba '{' para iniciar el bloque else") # Mostrar mensaje de error porque no existe la llave izquierda
                    return None

                else_cuerpo = [] # Lista auxiliar para guardar el cuerpo de un else

                while self.tokenActual()[0] != 'LLAVE_DER' and self.posicion < len(self.tokens): # Ejecutar hasta encontrar la llave de cierre
                    declaracion = self.declaracion() # Obtener la declaracion
                    if declaracion: # Validar si existe una declaracion
                        else_cuerpo.append(declaracion) # Guardar la declracion dentro del else en la lista
                    else:
                        self.posicion += 1  # Avanzar para evitar bucle infinito

                if not self.match('LLAVE_DER'): # Validar si se encontro una llave derecha
                    print("Error: Se esperaba '}' para cerrar el bloque else") # Mostrar mensaje de error porque no se encontro la llave de cierre 
                    return None

                return ('if_else', condition, if_cuerpo, else_cuerpo)

            # Solo if sin else
            return ('if', condition, if_cuerpo)

        elif tipoToken == 'ID' and valorToken == 'while': # Validar la estructura de un while
            self.match('ID', 'while')
            if not self.match('PARENTESIS_IZQ'): # Validar que exista un parentesis izquierdo
                print("Error: Se esperaba '(' despues de 'while'") # Mostrar mensaje de error porque no existe parentesis izquierdo despues del ID
                return None

            condition = self.expresion() # Obtener la condicion del while

            if not self.match('PARENTESIS_DER'): # Validar si no se encuentra el parentesis de cierre
                print("Error: Se esperaba ')' despues de la condicion") # Mostrar mensaje de erro porque no se encontro el parentesis de cierre del while
                return None

            # Verifica si es la parte final de un do-while (ejemplo: do { ... } while (condicion);)
            if self.tokenActual()[0] == 'PUNTO_COMA': # Validar si existe un punto y coma
                self.match('PUNTO_COMA')
                return ('do_while_end', condition) # Devoler el do while

            if not self.match('LLAVE_IZQ'): # Validar si existe un llave izquierda
                print("Error: Se esperaba '{' para iniciar el bloque while") # Mostrar mensaje de error porque se necesita de una llave para iniciar el ciclo de un while depsues del id
                return None

            # Analizar el cuerpo del bucle while
            cuerpo = []
            while self.tokenActual()[0] != 'LLAVE_DER' and self.posicion < len(self.tokens):
                declaracion = self.declaracion()
                if declaracion:
                    cuerpo.append(declaracion)
                else:
                    self.posicion += 1  # Avanzar para evitar bucle infinito

            if not self.match('LLAVE_DER'):
                print("Error: Se esperaba '}' para cerrar el bloque while")
                return None

            return ('while', condition, cuerpo)

        # Estructura for (ejemplo: for (int i = 0; i < 10; i++) { ... })
        elif tipoToken == 'ID' and valorToken == 'for':
            self.match('ID', 'for')
            if not self.match('PARENTESIS_IZQ'):
                print("Error: Se esperaba '(' despues de 'for'")
                return None

            # Analizar la inicializacion del for
            init = None
            if self.tokenActual()[0] == 'ID' and self.tokenActual()[1] in ['int', 'float', 'double', 'char', 'boolean', 'String']:
                # Declaracion e inicializacion en el for (ejemplo: int i = 0)
                tipo = self.match('ID')
                nombre = self.match('ID')
                if self.tokenActual() == ('OPERADOR', '='):
                    self.match('OPERADOR', '=')
                    valor_inicial = self.expresion()
                    init = ('declaracionInicializacion', tipo, nombre, valor_inicial)
                else:
                    init = ('declaracion', tipo, nombre)
            elif self.tokenActual()[0] == 'ID':
                # Asignacion simple en el for (ejemplo: i = 0)
                nombre = self.match('ID')
                if self.tokenActual() == ('OPERADOR', '='):
                    self.match('OPERADOR', '=')
                    expr = self.expresion()
                    init = ('asignacion', nombre, expr)

            self.match('PUNTO_COMA')

            # Analizar la condicion del for
            condition = self.expresion()
            self.match('PUNTO_COMA')

            # Analizar el incremento del for
            increment = None
            if self.tokenActual()[0] == 'ID':
                increment = self.expresion()

            if not self.match('PARENTESIS_DER'):
                print("Error: Se esperaba ')' despues de la condicion del for")
                return None

            if not self.match('LLAVE_IZQ'):
                print("Error: Se esperaba '{' para iniciar el bloque for")
                return None

            # Analizar el cuerpo del bucle for
            cuerpo = []
            while self.tokenActual()[0] != 'LLAVE_DER' and self.posicion < len(self.tokens):
                declaracion = self.declaracion()
                if declaracion:
                    cuerpo.append(declaracion)
                else:
                    self.posicion += 1  # Avanzar para evitar bucle infinito

            if not self.match('LLAVE_DER'):
                print("Error: Se esperaba '}' para cerrar el bloque for")
                return None

            return ('for', init, condition, increment, cuerpo) # Devoler el for encontrado

        elif tipoToken == 'ID' and valorToken == 'do': # Validar estructura de un do-while
            self.match('ID', 'do') # Validar mediante regex 
            
            if not self.match('LLAVE_IZQ'):
                print("Error: Se esperaba '{' para iniciar el bloque do-while") # Imprimir mensaje d error
                return None # No devolver nada

            cuerpo = [] # Variable auxiliar para guardar el cuerpo
            
            while self.tokenActual()[0] != 'LLAVE_DER' and self.posicion < len(self.tokens): # Analizar el cuerpo del ciclo do-while
                declaracion = self.declaracion() # Obtener la declracion
                if declaracion: # Validar que si exista una declaracion
                    cuerpo.append(declaracion) # Guardar la delcaracion
                else:
                    self.posicion += 1  # Avanzar la posciion para evitar bucle infinito

            if not self.match('LLAVE_DER'):
                print("Error: Se esperaba '}' para cerrar el bloque do-while") # Imprimir mensaje de error
                return None # Retornar nada

            # Verificar que sigue un 'while' despues del bloque 'do'
            if not (self.tokenActual()[0] == 'ID' and self.tokenActual()[1] == 'while'):
                print("Error: Se esperaba 'while' despues del bloque do") # Imprimir mensaje de error
                return None # Retornar nada

            self.match('ID', 'while')
            
            if not self.match('PARENTESIS_IZQ'):
                print("Error: Se esperaba '(' despues de 'while' en do-while") # Imprimir mensaje de error
                return None # Retornar nada

            # Analizar la condicion del do-while
            condition = self.expresion()

            if not self.match('PARENTESIS_DER'):
                print("Error: Se esperaba ')' despues de la condicion en do-while") # Imprimir mensaje de error
                return None # Retornar nada

            self.match('PUNTO_COMA')
            return ('do_while', condition, cuerpo) # Devoler el do-while encontrado

        # Declaracion return (ejemplo: return x+y;)
        elif tipoToken == 'ID' and valorToken == 'return':
            self.match('ID', 'return')
            expr = self.expresion()  # Analizar la expresion que se retorna
            self.match('PUNTO_COMA')
            return ('return', expr)

        return None

    def expresion(self):
        return self.analizarSintaxis_expresion()

    # Funcion para analizar una expresion recursivamente usando precedencia de operadores
        # Se implementa el algoritmo de pratt para realizar un analisis con precedencia
    def analizarSintaxis_expresion(self, min_precedente=0):
        left = self.term()  # Analiza el termino izquierdo
        if not left: # Si no existe termino izquierdo
            return None # Entonces devolver nada

        while True: # Iterar mientras existan operadores y se tenga precedencia suficiente
            if self.posicion >= len(self.tokens):
                break
                
            tipoToken, valorToken = self.tokenActual() # Obtener el tipo y el valor de la tupla del token actual
            if tipoToken != 'OPERADOR': # Validar si no coincide con un operador
                break

            precedente = self.obtenerPrecedentes(valorToken) # Verificar la precedencia del operador actual
            if precedente < min_precedente:
                break

            OPERADOR = self.match('OPERADOR') # Consumir el operador
            
            # Analizar el termino derecho con precedencia aumentada
            right = self.analizarSintaxis_expresion(precedente + 1)
            if not right:
                break
                
            left = ('binOPERADOR', OPERADOR, left, right) # Construir el nodo de operacion binaria

        return left # Devolver el lado izquierdo

    # Tabla de precedencia para operadores
    def obtenerPrecedentes(self, OPERADOR):
        precedentes = { # Determinar orden ( se le llama precedencia ) 
            '=': 1, # Asignacion (menor precedencia)
            '==': 2, '!=': 2, # Igualdad, desigualdad
            '<': 3, '>': 3, '<=': 3, '>=': 3,  # Comparaciones
            '+': 4, '-': 4, # Suma, resta
            '*': 5, '/': 5, '%': 5, # Multiplicacion, division, modulo
        }
        return precedentes.get(OPERADOR, 0)

    # Analiza un termino, que puede ser una expresion entre parentesis,
    # un operador unario, un identificador, una llamada de funcion o un literal
    def term(self):
        if self.posicion >= len(self.tokens):
            return None
            
        tipoToken, valorToken = self.tokenActual() # Obtener el tipo y valor del token

        if tipoToken == 'PARENTESIS_IZQ': # Expresion entre parentesis: (expresion)
            self.match('PARENTESIS_IZQ')
            expr = self.expresion()
            self.match('PARENTESIS_DER')
            return expr

        elif tipoToken == 'OPERADOR' and valorToken == '&': # Operador de direccion: &variable (usado en scanf)
            self.match('OPERADOR')
            id_expr = self.term()
            return ('address_of', id_expr)

        # Identificador o llamada a funcion
        elif tipoToken == 'ID':
            id_valor = self.match('ID')
            
            # Si sigue un parentesis izquierdo, es una llamada a funcion
            if self.tokenActual()[0] == 'PARENTESIS_IZQ':
                self.match('PARENTESIS_IZQ')
                
                # Procesar argumentos de la funcion
                argumentos = [] # Variable auxiliar para guardar los argumentos
                if self.tokenActual()[0] != 'PARENTESIS_DER': # Validar que no el token actual no sea el parentesis de cierre
                    arg = self.expresion() # Obtener la expresion
                    if arg: # Validar si existe un argumento
                        argumentos.append(arg) # Agregar el argumento a la lista
                    while self.tokenActual()[0] == 'COMA': # Analizar hasta encontrar una coma
                        self.match('COMA')
                        arg = self.expresion()
                        if arg:
                            argumentos.append(arg)
                self.match('PARENTESIS_DER')
                return ('llamadaFuncion', id_valor, argumentos) # Devolver una llamada de funcion
            else: # Etoncnes es una referencia a variable
                return ('ID', id_valor)

        elif tipoToken in ('NUMERO', 'CHAR', 'STRING'): # Literales: numeros, caracteres o cadenas
            self.posicion += 1 # Actualizar la posicion
            return (tipoToken, valorToken) # Devoler el tipo y el valor del token

        return None



# Analizador semantico

class analizadorSemantico:
    def __init__(self):
        self.symbol_table = {}     # nombre_var -> tipo
        self.function_table = {}   # nombre_func -> (tipo_retorno, [tipoParametros])
        self.current_function = None  # Para el analisis de retorno
        self.errors = []
        self.reserved_keywords = {
            'if', 'else', 'while', 'for', 'do'
        }
    
    # Funcion para registrar un error semantico con el numero de linea registrado
    def error(self, msg, line_no=None):
        if line_no: # Validar si existe un numero de lina
            self.errors.append(f"Linea {line_no}: {msg}") # Mostrar error y linea
        else: # Si no existe un numero de linea, de igual manera se muestra el error
            self.errors.append(f"Error semantico: {msg}") # Mostrar linea
        
    # Funcion para analizar el arbol AST. Primero se registra todas las declaraciones de fucniones apra permitir llamadas anticipadas
    # y posteriormente se procesan todas las declaraciones
    def analizar(self, ast):
        
        for node in ast: # Primero se registran todas las funciones si las hay
            if node and node[0] == 'declaracionFuncion': # Validar si existen declaraciones de funciones
                # ('declaracionFuncion', tipoRetorno, nombre, parametros, cuerpo)
                _, tipoRetorno, nombre, parametros, _ = node
                tipoParametros = [param[0] for param in parametros]  # Extraer tipos de parametros
                self.function_table[nombre] = (tipoRetorno, tipoParametros)
                
        for node in ast: # Analizar las declaraciones
            self.procesarNodo(node)
            
        if not self.errors: # Validar si no existen errores
            return True # Continuar
        else:            
            return False # Terminar
            
    # Funcion para procesar un nodo del AST, es capaz de idntificar el tipo de nodo y aplicar las reglas semanticas correspondientes
    def procesarNodo(self, node):
        if not node: # Validar si no existe un nodo
            return None
            
        tipoNodo = node[0] # Obtener el tipo de nodo
    
        if tipoNodo == 'declaracionFuncion': # Validar si el nodo es una declaracion de funcion
            # ('declaracionFuncion', tipoRetorno, nombre, parametros, cuerpo)
            _, tipoRetorno, nombre, parametros, cuerpo = node
            
            prev_function = self.current_function
            self.current_function = (nombre, tipoRetorno) # Guardar el contexto de la funcion actual
            
            # Crear un nuevo ambito para esta funcion
            prev_symbol_table = self.symbol_table.copy()
            self.symbol_table = {}
            
            # Registrar parametros en la tabla de simbolos de la funcion
            for tipoParametro, param_nombre in parametros:
                self.symbol_table[param_nombre] = tipoParametro
            
            # Procesar el cuerpo de la funcion
            for declaracion in cuerpo:
                self.procesarNodo(declaracion)
            
            # Restaurar el ambito anterior
            self.symbol_table = prev_symbol_table
            self.current_function = prev_function
            
            return tipoRetorno
            
        elif tipoNodo == 'declaracion': # Validar si el tipo de nodo es de declaracion
            # Declaracion simple sin inicializacion: ('declaration', tipo, nombre)
            _, tipo, nombre = node
            if nombre in self.symbol_table: # Validar si la variable ya ha sido declarada
                self.error(f"Variable '{nombre}' ya declarada")
            else: # Entonces no ha sido declarada
                self.symbol_table[nombre] = tipo
                return tipo
                
        elif tipoNodo == 'declaracionInicializacion': # Validar si el tipo de nodo es una declaracion con inicializacion
            # Declaracion con inicializacion: ('declaration_init', tipo, nombre, valor)
            _, tipo, nombre, valor = node
            if nombre in self.symbol_table: # Validar si la declaracion ya existe 
                self.error(f"Variable '{nombre}' ya declarada")
                return None
            else:
                self.symbol_table[nombre] = tipo
                tipoExpresion = self.revisarExpresion(valor)
                
                # Verificar compatibilidad de tipos
                    # Se valida los tipos de variables con las expresiones regulares que se pueden aceptar, esto para tener un conexto
                if tipo == 'String' and tipoExpresion == 'STRING': # string con regex tipoString
                    return tipo
                elif tipo == 'int' and tipoExpresion == 'NUMERO': # int unicamente es numerico
                    return tipo
                elif tipo == 'float' and (tipoExpresion == 'NUMERO' or tipoExpresion == 'float'): # float es numerico, adicional con punto
                    return tipo
                elif tipo == 'double' and (tipoExpresion == 'NUMERO' or tipoExpresion == 'double'): # double es numerico
                    return tipo
                elif tipo == 'char' and tipoExpresion == 'CHAR':
                    return tipo
                elif tipoExpresion and tipoExpresion != tipo:
                    self.error(f"No se puede asignar {tipoExpresion} a '{nombre}' de tipo {tipo}")
                
                return tipo
                
        elif tipoNodo == 'asignacion': # Validar si el tipo de nodo es de asignacion
            _, nombre, expr = node
            if nombre not in self.symbol_table:
                self.error(f"Variable '{nombre}' no declarada")
                return None
            else:
                var_type = self.symbol_table[nombre]
                tipoExpresion = self.revisarExpresion(expr)
                
                # Verificar compatibilidad de tipos
                if var_type == 'String' and tipoExpresion == 'STRING':
                    return var_type
                elif var_type == 'int' and tipoExpresion == 'NUMERO':
                    return var_type
                elif var_type == 'float' and (tipoExpresion == 'NUMERO' or tipoExpresion == 'float'):
                    return var_type
                elif var_type == 'double' and (tipoExpresion == 'NUMERO' or tipoExpresion == 'double'):
                    return var_type
                elif var_type == 'char' and tipoExpresion == 'CHAR':
                    return var_type
                elif tipoExpresion and tipoExpresion != var_type:
                    self.error(f"No se puede asignar {tipoExpresion} a '{nombre}' de tipo {var_type}")
                
                return var_type
                
        elif tipoNodo == 'if' or tipoNodo == 'while': # Validar el tipo de nodo con una estructrua de IF o WHILE
            # Estructura if o while: ('if', condition, cuerpo) o ('while', condition, cuerpo)
            _, condition, cuerpo = node
            
            # Verificar que la condicion sea booleana
            cond_type = self.revisarExpresion(condition)
            if cond_type not in ['boolean', 'NUMERO']:  # Permitir NUMERO para comparaciones simples
                self.error(f"La condicion debe ser de tipo booleano, se encontro: {cond_type}")
            
            # Procesar el cuerpo
            for declaracion in cuerpo:
                self.procesarNodo(declaracion)
                
            return None
                
        elif tipoNodo == 'if_else':
            # ('if_else', condition, if_cuerpo, else_cuerpo)
            _, condition, if_cuerpo, else_cuerpo = node
            
            # Verificar que la condicion sea booleana
            cond_type = self.revisarExpresion(condition)
            if cond_type not in ['boolean', 'NUMERO']:  # Permitir NUMERO para comparaciones simples
                self.error(f"La condicion debe ser de tipo booleano, se encontro: {cond_type}") # Mostrar mensaje de error

            for declaracion in if_cuerpo:
                self.procesarNodo(declaracion)
                
            for declaracion in else_cuerpo:
                self.procesarNodo(declaracion)
                
            return None
            
        elif tipoNodo == 'for': # Validar el tipo de nodo para FOR
            # ('for', init, condition, increment, cuerpo)
            _, init, condition, increment, cuerpo = node
            
            if init: # Procesar inicializacion
                self.procesarNodo(init)
                
            if condition:  # Verificar que la condicion sea booleana
                cond_type = self.revisarExpresion(condition)
                if cond_type not in ['boolean', 'NUMERO']:  # Permitir NUMERO para comparaciones simples
                    self.error(f"La condicion del for debe ser de tipo booleano, se encontro: {cond_type}") # Mostrar mensaje de error
            
            if increment: # Procesar incremento (normalmente una expresion)
                self.revisarExpresion(increment)
                
            for declaracion in cuerpo: # Procesar cuerpo
                self.procesarNodo(declaracion)
                
            return None
            
        elif tipoNodo == 'do_while': # Validar el tipo de nodo para do-while
            # ('do_while', condition, cuerpo)
            _, condition, cuerpo = node
            
            for declaracion in cuerpo:  # Procesar cuerpo
                self.procesarNodo(declaracion)
                
            cond_type = self.revisarExpresion(condition) # Verificar que la condicion sea booleana
            if cond_type not in ['boolean', 'NUMERO']:  # Permitir NUMERO para comparaciones simples
                self.error(f"La condicion del do-while debe ser de tipo booleano, se encontro: {cond_type}")
                
            return None
                
        elif tipoNodo == 'return': # Validar el nodo cuando se tenga una sentencia return
            # ('return', expresion)
            _, expr = node
            
            if not self.current_function: 
                self.error("Return fuera de funcion") # Mostrar mensaje de error
                return None
                
            current_func_nombre, current_tipoRetorno = self.current_function
            tipoExpresion = self.revisarExpresion(expr)
            
            # Verificar que el tipo de retorno coincida con el tipo declarado
            if current_tipoRetorno == 'void' and tipoExpresion is not None:
                self.error(f"La funcion '{current_func_nombre}' de tipo void no debe retornar un valor")
            elif current_tipoRetorno != 'void' and tipoExpresion is None:
                self.error(f"La funcion '{current_func_nombre}' debe retornar un valor de tipo {current_tipoRetorno}")
            elif current_tipoRetorno == 'int' and tipoExpresion == 'NUMERO':
                pass  # Permitir retorno de NUMERO para int
            elif current_tipoRetorno == 'float' and tipoExpresion in ['NUMERO', 'float']:
                pass  # Permitir retorno de NUMERO para float
            elif current_tipoRetorno == 'double' and tipoExpresion in ['NUMERO', 'double']:
                pass  # Permitir retorno de NUMERO para double
            elif tipoExpresion and tipoExpresion != current_tipoRetorno:
                self.error(f"La funcion '{current_func_nombre}' debe retornar {current_tipoRetorno}, pero retorna {tipoExpresion}")
                
            return None
            
        elif tipoNodo == 'llamadaFuncion_declaracion': # Validar el tipo de nodo par una llamada de funcion con declaracion
            # ('llamadaFuncion_declaracion', func_nombre, argumentos)
            _, func_nombre, argumentos = node
            
            # Verificar si la funcion existe
            if func_nombre not in self.function_table and func_nombre not in ['printf', 'scanf']:
                if func_nombre not in self.reserved_keywords:
                    self.error(f"Funcion '{func_nombre}' no declarada")
                return None
            
            if func_nombre in ['printf', 'scanf']: # Verificar argumentos para funciones estandar ( por ejemplo printf, scanf)
                if not argumentos or argumentos[0][0] != 'STRING':
                    self.error(f"Primer argumento de {func_nombre} debe ser una cadena de formato")
                
                for i, arg in enumerate(argumentos[1:], 1): # Verificar los demas argumentos
                    self.revisarExpresion(arg)
                return None
                
            # Para funciones normales, verificar los argumentos
            tipoRetorno, tipoParametros = self.function_table[func_nombre]
            
            if len(argumentos) != len(tipoParametros):
                self.error(f"Numero incorrecto de argumentos para '{func_nombre}': esperaba {len(tipoParametros)}, recibio {len(argumentos)}") # Mostrar mensaje de error
            else:
                for i, (arg, expected_type) in enumerate(zip(argumentos, tipoParametros)):
                    arg_type = self.revisarExpresion(arg)
                    if arg_type and arg_type != expected_type:
                        self.error(f"Tipo incorrecto para el argumento {i+1} de '{func_nombre}': esperaba {expected_type}, recibio {arg_type}") # Mostrar mensaje de error
                        
            return None
          
    # Funcion para verificar la semantica de una expresion y devolver su tipo. Esta funcion evalua diferentes tipos de expresiones ( como literales, variables, operaciones binarias
    # llamadas a fucniones, etc), ademas de determinas su tipo resultante
    def revisarExpresion(self, expr):
        if not expr:
            return None
            
        tipoExpresion = expr[0] # Obtener el tipo de expresion
        
        if tipoExpresion == 'NUMERO':
            return 'int'  # Simplificado, podria ser float/double segun el contexto
        elif tipoExpresion == 'STRING':
            return 'String'
        elif tipoExpresion == 'CHAR':
            return 'char'
        elif tipoExpresion == 'ID':
            # Referencia a variable: ('ID', nombre_var)
            _, nombre = expr
            if nombre not in self.symbol_table:
                self.error(f"Variable '{nombre}' no declarada")
                return None
            return self.symbol_table[nombre]
        elif tipoExpresion == 'binOPERADOR':
            # Operacion binaria: ('binOPERADOR', operador, expr_izq, expr_der)
            _, OPERADOR, left, right = expr
            left_type = self.revisarExpresion(left)
            right_type = self.revisarExpresion(right)
            
            # Verificar operadores relacionales (producen boolean)
            if OPERADOR in ['<', '>', '<=', '>=', '==', '!=']:
                return 'boolean'
                
            # Para operaciones aritmeticas, verificar compatibilidad
            if left_type == right_type:
                return left_type
            elif left_type == 'String' or right_type == 'String':
                if OPERADOR == '+':  # Concatenacion de cadenas
                    return 'String'
                else:
                    self.error(f"Operador '{OPERADOR}' no valido para String")
                    return None
            elif left_type in ['int', 'float', 'double'] and right_type in ['int', 'float', 'double']:
                # Reglas de promocion de tipos
                if 'double' in [left_type, right_type]:
                    return 'double'
                elif 'float' in [left_type, right_type]:
                    return 'float'
                else:
                    return 'int'
            else:
                self.error(f"Operador '{OPERADOR}' no valido entre {left_type} y {right_type}")
                return None
                
        elif tipoExpresion == 'llamadaFuncion':
            # Llamada a funcion como expresion: ('llamadaFuncion', nombre_func, argumentos)
            _, func_nombre, argumentos = expr
            
            # Verificar si la funcion existe
            if func_nombre not in self.function_table and func_nombre not in ['printf', 'scanf']:
                if func_nombre not in self.reserved_keywords:
                    self.error(f"Funcion '{func_nombre}' no declarada")
                return None
                
            # Para printf, scanf y otras funciones estandar (simplificado)
            if func_nombre in ['printf', 'scanf']:
                if not argumentos or argumentos[0][0] != 'STRING':
                    self.error(f"Primer argumento de {func_nombre} debe ser una cadena de formato")
                # Verificar los demas argumentos
                for i, arg in enumerate(argumentos[1:], 1):
                    self.revisarExpresion(arg)
                    
                return 'int'  # printf y scanf retornan int
                
            # Para funciones normales
            tipoRetorno, tipoParametros = self.function_table[func_nombre]
            
            if len(argumentos) != len(tipoParametros):
                self.error(f"Numero incorrecto de argumentos para '{func_nombre}': esperaba {len(tipoParametros)}, recibio {len(argumentos)}")
            else:
                for i, (arg, expected_type) in enumerate(zip(argumentos, tipoParametros)):
                    arg_type = self.revisarExpresion(arg)
                    if arg_type and arg_type != expected_type:
                        self.error(f"Tipo incorrecto para el argumento {i+1} de '{func_nombre}': esperaba {expected_type}, recibio {arg_type}")
                        
            return tipoRetorno

        elif tipoExpresion == 'address_of':
            # Operador de direccion: ('address_of', expr)
            _, id_expr = expr
            if id_expr[0] != 'ID':
                self.error("El operador '&' solo puede aplicarse a variables")
                return None

            id_nombre = id_expr[1]
            if id_nombre not in self.symbol_table:
                self.error(f"Variable '{id_nombre}' no declarada")
                return None

            # El tipo de &var es un puntero al tipo de var
            var_type = self.symbol_table[id_nombre]
            return f"pointer_{var_type}"  # Simplificado, para scanf

        elif tipoExpresion == 'binOPERADOR':
            # Operacion binaria (version duplicada): ('binOPERADOR', operador, expr_izq, expr_der)
            _, OPERADOR, left, right = expr
            left_type = self.revisarExpresion(left)
            right_type = self.revisarExpresion(right)

            if not left_type or not right_type:
                return None

            # Operadores aritmeticos
            if OPERADOR in ['+', '-', '*', '/']:
                if left_type in ['int', 'float', 'double'] and right_type in ['int', 'float', 'double']:
                    # Retornar el tipo mas general
                    if 'double' in [left_type, right_type]:
                        return 'double'
                    elif 'float' in [left_type, right_type]:
                        return 'float'
                    else:
                        return 'int'
                else:
                    self.error(f"Operacion '{OPERADOR}' no valida entre {left_type} y {right_type}")
                    return None

            # Operadores de comparacion
            elif OPERADOR in ['<', '>', '<=', '>=', '==', '!=']:
                if left_type == right_type or (left_type in ['int', 'float', 'double'] and right_type in ['int', 'float', 'double']):
                    return 'boolean'
                else:
                    self.error(f"Comparacion no valida entre {left_type} y {right_type}")
                    return None

            # Operadores logicos
            elif OPERADOR in ['&&', '||']: # Validar operadores
                if left_type == 'boolean' and right_type == 'boolean':
                    return 'boolean'
                else:
                    self.error(f"Operador logico '{OPERADOR}' requiere operandos booleanos, no {left_type} y {right_type}")
                    return None

            else:
                self.error(f"Operador desconocido: {OPERADOR}")
                return None

        return None



# Generacion de Codigo Intermedio
    # La clase implementa un generador de codigo intermedio para el compilador, el generador
    # transforma un arbol de sintaxis abstracta (AST) en codigo de tres direcciones ( comunemente 
    # es una representacion  intermedia utilizada en compiladores)

class generadorCodigo:
    def __init__(self):

        # Constructor de la clase generadorCodigo.
        # Variabls auxiliares
        self.temp_count = 0 # Contador para variables temporales
        self.label_count = 0 # Contador para etiquetas de salto
        self.code = []  # Lista para almacenar el codigo generado

    # Genera y devuelve un nuevo nombre de variable temporal. Cada llamada incremente el contador temporal
    def new_temp(self):
        self.temp_count += 1 # Actualizar el contador temporal
        return f"t{self.temp_count}" # Devoler el contador temporal actualizado

    # Genera y devuelve una nueva etiqueta para los saltos en el codigo, cada llamada
    # incrementa el contador de etiquetas ( L1, L2...) 
    def nuevaEtiqueta(self):
        self.label_count += 1 # Contador de etiquetas
        return f"L{self.label_count}" # Devolver el contador de etiquetas

    # Funcion principal que genera el codigo intermedio con base al AST, la funcion procesa
    # cada delcaracion en el AST t contruye conteido intermedio
    def generar(self, ast):
        self.code = []  # Reiniciar el codigo
        for declaracion in ast:
            self.generarDeclaracion(declaracion)
        return self.code

    # Funcion para genera el codigo intermedio para una delcracion en el AST, se manejan diferentes tipos de declaraciones
    # como asignaciones, condicionaels, bucles, etc
    def generarDeclaracion(self, declaracion):
        if not declaracion: # Valiar si np existe una delcaracion  
            return
            
        tipoDeclaracion = declaracion[0] # Variable auxiliar para almacenar los tipos de declracion
        
        if tipoDeclaracion == 'declaracion': # Una declaracion simple sin inicializacion no genera codigo intermedio solo reserva espacio en la tabla de simbolos
            pass
            
        elif tipoDeclaracion == 'declaracionInicializacion': # Declaracion con inicializacion, la cual genera codigo para el valor inicial
            _, tipo, nombre, expr = declaracion
            valor = self.generarExpresion(expr)
            self.code.append(f"{nombre} = {valor}")
            
        elif tipoDeclaracion == 'asignacion': # Asignacion de un valor a una variable existente      
            _, nombre, expr = declaracion
            valor = self.generarExpresion(expr)
            self.code.append(f"{nombre} = {valor}")
            
        elif tipoDeclaracion == 'if': # Estructura condicional if sin else            
            _, condition, cuerpo = declaracion
            cond_result = self.generarExpresion(condition)
            
            label_false = self.nuevaEtiqueta() # Etiqueta si la condicion es falsa
            label_end = self.nuevaEtiqueta() # Etiqueta para el final del if
            
            self.code.append(f"if {cond_result} == 0 goto {label_false}") # Si la condicion es falsa, saltar a label_false
            
            for b in cuerpo: # Cuerpo del if - generar codigo para cada declaracion en el cuerpo
                self.generarDeclaracion(b) # Generar
                           
            self.code.append(f"goto {label_end}") # Saltar al final despues de ejecutar el cuerpo       
            self.code.append(f"{label_false}:") # Etiqueta para saltar si la condicion es falsa
            self.code.append(f"{label_end}:") # Etiqueta de fin de la estructura if
            
        elif tipoDeclaracion == 'if_else': # Estructura condicional if_else
            # Estructura condicional if-else
            _, condition, if_cuerpo, else_cuerpo = declaracion
            cond_result = self.generarExpresion(condition)
            
            label_false = self.nuevaEtiqueta()  # Etiqueta si la condicion es falsa (else)
            label_end = self.nuevaEtiqueta()    # Etiqueta para el final del if-else
            
            self.code.append(f"if {cond_result} == 0 goto {label_false}") # Si la condicion es falsa, saltar al bloque else
            
            for b in if_cuerpo: # Cuerpo del if - generar codigo para cada declaracion
                self.generarDeclaracion(b)
                    
            self.code.append(f"goto {label_end}") # Saltar al final despues de ejecutar el cuerpo del if
            self.code.append(f"{label_false}:") # Etiqueta para el bloque else       
            
            for b in else_cuerpo: # Cuerpo del else - generar codigo para cada declaracion
                self.generarDeclaracion(b)
                
            # Etiqueta de fin de la estructura if-else
            self.code.append(f"{label_end}:")
            
        elif tipoDeclaracion == 'while':
            # Estructura de bucle while
            _, condition, cuerpo = declaracion
            
            label_start = self.nuevaEtiqueta()  # Etiqueta para el inicio del bucle
            label_end = self.nuevaEtiqueta()    # Etiqueta para el final del bucle
            
            # Etiqueta de inicio del bucle
            self.code.append(f"{label_start}:")
            
            # Evaluar condicion del bucle
            cond_result = self.generarExpresion(condition)
            
            # Si la condicion es falsa, saltar al final del bucle
            self.code.append(f"if {cond_result} == 0 goto {label_end}")
            
            # Cuerpo del bucle - generar codigo para cada declaracion
            for b in cuerpo:
                self.generarDeclaracion(b)
                
            # Volver al inicio del bucle para reevaluar la condicion
            self.code.append(f"goto {label_start}")
            
            # Etiqueta de fin del bucle
            self.code.append(f"{label_end}:")
            
        elif tipoDeclaracion == 'declaracionFuncion':
            # Declaracion de una funcion
            # Estructura: ('declaracionFuncion', tipoRetorno, nombre, parametros, cuerpo)
            _, tipoRetorno, nombre, parametros, cuerpo = declaracion
            
            # Generar etiqueta de funcion con su nombre
            self.code.append(f"function {nombre}:")
            
            # Procesar los parametros de la funcion
            for tipoParametro, param_nombre in parametros:
                # Opcional: se podria agregar codigo para manejar los parametros
                # Por ejemplo: self.code.append(f"param {param_nombre}")
                pass
            
            # Generar codigo para el cuerpo de la funcion
            for b in cuerpo:
                self.generarDeclaracion(b)
                
        elif tipoDeclaracion == 'return':
            # Sentencia de retorno dentro de una funcion
            _, expr = declaracion
            valor = self.generarExpresion(expr)
            self.code.append(f"return {valor}")
            
        elif tipoDeclaracion == 'llamadaFuncion_declaracion': # Llamada a funcion como declaracion (sin asignar el resultado)
            # Declaracion con inicializacion: ('declaration_init', tipo, nombre, valor)
            _, nombre, argumentos = declaracion
            
            # Generamos codigo para evaluar cada argumento
            arg_valors = []
            for arg in argumentos:
                arg_val = self.generarExpresion(arg)
                arg_valors.append(arg_val)
                
            # Generamos codigo para pasar cada parametro
            for i, arg_val in enumerate(arg_valors):
                self.code.append(f"param {arg_val}")
                
            # Como es una llamada como declaracion, no guardamos el resultado
            self.code.append(f"call {nombre}, {len(arg_valors)}")
            
        elif tipoDeclaracion == 'for':
            # Estructura de bucle for
            # Estructura: ('for', init, condition, increment, cuerpo)
            _, init, condition, increment, cuerpo = declaracion
            
            # Generar codigo para la inicializacion del bucle
            if init:
                self.generarDeclaracion(init)
                
            label_start = self.nuevaEtiqueta()  # Etiqueta para el inicio del bucle
            label_end = self.nuevaEtiqueta()    # Etiqueta para el final del bucle
            
            # Etiqueta de inicio del bucle
            self.code.append(f"{label_start}:")
            
            # Evaluar condicion del bucle si existe
            if condition:
                cond_result = self.generarExpresion(condition)
                self.code.append(f"if {cond_result} == 0 goto {label_end}")
            
            # Cuerpo del bucle - generar codigo para cada declaracion
            for b in cuerpo:
                self.generarDeclaracion(b)
                
            # Ejecutar el incremento si existe
            if increment:
                increment_val = self.generarExpresion(increment)
                # Para un incremento como expresion, no necesitamos guardar el resultado
            
            # Volver al inicio del bucle para reevaluar la condicion
            self.code.append(f"goto {label_start}")
            
            # Etiqueta de fin del bucle
            self.code.append(f"{label_end}:")
            
        elif tipoDeclaracion == 'do_while':
            # Estructura de bucle do-while
            # Estructura: ('do_while', condition, cuerpo)
            _, condition, cuerpo = declaracion
            
            label_start = self.nuevaEtiqueta()  # Etiqueta para el inicio del bucle
            
            # Etiqueta de inicio del bucle
            self.code.append(f"{label_start}:")
            
            # Cuerpo del bucle - generar codigo para cada declaracion
            # En do-while, el cuerpo se ejecuta al menos una vez antes de evaluar la condicion
            for b in cuerpo:
                self.generarDeclaracion(b)
                
            # Evaluar condicion del bucle
            cond_result = self.generarExpresion(condition)
            
            # Si la condicion es verdadera, volver al inicio del bucle
            self.code.append(f"if {cond_result} != 0 goto {label_start}")

    # Funcion para generar codigo intermedio para una expresion en el AST , maneja diferentes tipos de
    # de expresiones como lo son operaciones binarias, identificadores, literales, llamadas a funciones, etc.
    def generarExpresion(self, expr):
        if not expr:
            return "error"
            
        tipoExpresion = expr[0]
        
        if tipoExpresion == 'binOPERADOR':
            # Operacion binaria (suma, resta, multiplicacion, etc.)
            _, OPERADOR, left, right = expr
            left_val = self.generarExpresion(left) # Evaluar operando izquierdo
            right_val = self.generarExpresion(right) # Evaluar operando derecho
            temp = self.new_temp() # Crear variable temporal para el resultado
            self.code.append(f"{temp} = {left_val} {OPERADOR} {right_val}")
            return temp
            
        # Validar e identifica el tipo de expresion
        elif tipoExpresion == 'ID': # Identificador nombre de variable
            return expr[1]
            
        elif tipoExpresion == 'NUMERO': # Literales numericos
            return expr[1]
            
        elif tipoExpresion == 'CHAR': # Caractertes
            return expr[1]
            
        elif tipoExpresion == 'STRING': # Cadenas
            return expr[1]
            
        elif tipoExpresion == 'llamadaFuncion': # Llamada a funcion como expresion (para usar su valor de retorno)
            _, nombre, argumentos = expr
            
            arg_valors = [] # Lista auxiliar para agregar los valores de un argumento
            for arg in argumentos:
                # Se genera codigo para evaluar cada argumento
                arg_val = self.generarExpresion(arg)
                arg_valors.append(arg_val)
                
            # Generamos codigo para pasar cada parametro
            for i, arg_val in enumerate(arg_valors):
                self.code.append(f"param {arg_val}")
                
            # Se genera la llamada a la funcion y se guarda el resultado en una variable temporal
            temp = self.new_temp()
            self.code.append(f"{temp} = call {nombre}, {len(arg_valors)}")
            return temp
            
        # Operador de direccion (&) para obtener la direccion de memoria de una variable
        # Estructura: ('address_of', expr)
        elif tipoExpresion == 'address_of':
            _, id_expr = expr
            if id_expr[0] == 'ID':
                # Simplemente devolvemos la direccion (implementacion simplificada)
                return f"&{id_expr[1]}"
            return 'unknown'
            
        return 'unknown'  # Para expresiones no reconocidas



# Programa principal
    # Aqui se ejecutan las funciones principales y se prueba un codigo auxiliar
def main():
    
    # Codigo de pruebas completamente valido, no contiene errores
    codigoPrueba = """
        #include <stdio.h>

        // Funcion para calcular el doble de un numero
        int doble(int numero) {
            return numero * 2;
        }

        // Funcion para verificar si un numero es positivo
        int esPositivo(int numero) {
            if (numero > 0) {
                return 1;
            } else {
                return 0;
            }
        }

        /* Funcion principal
        Pide un numero y muestra su doble y si es positivo
        */

        int main() {
            int n;
            printf("Ingrese un numero: ");
            scanf("%d", &n);

            int resultado = doble(n);
            printf("El doble de %d es: %d\n", n, resultado);

            int positivo = esPositivo(n);
            if (positivo == 1) {
                printf("El numero es positivo\n");
            } else {
                printf("El numero no es positivo\n");
            }

            // Bucle simple con variable declarada
            int contador = 0;
            while (contador < 3) {
                printf("Contador: %d\n", contador);
                contador = contador + 1;
            }

            return 0;
        }
        """

    # Variable auxiliar de prueba con errores
    codigoError1 = """
        int variable1 = 10;
        flota variable2 = 3.14; // Error lexico: 'flota' no es una palabra clave valida
        if (variable1 == variable2) {
            print("Son iguales");
        }
        wh ile (variable1 > 0) { // Error sintactico: espacio incorrecto en 'while'
            variable1 = variable1 - 1
        }
        resultado = variable3 + 5; // Error semantico (para un analizador semantico): 'variable3' no esta definida
    """

    # Variable auxiliar de prueba con errores
    codigoError2 = """
        numero pi = 3.14159; // Error lexico: 'numero' no es una palabra clave valida
        if (condicion { // Error sintactico: falta el parentesis de cierre
            imprimir("Verdadero");
        }
        cadena texto = "Hola";
        longitud = texto - 5; // Error semantico (para un analizador semantico): operacion invalida entre cadena y entero
        $
    """

    print("Analisis lexico -------------------------------------------------------------------------------->")
    try:
        tokens = analizadorLexico(codigoPrueba) 
        print(tokens) 
    except RuntimeError as e: 
        print(f"Error lexico: {e}") 
        return 

    print("\n Analisis sintactico --------------------------------------------------------------------------------> ")
    sintaxis = analizadorSintactico(tokens)
    ast = sintaxis.analizarSintaxis()
    for node in ast:
        print(node)

    print("\nAnalisis semantico -------------------------------------------------------------------------------->")
    analizarr = analizadorSemantico()
    is_valid = analizarr.analizar(ast)
    
    if not is_valid:
        for error in analizarr.errors:
            print(error)
    else:
        print("No hay errores semanticos.")

    print("\nCodigo intermedio -------------------------------------------------------------------------------->")
    generator = generadorCodigo()
    code = generator.generar(ast)
    for line in code:
        print(line)

if __name__ == "__main__":
    main()