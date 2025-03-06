# Compiladores | Martinez Isaac

import re  # Expresiones regulares

TOKENS = [ #Definicio de los tokens
    ("PALABRA_CLAVE", r"\b(if|else|while|for|return|int|float|char|switch|case|break|default|do)\b"),
    ("NUMERO", r"\b\d+(\.\d+)?\b"),
    ("IDENTIFICADOR", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
    ("COMENTARIO", r"//.*|/\*[\s\S]*?\*/"),
    ("OPERADOR", r"[+\-*/%=<>!&|^~]+"),
    ("PARENTESIS", r"[()]"),
    ("LLAVE", r"[{}]"), 
    ("PUNTO_Y_COMA", r";"),
    ("COMA", r","),
    ("PUNTO", r"\."),
    ("DOS_PUNTOS", r":"),
    ("ESPACIO", r"\s+"),
]

# Patron para encontrar los tokens, busca todos los valores y se adjunta el nombre de cada token y su expresion regular
patron = re.compile("|".join(f"(?P<{nombre}>{regex})" for nombre, regex in TOKENS))

def analizadorLexico(codigo):
    #Variables auxiliares 
    max_caracteres_error = 100 # Numero maximo de caracteres para mostrar en caso de un error
    linea, columna, posicion = 1, 1, 0
    tokensEncontrados = [] # Variable para adjuntar los tokens que la funcion encuentra

    while posicion < len(codigo): #Validar que
        match = patron.match(codigo, posicion) #Buscar el patron en el codigo proporcionado (encontrar las expresiones)

        if match: #Si existe un match, entonces se obtiene el tipo y el valor del token, ademas de manejar las lineas y columnas
            tipo, valor = match.lastgroup, match.group() #Obtener el tipo y el valor del token
            fin = match.end() #Obtener la posicion final del token
            lineasNuevas = valor.count("\n") #Contar los saltos de linea en el valor del token

            if lineasNuevas > 0: #Manejar el contador de lineas y columnas
                linea += lineasNuevas #Sumar linea
                columna = 1 + len(valor.split("\n")[-1]) #Obtener la longitud de la linea de codigo
            else: #Si no hay saltos de linea, entonces se suma la longitud del valor al contador de columnas
                columna += len(valor)

            if tipo not in {"ESPACIO", "COMENTARIO"}: #Igonrar los espacios y los comentarios 
                tokensEncontrados.append((tipo, valor, linea, columna)) #Adjuntar el tipo de token, el valor de dicho token encontrado, la linea y su columna

            posicion = fin #Actualizar la posicion
        
        else: #Entonces no existe un match (Manejar los errores)
            fragmento = codigo[posicion:posicion + max_caracteres_error] #Obtener el fragmento de codigo
            siguiente_match = patron.match(codigo, posicion + 1) #Buscar un match valido a partir de la posicion actual

            #¿Porque nos interesa buscar un siguiente match?
            # Al buscar un siguiente match se puede obtener el fragmento de codigo que no es valido, si existe un match valido entonces esta variable guarda
            # el token o la expresion que esta mal, lo cual ayuda a determinar con exactitud el error en el codigo, es decir, busca desde el fragmento de codigo erroneo
            # hasta el siguiente token valido

            if siguiente_match: #Validar si existe un siguiente match para determinar el error
                error_fin = siguiente_match.start() #Obtener la posicion final del error
                error_fragmento = codigo[posicion:error_fin] #Obtener el fragmento de codigo que no es valido
            else:
                error_fragmento = fragmento #Si no existe un siguiente match, entonces el fragmento de codigo es el error

            raise ValueError(f"Error lexico en la linea {linea}, columna {columna}:\n'{error_fragmento}' no es un token valido.") #Mostrar el error en la terminal

    return tokensEncontrados #Devoler TIPO, VALOR, LINEA y COLUMNA de los tokens encontrados

# Codigos de prueba
codigo1 = """
int main() {
    int x = 23;
    int y = 12;
    if (x > y) {
        x = x + y;
    } else {
        y = y + x;
    }
    return 0;
}
"""

codigo2 = """
while (x != 0) {
    x = x - 1;
    return x;
}
"""

codigo3 = """
int suma(int a, int b) {
    int resultado = a + b;
    return resultado;
}
"""

codigoError1 = """  
@ hola mundo :) 
x = 10
y = 20
resultado = x + y
"""

# Main
tokens = analizadorLexico(codigoError1)

for tipo, valor, linea, columna in tokens:
    print(f"{tipo}: {valor}   |   Linea: {linea}, Columna: {columna}")