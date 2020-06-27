import clases
from PyQt5 import QtCore, QtGui, QtWidgets


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
                tablas_simbolos_temporal = self.tablas_simbolos.reverse()
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
                tablas_simbolos_temporal = self.tablas_simbolos.reverse()
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
        self.agregar_ambito()
        self.obtener_ambito().agregar_tabla_simbolos()
        self.detener_ejecucion = False

    def generar_codigo(self):
        if self.obtener_funciones():
            if self.existe_main():
                self.cargar_variables_globales()
                if not self.detener_ejecucion:
                    self.generar_codigo_main()
                    if not self.detener_ejecucion:
                        self.consola.setPlainText(str(self.codigo3d))
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
        if isinstance(expresion, (clases.Cadena, clases.Caracter)):
            return str(expresion.valor)
        if isinstance(expresion, clases.Decimal):
            return str(expresion.valor)
        if isinstance(expresion, clases.Identificador):
            return self.obtener_temporal_variable(expresion.valor)
        if isinstance(expresion, clases.ExpresionScan):
            registro = self.obtener_registro_temporal()
            self.codigo3d += registro + ' = read();\n'
            return registro
        return None

    def obtener_expresion_aritmetica(self, expresion):
        primero = self.obtener_expresion(expresion.primero)
        segundo = self.obtener_expresion(expresion.segundo)
        if primero and segundo:
            registro = self.obtener_registro_temporal()
            if expresion.operacion == '+':
                self.codigo3d += registro + ' = ' + primero + ' + ' + segundo + ';\n'
                return registro
            elif expresion.operacion == '-':
                self.codigo3d += registro + ' = ' + primero + ' - ' + segundo + ';\n'
                return registro
            elif expresion.operacion == '*':
                self.codigo3d += registro + ' = ' + primero + ' * ' + segundo + ';\n'
                return registro
            elif expresion.operacion == '/':
                self.codigo3d += registro + ' = ' + primero + ' / ' + segundo + ';\n'
                return registro
            elif expresion.operacion == '%':
                self.codigo3d += registro + ' = ' + primero + ' % ' + segundo + ';\n'
                return registro
        return None

    def obtener_expresion_relacional(self, expresion):
        primero = self.obtener_expresion(expresion.primero)
        segundo = self.obtener_expresion(expresion.segundo)
        if primero and segundo:
            registro = self.obtener_registro_temporal()
            if expresion.operacion == '==':
                self.codigo3d += registro + ' = ' + primero + ' == ' + segundo + ';\n'
                return registro
            elif expresion.operacion == '!=':
                self.codigo3d += registro + ' = ' + primero + ' != ' + segundo + ';\n'
                return registro
            elif expresion.operacion == '>':
                self.codigo3d += registro + ' = ' + primero + ' > ' + segundo + ';\n'
                return registro
            elif expresion.operacion == '<':
                self.codigo3d += registro + ' = ' + primero + ' < ' + segundo + ';\n'
                return registro
            elif expresion.operacion == '>=':
                self.codigo3d += registro + ' = ' + primero + ' >= ' + segundo + ";\n"
                return registro
            elif expresion.operacion == '<=':
                self.codigo3d += registro + ' = ' + primero + ' <= ' + segundo + ';\n'
                return registro
        return None

    def obtener_expresion_logica(self, expresion):
        primero = self.obtener_expresion(expresion.primero)
        segundo = self.obtener_expresion(expresion.segundo)
        if primero and segundo:
            registro = self.obtener_registro_temporal()
            if expresion.operacion == '&&':
                self.codigo3d += registro + ' = ' + primero + ' && ' + segundo + ';\n'
                return registro
            elif expresion.operacion == '||':
                self.codigo3d += registro + ' = ' + primero + ' || ' + segundo + ';\n'
                return registro
        return None

    def obtener_expresion_bit(self, expresion):
        primero = self.obtener_expresion(expresion.primero)
        segundo = self.obtener_expresion(expresion.segundo)
        if primero and segundo:
            registro = self.obtener_registro_temporal()
            if expresion.operacion == '<<':
                self.codigo3d += registro + ' = ' + primero + ' << ' + segundo + ';\n'
                return registro
            elif expresion.operacion == '>>':
                self.codigo3d += registro + ' = ' + primero + ' >> ' + segundo + ';\n'
                return registro
            elif expresion.operacion == '&':
                self.codigo3d += registro + ' = ' + primero + ' & ' + segundo + ';\n'
                return registro
            elif expresion.operacion == '|':
                self.codigo3d += registro + ' = ' + primero + ' | ' + segundo + ';\n'
                return registro
            elif expresion.operacion == '^':
                self.codigo3d += registro + ' = ' + primero + ' ^ ' + segundo + ';\n'
                return registro
        return None

    def obtener_expresion_unaria(self, expresion):
        operando = self.obtener_expresion(expresion.operando)
        if operando:
            registro = self.obtener_registro_temporal()
            if expresion.operacion == '-':
                self.codigo3d += registro + ' =  -' + operando + ';\n'
                return registro
            elif expresion.operacion == '!':
                self.codigo3d += registro + ' =  !' + operando + ';\n'
                return registro
            elif expresion.operacion == '~':
                self.codigo3d += registro + ' =  ~' + operando + ';\n'
                return registro
            elif expresion.operacion == '&':
                self.codigo3d += registro + ' =  &' + operando + ';\n'
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
            self.codigo3d += 'if('+expresion+') goto ' + \
                etiqueta_verdadero+';\n'
            self.codigo3d += registro + ' = '+segundo+';\n'
            self.codigo3d += 'goto '+etiqueta_salida+';\n'
            self.codigo3d += etiqueta_verdadero + ':\n'
            self.codigo3d += registro + ' = '+primero+';\n'
            self.codigo3d += etiqueta_salida + ':\n'
            return registro

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
                if isinstance(instrucciones, clases.Etiqueta):
                    self.generar_codigo_etiqueta(instruccion)
                elif isinstance(instruccion, clases.Salto):
                    self.generar_codigo_salto(instruccion)
                elif isinstance(instruccion, clases.Declaracion):
                    self.generar_codigo_declaracion(instruccion)
                elif isinstance(instruccion, clases.Asignacion):
                    self.generar_codigo_asignacion(instruccion)
                if self.detener_ejecucion:
                    break

    def generar_codigo_etiqueta(self, instruccion):
        self.codigo3d += instruccion.identificador + ':\n'

    def generar_codigo_salto(self, instruccion):
        self.codigo3d += 'goto '+instruccion.identificador+';\n'

    def generar_codigo_declaracion(self, instruccion):
        tipo = instruccion.tipo.valor
        for declaracion in instruccion.declaraciones:
            identificador = declaracion.identificador
            if self.obtener_ambito().buscar_simbolo_actual(identificador):
                self.mostrar_mensaje_consola(
                    'ERROR: Variable repetida en línea: '+declaracion.linea+'.')
                self.detener_ejecucion = True
            else:
                if declaracion.indices:
                    pass
                else:
                    self.generar_codigo_declaracion_estandar(
                        tipo, identificador, declaracion)

    def generar_codigo_declaracion_estandar(self, tipo, identificador, declaracion):
        if declaracion.expresion:
            temporal = self.obtener_expresion(
                declaracion.expresion)
            if temporal:
                self.obtener_ambito().agregar_simbolo(
                    Simbolo(tipo, identificador, temporal))
            else:
                self.mostrar_mensaje_consola(
                    'ERROR: Expresión no válida en línea: '+declaracion.linea+'.')
                self.detener_ejecucion = True
        else:
            self.obtener_ambito().agregar_simbolo(
                Simbolo(tipo, identificador, None))

    def generar_codigo_asignacion(self, instruccion):
        if isinstance(instruccion, clases.AsignacionNormal):
            self.generar_codigo_asignacion_normal(instruccion)

    def generar_codigo_asignacion_normal(self, instruccion):
        simbolo = self.existe_variable(instruccion.identificador)
        if simbolo:
            if instruccion.indices:
                pass
            else:
                temporal = self.obtener_expresion(instruccion.expresion)
                if temporal:
                    registro = simbolo.temporal
                    if not registro:
                        registro = self.obtener_registro_temporal()
                    if self.actualizar_temporal_variable(instruccion.identificador, registro):
                        self.codigo3d += registro + ' = '+temporal+';\n'
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
