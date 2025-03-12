# Compiladores | Martinez Isaac
# YESSIR

import re  # Expresiones regulares

TOKENS = [ #Definicio de los tokens
    ("PALABRA_CLAVE", r"\b(if|else|while|for|return|int|float|char|switch|case|break|default|do)\b"),
    ("NUMERO", r"\b\d+(\.\d+)?\b"),
    ("NUMERO_HEX", r"\b0[xX][0-9a-fA-F]+\b"),  # Soporte para números hexadecimales
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
    ("COMILLAS", r'"'),
    ("COMILLA_SIMPLE", r"'"),
    ("DIAGONAL_INVERSA", r'\\')
]

# Patron para encontrar los tokens, busca todos los valores y se adjunta el nombre de cada token y su expresion regular
patron = re.compile("|".join(f"(?P<{nombre}>{regex})" for nombre, regex in TOKENS))

def analizadorLexico(codigo):
    linea = 1
    columna = 1
    tokensEncontrados = []
    posicion = 0

    while posicion < len(codigo):
        match = patron.match(codigo, posicion)
        
        if match:
            tipo = match.lastgroup
            valor = match.group()
            inicio = posicion
            fin = match.end()

            lineasNuevas = valor.count("\n")
            
            if lineasNuevas > 0:
                linea += lineasNuevas
                columna = len(valor.split("\n")[-1])
            else:
                columna += len(valor)
            
            if tipo != "ESPACIO":
                tokensEncontrados.append((tipo, valor, linea, columna))
            
            posicion = fin
        else:
            tokensEncontrados.append(("ERROR", codigo[posicion], linea, columna))
            posicion += 1
            columna += 1
    
    return tokensEncontrados

# Codigos de prueba
codigo1 = """
/* hola
*/
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

codigoPrueba1 = """
int main() { 
char *str = "\xFF"; 
int x = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;
// Comentario
printf("%s %d", str, x); return 0; }
/*comentario
largo*/
"""

codigoPrueba2 = """
#define MEGA_DEFINE_AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
1 #define MEGA_DEFINE_BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
2 int main() { char *str = "cadena; int x = 100000000000000000000000000000000000000000000000000000000000000; // Entero demasiado grande /* Esto es un comentario sin cerrar... printf("\xFF\xFE\xFD"); 
// Caracteres fuera del rango ASCII normal return 0; }
"""

# Main
tokens = analizadorLexico(codigoPrueba2)

for tipo, valor, linea, columna in tokens:
    print(f"{tipo}: {valor}   |   Linea: {linea}, Columna: {columna}")