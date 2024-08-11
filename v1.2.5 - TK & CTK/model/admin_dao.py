"""
Contains all db methods to write, visualise, update and eliminate data
"""

from tkinter import messagebox
from .conexion_db import DBConection, AccescodeConection
from protect.decrypt import encrypt, decrypt
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

    def decrypt_in(user_data):

        private_key_string = private_db_key()
        private_key_bytes = private_key_string.encode('utf-8')
        loaded_private_key = serialization.load_pem_private_key(
            private_key_bytes, password=None)

        get_password = user_data.password

        decrypted_data = loaded_private_key.decrypt(
            get_password,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return decrypted_data

    decrypted_password = decrypt_in(user_d)

    public_key_string = public_table_key()
    public_key_bytes = public_key_string.encode('utf-8')
    loaded_public_key = serialization.load_pem_public_key(public_key_bytes)

    encrypted_password = loaded_public_key.encrypt(
        decrypted_password,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

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
