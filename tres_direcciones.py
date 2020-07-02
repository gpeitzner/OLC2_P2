import clases
import re
from PyQt5 import QtCore, QtGui, QtWidgets


class Optimizacion:
    def __init__(self, regla, antes, despues):
        self.regla = regla
        self.antes = antes
        self.despues = despues


class Simbolo:
    def __init__(self, tipo, identificador, temporal):
        self.tipo = tipo
        self.identificador = identificador
        self.temporal = temporal


class TablaSimbolos:
    def __init__(self):
        self.simbolos = {}


class Ambito:
    def __init__(self):
        self.tablas_simbolos = []

    def buscar_simbolo_actual(self, identificador):
        if len(self.tablas_simbolos) > 0:
            tabla_simbolos_actual = self.tablas_simbolos[len(
                self.tablas_simbolos) - 1]
            if identificador in tabla_simbolos_actual.simbolos.keys():
                return tabla_simbolos_actual.simbolos[identificador]
        return None

    def buscar_simbolo_ambito(self, identificador):
        if len(self.tablas_simbolos) > 0:
            tablas_simbolos_temporal = None
            if len(self.tablas_simbolos) > 1:
                tablas_simbolos_temporal = self.tablas_simbolos.copy()
                tablas_simbolos_temporal.reverse()
            else:
                tablas_simbolos_temporal = self.tablas_simbolos
            for tabla_auxiliar in tablas_simbolos_temporal:
                if str(identificador) in tabla_auxiliar.simbolos.keys():
                    return tabla_auxiliar.simbolos[identificador]
        return None

    def actualizar_simbolo_ambito(self, identificador, temporal):
        if len(self.tablas_simbolos) > 0:
            tablas_simbolos_temporal = None
            if len(self.tablas_simbolos) > 1:
                tablas_simbolos_temporal = self.tablas_simbolos.copy()
                tablas_simbolos_temporal.reverse()
            else:
                tablas_simbolos_temporal = self.tablas_simbolos
            for tabla_auxiliar in tablas_simbolos_temporal:
                if identificador in tabla_auxiliar.simbolos.keys():
                    tabla_auxiliar.simbolos[identificador].temporal = temporal
                    return True
        return False

    def agregar_tabla_simbolos(self):
        self.tablas_simbolos.append(TablaSimbolos())

    def eliminar_tabla_simbolos(self):
        if len(self.tablas_simbolos) > 0:
            self.tablas_simbolos.pop()

    def agregar_simbolo(self, simbolo):
        if len(self.tablas_simbolos) > 0:
            self.tablas_simbolos[len(
                self.tablas_simbolos) - 1].simbolos[simbolo.identificador] = simbolo


