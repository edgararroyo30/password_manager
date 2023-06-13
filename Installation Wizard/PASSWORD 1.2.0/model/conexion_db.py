import sqlite3


class ConexionDB:
    def __init__(self):
        self.base_datos = 'database/datos_usuarios.db'
        self.conexion = sqlite3.connect(self.base_datos)
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        self.conexion.commit()
        self.conexion.close()


class ConexionCodigo:
    def __init__(self):
        self.base_datos = 'database/codigo_acceso.db'
        self.conexion = sqlite3.connect(self.base_datos)
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        self.conexion.commit()
        self.conexion.close()
