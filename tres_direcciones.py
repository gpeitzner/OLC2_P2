import clases
from PyQt5 import QtCore, QtGui, QtWidgets


class Simbolo:
    def __init__(self, tipo, identificador, temporal):
        self.tipo = tipo
        self.identificador = identificador
        self.temporal = temporal


class TablaSimbolos:
    def __init__(self, ambito):
        self.ambito = ambito
        self.simbolos = {}

    def existe(self, identificador):
        if identificador in self.simbolos.keys():
            return True
        return False

    def obtener_temporal(self, identificador):
        if identificador in self.simbolos.keys():
            return self.simbolos[identificador]
        return None

    def actualizar(self, simbolo):
        self.simbolos[simbolo.identificador] = simbolo

    def obtener_ambito(self):
        return self.ambito


class TresDirecciones:

    def __init__(self, consola, ast):
        self.consola = consola
        self.ast = ast
        self.funciones = {}
        self.codigo3d = 'main:\n'
        self.contador_registros_temporales = 0
        self.contador_etiquetas_temporales = 0
        self.tabla_simbolos = [TablaSimbolos(0)]

    def generar_codigo(self):
        if self.obtener_funciones():
            if self.existe_main():
                if self.cargar_variables_globales():
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
                        variable = self.obtener_expresion(
                            declaracion.expresion)
                        if variable:
                            if variable.tipo == tipo or variable.tipo == 'ternary' or variable.tipo == 'scanf':
                                if not self.tabla_simbolos[0].existe(identificador):
                                    self.tabla_simbolos[0].actualizar(
                                        Simbolo(tipo, identificador, variable.valor))
                                else:
                                    self.mostrar_mensaje_consola(
                                        'ERROR: Ya existe la variable global en línea: '+str(declaracion.linea))
                                    return False
                            else:
                                self.mostrar_mensaje_consola(
                                    "ERROR: Tipo de expresión no válida en línea: "+str(declaracion.linea))
                                return False
                        else:
                            self.mostrar_mensaje_consola(
                                'ERROR: Expresión no válida en línea: '+str(declaracion.linea))
                            return False
                    else:
                        if not self.tabla_simbolos[0].existe(identificador):
                            self.tabla_simbolos[0].actualizar(
                                Simbolo(tipo, identificador, None))
                        else:
                            self.mostrar_mensaje_consola(
                                'ERROR: Ya existe la variable global en línea: '+str(declaracion.linea))
                            return False
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
            return clases.Variable('int', str(expresion.valor))
        if isinstance(expresion, (clases.Cadena, clases.Caracter)):
            return clases.Variable('char', str(expresion.valor))
        if isinstance(expresion, clases.Decimal):
            return clases.Variable('float', str(expresion.valor))
        if isinstance(expresion, clases.Identificador):
            if self.tabla_simbolos[0].existe(expresion.valor):
                simbolo = self.tabla_simbolos[0].obtener_temporal(
                    expresion.valor)
                if simbolo.temporal:
                    return clases.Variable(simbolo.tipo, simbolo.temporal)
                else:
                    return None
            else:
                return None
        if isinstance(expresion, clases.ExpresionScan):
            registro = self.obtener_registro_temporal()
            self.codigo3d += registro + ' = read();\n'
            return clases.Variable('scanf', registro)
        return None

    def obtener_expresion_aritmetica(self, expresion):
        primero = self.obtener_expresion(expresion.primero)
        segundo = self.obtener_expresion(expresion.segundo)
        if primero and segundo:
            registro = self.obtener_registro_temporal()
            if expresion.operacion == '+':
                self.codigo3d += registro + ' = ' + primero.valor + ' + ' + segundo.valor + ';\n'
                if primero.tipo in ['char', 'scanf', 'ternary'] and segundo.tipo in ['char', 'scanf', 'ternary']:
                    return clases.Variable('char', registro)
                elif primero.tipo in ['float', 'scanf', 'ternary'] and segundo.tipo in ['float', 'scanf', 'ternary']:
                    return clases.Variable('float', registro)
                elif primero.tipo in ['double', 'scanf', 'ternary'] and segundo.tipo in ['double', 'scanf', 'ternary']:
                    return clases.Variable('double', registro)
                elif primero.tipo in ['int', 'float', 'double', 'scanf', 'ternary'] and segundo.tipo in ['int', 'float', 'double', 'scanf', 'ternary']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '-':
                self.codigo3d += registro + ' = ' + primero.valor + ' - ' + segundo.valor + ';\n'
                if primero.tipo in ['float', 'scanf', 'ternary'] and segundo.tipo in ['float', 'scanf', 'ternary']:
                    return clases.Variable('float', registro)
                elif primero.tipo in ['double', 'scanf', 'ternary'] and segundo.tipo in ['double', 'scanf', 'ternary']:
                    return clases.Variable('double', registro)
                elif primero.tipo in ['int', 'float', 'double', 'scanf', 'ternary'] and segundo.tipo in ['int', 'float', 'double', 'scanf', 'ternary']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '*':
                self.codigo3d += registro + ' = ' + primero.valor + ' * ' + segundo.valor + ';\n'
                if primero.tipo in ['float', 'scanf', 'ternary'] and segundo.tipo in ['float', 'scanf', 'ternary']:
                    return clases.Variable('float', registro)
                elif primero.tipo in ['double', 'scanf', 'ternary'] and segundo.tipo in ['double', 'scanf', 'ternary']:
                    return clases.Variable('double', registro)
                elif primero.tipo in ['int', 'float', 'double', 'scanf', 'ternary'] and segundo.tipo in ['int', 'float', 'double', 'scanf', 'ternary']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '/':
                if segundo.valor != '0':
                    self.codigo3d += registro + ' = ' + primero.valor + ' / ' + segundo.valor + ';\n'
                    if primero.tipo in ['float', 'scanf', 'ternary'] and segundo.tipo in ['float', 'scanf', 'ternary']:
                        return clases.Variable('float', registro)
                    elif primero.tipo in ['double', 'scanf', 'ternary'] and segundo.tipo == ['double', 'scanf', 'ternary']:
                        return clases.Variable('double', registro)
                    elif primero.tipo in ['int', 'float', 'double', 'scanf', 'ternary'] and segundo.tipo in ['int', 'float', 'double', 'scanf', 'ternary']:
                        return clases.Variable('int', registro)
                    else:
                        return None
                else:
                    return None
            elif expresion.operacion == '%':
                if segundo.valor != '0':
                    self.codigo3d += registro + ' = ' + primero.valor + ' % ' + segundo.valor + ';\n'
                    if primero.tipo in ['float', 'scanf', 'ternary'] and segundo.tipo in ['float', 'scanf', 'ternary']:
                        return clases.Variable('float', registro)
                    elif primero.tipo in ['double', 'scanf', 'ternary'] and segundo.tipo in ['double', 'scanf', 'ternary']:
                        return clases.Variable('double', registro)
                    elif primero.tipo in ['int', 'float', 'double', 'scanf', 'ternary'] and segundo.tipo in ['int', 'float', 'double', 'scanf', 'ternary']:
                        return clases.Variable('int', registro)
                    else:
                        return None
                else:
                    return None
        return None

    def obtener_expresion_relacional(self, expresion):
        primero = self.obtener_expresion(expresion.primero)
        segundo = self.obtener_expresion(expresion.segundo)
        if primero and segundo:
            registro = self.obtener_registro_temporal()
            if expresion.operacion == '==':
                self.codigo3d += registro + ' = ' + primero.valor + ' == ' + segundo.valor + ';\n'
                if primero.tipo in ['char', 'scanf', 'ternary'] and segundo.tipo in ['char', 'scanf', 'ternary']:
                    return clases.Variable('char', registro)
                elif primero.tipo in ['int', 'float', 'double', 'scanf', 'ternary'] and segundo.tipo in ['int', 'float', 'double', 'scanf', 'ternary']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '!=':
                self.codigo3d += registro + ' = ' + primero.valor + ' != ' + segundo.valor + ';\n'
                if primero.tipo in ['char', 'scanf', 'ternary'] and segundo.tipo in ['char', 'scanf', 'ternary']:
                    return clases.Variable('char', registro)
                elif primero.tipo in ['int', 'float', 'double', 'scanf', 'ternary'] and segundo.tipo in ['int', 'float', 'double', 'scanf', 'ternary']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '>':
                self.codigo3d += registro + ' = ' + primero.valor + ' > ' + segundo.valor + ';\n'
                if primero.tipo in ['int', 'float', 'double', 'scanf', 'ternary'] and segundo.tipo in ['int', 'float', 'double', 'scanf', 'ternary']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '<':
                self.codigo3d += registro + ' = ' + primero.valor + ' < ' + segundo.valor + ';\n'
                if primero.tipo in ['int', 'float', 'double', 'scanf', 'ternary'] and segundo.tipo in ['int', 'float', 'double', 'scanf', 'ternary']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '>=':
                self.codigo3d += registro + ' = ' + primero.valor + ' >= ' + segundo.valor + ";\n"
                if primero.tipo in ['int', 'float', 'double', 'scanf', 'ternary'] and segundo.tipo in ['int', 'float', 'double', 'scanf', 'ternary']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '<=':
                self.codigo3d += registro + ' = ' + primero.valor + ' <= ' + segundo.valor + ';\n'
                if primero.tipo in ['int', 'float', 'double', 'scanf', 'ternary'] and segundo.tipo in ['int', 'float', 'double', 'scanf', 'ternary']:
                    return clases.Variable('int', registro)
                else:
                    return None
        return None

    def obtener_expresion_logica(self, expresion):
        primero = self.obtener_expresion(expresion.primero)
        segundo = self.obtener_expresion(expresion.segundo)
        if primero and segundo:
            registro = self.obtener_registro_temporal()
            if expresion.operacion == '&&':
                self.codigo3d += registro + ' = ' + \
                    primero.valor + ' and ' + segundo.valor + ';\n'
                if primero.tipo in ['int', 'scanf', 'ternary'] and segundo.tipo in ['int', 'scanf', 'ternary']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '||':
                self.codigo3d += registro + ' = ' + primero.valor + ' or ' + segundo.valor + ';\n'
                if primero.tipo in ['int', 'scanf', 'ternary'] and segundo.tipo in ['int', 'scanf', 'ternary']:
                    return clases.Variable('int', registro)
                else:
                    return None
        return None

    def obtener_expresion_bit(self, expresion):
        primero = self.obtener_expresion(expresion.primero)
        segundo = self.obtener_expresion(expresion.segundo)
        if primero and segundo:
            registro = self.obtener_registro_temporal()
            if expresion.operacion == '<<':
                self.codigo3d += registro + ' = ' + primero.valor + ' << ' + segundo.valor + ';\n'
                if primero.tipo in ['int', 'double', 'float', 'scanf', 'ternary'] and segundo.tipo in ['int', 'double', 'float', 'scanf', 'ternary']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '>>':
                self.codigo3d += registro + ' = ' + primero.valor + ' >> ' + segundo.valor + ';\n'
                if primero.tipo in ['int', 'double', 'float', 'scanf', 'ternary'] and segundo.tipo in ['int', 'double', 'float', 'scanf', 'ternary']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '&':
                self.codigo3d += registro + ' = ' + primero.valor + ' & ' + segundo.valor + ';\n'
                if primero.tipo in ['int', 'double', 'float', 'scanf', 'ternary'] and segundo.tipo in ['int', 'double', 'float', 'scanf', 'ternary']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '|':
                self.codigo3d += registro + ' = ' + primero.valor + ' | ' + segundo.valor + ';\n'
                if primero.tipo in ['int', 'double', 'float', 'scanf', 'ternary'] and segundo.tipo in ['int', 'double', 'float', 'scanf', 'ternary']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '^':
                self.codigo3d += registro + ' = ' + primero.valor + ' ^ ' + segundo.valor + ';\n'
                if primero.tipo in ['int', 'double', 'float', 'scanf', 'ternary'] and segundo.tipo in ['int', 'double', 'float', 'scanf', 'ternary']:
                    return clases.Variable('int', registro)
                else:
                    return None
        return None

    def obtener_expresion_unaria(self, expresion):
        operando = self.obtener_expresion(expresion.operando)
        if operando:
            registro = self.obtener_registro_temporal()
            if expresion.operacion == '-':
                self.codigo3d += registro + ' =  -' + operando + ';\n'
                if operando.tipo in ['int', 'double', 'float', 'scanf', 'ternary'] and operando.tipo in ['int', 'double', 'float', 'scanf', 'ternary']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '!':
                self.codigo3d += registro + ' =  !' + operando + ';\n'
                if operando.tipo in ['int', 'double', 'float', 'scanf', 'ternary'] and operando.tipo in ['int', 'double', 'float', 'scanf', 'ternary']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '~':
                self.codigo3d += registro + ' =  ~' + operando + ';\n'
                if operando.tipo in ['int', 'double', 'float', 'scanf', 'ternary'] and operando.tipo in ['int', 'double', 'float', 'scanf', 'ternary']:
                    return clases.Variable('int', registro)
                else:
                    return None
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
            self.codigo3d += 'if('+expresion.valor+') goto ' + \
                etiqueta_verdadero+';\n'
            self.codigo3d += registro + ' = '+segundo.valor+';\n'
            self.codigo3d += 'goto '+etiqueta_salida+';\n'
            self.codigo3d += etiqueta_verdadero + ':\n'
            self.codigo3d += registro + ' = '+primero.valor+';\n'
            self.codigo3d += etiqueta_salida + ':\n'
            return clases.Variable('ternary', registro)

    def obtener_registro_temporal(self):
        registro_temporal = '$t' + str(self.contador_registros_temporales)
        self.contador_registros_temporales += 1
        return registro_temporal

    def obtener_etiqueta_temporal(self):
        etiqueta_temporal = 'm_c_e' + \
            str(self.contador_etiquetas_temporales)
        self.contador_etiquetas_temporales += 1
        return etiqueta_temporal
