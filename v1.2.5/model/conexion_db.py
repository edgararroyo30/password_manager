import sqlite3
import os

class DBConection:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_datos = os.path.join(base_dir,'..','database', 'users.db')
        self.conexion = sqlite3.connect(self.base_datos)
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        self.conexion.commit()
        self.conexion.close()


class AccescodeConection:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_datos = os.path.join(base_dir, '..', 'database', 'access_code.db')
        self.conexion = sqlite3.connect(self.base_datos)
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        self.conexion.commit()
        self.conexion.close()
