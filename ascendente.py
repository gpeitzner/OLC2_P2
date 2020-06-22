import ply.yacc as yacc
import ply.lex as lex
palabras_reservadas = {
    'struct': '_struct',
    'continue': '_continue',
    'break': '_break',
    'return': '_return',
    'goto': '_goto',
    'if': '_if',
    'elseif': '_elseif',
    'else': '_else',
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
    'virgulilla',
    'decimal',
    'entero',
    'identificador',
    'cadena',
    'caracter'
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


def t_caracter(t):
    r'\'.{1}\''
    t.value = t.value[1:-1]
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


lexer = lex.lex()


precedence = ()


def p_init(t):
    '''
    INIT   :   CUERPO_GLOBAL
    '''


def p_cuerpo_global(t):
    '''
    CUERPO_GLOBAL   :   LISTA_GLOBAL
                    |   
    '''


def p_lista_global(t):
    '''
    LISTA_GLOBAL    :   LISTA_GLOBAL INSTRUCCION_GLOBAL
                    |   INSTRUCCION_GLOBAL
    '''


def p_instruccion_global(t):
    '''
    INSTRUCCION_GLOBAL  :   DECLARACION punto_coma
                        |   ESTRUCTURA punto_coma
                        |   FUNCION
    '''


def p_estructura(t):
    '''
    ESTRUCTURA  :   _struct identificador llave_abre CARACTERISTICAS llave_cierra
    '''


def p_caracteristicas(t):
    '''
    CARACTERISTICAS :   LISTA_CARACTERISTICAS
                    |   
    '''


def p_lista_caracteristicas(t):
    '''
    LISTA_CARACTERISTICAS   :   LISTA_CARACTERISTICAS punto_coma CARACTERISTICA
                            |   CARACTERISTICA
    '''


def p_funcion(t):
    '''
    FUNCION    :   TIPO identificador parentesis_abre PARAMETROS parentesis_cierra llave_abre CUERPO_LOCAL llave_cierra
    '''


def p_parametros(t):
    '''
    PARAMETROS  :   LISTA_PARAMETROS
                |
    '''


def p_lista_parametros(t):
    '''
    LISTA_PARAMETROS    :   LISTA_PARAMETROS coma CARACTERISTICA
                        |   CARACTERISTICA
    '''


def p_caracteristica(t):
    '''
    CARACTERISTICA  :   TIPO IDENTIFICADORES
    '''


def p_identificadores(t):
    '''
    IDENTIFICADORES :   asterisco asterisco identificador
                    |   asterisco identificador
                    |   identificador
                    |   parentesis_abre IDENTIFICADORES parentesis_cierra
    '''


def p_cuerpo_local(t):
    '''
    CUERPO_LOCAL    :   LISTA_LOCAL
                    |
    '''


def p_lista_local(t):
    '''
    LISTA_LOCAL :   LISTA_LOCAL INSTRUCCION_LOCAL
                |   INSTRUCCION_LOCAL
    '''


def p_instruccion_local(t):
    '''
    INSTRUCCION_LOCAL   :   ETIQUETA
                        |   SALTO
                        |   DECLARACION punto_coma
                        |   ASIGNACION punto_coma
                        |   IF
                        |   SWITCH
                        |   WHILE
                        |   DO
                        |   FOR
                        |   _continue punto_coma
                        |   _break punto_coma
                        |   _return EXPRESION punto_coma
    '''


def p_etiqueta(t):
    '''
    ETIQUETA    :   identificador dos_puntos
    '''


def p_salto(t):
    '''
    SALTO   :   _goto identificador punto_coma
    '''


def p_declaracion(t):
    '''
    DECLARACION :   TIPO LISTA_DECLARACION
    '''


def p_lista_declaracion(t):
    '''
    LISTA_DECLARACION   :   LISTA_DECLARACION coma DECLARACION_FINAL
                        |   DECLARACION_FINAL
    '''


def p_declaracion_final(t):
    '''
    DECLARACION_FINAL   :   IDENTIFICADORES INDICES igual EXPRESION
                        |   IDENTIFICADORES INDICES
    '''


def p_indices(t):
    '''
    INDICES :   ACCESOS
            |
    '''


def p_accesos(t):
    '''
    ACCESOS :   ACCESOS ACCESO
            |   ACCESO
    '''


def p_acceso(t):
    '''
    ACCESO  :   corchete_abre EXPRESION corchete_cierra
            |   corchete_abre corchete_cierra
    '''


def p_asignacion(t):
    '''
    ASIGNACION  :   IDENTIFICADORES INDICES COMPUESTO EXPRESION 
                |   IDENTIFICADORES INDICES punto identificador COMPUESTO EXPRESION 
                |   IDENTIFICADORES INDICES menos mayor identificador COMPUESTO EXPRESION 
                |   IDENTIFICADORES mas mas 
                |   IDENTIFICADORES menos menos 
    '''


def p_compuesto(t):
    '''
    COMPUESTO   :   igual
                |   mas igual
                |   asterisco igual
                |   division igual
                |   porcentaje igual
                |   menor menor igual
                |   mayor mayor igual
                |   et igual
                |   elevado igual
                |   pleca igual
    '''


def p_if(t):
    '''
    IF  :   _if parentesis_abre EXPRESION parentesis_cierra llave_abre CUERPO_LOCAL llave_cierra ELSEIFS ELSE
    '''


def p_elseifs(t):
    '''
    ELSEIFS     :   LISTA_ELSEIF
                |   
    '''


def p_lista_elseif(t):
    '''
    LISTA_ELSEIF    :   LISTA_ELSEIF ELSEIF
                    |   ELSEIF
    '''


def p_elseif(t):
    '''
    ELSEIF  :   _elseif parentesis_abre EXPRESION parentesis_cierra llave_abre CUERPO_LOCAL llave_cierra
    '''


def p_else(t):
    '''
    ELSE    :   _else llave_abre CUERPO_LOCAL llave_cierra
    '''


def p_switch(t):
    '''
    SWITCH  :   _switch parentesis_abre EXPRESION parentesis_cierra llave_abre CASES DEFAULT_CASE llave_cierra
    '''


def p_cases(t):
    '''
    CASES   :   LISTA_CASE
            |
    '''


def p_lista_case(t):
    '''
    LISTA_CASE  :   LISTA_CASE CASE
                |   CASE
    '''


def p_case(t):
    '''
    CASE    :   _case EXPRESION dos_puntos CUERPO_LOCAL
    '''


def p_default_case(t):
    '''
    DEFAULT_CASE    :   _default dos_puntos CUERPO_LOCAL
    '''


def p_while(t):
    '''
    WHILE   :   _while parentesis_abre EXPRESION parentesis_cierra llave_abre CUERPO_LOCAL llave_cierra
    '''


def p_do(t):
    '''
    DO  :   _do llave_abre CUERPO_LOCAL llave_cierra _while parentesis_abre EXPRESION parentesis_cierra punto_coma
    '''


def p_for(t):
    '''
    FOR :   _for parentesis_abre DECLARACION punto_coma EXPRESION punto_coma ASIGNACION parentesis_cierra llave_abre CUERPO_LOCAL llave_cierra
    '''


def p_expresion(t):
    '''
    EXPRESION   :   EXPRESION mas EXPRESION
                |   EXPRESION menos EXPRESION
                |   EXPRESION asterisco EXPRESION
                |   EXPRESION division EXPRESION
                |   EXPRESION porcentaje EXPRESION
                |   EXPRESION igual igual EXPRESION
                |   EXPRESION exclamacion igual EXPRESION
                |   EXPRESION mayor EXPRESION
                |   EXPRESION menor EXPRESION
                |   EXPRESION mayor igual EXPRESION
                |   EXPRESION menor igual EXPRESION
                |   EXPRESION et et EXPRESION
                |   EXPRESION pleca pleca EXPRESION
                |   EXPRESION menor menor EXPRESION
                |   EXPRESION mayor mayor EXPRESION
                |   EXPRESION et EXPRESION
                |   EXPRESION elevado EXPRESION
                |   EXPRESION pregunta EXPRESION dos_puntos EXPRESION
                |   menos EXPRESION
                |   exclamacion EXPRESION
                |   virgulilla EXPRESION
                |   parentesis_abre TIPO asterisco parentesis_cierra _malloc parentesis_abre _sizeof parentesis_abre TIPO parentesis_cierra parentesis_cierra
                |   identificador
                |   identificador parentesis_abre EXPRESIONES parentesis_cierra
                |   identificador punto identificador
                |   identificador ACCESOS
                |   identificador menos mayor identificador
                |   et identificador
                |   llave_abre EXPRESIONES llave_cierra
                |   caracter
                |   cadena
                |   entero
                |   decimal
    '''


def p_expresiones(t):
    '''
    EXPRESIONES :   LISTA_EXPRESIONES
                |
    '''


def p_lista_expresiones(t):
    '''
    LISTA_EXPRESIONES   :   LISTA_EXPRESIONES coma EXPRESION
                        |   EXPRESION
    '''


def p_tipo(t):
    '''
    TIPO    :   _int
            |   _char
            |   _double
            |   _float
            |   _struct identificador
            |   _void
    '''


def p_error(t):
    print(t)
    print("Error sintáctico en '%s'" % t.value)


parser = yacc.yacc()


def parse(input):
    return parser.parse(input)