class TresDirecciones:

    def __init__(self, consola, ast):
        self.consola = consola
        self.ast = ast
        self.funciones = {}
        self.codigo3d = 'main:\n'
        self.contador_registros_temporales = 0
        self.contador_etiquetas_temporales = 0
        self.ambitos = []
        self.detener_ejecucion = False
        self.etiquetas_salida = []
        self.etiquetas_inicio = []
        self.etiquetas_internas = []
        self.optimizaciones = []

    def generar_codigo(self):
        if self.obtener_funciones():
            if self.existe_main():
                self.agregar_ambito()
                self.obtener_ambito().agregar_tabla_simbolos()
                self.cargar_variables_globales()
                if not self.detener_ejecucion:
                    self.generar_codigo_main()
                    if not self.detener_ejecucion:
                        self.consola.setPlainText(str(self.codigo3d))
                        self.optimizar_codigo()
            else:
                self.mostrar_mensaje_consola(
                    'ERROR: No existe la función main.')
        else:
            self.mostrar_mensaje_consola('ERROR: Función repetida.')

    def obtener_funciones(self):
        for instruccion_global in self.ast:
            if isinstance(instruccion_global, clases.Funcion):
                if instruccion_global.identificador in self.funciones.keys():
                    return False
                else:
                    self.funciones[str(
                        instruccion_global.identificador)] = instruccion_global
        return True

    def mostrar_mensaje_consola(self, mensaje):
        self.consola.appendPlainText(str(mensaje))
        cursor_temporal = self.consola.textCursor()
        cursor_temporal.setPosition(len(self.consola.toPlainText()))
        self.consola.setTextCursor(cursor_temporal)

    def existe_main(self):
        if 'main' in self.funciones.keys():
            return True
        return False

    def cargar_variables_globales(self):
        for instruccion_global in self.ast:
            if isinstance(instruccion_global, clases.Declaracion):
                self.generar_codigo_declaracion(instruccion_global)

    def obtener_expresion(self, expresion):
        if isinstance(expresion, clases.ExpresionAritmetica):
            return self.obtener_expresion_aritmetica(expresion)
        if isinstance(expresion, clases.ExpresionRelacional):
            return self.obtener_expresion_relacional(expresion)
        if isinstance(expresion, clases.ExpresionLogica):
            return self.obtener_expresion_logica(expresion)
        if isinstance(expresion, clases.ExpresionBit):
            return self.obtener_expresion_bit(expresion)
        if isinstance(expresion, clases.ExpresionUnaria):
            return self.obtener_expresion_unaria(expresion)
        if isinstance(expresion, clases.ExpresionTernaria):
            return self.obtener_expresion_ternaria(expresion)
        if isinstance(expresion, clases.Entero):
            return str(expresion.valor)
        if isinstance(expresion, clases.Cadena):
            return '"'+str(expresion.valor)+'"'
        if isinstance(expresion, clases.Caracter):
            return "'"+str(expresion.valor)+"'"
        if isinstance(expresion, clases.Decimal):
            return str(expresion.valor)
        if isinstance(expresion, clases.Identificador):
            return self.obtener_temporal_variable(expresion.valor)
        if isinstance(expresion, clases.ExpresionReferencia):
            temporal = self.obtener_temporal_variable(expresion.identificador)
            if temporal:
                return '&'+str(temporal)
            return None
        if isinstance(expresion, clases.ExpresionCasteo):
            return self.obtener_expresion_casteo(expresion)
        if isinstance(expresion, clases.ExpresionIdentificadorArreglo):
            return self.obtener_expresion_identificador_arreglo(expresion)
        if isinstance(expresion, clases.ExpresionEstructura):
            return self.obtener_expresion_estructura(expresion)
        if isinstance(expresion, clases.ExpresionAumentoDecremento):
            return self.obtener_expresion_aumento_decremento(expresion)
        if isinstance(expresion, clases._SizeOf):
            return self.obtener_expresion_sizeof(expresion)
        if isinstance(expresion, clases.ExpresionScan):
            registro = self.obtener_registro_temporal()
            self.codigo3d += registro + '=read();\n'
            return registro
        return None

    def obtener_expresion_aritmetica(self, expresion):
        primero = self.obtener_expresion(expresion.primero)
        segundo = self.obtener_expresion(expresion.segundo)
        if primero and segundo:
            registro = self.obtener_registro_temporal()
            if expresion.operacion == '+':
                self.codigo3d += registro + '=' + primero + '+' + segundo + ';\n'
                return registro
            elif expresion.operacion == '-':
                self.codigo3d += registro + '=' + primero + '-' + segundo + ';\n'
                return registro
            elif expresion.operacion == '*':
                self.codigo3d += registro + '=' + primero + '*' + segundo + ';\n'
                return registro
            elif expresion.operacion == '/':
                self.codigo3d += registro + '=' + primero + '/' + segundo + ';\n'
                return registro
            elif expresion.operacion == '%':
                self.codigo3d += registro + '=' + primero + '%' + segundo + ';\n'
                return registro
        return None

    def obtener_expresion_relacional(self, expresion):
        primero = self.obtener_expresion(expresion.primero)
        segundo = self.obtener_expresion(expresion.segundo)
        if primero and segundo:
            registro = self.obtener_registro_temporal()
            if expresion.operacion == '==':
                self.codigo3d += registro + '=' + primero + '==' + segundo + ';\n'
                return registro
            elif expresion.operacion == '!=':
                self.codigo3d += registro + '=' + primero + '!=' + segundo + ';\n'
                return registro
            elif expresion.operacion == '>':
                self.codigo3d += registro + '=' + primero + '>' + segundo + ';\n'
                return registro
            elif expresion.operacion == '<':
                self.codigo3d += registro + '=' + primero + '<' + segundo + ';\n'
                return registro
            elif expresion.operacion == '>=':
                self.codigo3d += registro + '=' + primero + '>=' + segundo + ";\n"
                return registro
            elif expresion.operacion == '<=':
                self.codigo3d += registro + '=' + primero + '<=' + segundo + ';\n'
                return registro
        return None

    def obtener_expresion_logica(self, expresion):
        primero = self.obtener_expresion(expresion.primero)
        segundo = self.obtener_expresion(expresion.segundo)
        if primero and segundo:
            registro = self.obtener_registro_temporal()
            if expresion.operacion == '&&':
                self.codigo3d += registro + '=' + primero + '&&' + segundo + ';\n'
                return registro
            elif expresion.operacion == '||':
                self.codigo3d += registro + '=' + primero + '||' + segundo + ';\n'
                return registro
        return None

    def obtener_expresion_bit(self, expresion):
        primero = self.obtener_expresion(expresion.primero)
        segundo = self.obtener_expresion(expresion.segundo)
        if primero and segundo:
            registro = self.obtener_registro_temporal()
            if expresion.operacion == '<<':
                self.codigo3d += registro + '=' + primero + '<<' + segundo + ';\n'
                return registro
            elif expresion.operacion == '>>':
                self.codigo3d += registro + '=' + primero + '>>' + segundo + ';\n'
                return registro
            elif expresion.operacion == '&':
                self.codigo3d += registro + '=' + primero + '&' + segundo + ';\n'
                return registro
            elif expresion.operacion == '|':
                self.codigo3d += registro + '=' + primero + '|' + segundo + ';\n'
                return registro
            elif expresion.operacion == '^':
                self.codigo3d += registro + '=' + primero + '^' + segundo + ';\n'
                return registro
        return None

    def obtener_expresion_unaria(self, expresion):
        operando = self.obtener_expresion(expresion.operando)
        if operando:
            registro = self.obtener_registro_temporal()
            if expresion.operacion == '-':
                self.codigo3d += registro + '=-' + operando + ';\n'
                return registro
            elif expresion.operacion == '!':
                self.codigo3d += registro + '=!' + operando + ';\n'
                return registro
            elif expresion.operacion == '~':
                self.codigo3d += registro + '=~' + operando + ';\n'
                return registro
        return None

    def obtener_expresion_ternaria(self, expresion):
        primero = self.obtener_expresion(expresion.primero)
        segundo = self.obtener_expresion(expresion.segundo)
        expresion = self.obtener_expresion(expresion.expresion)
        if primero and segundo and expresion:
            registro = self.obtener_registro_temporal()
            etiqueta_verdadero = self.obtener_etiqueta_temporal()
            etiqueta_salida = self.obtener_etiqueta_temporal()
            self.codigo3d += 'if('+expresion+')goto ' + \
                etiqueta_verdadero+';\n'
            self.codigo3d += registro + '='+segundo+';\n'
            self.codigo3d += 'goto '+etiqueta_salida+';\n'
            self.codigo3d += etiqueta_verdadero + ':\n'
            self.codigo3d += registro + '='+primero+';\n'
            self.codigo3d += etiqueta_salida + ':\n'
            return registro
        return None

    def obtener_expresion_casteo(self, expresion):
        operando = self.obtener_expresion(expresion.expresion)
        if operando:
            if expresion.tipo.valor in ['int', 'float', 'char']:
                registro = self.obtener_registro_temporal()
                self.codigo3d += registro + \
                    '=('+expresion.tipo.valor+')'+operando+';\n'
                return registro
        return None

    def obtener_expresion_identificador_arreglo(self, expresion):
        temporal = self.obtener_temporal_variable(expresion.identificador)
        if temporal:
            temporales = []
            for expresion_temporal in expresion.accesos:
                acceso = self.obtener_expresion(expresion_temporal)
                if acceso:
                    temporales.append(acceso)
                else:
                    return None
            respuesta = temporal
            for temporal in temporales:
                respuesta += '['+temporal+']'
            return respuesta
        return None

    def obtener_expresion_estructura(self, expresion):
        temporal = self.obtener_temporal_variable(expresion.identificador)
        if temporal:
            if expresion.indices_primario:
                for acceso in expresion.indices_primario:
                    expresion_temporal = self.obtener_expresion(acceso)
                    if expresion_temporal:
                        temporal += '['+expresion_temporal+']'
                    else:
                        return None
            temporal += '["'+expresion.atributo+'"]'
            if expresion.indices_secundario:
                for acceso in expresion.indices_secundario:
                    expresion_temporal = self.obtener_expresion(acceso)
                    if expresion_temporal:
                        temporal += '['+expresion_temporal+']'
                    else:
                        return None
            return temporal
        return None

    def obtener_expresion_aumento_decremento(self, expresion):
        temporal = self.obtener_temporal_variable(expresion.identificador)
        if temporal:
            if expresion.operacion == '++':
                if expresion.orden == 'post':
                    registro = self.obtener_registro_temporal()
                    self.codigo3d += registro + '='+temporal+';\n'
                    self.codigo3d += temporal + '='+temporal+'+1;\n'
                    return registro
                elif expresion.orden == 'pre':
                    self.codigo3d += temporal + '='+temporal+'+1;\n'
                    return temporal
            elif expresion.operacion == '--':
                if expresion.orden == 'post':
                    registro = self.obtener_registro_temporal()
                    self.codigo3d += registro + '='+temporal+';\n'
                    self.codigo3d += temporal + '='+temporal+'-1;\n'
                    return registro
                elif expresion.orden == 'pre':
                    self.codigo3d += temporal + '='+temporal+'-1;\n'
                    return temporal
        return None

    def obtener_expresion_sizeof(self, expresion):
        if expresion.tipo.valor == 'int':
            return '4'
        elif expresion.tipo.valor == 'char':
            return '1'
        elif expresion.tipo.valor == 'double':
            return '8'
        elif expresion.tipo.valor == 'float':
            return '4'
        elif expresion.tipo.valor == 'void':
            return '1'
        elif expresion.tipo.valor == 'struct':
            return '16'
        return None

    def obtener_registro_temporal(self):
        registro_temporal = '$t' + str(self.contador_registros_temporales)
        self.contador_registros_temporales += 1
        return registro_temporal

    def obtener_etiqueta_temporal(self):
        etiqueta_temporal = 'm_c_e' + \
            str(self.contador_etiquetas_temporales)
        self.contador_etiquetas_temporales += 1
        return etiqueta_temporal

    def generar_codigo_main(self):
        self.codigo3d += 'm_c_ep:\n'
        principal = self.funciones['main']
        self.agregar_ambito()
        self.obtener_ambito().agregar_tabla_simbolos()
        self.generar_codigo_instrucciones(principal.cuerpo)
        self.obtener_ambito().eliminar_tabla_simbolos()
        self.eliminar_ambito()
        self.codigo3d += 'exit;\n'

    def generar_codigo_instrucciones(self, instrucciones):
        if instrucciones:
            for instruccion in instrucciones:
                if isinstance(instruccion, clases.Etiqueta):
                    self.generar_codigo_etiqueta(instruccion)
                elif isinstance(instruccion, clases.Salto):
                    self.generar_codigo_salto(instruccion)
                elif isinstance(instruccion, clases.Declaracion):
                    self.generar_codigo_declaracion(instruccion)
                elif isinstance(instruccion, clases.Asignacion):
                    self.generar_codigo_asignacion(instruccion)
                elif isinstance(instruccion, clases._If):
                    self.generar_codigo_if(instruccion)
                elif isinstance(instruccion, clases._Switch):
                    self.generar_codigo_switch(instruccion)
                elif isinstance(instruccion, clases._Break):
                    self.generar_codigo_break(instruccion)
                elif isinstance(instruccion, clases._While):
                    self.generar_codigo_while(instruccion)
                elif isinstance(instruccion, clases._Do):
                    self.generar_codigo_do(instruccion)
                elif isinstance(instruccion, clases._Continue):
                    self.generar_codigo_continue(instruccion)
                elif isinstance(instruccion, clases._For):
                    self.generar_codigo_for(instruccion)
                elif isinstance(instruccion, clases.Metodo):
                    self.generar_codigo_metodo(instruccion)
                elif isinstance(instruccion, clases._PrintF):
                    self.generar_codigo_printf(instruccion)
                if self.detener_ejecucion:
                    break

    def generar_codigo_etiqueta(self, instruccion):
        if not instruccion.identificador in self.etiquetas_internas:
            self.codigo3d += instruccion.identificador + ':\n'
            self.etiquetas_internas.append(instruccion.identificador)
        else:
            self.mostrar_mensaje_consola(
                'ERROR: Etiqueta repetida en línea: '+instruccion.linea+'.')
            self.detener_ejecucion = True

    def generar_codigo_salto(self, instruccion):
        if instruccion.identificador in self.etiquetas_internas:
            self.codigo3d += 'goto '+instruccion.identificador+';\n'
        else:
            self.mostrar_mensaje_consola(
                'ERROR: Etiqueta inexistente en línea: '+instruccion.linea+'.')
            self.detener_ejecucion = True

    def generar_codigo_declaracion(self, instruccion):
        tipo = instruccion.tipo.valor
        for declaracion in instruccion.declaraciones:
            identificador = declaracion.identificador
            if self.obtener_ambito().buscar_simbolo_actual(identificador):
                self.mostrar_mensaje_consola(
                    'ERROR: Variable repetida en línea: '+declaracion.linea+'.')
                self.detener_ejecucion = True
            else:
                if tipo == 'struct':
                    registro = self.obtener_registro_temporal()
                    self.codigo3d += registro + '=array();\n'
                    self.obtener_ambito().agregar_simbolo(
                        Simbolo(tipo, identificador, registro))
                elif declaracion.indices:
                    self.generar_codigo_declaracion_arreglo(
                        tipo, identificador, declaracion)
                else:
                    self.generar_codigo_declaracion_estandar(
                        tipo, identificador, declaracion)

    def generar_codigo_declaracion_estandar(self, tipo, identificador, declaracion):
        if declaracion.expresion:
            temporal = self.obtener_expresion(
                declaracion.expresion)
            if temporal:
                registro = self.obtener_registro_temporal()
                self.codigo3d += registro + '='+temporal+';\n'
                self.obtener_ambito().agregar_simbolo(
                    Simbolo(tipo, identificador, registro))
            else:
                self.mostrar_mensaje_consola(
                    'ERROR: Expresión no válida en línea: '+declaracion.linea+'.')
                self.detener_ejecucion = True
        else:
            registro = self.obtener_registro_temporal()
            self.codigo3d += registro + '=0;\n'
            self.obtener_ambito().agregar_simbolo(
                Simbolo(tipo, identificador, registro))

    def generar_codigo_declaracion_arreglo(self, tipo, identificador, declaracion):
        if declaracion.expresion:
            if isinstance(declaracion.expresion, clases.ExpresionElementos):
                registro = self.obtener_registro_temporal()
                self.codigo3d += registro + ' =array();\n'
                self.obtener_ambito().agregar_simbolo(
                    Simbolo(tipo, identificador, registro))
                if isinstance(declaracion.expresion.expresiones[0], clases.ExpresionElementos):
                    filas = 0
                    for lista in declaracion.expresion.expresiones:
                        columnas = 0
                        for expresion in lista.expresiones:
                            temporal = self.obtener_expresion(expresion)
                            if temporal:
                                self.codigo3d += registro + \
                                    '['+str(filas)+']['+str(columnas) + \
                                    ']'+'='+temporal+';\n'
                            else:
                                self.mostrar_mensaje_consola(
                                    'ERROR: Expresión no válida en línea: '+declaracion.linea+'.')
                                self.detener_ejecucion = True
                                break
                            columnas += 1
                        filas += 1
                else:
                    indice = 0
                    for expresion in declaracion.expresion.expresiones:
                        temporal = self.obtener_expresion(expresion)
                        if temporal:
                            self.codigo3d += registro + \
                                '['+str(indice)+']'+'='+temporal+';\n'
                        else:
                            self.mostrar_mensaje_consola(
                                'ERROR: Expresión no válida en línea: '+declaracion.linea+'.')
                            self.detener_ejecucion = True
                            break
                        indice += 1
            elif isinstance(declaracion.expresion, clases.Cadena):
                registro = self.obtener_registro_temporal()
                self.codigo3d += registro + '="'+declaracion.expresion.valor+'";\n'
                self.obtener_ambito().agregar_simbolo(
                    Simbolo(tipo, identificador, registro))
            else:
                self.mostrar_mensaje_consola(
                    'ERROR: Expresión no válida en línea: '+declaracion.linea+'.')
                self.detener_ejecucion = True
        else:
            registro = self.obtener_registro_temporal()
            self.codigo3d += registro + '=array();\n'
            self.obtener_ambito().agregar_simbolo(
                Simbolo(tipo, identificador, registro))

    def generar_codigo_asignacion(self, instruccion):
        if isinstance(instruccion, clases.AsignacionNormal):
            self.generar_codigo_asignacion_normal(instruccion)
        elif isinstance(instruccion, clases.AsignacionAumento):
            self.generar_codigo_asignacion_aumento(instruccion)
        elif isinstance(instruccion, clases.AsignacionDecremento):
            self.generar_codigo_asignacion_decremento(instruccion)
        elif isinstance(instruccion, clases.AsignacionEstructura):
            self.generar_codigo_asignacion_estructura(instruccion)

    def generar_codigo_asignacion_normal(self, instruccion):
        simbolo = self.existe_variable(instruccion.identificador)
        if simbolo:
            if instruccion.indices:
                registro = simbolo.temporal
                for acceso in instruccion.indices:
                    expresion_temporal = self.obtener_expresion(acceso)
                    if expresion_temporal:
                        registro += '['+expresion_temporal+']'
                    else:
                        self.mostrar_mensaje_consola(
                            'ERROR: Expresión no válida en línea: '+instruccion.linea+'.')
                        self.detener_ejecucion = True
                if not self.detener_ejecucion:
                    temporal = self.obtener_expresion(instruccion.expresion)
                    if temporal:
                        self.codigo3d += registro + '='+temporal+';\n'
                    else:
                        self.mostrar_mensaje_consola(
                            'ERROR: Expresión no válida en línea: '+instruccion.linea+'.')
                        self.detener_ejecucion = True
            else:
                temporal = self.obtener_expresion(instruccion.expresion)
                if temporal:
                    registro = simbolo.temporal
                    if self.actualizar_temporal_variable(instruccion.identificador, registro):
                        self.generar_codigo_compuesto(
                            instruccion, registro, temporal)
                    else:
                        self.mostrar_mensaje_consola(
                            'ERROR: Asignación no válida en línea: '+instruccion.linea+'.')
                        self.detener_ejecucion = True
                else:
                    self.mostrar_mensaje_consola(
                        'ERROR: Expresión no válida en línea: '+instruccion.linea+'.')
                    self.detener_ejecucion = True
        else:
            self.mostrar_mensaje_consola(
                'ERROR: No existe la variable en línea: '+instruccion.linea+'.')
            self.detener_ejecucion = True

    def generar_codigo_asignacion_estructura(self, instruccion):
        simbolo = self.existe_variable(instruccion.identificador)
        if simbolo:
            temporal = self.obtener_expresion(instruccion.expresion)
            if temporal:
                registro = simbolo.temporal
                if instruccion.indices_primario:
                    for acceso in instruccion.indices_primario:
                        expresion = self.obtener_expresion(acceso)
                        if expresion:
                            registro += '['+expresion+']'
                        else:
                            self.mostrar_mensaje_consola(
                                'ERROR: Expresión no válida en línea: '+instruccion.linea+'.')
                            self.detener_ejecucion = True
                if not self.detener_ejecucion:
                    registro += '["'+instruccion.atributo+'"]'
                    if instruccion.indices_secundario:
                        for acceso in instruccion.indices_secundario:
                            expresion = self.obtener_expresion(acceso)
                            if expresion:
                                registro += '['+expresion+']'
                            else:
                                self.mostrar_mensaje_consola(
                                    'ERROR: Expresión no válida en línea: '+instruccion.linea+'.')
                                self.detener_ejecucion = True
                    if not self.detener_ejecucion:
                        self.generar_codigo_compuesto(
                            instruccion, registro, temporal)
            else:
                self.mostrar_mensaje_consola(
                    'ERROR: Expresión no válida en línea: '+instruccion.linea+'.')
                self.detener_ejecucion = True
        else:
            self.mostrar_mensaje_consola(
                'ERROR: No existe la variable en línea: '+instruccion.linea+'.')
            self.detener_ejecucion = True

    def generar_codigo_asignacion_aumento(self, instruccion):
        simbolo = self.existe_variable(instruccion.identificador)
        if simbolo:
            registro = simbolo.temporal
            if not registro:
                registro = self.obtener_registro_temporal()
            self.codigo3d += registro + '='+registro+'+1;\n'
        else:
            self.mostrar_mensaje_consola(
                'ERROR: No existe la variable en línea: '+instruccion.linea+'.')
            self.detener_ejecucion = True

    def generar_codigo_asignacion_decremento(self, instruccion):
        simbolo = self.existe_variable(instruccion.identificador)
        if simbolo:
            registro = simbolo.temporal
            if not registro:
                registro = self.obtener_registro_temporal()
            self.codigo3d += registro + '='+registro+'-1;\n'
        else:
            self.mostrar_mensaje_consola(
                'ERROR: No existe la variable en línea: '+instruccion.linea+'.')
            self.detener_ejecucion = True

    def generar_codigo_compuesto(self, instruccion, registro, temporal):
        if instruccion.compuesto == '=':
            self.codigo3d += registro + '='+temporal+';\n'
        elif instruccion.compuesto == '+':
            self.codigo3d += registro + '='+registro+'+'+temporal+';\n'
        elif instruccion.compuesto == '-':
            self.codigo3d += registro + '='+registro+'-'+temporal+';\n'
        elif instruccion.compuesto == '*':
            self.codigo3d += registro + '='+registro+'*'+temporal+';\n'
        elif instruccion.compuesto == '/':
            self.codigo3d += registro + '='+registro+'/'+temporal+';\n'
        elif instruccion.compuesto == '%':
            self.codigo3d += registro + '='+registro+'%'+temporal+';\n'
        elif instruccion.compuesto == '<<':
            self.codigo3d += registro + '='+registro+'<<'+temporal+';\n'
        elif instruccion.compuesto == '>>':
            self.codigo3d += registro + '='+registro+'>>'+temporal+';\n'
        elif instruccion.compuesto == '&':
            self.codigo3d += registro + '='+registro+'&'+temporal+';\n'
        elif instruccion.compuesto == '^':
            self.codigo3d += registro + '='+registro+'^'+temporal+';\n'
        elif instruccion.compuesto == '|':
            self.codigo3d += registro + '='+registro+'|'+temporal+';\n'

    def generar_codigo_if(self, instruccion):
        expresion_inicio = self.obtener_expresion(instruccion.expresion)
        if expresion_inicio:
            etiqueta_inicio = self.obtener_etiqueta_temporal()
            etiqueta_salida = self.obtener_etiqueta_temporal()
            self.codigo3d += 'if('+expresion_inicio + \
                ')goto '+etiqueta_inicio+';\n'
            etiquetas_temporales = []
            if instruccion.elseifs:
                for expresion_elseif in instruccion.elseifs:
                    expresion_temporal = self.obtener_expresion(
                        expresion_elseif.expresion)
                    if expresion_temporal:
                        etiqueta_temporal = self.obtener_etiqueta_temporal()
                        etiquetas_temporales.append(etiqueta_temporal)
                        self.codigo3d += 'if('+expresion_temporal + \
                            ')goto '+etiqueta_temporal+';\n'
                    else:
                        self.mostrar_mensaje_consola(
                            'ERROR: Expresión no válida en línea: '+instruccion.linea+'.')
                        self.detener_ejecucion = True
                        break
            if not self.detener_ejecucion:
                if instruccion._else:
                    self.obtener_ambito().agregar_tabla_simbolos()
                    self.generar_codigo_instrucciones(instruccion._else.cuerpo)
                    self.obtener_ambito().eliminar_tabla_simbolos()
                self.codigo3d += 'goto '+etiqueta_salida+';\n'
                self.codigo3d += etiqueta_inicio + ':\n'
                self.obtener_ambito().agregar_tabla_simbolos()
                self.generar_codigo_instrucciones(instruccion.cuerpo)
                self.obtener_ambito().eliminar_tabla_simbolos()
                self.codigo3d += 'goto '+etiqueta_salida+';\n'
                if instruccion.elseifs:
                    indice_etiqueta_temporal = 0
                    for expresion_elseif in instruccion.elseifs:
                        self.codigo3d += etiquetas_temporales[indice_etiqueta_temporal] + ':\n'
                        self.obtener_ambito().agregar_tabla_simbolos()
                        self.generar_codigo_instrucciones(
                            expresion_elseif.cuerpo)
                        self.obtener_ambito().eliminar_tabla_simbolos()
                        self.codigo3d += 'goto '+etiqueta_salida+';\n'
                        indice_etiqueta_temporal += 1
                self.codigo3d += etiqueta_salida + ':\n'
        else:
            self.mostrar_mensaje_consola(
                'ERROR: Expresión no válida en línea: '+instruccion.linea)
            self.detener_ejecucion = True

    def generar_codigo_switch(self, instruccion):
        expresion_inicio = self.obtener_expresion(instruccion.expresion)
        if expresion_inicio:
            etiqueta_salida = self.obtener_etiqueta_temporal()
            self.etiquetas_salida.append(etiqueta_salida)
            etiquetas_temporales = []
            if instruccion.cases:
                for caso in instruccion.cases:
                    expresion_caso = self.obtener_expresion(caso.expresion)
                    if expresion_caso:
                        etiqueta_temporal = self.obtener_etiqueta_temporal()
                        etiquetas_temporales.append(etiqueta_temporal)
                        self.codigo3d += 'if('+expresion_inicio+'==' + \
                            expresion_caso+')goto '+etiqueta_temporal+';\n'
                    else:
                        self.mostrar_mensaje_consola(
                            'ERROR: Expresión no válida en línea: '+instruccion.linea)
                        self.detener_ejecucion = True
                        break
            if not self.detener_ejecucion:
                etiqueta_defecto = None
                if instruccion.defecto:
                    etiqueta_defecto = self.obtener_etiqueta_temporal()
                    self.codigo3d += 'goto '+etiqueta_defecto+';\n'
                self.codigo3d += 'goto '+etiqueta_salida+';\n'
                if instruccion.cases:
                    indice_etiqueta_temporal = 0
                    self.obtener_ambito().agregar_tabla_simbolos()
                    for caso in instruccion.cases:
                        self.codigo3d += etiquetas_temporales[indice_etiqueta_temporal] + ':\n'
                        self.generar_codigo_instrucciones(
                            caso.cuerpo)
                        indice_etiqueta_temporal += 1
                    self.obtener_ambito().eliminar_tabla_simbolos()
                if etiqueta_defecto:
                    self.codigo3d += etiqueta_defecto + ':\n'
                    self.obtener_ambito().agregar_tabla_simbolos()
                    self.generar_codigo_instrucciones(
                        instruccion.defecto.cuerpo)
                    self.obtener_ambito().eliminar_tabla_simbolos()
                self.codigo3d += etiqueta_salida + ':\n'
            self.etiquetas_salida.pop()
        else:
            self.mostrar_mensaje_consola(
                'ERROR: Expresión no válida en línea: '+instruccion.linea)
            self.detener_ejecucion = True

    def generar_codigo_break(self, instruccion):
        if len(self.etiquetas_salida) > 0:
            self.codigo3d += 'goto '+self.etiquetas_salida[len(
                self.etiquetas_salida)-1]+';\n'
        else:
            self.mostrar_mensaje_consola(
                'ERROR: Break no válido en línea: '+instruccion.linea)
            self.detener_ejecucion = True

    def generar_codigo_while(self, instruccion):
        etiqueta_inicio = self.obtener_etiqueta_temporal()
        self.codigo3d += etiqueta_inicio + ':\n'
        expresion = self.obtener_expresion(instruccion.expresion)
        if expresion:
            etiqueta_verdadero = self.obtener_etiqueta_temporal()
            etiqueta_fin = self.obtener_etiqueta_temporal()
            self.etiquetas_inicio.append(etiqueta_inicio)
            self.etiquetas_salida.append(etiqueta_fin)
            self.codigo3d += 'if('+expresion+')goto '+etiqueta_verdadero+';\n'
            self.codigo3d += 'goto '+etiqueta_fin+';\n'
            self.codigo3d += etiqueta_verdadero + ':\n'
            self.obtener_ambito().agregar_tabla_simbolos()
            self.generar_codigo_instrucciones(instruccion.cuerpo)
            self.obtener_ambito().eliminar_tabla_simbolos()
            self.codigo3d += 'goto '+etiqueta_inicio+';\n'
            self.codigo3d += etiqueta_fin+':\n'
            self.etiquetas_inicio.pop()
            self.etiquetas_salida.pop()
        else:
            self.mostrar_mensaje_consola(
                'ERROR: Expresión no válida en línea: '+instruccion.linea)
            self.detener_ejecucion = True

    def generar_codigo_do(self, instruccion):
        etiqueta_inicio = self.obtener_etiqueta_temporal()
        etiqueta_fin = self.obtener_etiqueta_temporal()
        etiqueta_inicio_ciclo = self.obtener_etiqueta_temporal()
        self.etiquetas_inicio.append(etiqueta_inicio_ciclo)
        self.etiquetas_salida.append(etiqueta_fin)
        self.codigo3d += etiqueta_inicio + ':\n'
        self.obtener_ambito().agregar_tabla_simbolos()
        self.generar_codigo_instrucciones(instruccion.cuerpo)
        self.obtener_ambito().eliminar_tabla_simbolos()
        self.etiquetas_inicio.pop()
        self.etiquetas_salida.pop()
        self.codigo3d += etiqueta_inicio_ciclo+':\n'
        expresion = self.obtener_expresion(instruccion.expresion)
        if expresion:
            self.codigo3d += 'if('+expresion+')goto '+etiqueta_inicio+';\n'
            self.codigo3d += etiqueta_fin+':\n'
        else:
            self.mostrar_mensaje_consola(
                'ERROR: Expresión no válida en línea: '+instruccion.linea)
            self.detener_ejecucion = True

    def generar_codigo_continue(self, instruccion):
        if len(self.etiquetas_inicio) > 0:
            self.codigo3d += 'goto '+self.etiquetas_inicio[len(
                self.etiquetas_inicio)-1]+';\n'
        else:
            self.mostrar_mensaje_consola(
                'ERROR: Continue no válido en línea: '+instruccion.linea)
            self.detener_ejecucion = True

    def generar_codigo_for(self, instruccion):
        self.obtener_ambito().agregar_tabla_simbolos()
        self.generar_codigo_instrucciones([instruccion.inicio])
        if not self.detener_ejecucion:
            if isinstance(instruccion.expresion, (clases.ExpresionRelacional, clases.ExpresionLogica)):
                etiqueta_inicio = self.obtener_etiqueta_temporal()
                etiqueta_fin = self.obtener_etiqueta_temporal()
                etiqueta_verdadero = self.obtener_etiqueta_temporal()
                self.etiquetas_salida.append(etiqueta_fin)
                self.codigo3d += etiqueta_inicio + ':\n'
                expresion = self.obtener_expresion(instruccion.expresion)
                if expresion:
                    etiqueta_inicio_ciclo = self.obtener_etiqueta_temporal()
                    self.etiquetas_inicio.append(etiqueta_inicio_ciclo)
                    self.codigo3d += 'if('+expresion+')goto ' + \
                        etiqueta_verdadero+';\n'
                    self.codigo3d += 'goto '+etiqueta_fin+';\n'
                    self.codigo3d += etiqueta_verdadero+':\n'
                    self.obtener_ambito().agregar_tabla_simbolos()
                    self.generar_codigo_instrucciones(instruccion.cuerpo)
                    self.obtener_ambito().eliminar_tabla_simbolos()
                    self.codigo3d += etiqueta_inicio_ciclo + ':\n'
                    self.generar_codigo_instrucciones([instruccion.asignacion])
                    self.codigo3d += 'goto '+etiqueta_inicio+';\n'
                    self.codigo3d += etiqueta_fin+':\n'
                    self.etiquetas_inicio.pop()
                else:
                    self.mostrar_mensaje_consola(
                        'ERROR: Expresión no válida en línea: '+instruccion.linea)
                    self.detener_ejecucion = True
                self.etiquetas_salida.pop()
            else:
                self.mostrar_mensaje_consola(
                    'ERROR: Expresión no válida en línea: '+instruccion.linea)
                self.detener_ejecucion = True
        self.obtener_ambito().eliminar_tabla_simbolos()

    def generar_codigo_metodo(self, instruccion):
        if instruccion.identificador in self.funciones.keys():
            funcion = self.funciones[instruccion.identificador]
            if funcion.parametros:
                if instruccion.expresiones:
                    if len(funcion.parametros) == len(instruccion.expresiones):
                        temporales = []
                        for expresion in instruccion.expresiones:
                            temporal = self.obtener_expresion(expresion)
                            if temporal:
                                temporales.append(temporal)
                            else:
                                self.mostrar_mensaje_consola(
                                    'ERROR: Expresión no válida en línea: '+instruccion.linea)
                                self.detener_ejecucion = True
                                break
                        if not self.detener_ejecucion:
                            self.agregar_ambito()
                            self.obtener_ambito().agregar_tabla_simbolos()
                            etiqueta_funcion = self.obtener_etiqueta_temporal()
                            self.codigo3d += etiqueta_funcion + ':\n'
                            parametros = []
                            for parametro in funcion.parametros:
                                parametros.append(parametro)
                            if len(parametros) == len(set(parametros)):
                                indice_temporales = 0
                                for parametro in funcion.parametros:
                                    if parametro.modo:
                                        referencia = temporales[indice_temporales]
                                        self.obtener_ambito().agregar_simbolo(
                                            Simbolo(parametro.tipo, parametro.identificador, referencia))
                                    else:
                                        temporal = self.obtener_registro_temporal()
                                        valor = temporales[indice_temporales]
                                        self.codigo3d += temporal + '='+valor+';\n'
                                        self.obtener_ambito().agregar_simbolo(
                                            Simbolo(parametro.tipo, parametro.identificador, temporal))
                                    indice_temporales += 1
                                self.generar_codigo_instrucciones(
                                    funcion.cuerpo)
                            else:
                                self.mostrar_mensaje_consola(
                                    'ERROR: Parametros no válidos en línea: '+instruccion.linea)
                                self.detener_ejecucion = True
                            self.obtener_ambito().eliminar_tabla_simbolos()
                            self.eliminar_ambito()
                    else:
                        self.mostrar_mensaje_consola(
                            'ERROR: Cantidad de parametros no válida en línea: '+instruccion.linea)
                        self.detener_ejecucion = True
                else:
                    self.mostrar_mensaje_consola(
                        'ERROR: Cantidad de parametros no válida en línea: '+instruccion.linea)
                    self.detener_ejecucion = True
            else:
                if not instruccion.expresiones:
                    self.agregar_ambito()
                    self.obtener_ambito().agregar_tabla_simbolos()
                    etiqueta_funcion = self.obtener_etiqueta_temporal()
                    self.codigo3d += etiqueta_funcion + ':\n'
                    self.generar_codigo_instrucciones(funcion.cuerpo)
                    self.obtener_ambito().eliminar_tabla_simbolos()
                    self.eliminar_ambito()
                else:
                    self.mostrar_mensaje_consola(
                        'ERROR: Cantidad de parametros no válida en línea: '+instruccion.linea)
                    self.detener_ejecucion = True
        else:
            self.mostrar_mensaje_consola(
                'ERROR: La función no existe en línea: '+instruccion.linea)
            self.detener_ejecucion = True

    def generar_codigo_printf(self, instruccion):
        if isinstance(instruccion.expresiones[0], clases.Cadena):
            if len(instruccion.expresiones) > 1:
                salida_temporal = instruccion.expresiones[0].valor.split('%')
                if (len(instruccion.expresiones) - 1) == len(salida_temporal) - 1:
                    temporales = []
                    indice_expresiones = 1
                    while indice_expresiones < len(instruccion.expresiones):
                        registro = self.obtener_expresion(
                            instruccion.expresiones[indice_expresiones])
                        if registro:
                            temporales.append(registro)
                        else:
                            self.mostrar_mensaje_consola(
                                'ERROR: Expresión no válida en línea: '+instruccion.linea)
                            self.detener_ejecucion = True
                            break
                        indice_expresiones += 1
                    if not self.detener_ejecucion:
                        indice_expresiones = 0
                        indice_temporales = 0
                        for salida_auxiliar in salida_temporal:
                            if indice_expresiones > 0:
                                if temporales[indice_temporales] != '':
                                    self.codigo3d += 'print(' + \
                                        temporales[indice_temporales]+');\n'
                                self.generar_codigo_saltos_linea(
                                    salida_auxiliar[1:])
                                indice_temporales += 1
                            else:
                                self.generar_codigo_saltos_linea(
                                    salida_auxiliar)
                                indice_expresiones += 1
                else:
                    self.mostrar_mensaje_consola(
                        'ERROR: Número de expreiones no válido en línea: '+instruccion.linea)
                    self.detener_ejecucion = True
            else:
                self.generar_codigo_saltos_linea(
                    instruccion.expresiones[0].valor)
        else:
            self.mostrar_mensaje_consola(
                'ERROR: Expresión no válida en línea: '+instruccion.linea)
            self.detener_ejecucion = True

    def generar_codigo_saltos_linea(self, cadena):
        salida = (cadena.replace('\\t', '     ')).split('\\n')
        if len(salida) > 1:
            indice_salida = 0
            while indice_salida < len(salida):
                if indice_salida > 0:
                    self.codigo3d += 'print("\\n");\n'
                if salida[indice_salida] != '':
                    self.codigo3d += 'print("' + \
                        salida[indice_salida]+'");\n'
                indice_salida += 1
        else:
            if salida[0] != '':
                self.codigo3d += 'print("'+salida[0]+'");\n'

    def agregar_ambito(self):
        self.ambitos.append(Ambito())

    def eliminar_ambito(self):
        if len(self.ambitos) > 0:
            self.ambitos.pop()

    def obtener_ambito(self):
        if len(self.ambitos) > 0:
            return self.ambitos[len(self.ambitos) - 1]

    def obtener_temporal_variable(self, identificador):
        if len(self.ambitos) > 0:
            registro = self.obtener_ambito().buscar_simbolo_ambito(identificador)
            if registro:
                return registro.temporal
            registro = self.ambitos[0].buscar_simbolo_ambito(identificador)
            if registro:
                return registro.temporal
        return None

    def actualizar_temporal_variable(self, identificador, temporal):
        if len(self.ambitos) > 0:
            if self.obtener_ambito().actualizar_simbolo_ambito(identificador, temporal):
                return True
            if self.ambitos[0].actualizar_simbolo_ambito(identificador, temporal):
                return True
        return False

    def existe_variable(self, identificador):
        if len(self.ambitos) > 0:
            registro = self.obtener_ambito().buscar_simbolo_ambito(identificador)
            if registro:
                return registro
            registro = self.ambitos[0].buscar_simbolo_ambito(identificador)
            if registro:
                return registro
        return None

    def optimizar_codigo(self):
        codigo_optimizado = self.codigo3d
        codigo_optimizado = codigo_optimizado.split('\n')
        codigo_optimizado = self.optimizar_regla1(codigo_optimizado)
        codigo_optimizado = self.optimizar_regla2(codigo_optimizado)
        for optimizacion in self.optimizaciones:
            print('REGLA: '+optimizacion.regla)
            print('ANTES: '+optimizacion.antes)
            print('DESPUES: '+optimizacion.despues)
            print('')
        print(''.join(codigo_optimizado))

    def optimizar_regla1(self, codigo_optimizado):
        indice = 0
        codigo_temporal = []
        while indice < len(codigo_optimizado):
            if codigo_optimizado[indice]:
                if (indice + 1) < len(codigo_optimizado):
                    instruccion_actual = codigo_optimizado[indice].replace(
                        ';', '').split('=')
                    instruccion_siguiente = codigo_optimizado[indice+1].replace(';', '').split(
                        '=')
                    if len(instruccion_actual) == 2 and len(instruccion_siguiente) == 2:
                        if (instruccion_actual[0] == instruccion_siguiente[1] and
                                instruccion_actual[1] == instruccion_siguiente[0]):
                            if (re.search(r'\$t[0-9]+', instruccion_actual[0]) and
                                    re.search(r'\$t[0-9]+', instruccion_actual[0])):
                                self.optimizaciones.append(Optimizacion(
                                    'Regla 1', codigo_optimizado[indice]+codigo_optimizado[indice+1], codigo_optimizado[indice]))
                                codigo_temporal.append(
                                    codigo_optimizado[indice])
                                codigo_optimizado[indice+1] = None
                                indice += 1
                            else:
                                codigo_temporal.append(
                                    codigo_optimizado[indice])
                                indice += 1
                        else:
                            codigo_temporal.append(codigo_optimizado[indice])
                            indice += 1
                    else:
                        codigo_temporal.append(codigo_optimizado[indice])
                        indice += 1
                else:
                    codigo_temporal.append(codigo_optimizado[indice])
                    indice += 1
            else:
                indice += 1
        return codigo_temporal

    def optimizar_regla2(self, codigo_optimizado):
        indice = 0
        codigo_temporal = []
        while indice < len(codigo_optimizado):
            if codigo_optimizado[indice]:
                instruccion = codigo_optimizado[indice].split(' ')
                if len(instruccion) == 2:
                    if instruccion[0] == 'goto':
                        indice_busqueda = indice
                        indice_busqueda += 1
                        etiqueta_encontrada = False
                        while indice_busqueda < len(codigo_optimizado):
                            instruccion_temporal = codigo_optimizado[indice_busqueda]
                            if re.search(r'[a-zA-Z_][a-zA-Z_0-9]*:', instruccion_temporal):
                                instruccion_auxiliar = instruccion_temporal.split(
                                    ':')
                                instruccion_inicial = instruccion[1].split(';')
                                if instruccion_auxiliar[0] == instruccion_inicial[0]:
                                    etiqueta_encontrada = True
                                    break
                                else:
                                    break
                            indice_busqueda += 1
                        if etiqueta_encontrada:
                            codigo_eliminado = ''
                            while indice <= indice_busqueda:
                                codigo_eliminado += codigo_optimizado[indice]
                                indice += 1
                            indice -= 1
                            self.optimizaciones.append(Optimizacion(
                                'Regla 2', codigo_eliminado, codigo_optimizado[indice]))
                            codigo_temporal.append(codigo_optimizado[indice])
                            indice += 1
                        else:
                            codigo_temporal.append(codigo_optimizado[indice])
                            indice += 1
                    else:
                        codigo_temporal.append(codigo_optimizado[indice])
                        indice += 1
                else:
                    codigo_temporal.append(codigo_optimizado[indice])
                    indice += 1
            else:
                indice += 1
        return codigo_temporal
