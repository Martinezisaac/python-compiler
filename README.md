# 🛠️ Compilador de C en Python

> Proyecto académico de Ingeniería en Computación — **Martínez Isaac**

Un compilador completo del lenguaje **C** implementado íntegramente en **Python**. El proyecto recorre las cuatro etapas clásicas de la construcción de compiladores: análisis léxico, análisis sintáctico, análisis semántico y generación de código intermedio.

---

## 📚 Tabla de Contenidos

1. [¿De qué trata el proyecto?](#de-qué-trata-el-proyecto)
2. [Pipeline de compilación](#pipeline-de-compilación)
3. [Características del lenguaje soportado](#características-del-lenguaje-soportado)
4. [Estructura del repositorio](#estructura-del-repositorio)
5. [Requisitos e instalación](#requisitos-e-instalación)
6. [Cómo ejecutar](#cómo-ejecutar)
7. [Descripción de cada módulo](#descripción-de-cada-módulo)
8. [Formato del código intermedio](#formato-del-código-intermedio)
9. [Manejo de errores](#manejo-de-errores)
10. [Ejemplo de uso](#ejemplo-de-uso)

---

## ¿De qué trata el proyecto?

Este repositorio contiene un **compilador didáctico** capaz de procesar programas escritos en un subconjunto del lenguaje **C**. Su objetivo es ilustrar, de forma práctica y progresiva, cada una de las fases que un compilador real ejecuta al transformar código fuente en código ejecutable.

El compilador **no genera código máquina nativo**, sino **código de tres direcciones** (código intermedio), que es el paso previo a la optimización y la generación de código final en compiladores industriales.

Este proyecto es ideal para:
- Estudiantes de Ingeniería en Sistemas / Computación que cursan **Teoría de Compiladores**.
- Cualquier persona que quiera entender **cómo funciona un compilador** desde cero.
- Desarrolladores que deseen explorar técnicas de análisis de lenguajes usando Python.

---

## Pipeline de compilación

```
┌─────────────────────┐
│   Código Fuente C   │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Análisis Léxico    │  ← analizadorLexico()
│  (Tokenización)     │    Convierte texto en tokens
└─────────┬───────────┘
          │  Lista de tokens (tipo, valor)
          ▼
┌─────────────────────┐
│  Análisis Sintáctico│  ← analizadorSintactico
│  (Parser)           │    Construye el AST (Árbol de Sintaxis Abstracta)
└─────────┬───────────┘
          │  AST (tuplas anidadas)
          ▼
┌─────────────────────┐
│  Análisis Semántico │  ← analizadorSemantico
│  (Tipos y semántica)│    Verifica tipos, variables declaradas, etc.
└─────────┬───────────┘
          │  AST validado + tabla de símbolos
          ▼
┌─────────────────────┐
│  Generación de      │  ← generadorCodigo
│  Código Intermedio  │    Produce código de tres direcciones
└─────────────────────┘
```

---

## Características del lenguaje soportado

### Tipos de datos
| Tipo     | Descripción                         |
|----------|-------------------------------------|
| `int`    | Enteros                             |
| `float`  | Punto flotante simple precisión     |
| `double` | Punto flotante doble precisión      |
| `char`   | Carácter individual                 |
| `String` | Cadena de texto *(extensión del compilador)* |
| `void`   | Sin tipo de retorno (funciones)     |

### Estructuras de control
| Estructura    | Ejemplo                                         |
|---------------|-------------------------------------------------|
| `if / else`   | `if (x > 0) { ... } else { ... }`               |
| `while`       | `while (i < 10) { ... }`                        |
| `for`         | `for (int i = 0; i < n; i++) { ... }`           |
| `do-while`    | `do { ... } while (cond);`                      |

### Operadores
| Categoría    | Operadores                          |
|--------------|-------------------------------------|
| Aritméticos  | `+`, `-`, `*`, `/`, `%`             |
| Relacionales | `<`, `>`, `<=`, `>=`, `==`, `!=`    |
| Lógicos      | `&&`, `\|\|`                        |
| Asignación   | `=`                                 |
| Unarios      | `-` (negación), `+`, `&` (dirección)|

### Otras características
- Declaración de **funciones** con parámetros y retorno
- Llamadas a funciones (`printf`, `scanf`, funciones definidas por el usuario)
- **Directivas del preprocesador**: `#include`, `#define`
- **Comentarios**: de línea (`//`) y de bloque (`/* ... */`)
- **Inicialización** de variables en la declaración
- Precedencia de operadores con paréntesis

---

## Estructura del repositorio

```
python-compiler/
├── README.md
│       Documentación del proyecto (este archivo)
│
├── Compilador_martinezIsaac.py
│       ★ ARCHIVO PRINCIPAL — Pipeline completo de compilación:
│         · Análisis léxico
│         · Análisis sintáctico (parser descendente recursivo)
│         · Análisis semántico (tabla de símbolos y tipos)
│         · Generación de código intermedio (tres direcciones)
│         · Suite de pruebas integrada
│
├── tokens_Martínez Isaac.py
│       Demostración aislada del analizador léxico.
│       Tokeniza código C con seguimiento de línea y columna.
│
├── analizadorSintactico_Martínez isaac.py
│       Demostración del parser para expresiones matemáticas.
│       Construye y visualiza el AST usando NLTK.
│
├── extensionGramatica_Martínez Isaac.py
│       Gramática extendida con NLTK (CFG + parser de Earley).
│       Soporta funciones matemáticas: sin, cos, sqrt, max, min.
│
└── Validacion cruzada_martinezIsaac.py
        Integración léxico + parser con validación cruzada.
        Demuestra el flujo completo para expresiones aritméticas.
```

---

## Requisitos e instalación

### Requisitos previos
- **Python 3.7+**
- **pip** (gestor de paquetes de Python)

### Instalación de dependencias

```bash
pip install nltk
```

> **Nota:** Los módulos `re` (expresiones regulares) de la biblioteca estándar de Python son suficientes para el análisis léxico. La librería `nltk` se utiliza en los módulos de gramática extendida y visualización de árboles.

---

## Cómo ejecutar

### Ejecutar el compilador completo

```bash
python Compilador_martinezIsaac.py
```

Al correr este archivo obtendrás la salida de **todas las etapas** del compilador para los casos de prueba integrados:

```
=== ANÁLISIS LÉXICO ===
[('keyword', 'int'), ('id', 'main'), ('(', '('), ...]

=== ANÁLISIS SINTÁCTICO ===
('programa', [('funcion', 'main', ...)])

=== ANÁLISIS SEMÁNTICO ===
Análisis semántico completado sin errores.

=== CÓDIGO INTERMEDIO ===
function main:
    t1 = 5
    x = t1
    ...
```

### Ejecutar los módulos individuales

```bash
# Solo el analizador léxico
python "tokens_Martínez Isaac.py"

# Solo el analizador sintáctico (expresiones matemáticas)
python "analizadorSintactico_Martínez isaac.py"

# Gramática extendida con NLTK
python "extensionGramatica_Martínez Isaac.py"

# Validación cruzada léxico + parser
python "Validacion cruzada_martinezIsaac.py"
```

---

## Descripción de cada módulo

### 1. Análisis Léxico (`analizadorLexico`)

**Archivo:** `Compilador_martinezIsaac.py` — líneas 12–76  
**Archivo independiente:** `tokens_Martínez Isaac.py`

Convierte el código fuente C (texto plano) en una **secuencia de tokens**. Cada token es una tupla `(tipo, valor)`, por ejemplo:

```
("keyword", "int")
("id",      "x")
("op",      "=")
("num",     "5")
("delim",   ";")
```

**Tipos de tokens reconocidos:**

| Token            | Descripción                                |
|------------------|--------------------------------------------|
| `keyword`        | Palabras reservadas de C                   |
| `id`             | Identificadores (variables, funciones)     |
| `num`            | Números enteros y decimales                |
| `string`         | Literales de cadena `"..."`                |
| `char_literal`   | Literales de carácter `'...'`              |
| `op`             | Operadores (`+`, `-`, `*`, `==`, etc.)     |
| `delim`          | Delimitadores (`;`, `{`, `}`, `(`, `)`)    |
| `comment`        | Comentarios de línea y bloque              |
| `preprocessor`   | Directivas `#include`, `#define`           |

El analizador léxico **ignora espacios en blanco** y **saltos de línea**, reportando errores para caracteres no reconocidos.

---

### 2. Análisis Sintáctico (`analizadorSintactico`)

**Archivo:** `Compilador_martinezIsaac.py` — líneas 85–586  
**Archivo independiente:** `analizadorSintactico_Martínez isaac.py`

Recibe la lista de tokens y construye el **Árbol de Sintaxis Abstracta (AST)**. Utiliza un **parser descendente recursivo** con gestión de precedencia de operadores (algoritmo Pratt).

El AST se representa como tuplas anidadas. Por ejemplo, para `int x = 5 + y;`:

```python
('declaracion', 'int', 'x', ('op', '+', ('num', 5), ('id', 'y')))
```

**Construcciones parseadas:**
- Declaraciones de variables con y sin inicialización
- Definiciones y llamadas a funciones
- Sentencias de control (`if`, `while`, `for`, `do-while`)
- Expresiones con precedencia correcta

---

### 3. Análisis Semántico (`analizadorSemantico`)

**Archivo:** `Compilador_martinezIsaac.py` — líneas 591–987

Recorre el AST y verifica la **corrección semántica** del programa:

- **Tabla de símbolos:** registra cada variable con su tipo y ámbito.
- **Tabla de funciones:** registra firmas de funciones (nombre, parámetros, tipo de retorno).
- **Verificación de tipos:** detecta asignaciones incompatibles (p.ej., `int x = "hola"`).
- **Variables no declaradas:** error al usar una variable sin declararla.
- **Llamadas a funciones:** verifica que el número y tipos de argumentos sean correctos.
- **Promoción de tipos:** aplica reglas `double > float > int`.

Ejemplo de error detectado:
```
Error semántico: Variable 'z' no declarada.
Error semántico: Tipos incompatibles en asignación: int = String.
```

---

### 4. Generación de Código Intermedio (`generadorCodigo`)

**Archivo:** `Compilador_martinezIsaac.py` — líneas 996–1264

Transforma el AST validado en **código de tres direcciones**, una representación lineal que es independiente de la arquitectura de hardware objetivo.

**Convenciones:**
- Variables temporales: `t1`, `t2`, `t3`, ...
- Etiquetas de salto: `L1`, `L2`, `L3`, ...

**Ejemplo de código generado para un `if`:**

```c
// Código fuente C:
if (x > 0) {
    y = x + 1;
} else {
    y = 0;
}
```

```
# Código intermedio generado:
    t1 = x > 0
    if t1 goto L1
    goto L2
L1:
    t2 = x + 1
    y = t2
    goto L3
L2:
    y = 0
L3:
```

---

### 5. Gramática Extendida (`extensionGramatica_Martínez Isaac.py`)

Usa la librería **NLTK** con una **Gramática Libre de Contexto (CFG)** y el **parser de Earley** para analizar expresiones matemáticas complejas.

**Gramática (simplificada):**
```
Expr   → Expr '+' Term | Expr '-' Term | Term
Term   → Term '*' Factor | Term '/' Factor | Term '%' Factor | Factor
Factor → Power | Unary
Power  → Atom '^' Power | Atom
Atom   → Número | Constante | '(' Expr ')' | Función
Función→ sin(Expr) | cos(Expr) | sqrt(Expr) | max(Expr,Expr) | min(Expr,Expr)
```

**Expresión de ejemplo:**
```
123.45 + sin(PI) * 2 / (1 - 5)^2^3
```

---

### 6. Validación Cruzada (`Validacion cruzada_martinezIsaac.py`)

Integra el analizador léxico y el sintáctico para demostrar el **flujo completo** en expresiones aritméticas. Incluye:

- Distinción inteligente entre operadores **unarios** y **binarios** (p. ej., `-5` vs `a - b`).
- Construcción y visualización del AST con NLTK.
- **Intérprete** que evalúa el AST y calcula el resultado numérico.

**Casos de prueba:**

| Expresión     | Resultado |
|---------------|-----------|
| `-5 * (3 + 2)` | `-25`    |
| `5 - -3`       | `8`      |
| `2 ^ 3 ^ 2`    | `512`    |

---

## Formato del código intermedio

El código intermedio generado sigue el formato de **instrucciones de tres direcciones**:

| Instrucción              | Significado                            |
|--------------------------|----------------------------------------|
| `t1 = a + b`             | Asignación con operación binaria       |
| `t1 = -a`                | Operación unaria                       |
| `x = t1`                 | Asignación simple                      |
| `L1:`                    | Definición de etiqueta                 |
| `if t1 goto L2`          | Salto condicional                      |
| `goto L1`                | Salto incondicional                    |
| `function main:`         | Inicio de función                      |
| `return t1`              | Retorno de función                     |
| `param x`                | Paso de parámetro                      |
| `call func, n`           | Llamada a función con `n` argumentos   |

---

## Manejo de errores

El compilador detecta y reporta tres categorías de errores:

### Errores Léxicos
Caracteres o secuencias que no corresponden a ningún token válido.
```
Error léxico en línea 3: carácter no reconocido '@'
```

### Errores Sintácticos
Estructuras gramaticales incorrectas (falta `;`, paréntesis sin cerrar, etc.).
```
Error sintáctico: se esperaba ';' después de la expresión.
Error sintáctico: declaración de función malformada.
```

### Errores Semánticos
Uso incorrecto de variables, tipos incompatibles, funciones mal llamadas.
```
Error semántico: Variable 'x' no declarada.
Error semántico: Tipos incompatibles: no se puede asignar String a int.
Error semántico: La función 'suma' espera 2 argumentos, se recibieron 3.
```

---

## Ejemplo de uso

```python
from Compilador_martinezIsaac import (
    analizadorLexico,
    analizadorSintactico,
    analizadorSemantico,
    generadorCodigo
)

codigo_fuente = """
int suma(int a, int b) {
    return a + b;
}

int main() {
    int x = 10;
    int y = 20;
    int resultado = suma(x, y);
    printf("%d", resultado);
    return 0;
}
"""

# Etapa 1: Análisis léxico
tokens = analizadorLexico(codigo_fuente)
print("Tokens:", tokens)

# Etapa 2: Análisis sintáctico
parser = analizadorSintactico(tokens)
ast = parser.analizarSintaxis()
print("AST:", ast)

# Etapa 3: Análisis semántico
semantico = analizadorSemantico()
valido = semantico.analizar(ast)
print("Semánticamente válido:", valido)

# Etapa 4: Generación de código intermedio
generador = generadorCodigo()
codigo_intermedio = generador.generar(ast)
print("Código intermedio:")
for instruccion in codigo_intermedio:
    print(" ", instruccion)
```

---

## Autor

**Martínez Isaac** — Ingeniería en Computación

---

*Este proyecto es de carácter educativo y fue desarrollado para la materia de Teoría de Compiladores.*
