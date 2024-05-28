import sys
import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QTextEdit, QFileDialog
from PyQt6.QtCore import Qt

class Nodo:
    def __init__(self, id, nombre, apellido, carrera):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.carrera = carrera
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class AVLarbol:
    def __init__(self):
        self.raiz = None

    def obtener_altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def obtener_balance(self, nodo):
        if not nodo:
            return 0
        return self.obtener_altura(nodo.izquierda) - self.obtener_altura(nodo.derecha)

    def rotacion_derecha(self, z):
        y = z.izquierda
        T3 = y.derecha

        y.derecha = z
        z.izquierda = T3

        z.altura = 1 + max(self.obtener_altura(z.izquierda), self.obtener_altura(z.derecha))
        y.altura = 1 + max(self.obtener_altura(y.izquierda), self.obtener_altura(y.derecha))

        return y

    def rotacion_izquierda(self, z):
        y = z.derecha
        T2 = y.izquierda

        y.izquierda = z
        z.derecha = T2

        z.altura = 1 + max(self.obtener_altura(z.izquierda), self.obtener_altura(z.derecha))
        y.altura = 1 + max(self.obtener_altura(y.izquierda), self.obtener_altura(y.derecha))

        return y

    def insertar(self, nodo, id, nombre, apellido, carrera):
        if not nodo:
            return Nodo(id, nombre, apellido, carrera)
        elif id < nodo.id:
            nodo.izquierda = self.insertar(nodo.izquierda, id, nombre, apellido, carrera)
        else:
            nodo.derecha = self.insertar(nodo.derecha, id, nombre, apellido, carrera)

        nodo.altura = 1 + max(self.obtener_altura(nodo.izquierda), self.obtener_altura(nodo.derecha))
        balance = self.obtener_balance(nodo)

        # Verificar balance y realizar rotaciones si es necesario
        if balance > 1:
            if id < nodo.izquierda.id:
                return self.rotacion_derecha(nodo)
            else:
                nodo.izquierda = self.rotacion_izquierda(nodo.izquierda)
                return self.rotacion_derecha(nodo)
        if balance < -1:
            if id > nodo.derecha.id:
                return self.rotacion_izquierda(nodo)
            else:
                nodo.derecha = self.rotacion_derecha(nodo.derecha)
                return self.rotacion_izquierda(nodo)

        return nodo

    def eliminar(self, nodo, id):
        if not nodo:
            return nodo

        if id < nodo.id:
            nodo.izquierda = self.eliminar(nodo.izquierda, id)
        elif id > nodo.id:
            nodo.derecha = self.eliminar(nodo.derecha, id)
        else:
            if not nodo.izquierda:
                return nodo.derecha
            elif not nodo.derecha:
                return nodo.izquierda

            temp = self.obtener_minimo(nodo.derecha)
            nodo.id = temp.id
            nodo.nombre = temp.nombre
            nodo.apellido = temp.apellido
            nodo.carrera = temp.carrera
            nodo.derecha = self.eliminar(nodo.derecha, temp.id)

        nodo.altura = 1 + max(self.obtener_altura(nodo.izquierda), self.obtener_altura(nodo.derecha))
        balance = self.obtener_balance(nodo)

        # Verificar balance y realizar rotaciones si es necesario
        if balance > 1:
            if self.obtener_balance(nodo.izquierda) >= 0:
                return self.rotacion_derecha(nodo)
            else:
                nodo.izquierda = self.rotacion_izquierda(nodo.izquierda)
                return self.rotacion_derecha(nodo)
        if balance < -1:
            if self.obtener_balance(nodo.derecha) <= 0:
                return self.rotacion_izquierda(nodo)
            else:
                nodo.derecha = self.rotacion_derecha(nodo.derecha)
                return self.rotacion_izquierda(nodo)

        return nodo

    def obtener_minimo(self, nodo):
        if nodo is None or nodo.izquierda is None:
            return nodo
        return self.obtener_minimo(nodo.izquierda)

    def agregar_estudiante(self, id, nombre, apellido, carrera):
        self.raiz = self.insertar(self.raiz, id, nombre, apellido, carrera)

    def eliminar_estudiante(self, id):
        self.raiz = self.eliminar(self.raiz, id)

    def buscar_estudiante(self, id):
        return self.buscar(self.raiz, id)

    def buscar(self, nodo, id):
        if nodo is None or nodo.id == id:
            return nodo
        if id < nodo.id:
            return self.buscar(nodo.izquierda, id)
        return self.buscar(nodo.derecha, id)

    def listar_estudiantes(self):
        estudiantes = []
        self.inorden(self.raiz, estudiantes)
        return estudiantes

    def inorden(self, nodo, estudiantes):
        if not nodo:
            return
        self.inorden(nodo.izquierda, estudiantes)
        estudiantes.append((nodo.id, nodo.nombre, nodo.apellido, nodo.carrera))
        self.inorden(nodo.derecha, estudiantes)

