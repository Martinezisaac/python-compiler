# Martínez Isaac

# Librerias
import nltk
from nltk import CFG

# Definir la gramática en formato CFG
grammar = CFG.fromstring("""
    Expr -> Expr '+' Term | Expr '-' Term | Term
    Term -> Term '*' Power | Term '/' Power | Term '%' Power | Power
    Power -> Unary '^' Power | Unary
    Unary -> '+' Unary | '-' Unary | Factor
    Factor -> '(' Expr ')' | Func | Const | Number | ID | ID '=' Expr

    Func -> FuncName '(' ArgList ')'
    FuncName -> 'sin' | 'cos' | 'sqrt' | 'max'

    ArgList -> Expr | Expr ',' ArgList

    Const -> 'PI' | 'E'
    ID -> 'x' | 'y' | 'z' | 'a' | 'b' | 'c'

    Number -> '1' | '2' | '3' | '4' | '5'
""")


tokens = ['3', '+', '4', '*', '2', '/', '(', '1', '-', '5', ')', '^', '2', '^', '3'] # Definir tokens ( en este caso el ejemplo: '3 + 4 * 2 / (1 - 5) ^ 2 ^ 3')


parser = nltk.parse.EarleyChartParser(grammar) # Analizar utilizando el algoritmo de Earley

# Intentar analizar la expresión e imprimir el árbol de derivación
for tree in parser.parse(tokens):
    tree.pretty_print()  # Imprimir texto con foramto de arbol ( terminal / consola)
    tree.draw()  # Mostrar el árbol en una ventana