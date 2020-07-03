# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'principal.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

import recursos
import os
import pyperclip
import webbrowser
import tres_direcciones
import sys
import interprete
import time
from PyQt5 import QtCore, QtGui, QtWidgets


class Resaltador(QtGui.QSyntaxHighlighter):

    expresiones = ((r'[0-9]+|\d+\.\d+', QtGui.QColor(178, 202, 164)),
                   (r'[a-zA-Z_][a-zA-Z_0-9]*', QtGui.QColor(212, 212, 212)),
                   (r'\b(auto|struct|break|else|switch|case|enum|register|typedef|extern|return|union|const|continue|for|default|goto|sizeof|volatile|do|if|static|while|printf|scanf|elseif)\b', QtGui.QColor(62, 194, 176)),
                   (r'\b(double|int|long|char|float|short|unsigned|signed|void)\b',
                    QtGui.QColor(75, 156, 208)),
                   (r'\'[^\']*\'|\"[^\"]*\"', QtGui.QColor(201, 143, 120)),
                   (r'/\*.*\*/|//.*', QtGui.QColor(99, 142, 71)))

    def highlightBlock(self, text):
        formato = QtGui.QTextCharFormat()
        for expresion in self.expresiones:
            formato.setForeground(QtGui.QColor(expresion[1]))
            patron = expresion[0]
            expresion_temporal = QtCore.QRegExp(patron)
            indice = expresion_temporal.indexIn(text, 0)
            while indice >= 0:
                longitud = expresion_temporal.matchedLength()
                self.setFormat(indice, longitud, formato)
                indice = expresion_temporal.indexIn(text, indice + longitud)


