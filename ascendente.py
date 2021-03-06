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

gramatical = ''


def p_init(t):
    '''
    INIT   :   CUERPO_GLOBAL
    '''
    t[0] = t[1]
    global gramatical
    gramaticalTemporal = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Gramatical</title></head><body>'
    gramaticalTemporal += '<center><h1>Gramatical</h1>'
    gramaticalTemporal += '<table border="1"><tr><th>Produccion</th><th>Regla</th></tr>'
    gramatical += '<tr>'
    gramatical += '<td>INIT -> CUERPO_GLOBAL</td>'
    gramatical += '<td>INIT.VAL = CUERPO_GLOBAL.VAL;</td>'
    gramatical += '</tr>'
    gramaticalTemporal += gramatical
    gramaticalTemporal += '</table><center>'
    gramaticalTemporal += '</body></html>'
    f = open("gramatical.html", "w")
    f.write(gramaticalTemporal)
    f.close()


def p_cuerpo_global(t):
    '''
    CUERPO_GLOBAL   :   LISTA_GLOBAL
    '''
    t[0] = t[1]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>CUERPO_GLOBAL -> LISTA_GLOBAL</td>'
    gramatical += '<td>CUERPO_GLOBAL.VAL = LISTA_GLOBAL.VAL;</td>'
    gramatical += '</tr>'


def p_cuerpo_global_vacio(t):
    '''
    CUERPO_GLOBAL   :
    '''
    t[0] = None
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>CUERPO_GLOBAL -> </td>'
    gramatical += '<td>CUERPO_GLOBAL.VAL = NONE;</td>'
    gramatical += '</tr>'


def p_lista_global_lista(t):
    '''
    LISTA_GLOBAL    :   LISTA_GLOBAL INSTRUCCION_GLOBAL
    '''
    t[1].append(t[2])
    t[0] = t[1]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>LISTA_GLOBAL -> LISTA_GLOBAL1 INSTRUCCION_GLOBAL</td>'
    gramatical += '<td>LISTA_GLOBAL1.ADD(INSTRUCCION_GLOBAL); LISTA_GLOBAL.VAL = LISTA_GLOBAL1.VAL;</td>'
    gramatical += '</tr>'


def p_lista_global_instruccion(t):
    '''
    LISTA_GLOBAL    :   INSTRUCCION_GLOBAL
    '''
    t[0] = [t[1]]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>LISTA_GLOBAL -> INSTRUCCION_GLOBAL</td>'
    gramatical += '<td>LISTA_GLOBAL.VAL = Lista(INSTRUCCION_GLOBAL.VAL);</td>'
    gramatical += '</tr>'


def p_instruccion_global(t):
    '''
    INSTRUCCION_GLOBAL  :   DECLARACION punto_coma
                        |   ESTRUCTURA punto_coma
                        |   FUNCION
    '''
    t[0] = t[1]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>INSTRUCCION_GLOBAL -> DECLARACION; | ESTRUCTURA ; | FUNCION</td>'
    gramatical += '<td>INSTRUCCION_GLOBAL.VAL = DECLARACION.VAL | ESTRUCTURA.VAL | FUNCION.VAL;</td>'
    gramatical += '</tr>'


