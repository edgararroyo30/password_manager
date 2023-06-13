from tkinter import messagebox
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import bcrypt
from .conexion_db import ConexionDB, ConexionCodigo
from model.key import public_table_key, private_db_key

def crear_tabla():
    conexion = ConexionDB()

    sql = '''
    CREATE TABLE if NOT EXISTS datos_cifrados(
        id_user INTEGER,
        sitio text,
        username text,
        password BLOB,
        PRIMARY KEY(id_user AUTOINCREMENT)
        )'''
    
    conexion.cursor.execute(sql)
    conexion.cerrar()


def borrar_tabla():
    conexion = ConexionDB()

    sql = 'DROP TABLE datos_cifrados'

    try:

        conexion.cursor.execute(sql)
        conexion.cerrar()
        titulo = 'Crear Registro'
        mensaje = 'La tabla de la base de datos se borro con exito'
        messagebox.showinfo(titulo, mensaje)

    except:
        titulo = 'Crear Registro'
        mensaje = 'No hay tabla para borrar'
        messagebox.showerror(titulo, mensaje)


class user:
    def __init__(self, sitio, username, password):
        self.id_user = None
        self.sitio = sitio
        self.username = username
        self.password = password

    def __str__(self):
        return f'user[{self.sitio}, {self.username}, {self.password}]'


def guardar(user_d):
    conexion = ConexionDB()
    get_password = user_d.password
    decrypted_data = private_db_key().decrypt(
    get_password,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        )
    )
    encoded_password = decrypted_data.encode()
    encrypted_password = public_table_key().encrypt(
    encoded_password,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        )
    )
    get_sitio = user_d.sitio
    get_username = user_d.username
    sql = """
    INSERT INTO datos_cifrados (sitio, username, password)
    VALUES (?, ?, ?)
    """
    try:
        conexion.cursor.execute(
            sql, (get_sitio, get_username, encrypted_password))
        conexion.cerrar()
    except Exception as e:
        print(e)
        titulo = 'Conexion al registro'
        mensaje = 'La tabla no esta creado en la base de datos'
        messagebox.showerror(titulo, mensaje)


def listar():
    conexion = ConexionDB()

    lista_usuarios = []
    sql = 'SELECT * FROM datos_cifrados'

    try:
        conexion.cursor.execute(sql)
        lista_usuarios = conexion.cursor.fetchall()
        conexion.cerrar()
    except:
        titulo = 'Conexion al Registro'
        mensaje = 'Crea la tabla en la base de datos'
        messagebox.showwarning(titulo, mensaje)

    return lista_usuarios


def editar(user_d, id_user):
    conexion = ConexionDB()
    get_password = user_d.password
    encoded_password = get_password.encode()
    encrypted_password = f.encrypt(encoded_password)

    sql = f"""UPDATE datos_cifrados
    SET sitio = ?, username = ?,
    password = ?
    WHERE id_user = ?
    """

    try:
        conexion.cursor.execute(
            sql, (user_d.sitio, user_d.username, encrypted_password, id_user))
        conexion.cerrar()

    except:
        titulo = 'Edicion de datos'
        mensaje = 'No se a podido editar este registro'
        messagebox.showerror(titulo, mensaje)


def eliminar(id_user):
    conexion = ConexionDB()

    sql = f'DELETE FROM datos_cifrados WHERE id_user = {id_user}'

    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()

    except:
        titulo = 'Eliminar datos'
        mensaje = 'No se pudo eliminar el registro'
        messagebox.showerror(titulo, mensaje)


def cuenta_id():
    conexion = ConexionDB()

    numero_contrasenas = []
    sql = 'SELECT id_user FROM datos_cifrados'

    try:
        conexion.cursor.execute(sql)
        numero_contrasenas = conexion.cursor.fetchall()
        conexion.cerrar()
    except:
        titulo = 'Conexion al Registro'
        mensaje = 'Crea la tabla en la base de datos'
        messagebox.showwarning(titulo, mensaje)

    return numero_contrasenas


def create_table_codigo():
    conexion = ConexionCodigo()

    sql = """CREATE TABLE if NOT EXISTS codigo (
        code BLOB
        )"""

    conexion.cursor.execute(sql)
    conexion.cerrar()


def solicitar_clave_acceso():
    conexion = ConexionCodigo()

    sql = 'SELECT * FROM codigo'

    conexion.cursor.execute(sql)
    codigo = conexion.cursor.fetchone()
    conexion.cerrar()

    if codigo is None:
        return False

    return True


def save_code(code):
    conexion = ConexionCodigo()

    codgio_bytes = code.encode()
    codigo_hashed = bcrypt.hashpw(codgio_bytes, bcrypt.gensalt())

    sql = """INSERT INTO codigo VALUES (?)"""

    conexion.cursor.execute(sql, (codigo_hashed,))
    conexion.cerrar()


def check_code(code):
    conexion = ConexionCodigo()

    sql = 'SELECT code FROM codigo'

    conexion.cursor.execute(sql)
    codigo = conexion.cursor.fetchone()
    conexion.cerrar()

    if codigo is not None:
        hashed_password = codigo[0]
        codigo_bytes = code.encode()
        return bcrypt.checkpw(codigo_bytes, hashed_password)
    return False