class AVLWindow2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.arbol = AVLarbol()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Gestión de Estudiantes AVL")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("ID")
        layout.addWidget(self.input_id)

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre")
        layout.addWidget(self.input_nombre)

        self.input_apellido = QLineEdit()
        self.input_apellido.setPlaceholderText("Apellido")
        layout.addWidget(self.input_apellido)

        self.input_carrera = QLineEdit()
        self.input_carrera.setPlaceholderText("Carrera")
        layout.addWidget(self.input_carrera)

        self.insert_button = QPushButton("Agregar Estudiante")
        self.insert_button.clicked.connect(self.agregar_estudiante)
        layout.addWidget(self.insert_button)

        self.delete_button = QPushButton("Eliminar Estudiante")
        self.delete_button.clicked.connect(self.eliminar_estudiante)
        layout.addWidget(self.delete_button)

        self.search_button = QPushButton("Buscar Estudiante")
        self.search_button.clicked.connect(self.buscar_estudiante)
        layout.addWidget(self.search_button)

        self.list_button = QPushButton("Listar Estudiantes")
        self.list_button.clicked.connect(self.listar_estudiantes)
        layout.addWidget(self.list_button)

        self.export_button = QPushButton("Exportar Estudiantes a CSV")
        self.export_button.clicked.connect(self.exportar_estudiantes)
        layout.addWidget(self.export_button)

        self.message_label = QLabel("")
        layout.addWidget(self.message_label)

        self.list_text = QTextEdit()
        self.list_text.setReadOnly(True)
        layout.addWidget(self.list_text)

    def agregar_estudiante(self):
        try:
            id = int(self.input_id.text())
            nombre = self.input_nombre.text()
            apellido = self.input_apellido.text()
            carrera = self.input_carrera.text()
            if not nombre or not apellido or not carrera:
                raise ValueError("Todos los campos son obligatorios.")
            self.arbol.agregar_estudiante(id, nombre, apellido, carrera)
            self.clear_inputs()
            self.message_label.setText(f"Estudiante {nombre} {apellido} agregado.")
        except ValueError as e:
            self.message_label.setText(str(e))

    def eliminar_estudiante(self):
        try:
            id = int(self.input_id.text())
            self.arbol.eliminar_estudiante(id)
            self.clear_inputs()
            self.message_label.setText(f"Estudiante con ID {id} eliminado.")
        except ValueError:
            self.message_label.setText("Por favor, ingrese un ID válido.")

    def buscar_estudiante(self):
        try:
            id = int(self.input_id.text())
            estudiante = self.arbol.buscar_estudiante(id)
            if estudiante:
                self.message_label.setText(f"Estudiante encontrado: ID: {estudiante.id}, Nombre: {estudiante.nombre}, Apellido: {estudiante.apellido}, Carrera: {estudiante.carrera}")
            else:
                self.message_label.setText("Estudiante no encontrado.")
        except ValueError:
            self.message_label.setText("Por favor, ingrese un ID válido.")

    def listar_estudiantes(self):
        estudiantes = self.arbol.listar_estudiantes()
        self.list_text.clear()
        for id, nombre, apellido, carrera in estudiantes:
            self.list_text.append(f"ID: {id}, Nombre: {nombre}, Apellido: {apellido}, Carrera: {carrera}")

    def exportar_estudiantes(self):
        estudiantes = self.arbol.listar_estudiantes()
        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Estudiantes", "", "CSV Files (*.csv);;All Files (*)")
        if archivo:
            with open(archivo, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Nombre", "Apellido", "Carrera"])
                for estudiante in estudiantes:
                    writer.writerow(estudiante)
            self.message_label.setText("Estudiantes exportados correctamente a CSV.")

    def clear_inputs(self):
        self.input_id.clear()
        self.input_nombre.clear()
        self.input_apellido.clear()
        self.input_carrera.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AVLWindow2()
    window.show()
    sys.exit(app.exec())


