import clases
from PyQt5 import QtCore, QtGui, QtWidgets


class TresDirecciones:

    def __init__(self, consola, ast):
        self.consola = consola
        self.ast = ast
        self.funciones = {}
        self.codigo3d = 'main:\n'
        self.contador_registros_temporales = 0
        self.contador_etiquetas_temporales = 0
        self.tabla_simbolos = None
        self.etiquetas = []
        self.detener_ejecucion = False

    def generar_codigo(self):
        if self.obtener_funciones():
            if self.existe_main():
                if self.cargar_variables_globales():
                    self.generar_codigo_main()
                    print(self.codigo3d)
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
                tipo = instruccion_global.tipo.valor
                for declaracion in instruccion_global.declaraciones:
                    identificador = declaracion.identificador
                    if declaracion.expresion:
                        temporal = self.obtener_expresion(
                            declaracion.expresion)
                        print('Tipo: '+tipo+' Identificador: ' +
                              identificador+' Temporal: '+temporal)
        return True

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
            pass
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
                self.codigo3d += registro + ' = ' + primero + ' and ' + segundo + ';\n'
                return registro
            elif expresion.operacion == '||':
                self.codigo3d += registro + ' = ' + primero + ' or ' + segundo + ';\n'
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
        self.generar_codigo_instrucciones(principal.cuerpo)
        self.codigo3d += 'exit;\n'

    def generar_codigo_instrucciones(self, instrucciones):
        for instruccion in instrucciones:
            if isinstance(instrucciones, clases.Etiqueta):
                self.generar_codigo_etiqueta(instruccion)
            elif isinstance(instruccion, clases.Salto):
                pass
            if self.detener_ejecucion:
                break

    def generar_codigo_etiqueta(self, instruccion):
        if not instruccion.identificador in self.etiquetas:
            self.codigo3d += instruccion.identificador + ':\n'
            self.etiquetas.append(instruccion.identificador)
        else:
            self.detener_ejecucion = True
            self.mostrar_mensaje_consola('ERROR: Etiqueta repetida.')

    def generar_codigo_salto(self, instruccion):
        pass
