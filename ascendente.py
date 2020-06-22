import ply.lex as lex
palabras_reservadas = {
    'struct': '_struct',
    'continue': '_continue',
    'break': '_break',
    'return': '_return',
    'goto': '_goto',
    'if': '_if',
    'elseif': '_elseif',
    'else': 'else',
    'switch': '_switch',
    'case': '_case',
    'default': '_default',
    'while': '_while',
    'do': '_do',
    'for': '_for',
    'malloc': '_malloc',
    'sizeof': '_sizeof',
    'int': '_int',
    'char': '_char',
    'double': '_double',
    'float': '_float',
    'void': '_void'
}

tokens = [
    'llave_abre',
    'llave_cierra',
    'punto_coma',
    'parentesis_abre',
    'parentesis_cierra',
    'coma',
    'asterisco',
    'dos_puntos',
    'corchete_abre',
    'corchete_cierra',
    'punto',
    'mas',
    'menos',
    'igual',
    'division',
    'porcentaje',
    'mayor',
    'menor',
    'et',
    'elevado',
    'pleca',
    'pregunta',
    'exclamacion',
    'virgulilla'
] + list(palabras_reservadas.values())

t_llave_abre = r'{'
t_llave_cierra = r'}'
t_punto_coma = r';'
t_parentesis_abre = r'\('
t_parentesis_cierra = r'\)'
t_coma = r','
t_asterisco = r'\*'
t_dos_puntos = r':'
t_corchete_abre = r'\['
t_corchete_cierra = r'\]'
t_punto = r'.'
t_mas = r'\+'
t_menos = r'-'
t_igual = r'='
t_division = r'/'
t_porcentaje = r'%'
t_mayor = r'>'
t_menor = r'<'
t_et = r'&'
t_elevado = r'\^'
t_pleca = r'\|'
t_pregunta = r'\?'
t_exclamacion = r'!'
t_virgulilla = r'~'


def t_decimal(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Valor de float muy grande: %d", t.value)
        t.value = 0
    return t


def t_entero(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Valor de entero muy grande %d", t.value)
        t.value = 0
    return t


def t_identificador(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = palabras_reservadas.get(t.value.lower(), 'identificador')
    return t


def t_cadena(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t


def t_comentario_multilinea(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')


def t_comentario_simple(t):
    r'//.*\n'
    t.lexer.lineno += 1


t_ignore = " \t"


def t_nueva_linea(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Carácter no válido: '%s'" % t.value[0])
    t.lexer.skip(1)


def t_caracter(t):
    r'\'.{1}\'|\".{1}\"'
    t.value = t.value[1:-1]
    return t


lexer = lex.lex()
