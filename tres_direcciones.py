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

    def generar_codigo(self):
        if self.obtener_funciones():
            if self.existe_main():
                self.cargar_variables_globales()
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
                tipo = instruccion_global.tipo
                for declaracion in instruccion_global.declaraciones:
                    identificador = declaracion.identificador
                    print(str(tipo.valor)+' '+str(identificador))
                    print(self.obtener_expresion(declaracion.expresion))
                    print(self.codigo3d)

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
        return None

    def obtener_expresion_aritmetica(self, expresion):
        primero = self.obtener_expresion(expresion.primero)
        segundo = self.obtener_expresion(expresion.segundo)
        if primero and segundo:
            registro = self.obtener_registro_temporal()
            if expresion.operacion == '+':
                self.codigo3d += registro + ' = ' + primero.valor + ' + ' + segundo.valor + ';\n'
                if primero.tipo == 'char' and segundo.tipo == 'char':
                    return clases.Variable('char', registro)
                elif primero.tipo == 'float' and segundo.tipo == 'float':
                    return clases.Variable('float', registro)
                elif primero.tipo == 'double' and segundo.tipo == 'double':
                    return clases.Variable('double', registro)
                elif primero.tipo in ['int', 'float', 'double'] and segundo.tipo in ['int', 'float', 'double']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '-':
                self.codigo3d += registro + ' = ' + primero.valor + ' - ' + segundo.valor + ';\n'
                if primero.tipo == 'float' and segundo.tipo == 'float':
                    return clases.Variable('float', registro)
                elif primero.tipo == 'double' and segundo.tipo == 'double':
                    return clases.Variable('double', registro)
                elif primero.tipo in ['int', 'float', 'double'] and segundo.tipo in ['int', 'float', 'double']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '*':
                self.codigo3d += registro + ' = ' + primero.valor + ' * ' + segundo.valor + ';\n'
                if primero.tipo == 'float' and segundo.tipo == 'float':
                    return clases.Variable('float', registro)
                elif primero.tipo == 'double' and segundo.tipo == 'double':
                    return clases.Variable('double', registro)
                elif primero.tipo in ['int', 'float', 'double'] and segundo.tipo in ['int', 'float', 'double']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '/':
                if segundo.valor != '0':
                    self.codigo3d += registro + ' = ' + primero.valor + ' / ' + segundo.valor + ';\n'
                    if primero.tipo == 'float' and segundo.tipo == 'float':
                        return clases.Variable('float', registro)
                    elif primero.tipo == 'double' and segundo.tipo == 'double':
                        return clases.Variable('double', registro)
                    elif primero.tipo in ['int', 'float', 'double'] and segundo.tipo in ['int', 'float', 'double']:
                        return clases.Variable('int', registro)
                    else:
                        return None
                else:
                    return None
            elif expresion.operacion == '%':
                if segundo.valor != '0':
                    self.codigo3d += registro + ' = ' + primero.valor + ' % ' + segundo.valor + ';\n'
                    if primero.tipo == 'float' and segundo.tipo == 'float':
                        return clases.Variable('float', registro)
                    elif primero.tipo == 'double' and segundo.tipo == 'double':
                        return clases.Variable('double', registro)
                    elif primero.tipo in ['int', 'float', 'double'] and segundo.tipo in ['int', 'float', 'double']:
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
                if primero.tipo == 'char' and segundo.tipo == 'char':
                    return clases.Variable('char', registro)
                elif primero.tipo in ['int', 'float', 'double'] and segundo.tipo in ['int', 'float', 'double']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '!=':
                self.codigo3d += registro + ' = ' + primero.valor + ' != ' + segundo.valor + ';\n'
                if primero.tipo == 'char' and segundo.tipo == 'char':
                    return clases.Variable('char', registro)
                elif primero.tipo in ['int', 'float', 'double'] and segundo.tipo in ['int', 'float', 'double']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '>':
                self.codigo3d += registro + ' = ' + primero.valor + ' > ' + segundo.valor + ';\n'
                if primero.tipo in ['int', 'float', 'double'] and segundo.tipo in ['int', 'float', 'double']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '<':
                self.codigo3d += registro + ' = ' + primero.valor + ' < ' + segundo.valor + ';\n'
                if primero.tipo in ['int', 'float', 'double'] and segundo.tipo in ['int', 'float', 'double']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '>=':
                self.codigo3d += registro + ' = ' + primero.valor + ' >= ' + segundo.valor + ";\n"
                if primero.tipo in ['int', 'float', 'double'] and segundo.tipo in ['int', 'float', 'double']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '<=':
                self.codigo3d += registro + ' = ' + primero.valor + ' <= ' + segundo.valor + ';\n'
                if primero.tipo in ['int', 'float', 'double'] and segundo.tipo in ['int', 'float', 'double']:
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
                if primero.tipo == 'int' and segundo.tipo == 'int':
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '||':
                self.codigo3d += registro + ' = ' + primero.valor + ' or ' + segundo.valor + ';\n'
                if primero.tipo == 'int' and segundo.tipo == 'int':
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
                if primero.tipo in ['int', 'double', 'float'] and segundo.tipo in ['int', 'double', 'float']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '>>':
                self.codigo3d += registro + ' = ' + primero.valor + ' >> ' + segundo.valor + ';\n'
                if primero.tipo in ['int', 'double', 'float'] and segundo.tipo in ['int', 'double', 'float']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '&':
                self.codigo3d += registro + ' = ' + primero.valor + ' & ' + segundo.valor + ';\n'
                if primero.tipo in ['int', 'double', 'float'] and segundo.tipo in ['int', 'double', 'float']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '|':
                self.codigo3d += registro + ' = ' + primero.valor + ' | ' + segundo.valor + ';\n'
                if primero.tipo in ['int', 'double', 'float'] and segundo.tipo in ['int', 'double', 'float']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '^':
                self.codigo3d += registro + ' = ' + primero.valor + ' ^ ' + segundo.valor + ';\n'
                if primero.tipo in ['int', 'double', 'float'] and segundo.tipo in ['int', 'double', 'float']:
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
                if operando.tipo in ['int', 'double', 'float'] and operando.tipo in ['int', 'double', 'float']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '!':
                self.codigo3d += registro + ' =  !' + operando + ';\n'
                if operando.tipo in ['int', 'double', 'float'] and operando.tipo in ['int', 'double', 'float']:
                    return clases.Variable('int', registro)
                else:
                    return None
            elif expresion.operacion == '~':
                self.codigo3d += registro + ' =  ~' + operando + ';\n'
                if operando.tipo in ['int', 'double', 'float'] and operando.tipo in ['int', 'double', 'float']:
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
