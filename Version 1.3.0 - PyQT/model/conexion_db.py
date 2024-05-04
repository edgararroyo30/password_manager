import sqlite3


class DBConection:
    def __init__(self):
        self.base_datos = 'database/users.db'
        self.conexion = sqlite3.connect(self.base_datos)
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        self.conexion.commit()
        self.conexion.close()


class AccescodeConection:
    def __init__(self):
        self.base_datos = 'database/access_code.db'
        self.conexion = sqlite3.connect(self.base_datos)
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        self.conexion.commit()
        self.conexion.close()
