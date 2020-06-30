import ply.yacc as yacc
import ply.lex as lex
import clases
from PyQt5 import QtWidgets, QtGui
palabras_reservadas = {
    'struct': '_struct',
    'continue': '_continue',
    'break': '_break',
    'return': '_return',
    'goto': '_goto',
    'if': '_if',
    'else': '_else',
    'switch': '_switch',
    'case': '_case',
    'default': '_default',
    'while': '_while',
    'do': '_do',
    'for': '_for',
    'sizeof': '_sizeof',
    'int': '_int',
    'char': '_char',
    'double': '_double',
    'float': '_float',
    'void': '_void',
    'printf': '_printf',
    'scanf': '_scanf'
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
    'aumento',
    'decremento',
    'desplazamiento_izquierdo',
    'desplazamiento_derecho',
    'mayor_igual',
    'menor_igual',
    'equivale',
    'distinto',
    'and',
    'or',
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
t_punto = r'\.'
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
t_aumento = r'\+\+'
t_decremento = r'--'
t_desplazamiento_izquierdo = r'<<'
t_desplazamiento_derecho = r'>>'
t_mayor_igual = r'>='
t_menor_igual = r'<='
t_equivale = r'=='
t_distinto = r'!='
t_and = r'&&'
t_or = r'\|\|'


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
    mostar_error("ERROR: Léxico en: "+str(t.value[0])+", línea: " + str(
        t.lineno)+", columna: "+str(obtener_columna(entrada, t))+".")
    errores_lexicos.append(clases._Error(str(t.value[0]), str(
        t.lineno), str(obtener_columna(entrada, t))))
    t.lexer.skip(1)


precedence = (('left', 'coma'), ('right', 'NIVEL14'), ('right', 'NIVEL13'),
              ('left', 'or'), ('left', 'and'), ('left', 'pleca'),
              ('left', 'elevado'), ('left', 'et'), ('left', 'equivale', 'distinto'),
              ('left', 'mayor', 'menor', 'mayor_igual', 'menor_igual'),
              ('left', 'desplazamiento_izquierdo',
               'desplazamiento_derecho'), ('left', 'mas', 'menos'),
              ('left', 'asterisco', 'division', 'porcentaje'), ('right', 'NIVEL2'),
              ('left', 'parentesis_abre', 'parentesis_cierra', 'corchete_abre', 'corchete_cierra'))


def p_init(t):
    '''
    INIT   :   CUERPO_GLOBAL
    '''
    t[0] = t[1]


def p_cuerpo_global(t):
    '''
    CUERPO_GLOBAL   :   LISTA_GLOBAL
    '''
    t[0] = t[1]


def p_cuerpo_global_vacio(t):
    '''
    CUERPO_GLOBAL   :
    '''
    t[0] = None


def p_lista_global_lista(t):
    '''
    LISTA_GLOBAL    :   LISTA_GLOBAL INSTRUCCION_GLOBAL
    '''
    t[1].append(t[2])
    t[0] = t[1]


def p_lista_global_instruccion(t):
    '''
    LISTA_GLOBAL    :   INSTRUCCION_GLOBAL
    '''
    t[0] = [t[1]]


def p_instruccion_global(t):
    '''
    INSTRUCCION_GLOBAL  :   DECLARACION punto_coma
                        |   ESTRUCTURA punto_coma
                        |   FUNCION
    '''
    t[0] = t[1]


def p_estructura(t):
    '''
    ESTRUCTURA  :   _struct identificador llave_abre CARACTERISTICAS llave_cierra
    '''
    t[0] = clases.Estructura(t[2], t[4], str(t.slice[1].lineno))


def p_caracteristicas(t):
    '''
    CARACTERISTICAS :   LISTA_CARACTERISTICAS
    '''
    t[0] = t[1]


def p_caracteristicas_vacio(t):
    '''
    CARACTERISTICAS :
    '''
    t[0] = None


def p_lista_caracteristicas_lista(t):
    '''
    LISTA_CARACTERISTICAS   :   LISTA_CARACTERISTICAS CARACTERISTICA
    '''
    t[1].append(t[2])
    t[0] = t[1]


def p_lista_caracteristicas_caracteristica(t):
    '''
    LISTA_CARACTERISTICAS : CARACTERISTICA
    '''
    t[0] = [t[1]]


def p_caracteristica(t):
    '''
    CARACTERISTICA  :   DECLARACION punto_coma
    '''
    t[0] = t[1]


def p_funcion(t):
    '''
    FUNCION    :   TIPO identificador parentesis_abre PARAMETROS parentesis_cierra llave_abre CUERPO_LOCAL llave_cierra
    '''
    t[0] = clases.Funcion(t[1], t[2], t[4], t[7])


def p_parametros(t):
    '''
    PARAMETROS  :   LISTA_PARAMETROS
    '''
    t[0] = t[1]


def p_parametros_vacio(t):
    '''
    PARAMETROS  :
    '''
    t[0] = None


def p_lista_parametros_lista(t):
    '''
    LISTA_PARAMETROS    :   LISTA_PARAMETROS coma PARAMETRO
    '''
    t[1].append(t[3])
    t[0] = t[1]


def p_lista_parametros_parametro(t):
    '''
    LISTA_PARAMETROS    :   PARAMETRO
    '''
    t[0] = [t[1]]


def p_parametro(t):
    '''
    PARAMETRO   :   TIPO identificador
    '''
    t[0] = clases.Parametro(t[1], False, t[2])


def p_parametro_apuntador(t):
    '''
    PARAMETRO   :   TIPO et identificador
    '''
    t[0] = clases.Parametro(t[1], True, t[3])


def p_cuerpo_local(t):
    '''
    CUERPO_LOCAL    :   LISTA_LOCAL
    '''
    t[0] = t[1]


def p_cuerpo_local_vacio(t):
    '''
    CUERPO_LOCAL    :
    '''
    t[0] = None


def p_lista_local(t):
    '''
    LISTA_LOCAL :   LISTA_LOCAL INSTRUCCION_LOCAL
    '''
    t[1].append(t[2])
    t[0] = t[1]


def p_lista_local_instruccion(t):
    '''
    LISTA_LOCAL :   INSTRUCCION_LOCAL
    '''
    t[0] = [t[1]]


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
                        |   PRINT punto_coma
                        |   METODO punto_coma

    '''
    t[0] = t[1]


def p_instruccion_local_print(t):
    '''
    PRINT   :   _printf parentesis_abre LISTA_EXPRESIONES parentesis_cierra
    '''
    t[0] = clases._PrintF(t[3], str(t.slice[1].lineno))


def p_instruccion_local_continue(t):
    '''
    INSTRUCCION_LOCAL   :   _continue punto_coma
    '''
    t[0] = clases._Continue(str(t.slice[1].lineno))


def p_instruccion_local_break(t):
    '''
    INSTRUCCION_LOCAL   :   _break punto_coma
    '''
    t[0] = clases._Break(str(t.slice[1].lineno))


def p_instruccion_local_return(t):
    '''
    INSTRUCCION_LOCAL   :   _return EXPRESION punto_coma
    '''
    t[0] = clases._Return(t[2], str(t.slice[1].lineno))


def p_instruccion_local_return_vacio(t):
    '''
    INSTRUCCION_LOCAL   :   _return punto_coma
    '''
    t[0] = clases._Return(None, str(t.slice[1].lineno))


def p_metodo(t):
    '''
    METODO  :   identificador parentesis_abre EXPRESIONES parentesis_cierra 
    '''
    t[0] = clases.Metodo(t[1], t[3], str(t.slice[1].lineno))


def p_etiqueta(t):
    '''
    ETIQUETA    :   identificador dos_puntos
    '''
    t[0] = clases.Etiqueta(t[1], str(t.slice[1].lineno))


def p_salto(t):
    '''
    SALTO   :   _goto identificador punto_coma
    '''
    t[0] = clases.Salto(t[2], str(t.slice[1].lineno))


def p_declaracion(t):
    '''
    DECLARACION :   TIPO LISTA_DECLARACION
    '''
    t[0] = clases.Declaracion(t[1], t[2])


def p_lista_declaracion_lista(t):
    '''
    LISTA_DECLARACION   :   LISTA_DECLARACION coma DECLARACION_FINAL
    '''
    t[1].append(t[3])
    t[0] = t[1]


def p_lista_declaracion_declaracion(t):
    '''
    LISTA_DECLARACION   :   DECLARACION_FINAL
    '''
    t[0] = [t[1]]


def p_declaracion_final(t):
    '''
    DECLARACION_FINAL   :   identificador INDICES
    '''
    t[0] = clases.DeclaracionFinal(t[1], t[2], None, str(t.slice[1].lineno))


def p_declaracion_final_expresion(t):
    '''
    DECLARACION_FINAL   :   identificador INDICES igual EXPRESION
    '''
    t[0] = clases.DeclaracionFinal(t[1], t[2], t[4], str(t.slice[1].lineno))


def p_indices(t):
    '''
    INDICES :   ACCESOS
    '''
    t[0] = t[1]


def p_indices_vacio(t):
    '''
    INDICES :
    '''
    t[0] = None


def p_accesos_lista(t):
    '''
    ACCESOS :   ACCESOS ACCESO
    '''
    t[1].append(t[2])
    t[0] = t[1]


def p_accesos_acceso(t):
    '''
    ACCESOS :   ACCESO
    '''
    t[0] = [t[1]]


def p_acceso(t):
    '''
    ACCESO  :   corchete_abre EXPRESION corchete_cierra 
    '''
    t[0] = t[2]


def p_acceso_vacio(t):
    '''
    ACCESO : corchete_abre corchete_cierra
    '''
    t[0] = []


def p_asignacion_normal(t):
    '''
    ASIGNACION  :   identificador INDICES COMPUESTO EXPRESION 
    '''
    t[0] = clases.AsignacionNormal(
        t[1], t[2], t[3], t[4], str(t.slice[1].lineno))


def p_asignacion_estructura(t):
    '''
    ASIGNACION  :   identificador INDICES punto identificador COMPUESTO EXPRESION 
    '''
    t[0] = clases.AsignacionEstructura(
        t[1], t[2], t[4], t[5], t[6], str(t.slice[1].lineno))


def p_asignacion_aumento(t):
    '''
    ASIGNACION  :   identificador aumento %prec NIVEL2
    '''
    t[0] = clases.AsignacionAumento(t[1], str(t.slice[1].lineno))


def p_asignacion_decremento(t):
    '''
    ASIGNACION  :   identificador decremento %prec NIVEL2
    '''
    t[0] = clases.AsignacionDecremento(t[1], str(t.slice[1].lineno))


def p_compuesto(t):
    '''
    COMPUESTO   :   igual %prec NIVEL14
                |   mas igual %prec NIVEL14
                |   menos igual %prec NIVEL14
                |   asterisco igual %prec NIVEL14
                |   division igual %prec NIVEL14
                |   porcentaje igual %prec NIVEL14
                |   desplazamiento_izquierdo igual %prec NIVEL14
                |   desplazamiento_derecho igual %prec NIVEL14
                |   et igual %prec NIVEL14
                |   elevado igual %prec NIVEL14
                |   pleca igual %prec NIVEL14
    '''
    t[0] = t[1]


def p_if(t):
    '''
    IF  :   _if parentesis_abre EXPRESION parentesis_cierra llave_abre CUERPO_LOCAL llave_cierra
    '''
    t[0] = clases._If(t[3], t[6], None, None, str(t.slice[1].lineno))


def p_if_else(t):
    '''
    IF  :   _if parentesis_abre EXPRESION parentesis_cierra llave_abre CUERPO_LOCAL llave_cierra ELSE
    '''
    t[0] = clases._If(t[3], t[6], None, t[8], str(t.slice[1].lineno))


def p_if_elseif(t):
    '''
    IF  :   _if parentesis_abre EXPRESION parentesis_cierra llave_abre CUERPO_LOCAL llave_cierra ELSEIF IF_FINAL
    '''
    _else = None
    _elseifs = [t[8]]
    if len(t[9]) > 0:
        if isinstance(t[9][len(t[9])-1], clases._Else):
            _else = t[9].pop()
        _elseifs = _elseifs + t[9]
    t[0] = clases._If(t[3], t[6], _elseifs, _else, str(t.slice[1].lineno))


def p_if_final_elseif(t):
    '''
    IF_FINAL    :   ELSEIF  IF_FINAL
    '''
    t[0] = [t[1]] + t[2]


def p_if_final_else(t):
    '''
    IF_FINAL    :   ELSE
    '''
    t[0] = [t[1]]


def p_if_final_vacio(t):
    '''
    IF_FINAL    :   
    '''
    t[0] = []


def p_elseif(t):
    '''
    ELSEIF  :   _else _if parentesis_abre EXPRESION parentesis_cierra llave_abre CUERPO_LOCAL llave_cierra
    '''
    t[0] = clases._ElseIf(t[4], t[7])


def p_else(t):
    '''
    ELSE    :   _else llave_abre CUERPO_LOCAL llave_cierra
    '''
    t[0] = clases._Else(t[3])


def p_switch(t):
    '''
    SWITCH  :   _switch parentesis_abre EXPRESION parentesis_cierra llave_abre CASES DEFAULT_CASE llave_cierra
    '''
    t[0] = clases._Switch(t[3], t[6], t[7], str(t.slice[1].lineno))


def p_cases(t):
    '''
    CASES   :   LISTA_CASE
    '''
    t[0] = t[1]


def p_cases_vacio(t):
    '''
    CASES   :
    '''
    t[0] = None


def p_lista_case_lista(t):
    '''
    LISTA_CASE  :   LISTA_CASE CASE
    '''
    t[1].append(t[2])
    t[0] = t[1]


def p_lista_case_case(t):
    '''
    LISTA_CASE  :   CASE
    '''
    t[0] = [t[1]]


def p_case(t):
    '''
    CASE    :   _case EXPRESION dos_puntos CUERPO_LOCAL
    '''
    t[0] = clases._Case(t[2], t[4])


def p_default_case(t):
    '''
    DEFAULT_CASE    :   _default dos_puntos CUERPO_LOCAL
    '''
    t[0] = clases._DefaultCase(t[3])


def p_default_case_vacio(t):
    '''
    DEFAULT_CASE    :
    '''
    t[0] == None


def p_while(t):
    '''
    WHILE   :   _while parentesis_abre EXPRESION parentesis_cierra llave_abre CUERPO_LOCAL llave_cierra
    '''
    t[0] = clases._While(t[3], t[6], str(t.slice[1].lineno))


def p_do(t):
    '''
    DO  :   _do llave_abre CUERPO_LOCAL llave_cierra _while parentesis_abre EXPRESION parentesis_cierra punto_coma
    '''
    t[0] = clases._Do(t[3], t[7], str(t.slice[1].lineno))


def p_for(t):
    '''
    FOR :   _for parentesis_abre INICIO_FOR punto_coma EXPRESION punto_coma ASIGNACION parentesis_cierra llave_abre CUERPO_LOCAL llave_cierra
    '''
    t[0] = clases._For(t[3], t[5], t[7], t[10], str(t.slice[1].lineno))


def p_(t):
    '''
    INICIO_FOR  :   DECLARACION
                |   ASIGNACION
    '''
    t[0] = t[1]


def p_expresion_aritmetica(t):
    '''
    EXPRESION   :   EXPRESION mas EXPRESION 
                |   EXPRESION menos EXPRESION
                |   EXPRESION asterisco EXPRESION
                |   EXPRESION division EXPRESION 
                |   EXPRESION porcentaje EXPRESION 
    '''
    t[0] = clases.ExpresionAritmetica(t[1], t[2], t[3])


def p_expresion_relacional(t):
    '''
    EXPRESION   :   EXPRESION equivale EXPRESION 
                |   EXPRESION distinto EXPRESION
                |   EXPRESION mayor EXPRESION 
                |   EXPRESION menor EXPRESION 
                |   EXPRESION mayor_igual EXPRESION 
                |   EXPRESION menor_igual EXPRESION
    '''
    t[0] = clases.ExpresionRelacional(t[1], t[2], t[3])


def p_expresion_logica(t):
    '''
    EXPRESION   :   EXPRESION and EXPRESION 
                |   EXPRESION or EXPRESION 
    '''
    t[0] = clases.ExpresionLogica(t[1], t[2], t[3])


def p_expresion_bit(t):
    '''
    EXPRESION   :   EXPRESION desplazamiento_izquierdo EXPRESION 
                |   EXPRESION desplazamiento_derecho EXPRESION 
                |   EXPRESION et EXPRESION
                |   EXPRESION pleca EXPRESION
                |   EXPRESION elevado EXPRESION
    '''
    t[0] = clases.ExpresionBit(t[1], t[2], t[3])


def p_expresion_ternaria(t):
    '''
    EXPRESION   :   EXPRESION pregunta EXPRESION dos_puntos EXPRESION %prec NIVEL13
    '''
    t[0] = clases.ExpresionTernaria(t[1], t[3], t[5])


def p_expresion_unaria(t):
    '''
    EXPRESION   :   menos EXPRESION %prec NIVEL2
                |   exclamacion EXPRESION %prec NIVEL2
                |   virgulilla EXPRESION %prec NIVEL2
    '''
    t[0] = clases.ExpresionUnaria(t[1], t[2])


def p_expresion_referencia(t):
    '''
    EXPRESION   :   et identificador %prec NIVEL2
    '''
    t[0] = clases.ExpresionReferencia(t[2])


def p_expresion_metodo(t):
    '''
    EXPRESION   :   METODO
    '''
    t[0] = t[1]


def p_expresion_parentesis(t):
    '''
    EXPRESION   :   parentesis_abre EXPRESION parentesis_cierra
    '''
    t[0] = t[2]


def p_expresion_estructura(t):
    '''
    EXPRESION   :   identificador punto identificador
    '''
    t[0] = clases.ExpresionEstructura(t[1], t[3])


def p_expresion_identificador_arreglo(t):
    '''
    EXPRESION   :   identificador ACCESOS
    '''
    t[0] = clases.ExpresionIdentificadorArreglo(t[1], t[2])


def p_expresion_arreglo_estructura(t):
    '''
    EXPRESION   :   identificador ACCESOS punto identificador
    '''
    t[0] = clases.ExpresionArregloEstructura(t[1], t[2], t[4])


def p_expresion_expresiones(t):
    '''
    EXPRESION   :   llave_abre EXPRESIONES llave_cierra
    '''
    t[0] = clases.ExpresionElementos(t[2])


def p_expresion_sizeof(t):
    '''
    EXPRESION   :   _sizeof parentesis_abre TIPO parentesis_cierra %prec NIVEL2
    '''
    t[0] = clases._SizeOf(t[3])


def p_expresion_scanf(t):
    '''
    EXPRESION   :   _scanf parentesis_abre parentesis_cierra
    '''
    t[0] = clases.ExpresionScan()


def p_expresion_casteo(t):
    '''
    EXPRESION   :   parentesis_abre TIPO parentesis_cierra EXPRESION %prec NIVEL2
    '''
    t[0] = clases.ExpresionCasteo(t[2], t[4])


def p_expresion_caracter(t):
    'EXPRESION  :   caracter'
    t[0] = clases.Caracter(t[1])


def p_expresion_cadena(t):
    'EXPRESION  :   cadena'
    t[0] = clases.Cadena(t[1])


def p_expresion_entero(t):
    'EXPRESION  :   entero'
    t[0] = clases.Entero(t[1])


def p_expresion_decimal(t):
    'EXPRESION  :   decimal'
    t[0] = clases.Decimal(t[1])


def p_expresion_identificador(t):
    'EXPRESION  :   identificador'
    t[0] = clases.Identificador(t[1])


def p_expresiones(t):
    '''
    EXPRESIONES :   LISTA_EXPRESIONES
    '''
    t[0] = t[1]


def p_expresiones_vacio(t):
    '''
    EXPRESIONES :
    '''
    t[0] = None


def p_lista_expresiones_lista(t):
    '''
    LISTA_EXPRESIONES   :   LISTA_EXPRESIONES coma EXPRESION
    '''
    t[1].append(t[3])
    t[0] = t[1]


def p_lista_expresiones_expresion(t):
    '''
    LISTA_EXPRESIONES   :   EXPRESION
    '''
    t[0] = [t[1]]


def p_tipo(t):
    '''
    TIPO    :   _int
            |   _char
            |   _double
            |   _float
            |   _void
    '''
    t[0] = clases.Tipo(t[1], None)


def p_tipo_struct(t):
    '''
    TIPO    :   _struct identificador
    '''
    t[0] = clases.Tipo(t[1], t[2])


def p_error(t):
    if not t:
        return
    mostar_error("ERROR: Sintáctico en: "+str(t.value)+", línea: " +
                 str(t.lineno)+", columna: "+str(obtener_columna(entrada, t))+".")
    errores_sintacticos.append(clases._Error(
        str(t.value), str(t.lineno), str(obtener_columna(entrada, t))))
    while True:
        tok = parser.token()
        if not tok or tok.type == 'punto_coma':
            break
    parser.errok()
    return tok


def obtener_columna(entrada, token):
    linea_inicio = str(entrada).rfind('\n', 0, token.lexpos) + 1
    return ((token.lexpos - linea_inicio) + 1)


def mostar_error(mensaje):
    consola.appendPlainText(mensaje)
    cursor_temporal = consola.textCursor()
    cursor_temporal.setPosition(len(consola.toPlainText()))
    consola.setTextCursor(cursor_temporal)


def parse(_entrada, _errores_lexicos, _errores_sintacticos, _consola):
    global lexer, parser, entrada, errores_lexicos, errores_sintacticos, consola
    entrada = _entrada
    errores_lexicos = _errores_lexicos
    errores_sintacticos = _errores_sintacticos
    consola = _consola
    lexer = lex.lex()
    parser = yacc.yacc()
    return parser.parse(entrada)
