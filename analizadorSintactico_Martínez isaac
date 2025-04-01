# Martínez Isaac

# Librerias
import nltk
from nltk import CFG

# Definir la gramática en formato CFG
grammar = CFG.fromstring("""
    Expr -> Expr '+' Term | Expr '-' Term | Term
    Term -> Term '*' Factor | Factor
    Factor -> '(' Expr ')' | 'a' | 'b' | 'c' | 'd'
""")

tokens = ['a', '+', 'b', '*', '(', 'c', '-', 'd', ')'] # Definir tokens ( en este caso el ejemplo: 'a + b * (c - d)')

parser = nltk.parse.EarleyChartParser(grammar) # Analizar utilizando el algoritmo de Earley

# Intentar analizar la expresión e imprimir el árbol de derivación
for tree in parser.parse(tokens):
    tree.pretty_print()  # Imprimir texto con foramto de arbol ( terminal / consola)
    tree.draw()  # Mostrar el árbol en una ventana

# PREGUNTA
# ¿Cómo puedes modificar el código para analizar expresiones más complejas o incluir más tipos de datos?

# Es posible modificar la gramática CFG para incluir más reglas y tipos de datos. Por ejemplo, podemos agregar reglas para manejar números enteros, 
# cadenas de texto, o incluso estructuras de control como if-else o bucles. Tambien podemos definir funciones y procedimientos en la gramática para 
# hacerla más robusta y capaz de analizar programas completos.
# De igual manera esta la opcion de agregar más tokens a la lista de tokens y ajustar el analizador para que reconozca los nuevos tokens. Esto
# permitirá analizar una gama más amplia de expresiones y estructuras de código.

# Un ejemplo de como podrías modificar la gramatica puede ser el siguiente

grammar = CFG.fromstring("""
    Assign -> Variable '=' Expr
    Expr -> Expr '+' Term | Expr '-' Term | Term
    Term -> Term '*' Factor | Term '/' Factor | Factor
    Factor -> '(' Expr ')' | Number | Hexadecimal | Variable | String
    Number -> '42' | '10' | '20' | '30' | '100' | '255'  
    Variable -> 'x' | 'y' | 'z' | 'str'
    Hexadecimal -> '0xFF' | '0x1A' | '0xB4'  
    String -> '"' CharSequence '"'
    CharSequence -> Char | Char CharSequence
    Char -> 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'x' | 'F' | '\\' | '"'
""")

# por poner un ejemplo con los tokens:
# tokens = ['x', '=', '0xFF', '+', '42', '*', '(', 'y', '-', 'z', ')']