def p_estructura(t):
    '''
    ESTRUCTURA  :   _struct identificador llave_abre CARACTERISTICAS llave_cierra
    '''
    t[0] = clases.Estructura(t[2], t[4], str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>ESTRUCTURA -> struct identificador { CARACTERISTICAS }</td>'
    gramatical += '<td>ESTRUCTURA.VAL = Estructura(identificador, CARACTERISTICAS.VAL, lineno);</td>'
    gramatical += '</tr>'


def p_caracteristicas(t):
    '''
    CARACTERISTICAS :   LISTA_CARACTERISTICAS
    '''
    t[0] = t[1]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>CARACTERISTICAS -> LISTA_CARACTERISTICAS</td>'
    gramatical += '<td>CARACTERTISCIAS.VAL = LISTA_CARACTERISTICAS.VAL;</td>'
    gramatical += '</tr>'


def p_caracteristicas_vacio(t):
    '''
    CARACTERISTICAS :
    '''
    t[0] = None
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>CARACTERISTICAS -> </td>'
    gramatical += '<td>CARACTERTISICAS.VAL = NONE;</td>'
    gramatical += '</tr>'


def p_lista_caracteristicas_lista(t):
    '''
    LISTA_CARACTERISTICAS   :   LISTA_CARACTERISTICAS CARACTERISTICA
    '''
    t[1].append(t[2])
    t[0] = t[1]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>LISTA_CARACTERISTICAS -> LISTA_CARACTERISTICAS CARACTERISTICA</td>'
    gramatical += '<td>LISTA_CARACTERISTICAS1.APPEND(CARACTERISTICA.VAL); LISTA_CARACTERISTICAS.VAL = LISTA_CARACTERISTICAS1.VAL;</td>'
    gramatical += '</tr>'


def p_lista_caracteristicas_caracteristica(t):
    '''
    LISTA_CARACTERISTICAS : CARACTERISTICA
    '''
    t[0] = [t[1]]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>LISTA_CARACTERITISCAS -> CARACTERISTICA</td>'
    gramatical += '<td>LISTA_CARACTERISTICAS.VAL = Lista(CARACTERISTICA.VAL);</td>'
    gramatical += '</tr>'


def p_caracteristica(t):
    '''
    CARACTERISTICA  :   DECLARACION punto_coma
    '''
    t[0] = t[1]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>CARACTERISTICA -> DECLARACION;</td>'
    gramatical += '<td>CARACTERISTICA.VAL = DECLARACION.VAL;</td>'
    gramatical += '</tr>'


def p_funcion(t):
    '''
    FUNCION    :   TIPO identificador parentesis_abre PARAMETROS parentesis_cierra llave_abre CUERPO_LOCAL llave_cierra
    '''
    t[0] = clases.Funcion(t[1], t[2], t[4], t[7])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>FUNCION -> TIPO identificador ( PARAMETROS ) { CUERPO_LOCAL }</td>'
    gramatical += '<td>FUNCION.VAL = Funcion(TIPO.VAL, identificador, PARAMETROS.VAL, CUERPO.VAL);</td>'
    gramatical += '</tr>'


def p_parametros(t):
    '''
    PARAMETROS  :   LISTA_PARAMETROS
    '''
    t[0] = t[1]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>PARAMETROS -> LISTA_PARAMETROS</td>'
    gramatical += '<td>PARAMETROS.VAL = LISTA_PARAMETROS.VAL</td>'
    gramatical += '</tr>'


def p_parametros_vacio(t):
    '''
    PARAMETROS  :
    '''
    t[0] = None
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>PARAMETROS -> </td>'
    gramatical += '<td>PARAMETROS.VAL = NONE;</td>'
    gramatical += '</tr>'


def p_lista_parametros_lista(t):
    '''
    LISTA_PARAMETROS    :   LISTA_PARAMETROS coma PARAMETRO
    '''
    t[1].append(t[3])
    t[0] = t[1]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>LISTA_PARAMETROS -> LISTA_PARAMETROS1 , PARAMETRO</td>'
    gramatical += '<td>LISTA_PARAMETROS1.ADD(PARAMETRO.VAL); LISTA_PARAMETROS.VAL = LISTA_PARAMETROS1.VAL;</td>'
    gramatical += '</tr>'


def p_lista_parametros_parametro(t):
    '''
    LISTA_PARAMETROS    :   PARAMETRO
    '''
    t[0] = [t[1]]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>LISTA_PARAMETROS -> PARAMETRO</td>'
    gramatical += '<td>LISTA_PARAMETROS.VAL = Lista(PARAMETRO.VAL);</td>'
    gramatical += '</tr>'


def p_parametro(t):
    '''
    PARAMETRO   :   TIPO identificador
    '''
    t[0] = clases.Parametro(t[1], False, t[2])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>PARAMETRO -> TIPO identificador</td>'
    gramatical += '<td>PARAMETRO.VAL = Parametro(TIPO.VAL, false, identificador);</td>'
    gramatical += '</tr>'


def p_parametro_apuntador(t):
    '''
    PARAMETRO   :   TIPO et identificador
    '''
    t[0] = clases.Parametro(t[1], True, t[3])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>PARAMETRO -> TIPO & identificador</td>'
    gramatical += '<td>PARAMETRO.VAL = Parametro(TIPO.VAL, true, identificador);</td>'
    gramatical += '</tr>'


def p_cuerpo_local(t):
    '''
    CUERPO_LOCAL    :   LISTA_LOCAL
    '''
    t[0] = t[1]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>CUERPO_LOCAL -> LISTA_LOCAL</td>'
    gramatical += '<td>CUERPO_LOCAL.VAL = LISTA_LOCAL.VAL;</td>'
    gramatical += '</tr>'


def p_cuerpo_local_vacio(t):
    '''
    CUERPO_LOCAL    :
    '''
    t[0] = None
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>CUERPO_LOCAL -> </td>'
    gramatical += '<td>CUERPO_LOCAL.VAL = NONE;</td>'
    gramatical += '</tr>'


def p_lista_local(t):
    '''
    LISTA_LOCAL :   LISTA_LOCAL INSTRUCCION_LOCAL
    '''
    t[1].append(t[2])
    t[0] = t[1]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>LISTA_LOCAL -> LISTA_LOCAL1 INSTRUCCION_LOCAL</td>'
    gramatical += '<td>LISTA_LOCAL1.ADD(INSTRUCCION_LOCAL.VAL); LISTA_LOCAL.VAL = LISTA_LOCAL1.VAL;</td>'
    gramatical += '</tr>'


def p_lista_local_instruccion(t):
    '''
    LISTA_LOCAL :   INSTRUCCION_LOCAL
    '''
    t[0] = [t[1]]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>LISTA_LOCAL -> INSTRUCCION_LOCAL</td>'
    gramatical += '<td>LISTA_LOCAL.VAL = Lista(INSTRUCCION_LOCAL.VAL);</td>'
    gramatical += '</tr>'


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
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>INSTRUCCION_LOCAL -> ETIQUETA | SALTO | DECLARACION ; | ASIGNACION ; | IF | SWITCH | WHILE | DO | FOR | PRINT ; | METODO ;</td>'
    gramatical += '<td>INSTRUCCION_LOCAL.VAL = ETIQUETA.VAL | SALTO.VAL | DECLARACION.VAL | ASIGNACION.VAL | IF.VAL | SWITCH.VAL | WHILE.VAL | DO.VAL | FOR.VAL | PRINT.VAL | METODO.VAL;</td>'
    gramatical += '</tr>'


def p_instruccion_local_print(t):
    '''
    PRINT   :   _printf parentesis_abre LISTA_EXPRESIONES parentesis_cierra
    '''
    t[0] = clases._PrintF(t[3], str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>PRINT -> printf ( LISTA_EXPRESIONES )</td>'
    gramatical += '<td>PRINT.VAL = PrintF(LISTA_EXPRESIONES.VAL, lineno);</td>'
    gramatical += '</tr>'


def p_instruccion_local_continue(t):
    '''
    INSTRUCCION_LOCAL   :   _continue punto_coma
    '''
    t[0] = clases._Continue(str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>INSTRUCCION_LOCAL -> continue;</td>'
    gramatical += '<td>INSTRUCCION_LOCAL.VAL = Continue(lineno);</td>'
    gramatical += '</tr>'


def p_instruccion_local_break(t):
    '''
    INSTRUCCION_LOCAL   :   _break punto_coma
    '''
    t[0] = clases._Break(str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>INSTRUCCION_LOCAL -> break;</td>'
    gramatical += '<td>INSTRUCCION_LOCAL.VAL = Break(lineno);</td>'
    gramatical += '</tr>'


def p_instruccion_local_return(t):
    '''
    INSTRUCCION_LOCAL   :   _return EXPRESION punto_coma
    '''
    t[0] = clases._Return(t[2], str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>INSTRUCCION_LOCAL -> return EXPRESION;</td>'
    gramatical += '<td>INSTRUCCION_LOCAL.VAL = Return(EXPRESION.val, lineno);</td>'
    gramatical += '</tr>'


def p_instruccion_local_return_vacio(t):
    '''
    INSTRUCCION_LOCAL   :   _return punto_coma
    '''
    t[0] = clases._Return(None, str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>INSTRUCCION_LOCAL -> return;</td>'
    gramatical += '<td>INSTRUCCION_LOCAL.VAL = Return(NONE, lineno);</td>'
    gramatical += '</tr>'


def p_metodo(t):
    '''
    METODO  :   identificador parentesis_abre EXPRESIONES parentesis_cierra 
    '''
    t[0] = clases.Metodo(t[1], t[3], str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>METODO -> identificador ( EXPRESIONES )</td>'
    gramatical += '<td>METODO.VAL = Metodo(identidicador, EXPRESIONES.VAL, lineno);</td>'
    gramatical += '</tr>'


def p_etiqueta(t):
    '''
    ETIQUETA    :   identificador dos_puntos
    '''
    t[0] = clases.Etiqueta(t[1], str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>ETIQUETA -> identificador:</td>'
    gramatical += '<td>EITQUETA.VAL = Etiqueta(identificador, lineno);</td>'
    gramatical += '</tr>'


def p_salto(t):
    '''
    SALTO   :   _goto identificador punto_coma
    '''
    t[0] = clases.Salto(t[2], str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>SALTO -> goto identificador;</td>'
    gramatical += '<td>SALTO.VAL = Salto(identificador, lineno);</td>'
    gramatical += '</tr>'


def p_declaracion(t):
    '''
    DECLARACION :   TIPO LISTA_DECLARACION
    '''
    t[0] = clases.Declaracion(t[1], t[2])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>DECLARACION -> TIPO LISTA_DECLARACION</td>'
    gramatical += '<td>DECLARACION.VAL = Declaracion(TIPO.VAL, LISTA_DECLARACION.VAL);</td>'
    gramatical += '</tr>'


def p_lista_declaracion_lista(t):
    '''
    LISTA_DECLARACION   :   LISTA_DECLARACION coma DECLARACION_FINAL
    '''
    t[1].append(t[3])
    t[0] = t[1]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>LISTA_DECLARACION -> LISTA_DECLARACION1 , DECLARACION_FINAL</td>'
    gramatical += '<td>LISTA_DECLARACION1.ADD(DECLARACION_FINAL.VAL); LISTA_DECLARACION.VAL = LISTA_DECLARACION1.VAL;</td>'
    gramatical += '</tr>'


def p_lista_declaracion_declaracion(t):
    '''
    LISTA_DECLARACION   :   DECLARACION_FINAL
    '''
    t[0] = [t[1]]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>LISTA_DECLARACION -> DECLARACION_FINAL</td>'
    gramatical += '<td>LISTA_DEDCLARACION.VAL = Lista(DECLARACION_FINAL.VAL);</td>'
    gramatical += '</tr>'


def p_declaracion_final(t):
    '''
    DECLARACION_FINAL   :   identificador INDICES
    '''
    t[0] = clases.DeclaracionFinal(t[1], t[2], None, str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>DECLARACION_FINAL -> identificador INDICES</td>'
    gramatical += '<td>DECLARACION_FINAL.VAL = DeclaracionFinal(identificador, INDICES.VAL, NONE, lineno);</td>'
    gramatical += '</tr>'


def p_declaracion_final_expresion(t):
    '''
    DECLARACION_FINAL   :   identificador INDICES igual EXPRESION
    '''
    t[0] = clases.DeclaracionFinal(t[1], t[2], t[4], str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>DECLARACION_FINAL -> identificador INDICES = EXPRESION</td>'
    gramatical += '<td>DECLARACION_FINAL.VAL = DeclaracionFinal(identificador, INDICES.VAL, EXPRESIONES.VAL, lineno);</td>'
    gramatical += '</tr>'


def p_indices(t):
    '''
    INDICES :   ACCESOS
    '''
    t[0] = t[1]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>INDICES -> ACCESOS</td>'
    gramatical += '<td>INDICES.VAL = ACCESOS.VAL</td>'
    gramatical += '</tr>'


def p_indices_vacio(t):
    '''
    INDICES :
    '''
    t[0] = None
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>INDICES -> </td>'
    gramatical += '<td>INDICES.VAL = NONE;</td>'
    gramatical += '</tr>'


def p_accesos_lista(t):
    '''
    ACCESOS :   ACCESOS ACCESO
    '''
    t[1].append(t[2])
    t[0] = t[1]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>ACCESOS -> ACCESOS1 ACCESO</td>'
    gramatical += '<td>ACCESOS1.ADD(ACCESO.VAL); ACCESOS.VAL = ACCESOS1.VAL;</td>'
    gramatical += '</tr>'


def p_accesos_acceso(t):
    '''
    ACCESOS :   ACCESO
    '''
    t[0] = [t[1]]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>ACCESOS -> ACCESO</td>'
    gramatical += '<td>ACCESOS.VAL = Lista(ACCESO.VAL);</td>'
    gramatical += '</tr>'


def p_acceso(t):
    '''
    ACCESO  :   corchete_abre EXPRESION corchete_cierra 
    '''
    t[0] = t[2]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>ACCESO -> [ EXPRESION ] </td>'
    gramatical += '<td>ACCESO.VAL = EXPRESION.VAL;</td>'
    gramatical += '</tr>'


def p_acceso_vacio(t):
    '''
    ACCESO : corchete_abre corchete_cierra
    '''
    t[0] = []
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>ACCESO -> [ ]</td>'
    gramatical += '<td>ACCESO.VAL = Lista();</td>'
    gramatical += '</tr>'


def p_asignacion_normal(t):
    '''
    ASIGNACION  :   identificador INDICES COMPUESTO EXPRESION 
    '''
    t[0] = clases.AsignacionNormal(
        t[1], t[2], t[3], t[4], str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>ASIGNACION -> identificador INDICES COMPUESTO EXPRESION</td>'
    gramatical += '<td>ASIGNACION.VAL = AsignacionNormal(identificador, INDICES.VAL, COMPUESTO.VAL, EXPRESION.VAL, lineno);</td>'
    gramatical += '</tr>'


def p_asignacion_estructura(t):
    '''
    ASIGNACION  :   identificador INDICES punto identificador INDICES COMPUESTO EXPRESION 
    '''
    t[0] = clases.AsignacionEstructura(
        t[1], t[2], t[4], t[5], t[6], t[7], str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>ASIGNACION -> identificador INDICES . identificador INDICES COMPUESTO EXPRESION</td>'
    gramatical += '<td>ASIGNACION.VAL = AsignacionEstructura(identificador, INDICES.VAL, identificador, INDICES.val, COMPUESTO.VAL, EXPRESION.VAL, lineno);</td>'
    gramatical += '</tr>'


def p_asignacion_aumento_post(t):
    '''
    ASIGNACION  :   identificador aumento %prec NIVEL2
    '''
    t[0] = clases.AsignacionAumento(t[1], str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>ASIGNACION -> identificador ++</td>'
    gramatical += '<td>ASIGNACION.VAL = AsignacionAumento(identificador, lineno);</td>'
    gramatical += '</tr>'


def p_asignacion_aumento_pre(t):
    '''
    ASIGNACION  :   aumento identificador %prec NIVEL2
    '''
    t[0] = clases.AsignacionAumento(t[2], str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>ASIGNACION -> ++ identificador</td>'
    gramatical += '<td>ASIGNACION.VAL = AsignacionAumento(identificador, lineno);</td>'
    gramatical += '</tr>'


def p_asignacion_decremento_post(t):
    '''
    ASIGNACION  :   identificador decremento %prec NIVEL2
    '''
    t[0] = clases.AsignacionDecremento(t[1], str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>ASIGNACION -> identificador --</td>'
    gramatical += '<td>ASIGNACION.VAL = AsignacionDecremento(identificador, lineno);</td>'
    gramatical += '</tr>'


def p_asignacion_decremento_pre(t):
    '''
    ASIGNACION  :   decremento identificador %prec NIVEL2
    '''
    t[0] = clases.AsignacionDecremento(t[2], str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>ASIGNACION -> -- identificador</td>'
    gramatical += '<td>ASIGNACION.VAL = AsignacionDecremento(identificador, lineno);</td>'
    gramatical += '</tr>'


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
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>COMPUESTO -> = | += | -= | *= | /= | %= | <<= | >>= | & | |= | ^= </td>'
    gramatical += '<td>COMPUESTO.VAL = = | += | -= | *= | /= | %= | <<= | >>= | & | |= | ^=;</td>'
    gramatical += '</tr>'


def p_if(t):
    '''
    IF  :   _if parentesis_abre EXPRESION parentesis_cierra llave_abre CUERPO_LOCAL llave_cierra
    '''
    t[0] = clases._If(t[3], t[6], None, None, str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>IF -> if ( EXPRESION ) { CUERPO_LOCAL }</td>'
    gramatical += '<td>IF.VAL = If(EXPRESION.VAL, CUERPO_LOCAL.VAL, NONE, NONE, lineno);</td>'
    gramatical += '</tr>'


def p_if_else(t):
    '''
    IF  :   _if parentesis_abre EXPRESION parentesis_cierra llave_abre CUERPO_LOCAL llave_cierra ELSE
    '''
    t[0] = clases._If(t[3], t[6], None, t[8], str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>IF -> if ( EXPRESION ) { CUERPO_LOCAL } ELSE</td>'
    gramatical += '<td>IF.VAL = If(EXPRESION.VAL, CUERPO_LOCAL.VAL, NONE, ELSE.VAL, lineno);</td>'
    gramatical += '</tr>'


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
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>IF -> if ( EXPRESION ) { CUERPO_LOCAL } ELSEIF IF_FINAL</td>'
    gramatical += '<td>IF.VAL = If(EXPRESION.VAL, CUERPO_LOCAL.VAL, ELSEIF.VAL, IF_FINAL.VAL, lineno);</td>'
    gramatical += '</tr>'


def p_if_final_elseif(t):
    '''
    IF_FINAL    :   ELSEIF  IF_FINAL
    '''
    t[0] = [t[1]] + t[2]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>IF_FINAL -> ELSEIF IF_FINAL</td>'
    gramatical += '<td>IF_FINAL.VAL = Lista(ELSEIF) + IF_FINAL.VAL;</td>'
    gramatical += '</tr>'


def p_if_final_else(t):
    '''
    IF_FINAL    :   ELSE
    '''
    t[0] = [t[1]]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>IF_FINAL -> ELSE</td>'
    gramatical += '<td>IF_FINAL.VAL = Lista(ELSE.VAL);</td>'
    gramatical += '</tr>'


def p_if_final_vacio(t):
    '''
    IF_FINAL    :   
    '''
    t[0] = []
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>IF_FINAL -> </td>'
    gramatical += '<td>IF_FINAL.VAL = NONE;</td>'
    gramatical += '</tr>'


def p_elseif(t):
    '''
    ELSEIF  :   _else _if parentesis_abre EXPRESION parentesis_cierra llave_abre CUERPO_LOCAL llave_cierra
    '''
    t[0] = clases._ElseIf(t[4], t[7])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>ELSEIF -> else if ( EXPRESION ) { CUERPO_LOCAL }</td>'
    gramatical += '<td>ELSEIF.VAL -> ElseIf(EXPRESION.VAL, CUERPO_LOCAL.VAL);</td>'
    gramatical += '</tr>'


def p_else(t):
    '''
    ELSE    :   _else llave_abre CUERPO_LOCAL llave_cierra
    '''
    t[0] = clases._Else(t[3])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>ELSE -> else { CUERPO_LOCAL }</td>'
    gramatical += '<td>ELSE.VAL = Else(CUERPO_LOCAL.VAL);</td>'
    gramatical += '</tr>'


def p_switch(t):
    '''
    SWITCH  :   _switch parentesis_abre EXPRESION parentesis_cierra llave_abre CASES DEFAULT_CASE llave_cierra
    '''
    t[0] = clases._Switch(t[3], t[6], t[7], str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>SWITCH -> switch ( EXPRESION ) { CASES DEFAULT_CASE } </td>'
    gramatical += '<td>SWITCH.VAL = Switch(EXPRESION.VAL, CASES.VAL, DEFAULT_CASE.VAL, lineno);</td>'
    gramatical += '</tr>'


def p_cases(t):
    '''
    CASES   :   LISTA_CASE
    '''
    t[0] = t[1]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>CASES -> LISTA_CASE</td>'
    gramatical += '<td>CASES.VAL = LISTA_CASE.VAL</td>'
    gramatical += '</tr>'


def p_cases_vacio(t):
    '''
    CASES   :
    '''
    t[0] = None
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>CASES -> </td>'
    gramatical += '<td>CASES.VAL = NONE;</td>'
    gramatical += '</tr>'


def p_lista_case_lista(t):
    '''
    LISTA_CASE  :   LISTA_CASE CASE
    '''
    t[1].append(t[2])
    t[0] = t[1]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>LISTA_CASE = LISTA_CASE1 CASE</td>'
    gramatical += '<td>LISTA_CASE1.ADD(CASE.VAL); LISTA_CASE.VAL = LISTA_CASE1.VAL;</td>'
    gramatical += '</tr>'


def p_lista_case_case(t):
    '''
    LISTA_CASE  :   CASE
    '''
    t[0] = [t[1]]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>LISTA_CASE -> CASE</td>'
    gramatical += '<td>LISTA_CASE.VAL = Lista(CASE.VAL);</td>'
    gramatical += '</tr>'


def p_case(t):
    '''
    CASE    :   _case EXPRESION dos_puntos CUERPO_LOCAL
    '''
    t[0] = clases._Case(t[2], t[4])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>CASE -> case EXPRESION : CUERPO_LOCAL</td>'
    gramatical += '<td>CASE.VAL = Case(EXPRESION.VAL, CUERPO_LOCAL.VAL);</td>'
    gramatical += '</tr>'


def p_default_case(t):
    '''
    DEFAULT_CASE    :   _default dos_puntos CUERPO_LOCAL
    '''
    t[0] = clases._DefaultCase(t[3])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>DEFAULT_CASE -> default : CUERPO_LOCAL</td>'
    gramatical += '<td>DEFAULT_CASE.VAL = DefaultCase(CUERPO_LOCAL.VAL);</td>'
    gramatical += '</tr>'


def p_default_case_vacio(t):
    '''
    DEFAULT_CASE    :
    '''
    t[0] == None
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>DEFAULT_CASE -> </td>'
    gramatical += '<td>DEFAULT_CASE.VAL = NONE;</td>'
    gramatical += '</tr>'


def p_while(t):
    '''
    WHILE   :   _while parentesis_abre EXPRESION parentesis_cierra llave_abre CUERPO_LOCAL llave_cierra
    '''
    t[0] = clases._While(t[3], t[6], str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>WHILE -> while ( EXPRESION ) { CUERPO_LOCAL }</td>'
    gramatical += '<td>WHILE.VAL = While(EXPRESION.VAL, CUERPO_LOCAL.val, lineno);</td>'
    gramatical += '</tr>'


def p_do(t):
    '''
    DO  :   _do llave_abre CUERPO_LOCAL llave_cierra _while parentesis_abre EXPRESION parentesis_cierra punto_coma
    '''
    t[0] = clases._Do(t[3], t[7], str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>DO -> do { CUERPO_LOCAL } while ( EXPRESION ) ; </td>'
    gramatical += '<td>DO.VAL = Do(CUERPO_LOCAL.VAL, EXPRESION.VAL, lineno);</td>'
    gramatical += '</tr>'


def p_for(t):
    '''
    FOR :   _for parentesis_abre INICIO_FOR punto_coma EXPRESION punto_coma ASIGNACION parentesis_cierra llave_abre CUERPO_LOCAL llave_cierra
    '''
    t[0] = clases._For(t[3], t[5], t[7], t[10], str(t.slice[1].lineno))
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>FOR -> for ( INICIO_FOR ; EXPRESION ; ASIGNACION ) { CUERPO_LOCAL }</td>'
    gramatical += '<td>FOR.VAL = For(INICIO_FOR.VAL, EXPRESION.VAL; ASIGNACION.VAL, CUERPO_LOCAL.VAL, lineno);</td>'
    gramatical += '</tr>'


def p_(t):
    '''
    INICIO_FOR  :   DECLARACION
                |   ASIGNACION
    '''
    t[0] = t[1]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>INICIO_FOR -> DECLARACION | ASIGNACION</td>'
    gramatical += '<td>INICIO_FOR.VAL = DECLARACION.VAL | ASIGNACION.VAL;</td>'
    gramatical += '</tr>'


def p_expresion_aritmetica(t):
    '''
    EXPRESION   :   EXPRESION mas EXPRESION 
                |   EXPRESION menos EXPRESION
                |   EXPRESION asterisco EXPRESION
                |   EXPRESION division EXPRESION 
                |   EXPRESION porcentaje EXPRESION 
    '''
    t[0] = clases.ExpresionAritmetica(t[1], t[2], t[3])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> EXPRESION1 [+|-|*|/|%] EXPRESION2</td>'
    gramatical += '<td>EXPRESION.VAL -> ExpresionAritmetica(EXPRESION1.VAL, [+|-|*|/|%], EXPRESION2.VAL);</td>'
    gramatical += '</tr>'


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
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> EXPRESION1 [==|!=|>|<|>=|<=] EXPRESION2</td>'
    gramatical += '<td>EXPRESION.VAL = ExpresionRelacional(EXPRESION1.VAL, [==|!=|>|<|>=|<=], EXPRESION2.VAL);</td>'
    gramatical += '</tr>'


def p_expresion_logica(t):
    '''
    EXPRESION   :   EXPRESION and EXPRESION 
                |   EXPRESION or EXPRESION 
    '''
    t[0] = clases.ExpresionLogica(t[1], t[2], t[3])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> EXPRESION1 [and|or] EXPRESION2</td>'
    gramatical += '<td>EXPRESION.VAL = ExpresionLogica(EXPRESION1.VAL, [and|or], EXPRESION2.VAL);</td>'
    gramatical += '</tr>'


def p_expresion_bit(t):
    '''
    EXPRESION   :   EXPRESION desplazamiento_izquierdo EXPRESION 
                |   EXPRESION desplazamiento_derecho EXPRESION 
                |   EXPRESION et EXPRESION
                |   EXPRESION pleca EXPRESION
                |   EXPRESION elevado EXPRESION
    '''
    t[0] = clases.ExpresionBit(t[1], t[2], t[3])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> EXPRESION1 [<<|>>|&|"|"|^] EXPRESION2</td>'
    gramatical += '<td>EXPRESION.VAL = ExpresionBit(EXPRESION1, [<<|>>|&|"|"|^], EXPRESION2);</td>'
    gramatical += '</tr>'


def p_expresion_ternaria(t):
    '''
    EXPRESION   :   EXPRESION pregunta EXPRESION dos_puntos EXPRESION %prec NIVEL13
    '''
    t[0] = clases.ExpresionTernaria(t[1], t[3], t[5])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> EXPRESION1 ? EXPRESION2 : EXPRESION3</td>'
    gramatical += '<td>EXPRESION.VAL = ExpresionTernaria(EXPRESION1, EXPRESION2, EXPRESION3);</td>'
    gramatical += '</tr>'


def p_expresion_unaria(t):
    '''
    EXPRESION   :   menos EXPRESION %prec NIVEL2
                |   exclamacion EXPRESION %prec NIVEL2
                |   virgulilla EXPRESION %prec NIVEL2
    '''
    t[0] = clases.ExpresionUnaria(t[1], t[2])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> [-|!|~] EXPRESION1</td>'
    gramatical += '<td>EXPRESION.VAL = ExpresionUnaria([-|!|~], EXPRESION1);</td>'
    gramatical += '</tr>'


def p_expresion_referencia(t):
    '''
    EXPRESION   :   et identificador %prec NIVEL2
    '''
    t[0] = clases.ExpresionReferencia(t[2])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> & identificador</td>'
    gramatical += '<td>EXPRESION.VAL = ExpresionReferencia(identificador);</td>'
    gramatical += '</tr>'


def p_expresion_metodo(t):
    '''
    EXPRESION   :   METODO
    '''
    t[0] = t[1]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> METODO</td>'
    gramatical += '<td>EXPRESION.VAL = METODO.VAL;</td>'
    gramatical += '</tr>'


def p_expresion_parentesis(t):
    '''
    EXPRESION   :   parentesis_abre EXPRESION parentesis_cierra
    '''
    t[0] = t[2]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> ( EXPRESION1 )</td>'
    gramatical += '<td>EXPRESION.VAL = EXPRESION1.VAL;</td>'
    gramatical += '</tr>'


def p_expresion_estructura(t):
    '''
    EXPRESION   :   identificador INDICES punto identificador INDICES
    '''
    t[0] = clases.ExpresionEstructura(t[1], t[2], t[4], t[5])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> identificador INDICES . identificador INDICES</td>'
    gramatical += '<td>EXPRESION.VAL = ExpresionEstructura(identificador, INDICES.VAL, identificador, INDICES.VAL);</td>'
    gramatical += '</tr>'


def p_expresion_identificador_arreglo(t):
    '''
    EXPRESION   :   identificador ACCESOS
    '''
    t[0] = clases.ExpresionIdentificadorArreglo(t[1], t[2])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> identificador ACCESOS</td>'
    gramatical += '<td>EXPRESION.VAL = ExpresionIdentificadorArreglo(identificador, ACCESOS);</td>'
    gramatical += '</tr>'


def p_expresion_expresiones(t):
    '''
    EXPRESION   :   llave_abre EXPRESIONES llave_cierra
    '''
    t[0] = clases.ExpresionElementos(t[2])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> { EXPRESIONES }</td>'
    gramatical += '<td>EXPRESION.VAL = ExpresionElementos(EXPRESIONES.VAL);</td>'
    gramatical += '</tr>'


def p_expresion_sizeof(t):
    '''
    EXPRESION   :   _sizeof parentesis_abre TIPO parentesis_cierra %prec NIVEL2
    '''
    t[0] = clases._SizeOf(t[3])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> sizeof ( TIPO ) </td>'
    gramatical += '<td>EXPRESION.VAL = SizeOf(TIPO.VAL);</td>'
    gramatical += '</tr>'


def p_expresion_aumento_post(t):
    '''
    EXPRESION   :   identificador aumento %prec NIVEL2
    '''
    t[0] = clases.ExpresionAumentoDecremento(t[1], t[2], 'post')
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> identificador ++</td>'
    gramatical += '<td>EXPRESION.VAL = ExpresionAumentoDecremento(identificador, ++, post);</td>'
    gramatical += '</tr>'


def p_expresion_aumento_pre(t):
    '''
    EXPRESION   :   aumento identificador %prec NIVEL2
    '''
    t[0] = clases.ExpresionAumentoDecremento(t[2], t[1], 'pre')
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> ++ identificador</td>'
    gramatical += '<td>EXPRESION.VAL = ExpresionAumentoDecremento(identificador, ++, pre);</td>'
    gramatical += '</tr>'


def p_expresion_decremento_post(t):
    '''
    EXPRESION   :   identificador decremento %prec NIVEL2
    '''
    t[0] = clases.ExpresionAumentoDecremento(t[1], t[2], 'post')
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> identificador --</td>'
    gramatical += '<td>EXPRESION.VAL = ExpresionAumentoDecremento(identificador, --, post);</td>'
    gramatical += '</tr>'


def p_expresion_decremento_pre(t):
    '''
    EXPRESION   :   decremento identificador %prec NIVEL2
    '''
    t[0] = clases.ExpresionAumentoDecremento(t[2], t[1], 'pre')
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> -- identificador</td>'
    gramatical += '<td>EXPRESION.VAL = ExpresionAumentoDecremento(identificador, --, pre);</td>'
    gramatical += '</tr>'


def p_expresion_scanf(t):
    '''
    EXPRESION   :   _scanf parentesis_abre parentesis_cierra
    '''
    t[0] = clases.ExpresionScan()
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> scanf ( )</td>'
    gramatical += '<td>EXPRESION.VAL = ExpresionScan();</td>'
    gramatical += '</tr>'


def p_expresion_casteo(t):
    '''
    EXPRESION   :   parentesis_abre TIPO parentesis_cierra EXPRESION %prec NIVEL2
    '''
    t[0] = clases.ExpresionCasteo(t[2], t[4])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> ( TIPO ) EXPRESION</td>'
    gramatical += '<td>EXPRESION.VAL = ExpresionCasteo(TIPO.VAL, EXPRESION.VAL);</td>'
    gramatical += '</tr>'


def p_expresion_caracter(t):
    'EXPRESION  :   caracter'
    t[0] = clases.Caracter(t[1])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> caracter</td>'
    gramatical += '<td>EXPRESION.VAL = caracter;</td>'
    gramatical += '</tr>'


def p_expresion_cadena(t):
    'EXPRESION  :   cadena'
    t[0] = clases.Cadena(t[1])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> cadena</td>'
    gramatical += '<td>EXPRESION.VAL = cadena;</td>'
    gramatical += '</tr>'


def p_expresion_entero(t):
    'EXPRESION  :   entero'
    t[0] = clases.Entero(t[1])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> entero</td>'
    gramatical += '<td>EXPRESION.VAL = entero;</td>'
    gramatical += '</tr>'


def p_expresion_decimal(t):
    'EXPRESION  :   decimal'
    t[0] = clases.Decimal(t[1])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> decimal</td>'
    gramatical += '<td>EXPRESION.VAL = decimal;</td>'
    gramatical += '</tr>'


def p_expresion_identificador(t):
    'EXPRESION  :   identificador'
    t[0] = clases.Identificador(t[1])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESION -> identificador</td>'
    gramatical += '<td>EXPRESION.VAL = identificador;</td>'
    gramatical += '</tr>'


def p_expresiones(t):
    '''
    EXPRESIONES :   LISTA_EXPRESIONES
    '''
    t[0] = t[1]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESIONES -> LISTA_EXPRESIONES</td>'
    gramatical += '<td>EXPRESIONES.VAL = LISTA_EXPRESIONES.VAL</td>'
    gramatical += '</tr>'


def p_expresiones_vacio(t):
    '''
    EXPRESIONES :
    '''
    t[0] = None
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>EXPRESIONES -> </td>'
    gramatical += '<td>EXPRESIONES.VAL = NONE;</td>'
    gramatical += '</tr>'


def p_lista_expresiones_lista(t):
    '''
    LISTA_EXPRESIONES   :   LISTA_EXPRESIONES coma EXPRESION
    '''
    t[1].append(t[3])
    t[0] = t[1]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>LISTA_EXPRESIONES -> LISTA_EXPRESIONES1 , EXPRESION</td>'
    gramatical += '<td>LISTA_EXPRESIONES1.ADD(EXPRESION.VAL); LISTA_EXPRESIONES.VAL = LISTA_EXPRESIONES1.VAL;</td>'
    gramatical += '</tr>'


def p_lista_expresiones_expresion(t):
    '''
    LISTA_EXPRESIONES   :   EXPRESION
    '''
    t[0] = [t[1]]
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>LISTA_EXPRESIONES -> EXPRESION</td>'
    gramatical += '<td>LISTA_EXPRESIONES.VAL = Lista(EXPRESION.VAL);</td>'
    gramatical += '</tr>'


def p_tipo(t):
    '''
    TIPO    :   _int
            |   _char
            |   _double
            |   _float
            |   _void
    '''
    t[0] = clases.Tipo(t[1], None)
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>TIPO -> int | char | double | float | void</td>'
    gramatical += '<td>TIPO.VAL = Tipo([int|char|double|float|void], None);</td>'
    gramatical += '</tr>'


def p_tipo_struct(t):
    '''
    TIPO    :   _struct identificador
    '''
    t[0] = clases.Tipo(t[1], t[2])
    global gramatical
    gramatical += '<tr>'
    gramatical += '<td>TIPO -> struct identificador</td>'
    gramatical += '<td>TIPO.VAL = Tipo(struct, identificador);</td>'
    gramatical += '</tr>'


def p_error(t):
    if not t:
        return
    mostar_error('ERROR: Sintáctico en: '+str(t.value)+', línea: ' +
                 str(t.lineno)+', columna: '+str(obtener_columna(entrada, t))+'.')
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
    global lexer, parser, entrada, errores_lexicos, errores_sintacticos, consola, gramatical
    gramatical = ''
    entrada = _entrada
    errores_lexicos = _errores_lexicos
    errores_sintacticos = _errores_sintacticos
    consola = _consola
    lexer = lex.lex()
    parser = yacc.yacc()
    return parser.parse(entrada)
