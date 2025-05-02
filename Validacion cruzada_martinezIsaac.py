# Martinez Isaac
# Valdacion cruzada Lexer-Parser

# Nota: Es encesaario cerrar la ventana grafica para continuar viendo los resultados en consola
# de lo contrario no se vera el resultado de la siguiente expresion

# Librerias
import re
import nltk
from nltk.tree import Tree

class NodoAST:
    pass

class Numero(NodoAST): # Nodo para numeros
    def __init__(self, valor):
        self.valor = valor
    def __repr__(self):
        return f"Numero({self.valor})"

class OperacionBinaria(NodoAST): # Nodo para operaciones binarias (+, -, *, /, ^)
    def __init__(self, izquierda, operador, derecha):
        self.izquierda, self.operador, self.derecha = izquierda, operador, derecha
    def __repr__(self):
        return f"OperacionBinaria({self.izquierda}, '{self.operador}', {self.derecha})"

class OperacionUnaria(NodoAST): # Nodo para operaciones unarias
    def __init__(self, operador, operando):
        self.operador, self.operando = operador, operando
    def __repr__(self):
        return f"OperacionUnaria('{self.operador}', {self.operando})"

TOKENS = [ #Tokens distingue entre operadores unarios y binarios
    ('NUMERO', r'\d+(?:\.\d+)?'),
    ('MAS',    r'\+'),
    ('MENOS',  r'-'),
    ('MULT',   r'\*'),
    ('DIV',    r'/'),
    ('POT',    r'\^'),
    ('PA',     r'\('),
    ('PC',     r'\)'),
    ('ESPACIO', r'\s+')
]

regexTokens = re.compile('|'.join(f"(?P<{nombre}>" + patron + ")" for nombre, patron in TOKENS)) #Expresion regular para tokens

class Token:
    def __init__(self, tipo, valor):
        self.tipo, self.valor = tipo, valor
    def __repr__(self):
        return f"Token({self.tipo}, '{self.valor}')"

class AnalizadorLexico: # Analizador lexico: divide la cadena en tokens
    def __init__(self, texto):
        self.texto = texto
        self.tokens = []

    def tokenizar(self): # Tokeniza la cadena de entrada, es decir, la divide en tokens conformes a la expresion regular
        anterior = None
        for coincidencia in regexTokens.finditer(self.texto): #Itera sobre los tokens encontrados en la cadena de entrada
            tipo, valor = coincidencia.lastgroup, coincidencia.group()
            if tipo == 'ESPACIO': #Valoriza los espacios en blanco para ignorarlos
                continue
            if tipo in ('MENOS', 'MAS'): # Si el token es un operador unario, entonces se le asigna el tipo correspondiente
                if anterior in (None, 'MAS', 'MENOS', 'OPERADOR_BIN', 'MULT', 'DIV', 'POT', 'PA'): # Si el token anterior es un operador binario o un parentesis, entonces se le asigna el tipo correspondiente
                    tipo = 'OPERADOR_UNARIO'
                else: # Si el token es un operador binario, entonces se le asigna el tipo correspondiente
                    tipo = 'OPERADOR_BIN'
            self.tokens.append(Token(tipo, valor))
            anterior = tipo
        self.tokens.append(Token('FIN', None))
        return self.tokens

class AnalizadorSintactico: # Funcion para analizar la cadena de tokens y genera el arbol (AST)
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0

    def actual(self):
        return self.tokens[self.posicion]

    def consumir(self, tipoEsperado): # Consume el token actual si es del tipo esperado
        if self.actual().tipo == tipoEsperado:
            token = self.actual()
            self.posicion += 1
            return token
        raise SyntaxError(f"Se esperaba {tipoEsperado}, encontrado {self.actual().tipo}")

    def analizar(self): # Analiza la cadena de entrada y genera el arbol (AST)
        nodo = self.expresion()
        if self.actual().tipo != 'FIN':
            raise SyntaxError("Tokens extra al final")
        return nodo

    def expresion(self): # suma y resta
        nodo = self.termino()
        while self.actual().tipo == 'OPERADOR_BIN' and self.actual().valor in ('+', '-'):
            operador = self.consumir('OPERADOR_BIN').valor
            nodo = OperacionBinaria(nodo, operador, self.termino())
        return nodo

    def termino(self): # multiplicacion y division
        nodo = self.potencia()
        while self.actual().tipo in ('MULT', 'DIV'):
            operador = self.actual().valor
            self.consumir(self.actual().tipo)
            nodo = OperacionBinaria(nodo, operador, self.potencia())
        return nodo

    def potencia(self): # potencia
        nodo = self.atomo()
        if self.actual().tipo == 'POT':
            operador = self.consumir('POT').valor
            nodo = OperacionBinaria(nodo, operador, self.potencia())
        return nodo

    def atomo(self): # numeros y parentesis
        token = self.actual()
        if token.tipo == 'NUMERO':
            self.consumir('NUMERO')
            return Numero(float(token.valor))
        if token.tipo == 'OPERADOR_UNARIO':
            if token.valor != '-':
                raise SyntaxError(f"No soportado {token.valor}")
            operador = token.valor
            self.consumir('OPERADOR_UNARIO')
            return OperacionUnaria(operador, self.atomo())
        if token.tipo == 'PA':
            self.consumir('PA')
            nodo = self.expresion()
            self.consumir('PC')
            return nodo
        raise SyntaxError(f"Token inesperado: {token}")

def astANltk(nodo): # Convierte el AST a un arbol de NLTK para visualizarlo
    if isinstance(nodo, Numero):
        return Tree('Numero', [str(nodo.valor)])
    if isinstance(nodo, OperacionUnaria):
        return Tree('OperacionUnaria', [nodo.operador, astANltk(nodo.operando)])
    if isinstance(nodo, OperacionBinaria):
        return Tree(f"OperacionBinaria_{nodo.operador}", [astANltk(nodo.izquierda), nodo.operador, astANltk(nodo.derecha)])
    raise ValueError("Nodo AST desconocido")

def interpretar(nodo): # Se interpreta el AST y devuelve el resultado
    if isinstance(nodo, Numero):
        return nodo.valor
    if isinstance(nodo, OperacionUnaria):
        return -interpretar(nodo.operando)
    if isinstance(nodo, OperacionBinaria):
        izquierda = interpretar(nodo.izquierda)
        derecha = interpretar(nodo.derecha)
        return {
            '+': izquierda + derecha,
            '-': izquierda - derecha,
            '*': izquierda * derecha,
            '/': izquierda / derecha,
            '^': izquierda ** derecha
        }[nodo.operador]
    raise ValueError("Nodo AST desconocido")

expresiones = ["-5 * (3 + 2)", "5 - -3", "5 * + 3", "2 ^ 3 ^ 2"] #Variable auxiliar para relizar pruebas

for expresion in expresiones:
    print(f"\nExpresion: {expresion}")
    try:
        tokens = AnalizadorLexico(expresion).tokenizar()
        print(" Tokens:", tokens)
        ast = AnalizadorSintactico(tokens).analizar()
        print(" AST:", ast)
        arbol = astANltk(ast)
        arbol.pretty_print()
        arbol.draw()
        print(" Valor:", interpretar(ast))
    except Exception as error:
        print(" Error:", error)
