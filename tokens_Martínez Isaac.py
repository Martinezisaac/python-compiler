# Compiladores | Martínez Isaac

# Importacion de librerías
import re #Expresiones regulares

# Definicion de tokens
TOKENS = [
    ("PALABRA_CLAVE", r"\b(if|else|while|for|return|int|float|char|switch|case|break|default|do)"), # 
    ("NUMERO", r"\b\d+(\.\d+)?\b"), # Para los numeros se incluyen los enteros y los flotantes (por ello en la expresion hay un punto y un digito, siempre y vuando se incluya)
    ("IDENTIFICADOR", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"), # La expresion Incluye letras, numeros y guiones bajos
    ("OPERADOR", r"[+\-*/%=<>!&|^~]+"), # Suma, resta, multiplicación, división, módulo, asignación, comparación, negación, AND, OR, XOR, NOT
    ("PARENTESIS", r"[()]"),
    ("LLAVE", r"[{}]"), 
    ("PUNTO_Y_COMA", r";"),
    ("COMENTARIO", r"//.*|/\*.*?\*/"), #Existen dos tipos de comentarios. El comentario de una sola linea (//) y el comentario de varias lineas (/* */). Este token iuncluye ambos tipos
    ("ESPACIO", r"\s+"),
]

# Función para tokenizar
def tokenizar(codigo):
    cantidadCaracteresError = 20 # Cantidad de caracteres a mostrar en caso de error
    tokens_encontrados = [] # Lista para almacenar los tokens
    
    while codigo: # Recorrer el código
        for nombre, patron in TOKENS: # Recorrer los tokens, nombre hace referencia al Token y patron a la expresion regular
            regex = re.compile(patron) # Compilar la expresion regular
            coincidencia = regex.match(codigo) # Buscar coincidencias
            if coincidencia: # Validar si existen coincidencias
                if nombre != "ESPACIO":  # Ignorar los espacios en caso de encontrarlo en el codigo dado
                    tokens_encontrados.append((nombre, coincidencia.group(0))) # Agregar token encontrado a la lista
                codigo = codigo[coincidencia.end():] # Actualizar el código. Avanzar en la cadena eliminando las partes ya reconocidas
                break
        else: # Entonces no se encontró ningún token
            raise ValueError(f"Token no reconocido: {codigo[:cantidadCaracteresError]}") # Mostrar mensaje de error e indicar en donde se encontro el error (se indica X cantidad de caracteres con la variable)
    return tokens_encontrados # Devolver los tokens encontrados 

# Ejemplos para recorrer tokens en codigo C

# Ejemplo 1
codigoC = """
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

# Ejemplo 2
codigoC2 = """
while (x != 0) {
    x = x - 1;
    return x;
}
"""

# Imprimir los tokens encontrados
for token in tokenizar(codigoC):
    print(token)