class Ui_MainWindow(object):

    rutaArchivo = None
    errores_lexicos = []
    errores_sintacticos = []
    generador = None
    instrucciones = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            ":/imagenes/imagenes/icons8-code-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("color: rgb(223, 223, 223);\n"
                                 "background-color: rgb(37, 37, 38);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 30, 781, 331))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet("background-color: rgb(30, 30, 30);")
        self.textEdit.setObjectName("textEdit")
        self.resaltador = Resaltador(self.textEdit.document())
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 390, 781, 161))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(9)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setStyleSheet("background-color: rgb(30, 30, 30);")
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 51, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 370, 51, 16))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setAutoFillBackground(False)
        self.menubar.setStyleSheet("QMenuBar { color: rgb(223, 223, 223); background-color: rgb(60, 60, 60);selection-background-color: rgb(9, 71, 113); }QMenuBar::item { color: rgb(223, 223, 223); background-color: rgb(60, 60, 60);selection-background-color: rgb(9, 71, 113); }QMenuBar::item::selected { color: rgb(223, 223, 223); background-color: rgb(80, 80, 80);selection-background-color: rgb(9, 71, 113); }QMenuBar::item::pressed { color: rgb(223, 223, 223); background-color: rgb(80, 80, 80);selection-background-color: rgb(9, 71, 113); }\n"
                                   "\n"
                                   "")
        self.menubar.setObjectName("menubar")
        self.menuArchivo = QtWidgets.QMenu(self.menubar)
        self.menuArchivo.setStyleSheet("QMenu { color: rgb(223, 223, 223); background-color: rgb(37, 37, 38);selection-background-color: rgb(9, 71, 113); }\n"
                                       "QMenu::item { color: rgb(223, 223, 223); background-color: rgb(37, 37, 38);selection-background-color: rgb(9, 71, 113); }QMenu::item::selected { color: rgb(223, 223, 223);background-color: rgb(37, 37, 38);selection-background-color: rgb(9, 71, 113); }QMenu::item::pressed { color: rgb(223, 223, 223);background-color: rgb(37, 37, 38);selection-background-color: rgb(9, 71, 113); }")
        self.menuArchivo.setObjectName("menuArchivo")
        self.menuEditar = QtWidgets.QMenu(self.menubar)
        self.menuEditar.setStyleSheet("QMenu { color: rgb(223, 223, 223); background-color: rgb(37, 37, 38);selection-background-color: rgb(9, 71, 113); }\n"
                                      "QMenu::item { color: rgb(223, 223, 223); background-color: rgb(37, 37, 38);selection-background-color: rgb(9, 71, 113); }QMenu::item::selected { color: rgb(223, 223, 223);background-color: rgb(37, 37, 38);selection-background-color: rgb(9, 71, 113); }QMenu::item::pressed { color: rgb(223, 223, 223);background-color: rgb(37, 37, 38);selection-background-color: rgb(9, 71, 113); }")
        self.menuEditar.setObjectName("menuEditar")
        self.menuEjecutar = QtWidgets.QMenu(self.menubar)
        self.menuEjecutar.setStyleSheet("QMenu { color: rgb(223, 223, 223); background-color: rgb(37, 37, 38);selection-background-color: rgb(9, 71, 113); }\n"
                                        "QMenu::item { color: rgb(223, 223, 223); background-color: rgb(37, 37, 38);selection-background-color: rgb(9, 71, 113); }QMenu::item::selected { color: rgb(223, 223, 223);background-color: rgb(37, 37, 38);selection-background-color: rgb(9, 71, 113); }QMenu::item::pressed { color: rgb(223, 223, 223);background-color: rgb(37, 37, 38);selection-background-color: rgb(9, 71, 113); }")
        self.menuEjecutar.setObjectName("menuEjecutar")
        self.menuAyuda = QtWidgets.QMenu(self.menubar)
        self.menuAyuda.setStyleSheet("QMenu { color: rgb(223, 223, 223); background-color: rgb(37, 37, 38);selection-background-color: rgb(9, 71, 113); }\n"
                                     "QMenu::item { color: rgb(223, 223, 223); background-color: rgb(37, 37, 38);selection-background-color: rgb(9, 71, 113); }QMenu::item::selected { color: rgb(223, 223, 223);background-color: rgb(37, 37, 38);selection-background-color: rgb(9, 71, 113); }QMenu::item::pressed { color: rgb(223, 223, 223);background-color: rgb(37, 37, 38);selection-background-color: rgb(9, 71, 113); }")
        self.menuAyuda.setObjectName("menuAyuda")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setStyleSheet("color: rgb(223, 223, 223);\n"
                                     "background-color: rgb(0, 122, 204);\n"
                                     "")
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNuevo = QtWidgets.QAction(MainWindow)
        self.actionNuevo.setObjectName("actionNuevo")
        self.actionAbrir = QtWidgets.QAction(MainWindow)
        self.actionAbrir.setObjectName("actionAbrir")
        self.actionGuardar = QtWidgets.QAction(MainWindow)
        self.actionGuardar.setObjectName("actionGuardar")
        self.actionGuardar_como = QtWidgets.QAction(MainWindow)
        self.actionGuardar_como.setObjectName("actionGuardar_como")
        self.actionCerrar = QtWidgets.QAction(MainWindow)
        self.actionCerrar.setObjectName("actionCerrar")
        self.actionSalir = QtWidgets.QAction(MainWindow)
        self.actionSalir.setObjectName("actionSalir")
        self.actionCopiar = QtWidgets.QAction(MainWindow)
        self.actionCopiar.setObjectName("actionCopiar")
        self.actionPegar = QtWidgets.QAction(MainWindow)
        self.actionPegar.setObjectName("actionPegar")
        self.actionCortar = QtWidgets.QAction(MainWindow)
        self.actionCortar.setObjectName("actionCortar")
        self.actionAscendente = QtWidgets.QAction(MainWindow)
        self.actionAscendente.setObjectName("actionAscendente")
        self.actionErrores = QtWidgets.QAction(MainWindow)
        self.actionErrores.setObjectName("actionErrores")
        self.actionSimbolos = QtWidgets.QAction(MainWindow)
        self.actionSimbolos.setObjectName("actionSimbolos")
        self.actionGramatical = QtWidgets.QAction(MainWindow)
        self.actionGramatical.setObjectName("actionGramatical")
        self.actionAcerca_de = QtWidgets.QAction(MainWindow)
        self.actionAcerca_de.setObjectName("actionAcerca_de")
        self.actionAST = QtWidgets.QAction(MainWindow)
        self.actionAST.setObjectName("actionAST")
        self.actionOptimizaciones = QtWidgets.QAction(MainWindow)
        self.actionOptimizaciones.setObjectName("actionOptimizaciones")
        self.menuArchivo.addAction(self.actionNuevo)
        self.menuArchivo.addAction(self.actionAbrir)
        self.menuArchivo.addSeparator()
        self.menuArchivo.addAction(self.actionGuardar)
        self.menuArchivo.addAction(self.actionGuardar_como)
        self.menuArchivo.addSeparator()
        self.menuArchivo.addAction(self.actionCerrar)
        self.menuArchivo.addAction(self.actionSalir)
        self.menuEditar.addAction(self.actionCopiar)
        self.menuEditar.addAction(self.actionPegar)
        self.menuEditar.addAction(self.actionCortar)
        self.menuEjecutar.addAction(self.actionAscendente)
        self.menuEjecutar.addSeparator()
        self.menuEjecutar.addAction(self.actionAST)
        self.menuEjecutar.addAction(self.actionErrores)
        self.menuEjecutar.addAction(self.actionSimbolos)
        self.menuEjecutar.addAction(self.actionGramatical)
        self.menuEjecutar.addAction(self.actionOptimizaciones)
        self.menuAyuda.addAction(self.actionAcerca_de)
        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuEditar.menuAction())
        self.menubar.addAction(self.menuEjecutar.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.actionNuevo.triggered.connect(lambda: self.archivoNuevo())
        self.actionAbrir.triggered.connect(lambda: self.archivoAbrir())
        self.actionGuardar.triggered.connect(lambda: self.archivoGuardar())
        self.actionGuardar_como.triggered.connect(
            lambda: self.archivoGuardarComo())
        self.actionCerrar.triggered.connect(lambda: self.archivoCerrar())
        self.actionSalir.triggered.connect(lambda: self.archivoSalir())
        self.actionCopiar.triggered.connect(lambda: self.editarCopiar())
        self.actionPegar.triggered.connect(lambda: self.editarPegar())
        self.actionCortar.triggered.connect(lambda: self.editarCortar())
        self.actionAscendente.triggered.connect(
            lambda: self.ejecutarAscendente())
        self.actionAST.triggered.connect(lambda: self.ejecutarAST())
        self.actionErrores.triggered.connect(lambda: self.ejecutarErrores())
        self.actionSimbolos.triggered.connect(lambda: self.ejecutarSimbolos())
        self.actionOptimizaciones.triggered.connect(
            lambda: self.ejecutarOptimizaciones())
        self.actionGramatical.triggered.connect(
            lambda: self.ejecutarGramatical())
        self.actionAcerca_de.triggered.connect(lambda: self.ayudaAcercaDe())

        self.textEdit.cursorPositionChanged.connect(
            lambda: self.actualizarLineaColumna())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MinorC IDE"))
        self.plainTextEdit.setPlainText(_translate("MainWindow", "MinorC IDE\n"
                                                   "Copyright (C) Guillermo Peitzner, Todos los derechos reservados.\n"
                                                   ""))
        self.label.setText(_translate("MainWindow", "Untitled-1"))
        self.label_2.setText(_translate("MainWindow", "TERMINAL"))
        self.menuArchivo.setTitle(_translate("MainWindow", "Archivo"))
        self.menuEditar.setTitle(_translate("MainWindow", "Editar"))
        self.menuEjecutar.setTitle(_translate("MainWindow", "Ejecutar"))
        self.menuAyuda.setTitle(_translate("MainWindow", "Ayuda"))
        self.actionNuevo.setText(_translate("MainWindow", "Nuevo"))
        self.actionNuevo.setStatusTip(_translate(
            "MainWindow", "Crea un nuevo archivo"))
        self.actionNuevo.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionAbrir.setText(_translate("MainWindow", "Abrir"))
        self.actionAbrir.setStatusTip(
            _translate("MainWindow", "Abre un archivo"))
        self.actionAbrir.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionGuardar.setText(_translate("MainWindow", "Guardar"))
        self.actionGuardar.setStatusTip(
            _translate("MainWindow", "Guarda el archivo"))
        self.actionGuardar.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionGuardar_como.setText(
            _translate("MainWindow", "Guardar como"))
        self.actionGuardar_como.setStatusTip(_translate(
            "MainWindow", "Guarda el archivo en una ruta"))
        self.actionGuardar_como.setShortcut(
            _translate("MainWindow", "Ctrl+Shift+S"))
        self.actionCerrar.setText(_translate("MainWindow", "Cerrar"))
        self.actionCerrar.setStatusTip(
            _translate("MainWindow", "Cierra el archivo"))
        self.actionCerrar.setShortcut(_translate("MainWindow", "Ctrl+F4"))
        self.actionSalir.setText(_translate("MainWindow", "Salir"))
        self.actionSalir.setStatusTip(
            _translate("MainWindow", "Salir del editor"))
        self.actionCopiar.setText(_translate("MainWindow", "Copiar"))
        self.actionCopiar.setStatusTip(_translate(
            "MainWindow", "Copia el archivo al portapapeles"))
        self.actionCopiar.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionPegar.setText(_translate("MainWindow", "Pegar"))
        self.actionPegar.setStatusTip(_translate(
            "MainWindow", "Pega el portapapeles al archivo"))
        self.actionPegar.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.actionCortar.setText(_translate("MainWindow", "Cortar"))
        self.actionCortar.setStatusTip(_translate(
            "MainWindow", "Corta el archivo al portapapeles"))
        self.actionCortar.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.actionAscendente.setText(_translate("MainWindow", "Ascendente"))
        self.actionAscendente.setStatusTip(_translate(
            "MainWindow", "Ejecuta el archivo de manera ascendente"))
        self.actionAscendente.setShortcut(_translate("MainWindow", "F1"))
        self.actionErrores.setText(_translate("MainWindow", "Errores"))
        self.actionErrores.setStatusTip(_translate(
            "MainWindow", "Reporte de errores léxicos y sintácticos"))
        self.actionErrores.setShortcut(_translate("MainWindow", "F6"))
        self.actionSimbolos.setText(_translate("MainWindow", "Simbolos"))
        self.actionSimbolos.setStatusTip(_translate(
            "MainWindow", "Reporte de la tabla de símbolos"))
        self.actionSimbolos.setShortcut(_translate("MainWindow", "F7"))
        self.actionGramatical.setText(_translate("MainWindow", "Gramatical"))
        self.actionGramatical.setStatusTip(
            _translate("MainWindow", "Reporte gramátical"))
        self.actionGramatical.setShortcut(_translate("MainWindow", "F8"))
        self.actionAcerca_de.setText(_translate("MainWindow", "Acerca de"))
        self.actionAcerca_de.setStatusTip(_translate(
            "MainWindow", "Información del programa"))
        self.actionAST.setText(_translate("MainWindow", "AST"))
        self.actionAST.setStatusTip(_translate("MainWindow", "Reporte de AST"))
        self.actionAST.setShortcut(_translate("MainWindow", "F5"))
        self.actionOptimizaciones.setText(
            _translate("MainWindow", "Optimizaciones"))
        self.actionOptimizaciones.setStatusTip(
            _translate("MainWindow", "Reporte de optimizaciones"))
        self.actionOptimizaciones.setShortcut(_translate("MainWindow", "F9"))

    def archivoNuevo(self):
        self.rutaArchivo = None
        self.errores_lexicos = []
        self.errores_sintacticos = []
        self.generador = None
        self.instrucciones = None
        self.textEdit.setText("")
        self.label.setText("Untitled-1")
        self.plainTextEdit.setPlainText(
            "MinorC IDE\nCopyright (C) Guillermo Peitzner, Todos los derechos reservados.\n")

    def archivoAbrir(self):
        rutaArchivo = QtWidgets.QFileDialog.getOpenFileName()
        if(rutaArchivo[0]):
            with open(rutaArchivo[0], "r") as archivo:
                self.label.setText(str(os.path.basename(archivo.name)))
                self.textEdit.setText(archivo.read())
                self.rutaArchivo = str(rutaArchivo[0])
                self.plainTextEdit.appendPlainText(str(rutaArchivo[0]))

    def archivoGuardar(self):
        if not self.rutaArchivo:
            rutaArchivo = QtWidgets.QFileDialog.getSaveFileName()
            if rutaArchivo[0]:
                self.rutaArchivo = rutaArchivo[0]
        if self.rutaArchivo:
            try:
                archivo = open(self.rutaArchivo, "w")
                archivo.write(self.textEdit.toPlainText())
                archivo.close()
                self.label.setText(str(os.path.basename(archivo.name)))
            except:
                self.rutaArchivo = None
                self.plainTextEdit.appendPlainText(
                    "ERROR: No se pudo guardar el archivo.")

    def archivoGuardarComo(self):
        rutaArchivo = QtWidgets.QFileDialog.getSaveFileName()
        if rutaArchivo[0]:
            self.rutaArchivo = rutaArchivo[0]
            try:
                archivo = open(self.rutaArchivo, "w")
                archivo.write(self.textEdit.toPlainText())
                archivo.close()
                self.label.setText(str(os.path.basename(archivo.name)))
            except:
                self.rutaArchivo = None
                self.plainTextEdit.appendPlainText(
                    "ERROR: No se pudo guardar el archivo.")

    def archivoCerrar(self):
        self.rutaArchivo = None
        self.errores_lexicos = []
        self.errores_sintacticos = []
        self.generador = None
        self.instrucciones = None
        self.textEdit.setText("")
        self.label.setText("Untitled-1")

    def archivoSalir(self):
        sys.exit()

    def editarCopiar(self):
        pyperclip.copy(str(self.textEdit.toPlainText()))

    def editarPegar(self):
        self.textEdit.setText(str(pyperclip.paste()))

    def editarCortar(self):
        pyperclip.copy(str(self.textEdit.toPlainText()))
        self.textEdit.setText("")

    def ejecutarAscendente(self):
        self.erroresLexicos = []
        self.erroresSintacticos = []
        self.generador = None
        self.instrucciones = None
        if self.textEdit.toPlainText():
            self.plainTextEdit.appendPlainText(
                "\n[MINOR.C] ascendente.py "+self.label.text())
            import ascendente as ascendente
            self.instrucciones = ascendente.parse(self.textEdit.toPlainText(
            ), self.erroresLexicos, self.erroresSintacticos, self.plainTextEdit)
            if self.instrucciones:
                self.plainTextEdit.appendPlainText(
                    "[MINOR.C] tres_direcciones.py ascendente.out")
                try:
                    self.generador = tres_direcciones.TresDirecciones(
                        self.plainTextEdit, self.instrucciones)
                    self.generador.generar_codigo()
                    if not self.generador.detener_ejecucion:
                        self.plainTextEdit.appendPlainText(
                            "[AUGUS] ascendente_augus.py tres_direcciones.out")
                        import ascendente_augus as ascendente_augus
                        instrucciones_augus = ascendente_augus.parse(
                            self.generador.codigo3d, [], [], self.plainTextEdit)
                        if instrucciones_augus:
                            self.plainTextEdit.appendPlainText(
                                "[AUGUS] interprete.py ascendente_augus.out\n\n")
                            try:
                                interpretacion_augus = interprete.Interprete(
                                    self.plainTextEdit)
                                interpretacion_augus.procesar(
                                    instrucciones_augus)
                            except Exception as ex:
                                print(ex)
                                self.plainTextEdit.appendPlainText(
                                    "[AUGUS] ERROR: Error de ejecución.")
                except Exception as ex:
                    print(ex)
                    self.plainTextEdit.appendPlainText(
                        "[MINOR.C] ERROR: Error de ejecución.")

    def ejecutarAST(self):
        if self.generador:
            try:
                self.generador.graficar_ast(self.instrucciones)
            except Exception as ex:
                print(ex)
                self.plainTextEdit.appendPlainText(
                    "ERROR: No se pudo generar el reporte.")
        else:
            self.plainTextEdit.appendPlainText(
                "ERROR: Reporte no disponible.")

    def ejecutarErrores(self):
        if len(self.erroresLexicos) > 0 or len(self.erroresSintacticos) > 0:
            archivo = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Errores</title></head><body>'
            if len(self.erroresLexicos) > 0:
                archivo += '<center><h1>Lexicos</h1>'
                archivo += '<table border="1"><tr><th>Token</th><th>Linea</th><th>Columna</th></tr>'
                indiceLexico = 0
                while indiceLexico < len(self.erroresLexicos):
                    archivo += '<tr>'
                    archivo += '<td>' + \
                        str(self.erroresLexicos[indiceLexico].valor) + '</td>'
                    archivo += '<td>' + \
                        str(self.erroresLexicos[indiceLexico].linea) + '</td>'
                    archivo += '<td>' + \
                        str(self.erroresLexicos[indiceLexico].columna) + '</td>'
                    archivo += '</tr>'
                    indiceLexico += 1
                archivo += '</table></center>'
            if len(self.erroresSintacticos) > 0:
                archivo += '<center><h1>Sintacticos</h1>'
                archivo += '<table border="1"><tr><th>Token</th><th>Linea</th><th>Columna</th></tr>'
                indiceSintactico = 0
                while indiceSintactico < len(self.erroresSintacticos):
                    archivo += '<tr>'
                    archivo += '<td>' + \
                        str(self.erroresSintacticos[indiceSintactico].valor) + '</td>'
                    archivo += '<td>' + \
                        str(self.erroresSintacticos[indiceSintactico].linea) + '</td>'
                    archivo += '<td>' + \
                        str(self.erroresSintacticos[indiceSintactico].columna) + '</td>'
                    archivo += '</tr>'
                    indiceSintactico += 1
                archivo += '</table><center>'
            archivo += '</body></html>'
            f = open("errores.html", "w")
            f.write(archivo)
            f.close()
            webbrowser.open('file://'+os.path.realpath("errores.html"))
        else:
            self.plainTextEdit.appendPlainText(
                "ERROR: Reporte no disponible.")

    def ejecutarSimbolos(self):
        if self.generador:
            try:
                archivo = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Simbolos</title></head><body>'
                if self.generador.funciones:
                    archivo += '<center><h1>Funciones</h1>'
                    archivo += '<table border="1"><tr><th>Tipo</th><th>Identificador</th></tr>'
                    for llave in self.generador.funciones.keys():
                        funcion = self.generador.funciones[llave]
                        archivo += '<tr>'
                        archivo += '<td>'+str(funcion.tipo.valor)+'</td>'
                        archivo += '<td>'+str(funcion.identificador)+'</td>'
                        archivo += '</tr>'
                    archivo += '</table><center>'
                if self.generador.simbolos:
                    archivo += '<center><h1>Simbolos</h1>'
                    archivo += '<table border="1"><tr><th>Tipo</th><th>Identificador</th><th>Temporal</th></tr>'
                    for simbolo in self.generador.simbolos:
                        archivo += '<tr>'
                        archivo += '<td>'+str(simbolo.tipo)+'</td>'
                        archivo += '<td>'+str(simbolo.identificador)+'</td>'
                        archivo += '<td>'+str(simbolo.temporal)+'</td>'
                        archivo += '</tr>'
                    archivo += '</table><center>'
                archivo += '</body></html>'
                f = open("simbolos.html", "w")
                f.write(archivo)
                f.close()
                webbrowser.open('file://'+os.path.realpath("simbolos.html"))
            except Exception as ex:
                print(ex)
                self.plainTextEdit.appendPlainText(
                    "ERROR: No se pudo generar el reporte.")
        else:
            self.plainTextEdit.appendPlainText(
                "ERROR: Reporte no disponible.")

    def ejecutarGramatical(self):
        if self.instrucciones:
            webbrowser.open('file://'+os.path.realpath("gramatical.html"))
        else:
            self.plainTextEdit.appendPlainText(
                "ERROR: Reporte no disponible.")

    def ejecutarOptimizaciones(self):
        if self.generador:
            try:
                codigo_3d = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Codigo 3D</title></head><body>'
                codigo_3d += '<p>'+self.generador.codigo3d+'</p>'
                codigo_3d += '</body></html>'
                f = open("codigo_3d.html", "w")
                f.write(codigo_3d)
                f.close()
                webbrowser.open('file://'+os.path.realpath("codigo_3d.html"))
                time.sleep(1)
                codigo_optimizado = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Codigo Optimizado</title></head><body>'
                codigo_optimizado += '<p>'+self.generador.optimizar_codigo()+'</p>'
                codigo_optimizado += '</body></html>'
                f = open("codigo_optimizado.html", "w")
                f.write(codigo_optimizado)
                f.close()
                webbrowser.open(
                    'file://'+os.path.realpath("codigo_optimizado.html"))
                time.sleep(1)
                if self.generador.optimizaciones:
                    archivo = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Optimizaciones</title></head><body>'
                    archivo += '<center><h1>Optimizaciones</h1>'
                    archivo += '<table border="1"><tr><th>Regla</th><th>Antes</th><th>Despues</th></tr>'
                    for optimizacion in self.generador.optimizaciones:
                        archivo += '<tr>'
                        archivo += '<td>'+str(optimizacion.regla)+'</td>'
                        archivo += '<td>'+str(optimizacion.antes)+'</td>'
                        archivo += '<td>'+str(optimizacion.despues)+'</td>'
                        archivo += '</tr>'
                    archivo += '</table><center>'
                    archivo += '</body></html>'
                    f = open("optimizaciones.html", "w")
                    f.write(archivo)
                    f.close()
                    webbrowser.open(
                        'file://'+os.path.realpath("optimizaciones.html"))
            except Exception as ex:
                print(ex)
                self.plainTextEdit.appendPlainText(
                    "ERROR: No se pudo generar el reporte.")
        else:
            self.plainTextEdit.appendPlainText(
                "ERROR: Reporte no disponible.")

    def ayudaAcercaDe(self):
        self.plainTextEdit.appendPlainText(
            "https://github.com/gpeitzner/OLC2_Proyecto2")

    def actualizarLineaColumna(self):
        cursorTemporal = self.textEdit.textCursor()
        self.statusbar.showMessage(
            "Ln "+str(cursorTemporal.blockNumber() + 1)+", Col "+str(cursorTemporal.columnNumber() + 1) + "     UTF-8     CRLF     MinorC")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
