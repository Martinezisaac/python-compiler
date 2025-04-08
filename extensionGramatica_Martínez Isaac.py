# Martinez Isaac
# Compiladores

# Librerías necesarias
import nltk
from nltk.grammar import CFG
from nltk.parse import EarleyChartParser
import re

# Función para tokenizar la expresión
def tokenize(expression):
    token_patterns = [ # Definir patrones para identificar los diferentes tipos de tokens
        ('Num', r'\d+(\.\d+)?'),  # Números enteros y decimales
        ('Const', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Identificadores
        ('OP', r'[\+\-\*/\^\(\)=%,]')  # Operadores y delimitadores
    ]
    
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_patterns) # Compilar los patrones en una expresión regular
    token_pattern = re.compile(token_regex)
    
    # Listar los tokens encontrados en la expresión
    tokens = [] # Arreglo auxiliar para guardar los tokens encontrados
    pos = 0
    while pos < len(expression):
        match = token_pattern.match(expression, pos)
        
        if not match:
            if expression[pos].isspace(): # Ignorar espacios
                pos += 1
                continue
            raise ValueError(f"Token inválido en la posición {pos}: '{expression[pos:]}'") # Mostrar error
        
        token_type = match.lastgroup
        token_value = match.group()
        
        if token_type in ['Num', 'Const', 'OP']: # Agregar tokens a la lista dependiendo de su tipo
            tokens.append(token_value)
        
        pos = match.end()
    
    return tokens # Devolver el arreglo de tokens encontrados

# Función para convertir tokens numéricos en terminales permitidos por la gramática
def convert_number_to_digits(number_str):
    return [digit for digit in number_str] # Convertir un número a una lista de dígitos individuales

# Definir la gramática extendida para la expresión matemática
    # La gramática incluye:
    # operaciones aritméticas
    # funciones matemáticas
    # manejo de números enteros y flotantes
gramatica_extendida = CFG.fromstring("""
Expr -> Expr '+' Term | Expr '-' Term | Term
Term -> Term '*' Factor | Term '/' Factor | Term '%' Factor | Factor
Factor -> Power | Unary
Power -> Atom '^' Power | Atom
Unary -> '+' Atom | '-' Atom | Atom
Atom -> Number | Const | '(' Expr ')' | Function

Function -> 'sin' '(' Expr ')' | 'cos' '(' Expr ')' | 'sqrt' '(' Expr ')' | FunctionMulti
FunctionMulti -> 'max' '(' ExprList ')' | 'min' '(' ExprList ')'
ExprList -> Expr ',' Expr | ExprList ',' Expr

Number -> Digit | Number Digit | Number '.' Number
Digit -> '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
Const -> 'PI' | 'E' | 'sin' | 'cos' | 'sqrt' | 'max' | 'min'
""")

expresion = "123.45 + sin(PI) * 2 / (1 - 5)^2^3" # Definir la expresion que se va a evaluar

tokens = tokenize(expresion) # Tokenizar la expresión
print(f"Tokens: {tokens}") # Imprimir los tokens encontrados en la expresión
 
# Expandir los tokens numéricos en dígitos individuales para que coincidan con la gramática
expanded_tokens = []
for token in tokens:
    if token.replace('.', '', 1).isdigit():  # Si es un número (entero o decimal)
        if '.' in token:  # Si es un decimal
            parts = token.split('.')
            # Expandir la parte entera (se considera como un digito)
            for digit in parts[0]:
                expanded_tokens.append(digit)
            expanded_tokens.append('.') # Agregar el punto decimal
            
            for digit in parts[1]: # Expandir la parte decimal
                expanded_tokens.append(digit)
        else: # Enotnces es entero
            for digit in token:
                expanded_tokens.append(digit)
    else: # Si no es un número (operadores, identificadores, etc.)
        expanded_tokens.append(token)

print(f"Tokens expandidos: {expanded_tokens}")
parser = EarleyChartParser(gramatica_extendida) # Crear el analizador sintáctico con la gramática extendida

try: # Intentar analizar la expresión
    trees = list(parser.parse(expanded_tokens))
    if trees: # Si existen árboles, entonces se imprimen
        print(f"Se encontraron {len(trees)} árboles sintácticos")
        for i, tree in enumerate(trees):
            print(f"\nÁrbol #{i+1}:")
            tree.pretty_print()  # Imprimir árbol en consola
            tree.draw()  # Dibujar el árbol 
            break  # Solo mostrar el primer árbol encontrado (evitar imprimir arboles subyacentes)
    else: # Si no se encontraron árboles, se imprime un mensaje de error
        print("La expresión no se pudo analizar de acuerdo con la gramática")
except Exception as e: # Manejo de errores
    print(f"Error al analizar: {e}")

# Función para interpretar el arbol de sintaxis abstracta (AST) y calcular el resultado
def interpret_ast(tree):
    if isinstance(tree, nltk.Tree):
        label = tree.label()
        
        if label == 'Digit':
            return float(tree[0])  # Dígito individual
        elif label == 'Number':
            if len(tree) == 1:  # Un solo dígito
                return interpret_ast(tree[0])
            elif len(tree) == 2:
                if tree[1].label() == 'Digit':  # Formar número de múltiples dígitos
                    return 10 * interpret_ast(tree[0]) + interpret_ast(tree[1])
                else:  # Puede ser un número decimal
                    return interpret_ast(tree[0])
            elif len(tree) == 3 and tree[1] == '.':  # Número decimal Number '.' Number
                return float(str(interpret_ast(tree[0])) + '.' + str(interpret_ast(tree[2])))
        elif label == 'Expr' and len(tree) == 3: # Para manejar operaciones de suma y resta
            left = interpret_ast(tree[0])
            op = tree[1]
            right = interpret_ast(tree[2])
            if op == '+': # Suma
                return left + right
            elif op == '-': # Resta
                return left - right
        elif label == 'Term' and len(tree) == 3: # Manejo de operaciones de multiplicación, división y módulo
            left = interpret_ast(tree[0])
            op = tree[1]
            right = interpret_ast(tree[2])
            if op == '*': # Multiplicacion
                return left * right
            elif op == '/': # Division
                return left / right
            elif op == '%': # Modulo
                return left % right
        elif label == 'Power' and len(tree) == 3: # Manejo de operaciones de potencias
            base = interpret_ast(tree[0])
            op = tree[1]
            exponent = interpret_ast(tree[2])
            if op == '^': # Potencia
                return base ** exponent
        elif label == 'Atom' and len(tree) == 3: # Manejo de expresiones entre paréntesis
            return interpret_ast(tree[1])
        elif label == 'Unary' and len(tree) == 2: # Manejo de operaciones unarias
            op = tree[0]
            value = interpret_ast(tree[1])
            if op == '+':
                return value
            elif op == '-':
                return -value
        else: # Manejo de árboles con un solo hijo        
            if len(tree) == 1:
                return interpret_ast(tree[0])
    return tree # Caso base

# Prueba de interpretación si es necesario
if 'trees' in locals() and trees:
    resultado = interpret_ast(trees[0])
    print(f"\nResultado de la evaluación: {resultado}")