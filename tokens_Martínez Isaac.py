# Compiladores | Martínez Isaac

# Importacion de librerías
import re #Expresiones regulares

TOKENS = [ # Definicion de tokens
    ("PALABRA_CLAVE", r"\b(if|else|while|for|return|int|float|char|switch|case|break|default|do)"), # Declaracion de palabras clave en C y condiciones de control
    ("NUMERO", r"\b\d+(\.\d+)?\b"), # Para los numeros se incluyen los enteros y los flotantes (por ello en la expresion hay un punto y un digito, siempre y vuando se incluya)
    ("IDENTIFICADOR", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"), # La expresion Incluye letras, numeros y guiones bajos
    ("OPERADOR", r"[+\-*/%=<>!&|^~]+"), # Suma, resta, multiplicación, división, módulo, asignación, comparación, negación, AND, OR, XOR, NOT
    ("PARENTESIS", r"[()]"),
    ("LLAVE", r"[{}]"), 
    ("PUNTO_Y_COMA", r";"),
    ("COMENTARIO", r"//.*|/\*.*?\*/"), #Existen dos tipos de comentarios. El comentario de una sola linea (//) y el comentario de varias lineas (/* */). Este token iuncluye ambos tipos
    ("ESPACIO", r"\s+"),
]

patron = re.compile(
    "|".join(f"(?P<{nombre}>{regex})" for nombre, regex in TOKENS)
)
# patron muestra el nombre del token y la expresion / valor encontrador de acuerdo al tipo de token. Por lo tanto
    # nombre: nombre del token
    # expresion: expresion regular / valor del token para su identificacion
# Con re.comile el codigo se hace mas eficiente, se crea el patron compilado para depsues utilizarlo con metodos como match(), search() y findall(), esto sin tener que compilar la expresion regular cada vez que esta dentro del bucle

# Analizador lexico
def analizadorLexico(codigo):
    # Variables auxiliares
    cantidadCaracteresError = 100 # Cantidad de caracteres para extrar en caso de que exista un error 
    linea = 0 # Variable para almacenar la linea
    columna = 1 # Varoable para almacenar la columna
    tokensEntontrados = [] # Arreglo para almacenar los tokens encontrados
    posicion = 0 # Variable auxiliar para indicar si el codigo inicia una nueva linea o la termina

    while posicion < len(codigo): # Validar que la posicion sea menor a la longitud del codigo
        match = patron.match(codigo, posicion) # Buscar coincidencias en el codigo
        
        if match: # Validar si existe un salto de linea
            tipo = match.lastgroup # Obtener el tipo de token
            valor = match.group() # Obtener el valor del token (valor que coincida exactamente)
            inicio = posicion # Inicio de la posicion
            fin = match.end() # Devolver el indice de la posicion en el texto

            lineasNuevas = valor.count("\n") # Variable para indicar la cantidad de lineas nuevas en el codigo (salto de linea)
            
            # Actualizar línea y columna
            if lineasNuevas > 0: 
                # Calcular el numero de filas y obtener la posicion actual de la columna de acuerdo al ultimo caracter de columna
                linea += lineasNuevas # Sumar lineas
                columna = len(valor.split("\n")[-1]) #Siempre devuelve el ultimo caracter del token
            else: # Entonces solo existe una linea
                columna += len(valor) # Sumar columnas
            
            if tipo != "ESPACIO" and tipo != "COMENTARIO": # Ignorar espacios y comentarios
                tokensEntontrados.append((tipo, valor, linea, columna)) # Añadir el tipo de token, el valor del token y su respectiva posicion en el codigo
            
            posicion = fin # La posicion actual es el indice de la posicion en el texto
        
        else: # Entonces no existieron match
            # En vez de mostrar el error inmediatamente, buscamos el siguiente token válido
            fragmento = codigo[posicion:posicion+cantidadCaracteresError]
            siguiente_match = patron.match(codigo, posicion + 1)  # Intentamos hacer el match del siguiente token

            if siguiente_match:
                # Si encontramos un token válido, mostramos el error hasta esa posición
                fin_siguiente_token = siguiente_match.start() # Empezar a buscar despues del token no valido encontrado
                error_fragmento = codigo[posicion:fin_siguiente_token] # Indicar hasta donde mostrar el error
                raise ValueError(f"Error lexico en la linea {linea}, columna {columna}: \n'{error_fragmento}' no es un token valido.") # Imprimir en la terminal
            else:
                # Si no hay ningún token válido más adelante, mostramos hasta la cantidad de caracteres de error
                error_fragmento = codigo[posicion:posicion + cantidadCaracteresError] # Mostrar el error
                raise ValueError(f"Error lexico en la linea {linea}, columna {columna}: \n'{error_fragmento}' no es un token valido.") # Imprimir en la terminal

    return tokensEntontrados #Devoler los tokens [tipo, valor, linea, columna]

# Codigos de prueba

# Codigo 1
codigo1 = """
int main() {
    int x = 23;
    int y = 12;
    if (x > y) {
        x = x + y;
    } else {
        y = y + x}
    return 0;
}
"""

# Codigo 2
codigo2 = """
while (x != 0) {
    x = x - 1;
    return x;
}
"""

# Codigo error 1
codigoError1 = """  
@ hola mundo :) 
x = 10
y = 20
resultado = x + y
"""

# Main

tokens = analizadorLexico(codigo1) #Obtener los tokens y las propiedades necesarias de la funcion 

# Impresion de los tokens en pantalla
for tipo, valor, linea, columna in tokens: 
    print(f"{tipo}: {valor}   |   Linea: {linea}, Columna: {columna}") # Imprimir en pantall los tokens junto a su posicion