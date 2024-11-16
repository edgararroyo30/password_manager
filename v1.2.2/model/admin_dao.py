"""
Contains all db methods to write, visualise, update and eliminate data
"""

from tkinter import messagebox
from .conexion_db import DBConection, AccescodeConection
from protect.decrypt import encrypt, decrypt, hash_code, check_hash
import base64


def create_table():
    """
    Creates the table that contains the users data.
    Includes user_id, website, username and password
    """
    conexion = DBConection()

    sql = '''
    CREATE TABLE if NOT EXISTS encrypted_data(
        user_id INTEGER,
        website text,
        username text,
        password BLOB,
        PRIMARY KEY(user_id AUTOINCREMENT)
        )'''

    conexion.cursor.execute(sql)
    conexion.cerrar()

def delete_table():
    """ 
    
    """
    conexion = DBConection()

    sql = 'DROP TABLE encrypted_data'

    try:

        conexion.cursor.execute(sql)
        conexion.cerrar()
        title = 'Create DB'
        message = 'The table from the data base was deleted succesfully'
        messagebox.showinfo(title, message)

    except:
        title = 'Create DB'
        message = 'There is no table to delete'
        messagebox.showerror(title, message)


class user:
    def __init__(self, website, username, password):
        self.id_user = None
        self.website = website
        self.username = username
        self.password = password

    def __str__(self):
        return f'user[{self.website}, {self.username}, {self.password}]'

def save(user_d):
    conexion = DBConection()

    encrypted_password = encrypt(user_d.password)

    sql = """
    INSERT INTO encrypted_data (website, username, password)
    VALUES (?, ?, ?)
    """
    try:
        conexion.cursor.execute(
            sql, (user_d.website, user_d.username, encrypted_password))
        conexion.cerrar()
    except Exception as e:
        print(e)
        titulo = 'Conexion al registro'
        mensaje = 'La tabla no esta creada en la base de datos'
        messagebox.showerror(titulo, mensaje)

def listar_usuarios(user_id):
    conexion = DBConection()

    lista_usuarios = []
    final_list = []
    sql = 'SELECT * FROM encrypted_data WHERE user_id > ?'

   
    conexion.cursor.execute(sql, (user_id,))
    lista_usuarios = conexion.cursor.fetchall()
    conexion.cerrar()
    
    for p in lista_usuarios:
            final_list.append([p[0],p[1], p[2],decrypt(p[3])])
    
    return final_list

def editar(user_d, id_user):
    conexion = DBConection()

    encrypted_password = encrypt(user_d.password)

    sql = f"""UPDATE encrypted_data
    SET website = ?, username = ?,
    password = ?
    WHERE user_id = ?
    """

    try:
        conexion.cursor.execute(
            sql, (user_d.website, user_d.username, encrypted_password, id_user))
        conexion.cerrar()

    except Exception as e:
        print(e)

def eliminar(user_id):
    conexion = DBConection()

    sql = f'DELETE FROM encrypted_data WHERE user_id = {user_id}'

    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()

    except:
        titulo = 'Eliminar datos'
        mensaje = 'No se pudo eliminar el registro'
        messagebox.showerror(titulo, mensaje)

def cuenta_id():
    conexion = DBConection()

    numero_contrasenas = []
    sql = 'SELECT user_id FROM encrypted_data'

    try:
        conexion.cursor.execute(sql)
        numero_contrasenas = conexion.cursor.fetchall()
        conexion.cerrar()
        numero_contrasenas = len(numero_contrasenas)
        return numero_contrasenas
    except:
        titulo = 'Conexion al Registro'
        mensaje = 'La tabla esta vacia'
        messagebox.showwarning(titulo, mensaje)

def create_table_codigo():
    conexion = AccescodeConection()

    sql = """CREATE TABLE if NOT EXISTS access_code (
        code BLOB
        )"""

    conexion.cursor.execute(sql)
    conexion.cerrar()

def code_validation():
    conexion = AccescodeConection()

    sql = 'SELECT * FROM access_code'

    conexion.cursor.execute(sql)
    codigo = conexion.cursor.fetchone()
    conexion.cerrar()

    if codigo is None:
        return False

    return True

def insert_code(code):
    conexion = AccescodeConection()

    codigo_hashed = hash_code(code)

    sql = """INSERT INTO access_code VALUES (?)"""

    conexion.cursor.execute(sql, (codigo_hashed,))
    conexion.cerrar()

def check_code(code):
    conexion = AccescodeConection()

    sql = 'SELECT code FROM access_code'

    conexion.cursor.execute(sql)
    codigo = conexion.cursor.fetchone()
    conexion.cerrar()

    if codigo is None:
    
        return False
    else:
        
        return check_hash(codigo,code)