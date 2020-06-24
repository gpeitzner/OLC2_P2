class _Error:
    def __init__(self, valor, linea, columna):
        self.valor = valor
        self.linea = linea
        self.columna = columna


class Declaracion:
    def __init__(self, tipo, declaraciones):
        self.tipo = tipo
        self.declaraciones = declaraciones


class DeclaracionFinal:
    def __init__(self, identificador, indices, expresion, linea):
        self.identificador = identificador
        self.indices = indices
        self.expresion = expresion
        self.linea = linea


class Estructura:
    def __init__(self, identificador, caracteristicas, linea):
        self.identificador = identificador
        self.caracteristicas = caracteristicas
        self.linea = linea


class Funcion:
    def __init__(self, tipo, identificador, parametros, cuerpo):
        self.tipo = tipo
        self.identificador = identificador
        self.parametros = parametros
        self.cuerpo = cuerpo


class Parametro:
    def __init__(self, tipo, modo, identificador):
        self.tipo = tipo
        self.modo = modo
        self.identificador = identificador


class Metodo:
    def __init__(self, identificador, expresiones, linea):
        self.identificador = identificador
        self.expresiones = expresiones
        self.linea = linea


class Etiqueta:
    def __init__(self, identificador, linea):
        self.identificador = identificador
        self.linea = linea


class Salto:
    def __init__(self, identificador, linea):
        self.identificador = identificador
        self.linea = linea


class Asignacion:
    'Asignacion'


class AsignacionNormal(Asignacion):
    def __init__(self, identificador, indices, compuesto, expresion, linea):
        self.identificador = identificador
        self.indices = indices
        self.compuesto = compuesto
        self.expresion = expresion
        self.linea = linea


class AsignacionEstructura(Asignacion):
    def __init__(self, identificador, indices, atributo, compuesto, expresion, linea):
        self.identificador = identificador
        self.indices = indices
        self.atributo = atributo
        self.compuesto = compuesto
        self.expresion = expresion
        self.linea = linea


class AsignacionAumento(Asignacion):
    def __init__(self, identificador, linea):
        self.identificador = identificador
        self.linea = linea


class AsignacionDecremento(Asignacion):
    def __init__(self, identificador, linea):
        self.identificador = identificador
        self.linea = linea


class _If:
    def __init__(self, expresion, cuerpo, elseifs, _else, linea):
        self.expresion = expresion
        self.cuerpo = cuerpo
        self.elseifs = elseifs
        self._else = _else
        self.linea = linea


class _ElseIf:
    def __init__(self, expresion, cuerpo):
        self.expresion = expresion
        self.cuerpo = cuerpo


class _Else:
    def __init__(self, cuerpo):
        self.cuerpo = cuerpo


class _Switch:
    def __init__(self, expresion, cases, defecto, linea):
        self.expresion = expresion
        self.cases = cases
        self.defecto = defecto
        self.linea = linea


class _Case:
    def __init__(self, expresion, cuerpo):
        self.expresion = expresion
        self.cuerpo = cuerpo


class _DefaultCase:
    def __init__(self, cuerpo):
        self.cuerpo = cuerpo


class _While:
    def __init__(self, expresion, cuerpo, linea):
        self.expresion = expresion
        self.cuerpo = cuerpo
        self.linea = linea


class _Do:
    def __init__(self, cuerpo, expresion, linea):
        self.cuerpo = cuerpo
        self.expresion = expresion
        self.linea = linea


class _For:
    def __init__(self, declaracion, expresion, asignacion, cuerpo, linea):
        self.declaracion = declaracion
        self.expresion = expresion
        self.asignacion = asignacion
        self.cuerpo = cuerpo
        self.linea = linea


class Expresion:
    'Expresion'


class ExpresionAritmetica(Expresion):
    def __init__(self, primero, operacion, segundo):
        self.primero = primero
        self.operacion = operacion
        self.segundo = segundo


class ExpresionRelacional(Expresion):
    def __init__(self, primero, operacion, segundo):
        self.primero = primero
        self.operacion = operacion
        self.segundo = segundo


class ExpresionLogica(Expresion):
    def __init__(self, primero, operacion, segundo):
        self.primero = primero
        self.operacion = operacion
        self.segundo = segundo


class ExpresionBit(Expresion):
    def __init__(self, primero, operacion, segundo):
        self.primero = primero
        self.operacion = operacion
        self.segundo = segundo


class ExpresionTernaria(Expresion):
    def __init__(self, expresion, primero, segundo):
        self.expresion = expresion
        self.primero = primero
        self.segundo = segundo


class ExpresionUnaria(Expresion):
    def __init__(self, operacion, operando):
        self.operacion = operacion
        self.operando = operando


class ExpresionEstructura(Expresion):
    def __init__(self, identificador, atributo):
        self.identificador = identificador
        self.atributo = atributo


class ExpresionIdentificadorArreglo(Expresion):
    def __init__(self, identificador, accesos):
        self.identificador = identificador
        self.accesos = accesos


class ExpresionArregloEstructura(Expresion):
    def __init__(self, identificador, accesos, atributo):
        self.identificador = identificador
        self.accesos = accesos
        self.atributo = atributo


class ExpresionElementos(Expresion):
    def __init__(self, expresiones):
        self.expresiones = expresiones


class _SizeOf(Expresion):
    def __init__(self, tipo):
        self.tipo = tipo


class Valor:
    'Valor'


class Caracter(Valor):
    def __init__(self, valor):
        self.valor = valor


class Cadena(Valor):
    def __init__(self, valor):
        self.valor = valor


class Entero(Valor):
    def __init__(self, valor):
        self.valor = valor


class Decimal(Valor):
    def __init__(self, valor):
        self.valor = valor


class Identificador(Valor):
    def __init__(self, valor):
        self.valor = valor


class Tipo:
    def __init__(self, valor, identificador):
        self.valor = valor
        self.identificador = identificador


class _Continue:
    def __init__(self, linea):
        self.linea = linea


class _Break:
    def __init__(self, linea):
        self.linea = linea


class _Return:
    def __init__(self, expresion, linea):
        self.expresion = expresion
        self.linea = linea
