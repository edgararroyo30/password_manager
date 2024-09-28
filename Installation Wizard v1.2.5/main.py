import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ttkthemes import ThemedStyle
from PIL import ImageTk, Image
import shutil
import os
import winreg
import json
from pathlib import Path
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet
import sqlite3
import subprocess
import time
import threading
import win32com.client
import webbrowser
import sys
import base64
import ctypes

main_text=""" 
import customtkinter as ctk
from model.admin_dao import crear_tabla, create_table_codigo
from client.gui_app import Frame


def main():
    root = ctk.CTk()
    root.title('Administrador de contrasenas')
    root.iconbitmap('image/app-icon.ico')
    root.resizable(0, 0)

    app = Frame(root=root)

    app.mainloop()


if __name__ == '__main__':
    create_table_codigo()
    crear_tabla()
    main()"""

admin_dao_text = """
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

    def decrypt_in(user_data):

        private_key_string=private_db_key()
        private_key_bytes = private_key_string.encode('utf-8')
        loaded_private_key = serialization.load_pem_private_key(private_key_bytes,password=None)

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

    decrypted_password= decrypt_in(user_d)


    public_key_string=public_table_key()
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

    get_sitio = user_d.sitio
    get_username = user_d.username
    sql = "INSERT INTO datos_cifrados (sitio, username, password) VALUES (?, ?, ?)"
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
    def decrypt_in(user_data):

        private_key_string=private_db_key()
        private_key_bytes = private_key_string.encode('utf-8')
        loaded_private_key = serialization.load_pem_private_key(private_key_bytes,password=None)

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

    decrypted_password= decrypt_in(user_d)


    public_key_string=public_table_key()
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

    sql = f"UPDATE datos_cifrados SET sitio = ?, username = ?, password = ? WHERE id_user = ?"

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

    sql = "CREATE TABLE if NOT EXISTS codigo (code BLOB)"

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

    sql = "INSERT INTO codigo VALUES (?)"

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

"""
conexion_db_text = """
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
        self.conexion.close()"""

key_text = """
import json

def public_table_key():
    with open("keys.json", "r") as file:
        config = json.load(file)
    key = config["PUBLIC_TABLE_KEY"]
    
    return key


def private_db_key():
    with open("keys.json", "r") as file:
        config = json.load(file)
    key = config["PRIVATE_DB_KEY"]
    
    return key

def public_db_key():
    with open("keys.json", "r") as file:
        config = json.load(file)
    key = config["PUBLIC_DB_KEY"]
    
    return key
    
def private_table_key():
    with open("keys.json", "r") as file:
        config = json.load(file)
    key = config["PRIVATE_TABLE_KEY"]
    
    return key
"""
gui_app_text = """
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox

import secrets

import pyperclip
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from ttkthemes import ThemedStyle
from model.admin_dao import user, guardar, listar, eliminar, editar
from model.admin_dao import cuenta_id, solicitar_clave_acceso, save_code, check_code
from model.key import public_db_key, private_table_key

def generate_password():
    password_lenght = 12
    password = secrets.token_urlsafe(password_lenght)
    return password


def contar_id():

    get_id = cuenta_id()
    numero_id = len(get_id)
    return numero_id


class Frame(ttk.Frame):
    def __init__(self, root=None, data=None):
        super().__init__(root)
        self.root = root
        self.data = data
        self.pack()

        self.style = ThemedStyle(self.root)
        self.style.set_theme("equilux")
        self.style.theme_use('equilux')

        self.crear_widgets()
        self.cuenta_contrasenas()
        self.tabla_de_contrasenas()
        self.pop_menu()
        if solicitar_clave_acceso() is False:
            self.create_code()
        elif solicitar_clave_acceso() is True:
            self.input_code()

    def eliminar_datos(self):
        self.id_user = self.tabla.item(self.tabla.selection())['text']
        eliminar(self.id_user)
        self.tabla_de_contrasenas()
        self.pop_menu()
        self.cuenta_contrasenas()

    def mostrar_menu(self, event):
        self.popup_menu.post(event.x_root, event.y_root)

    def cuenta_contrasenas(self):
        mi_cuenta_usuarios = (f"{contar_id()} contraseñas guardadas")

        self.label_usuarios = ttk.Label(self, text=mi_cuenta_usuarios)
        self.style.configure(style='Equilux.TLabel')
        self.label_usuarios.config(
            width=30, font=('Segoe UI', 10, 'bold'))
        self.label_usuarios.grid(row=3, padx=(10, 180), pady=(12, 2))

    def crear_widgets(self):
        self.boton_nuevo = ttk.Button(
            self, text='Agregar Usuario', command=self.new_user, width=15)

        self.boton_nuevo.grid(row=3, column=2,
                              padx=(2, 10), pady=(10, 2))

        self.mi_busqueda = tk.StringVar()
        self.entry_buscar = ttk.Entry(self, textvariable=self.mi_busqueda)
        self.style.configure(style='Equilux.TEntry')
        self.entry_buscar.config(width=25, font=('Segoe UI', 9))
        self.entry_buscar.grid(
            row=3, padx=(250, 0), pady=(10, 2), columnspan=1)

        def buscar():
            self.search_and_highlight(self.tabla, self.mi_busqueda.get())

        self.boton_buscar = ttk.Button(self, text='Buscar', command=buscar)

        self.style.configure("TButton", width=10, font=('Segoe UI', 8),
                             cursor='hand2', focuscolor='none', borderwidth=2,
                             bd=2, relief="solid", anchor='center',
                             highlightcolor='#35BD6F', highlightbackground='#35BD6F')

        self.boton_buscar.grid(row=3, column=1,
                               padx=(2, 0), pady=(10, 2))

    def new_user(self):
        ventana = tk.Toplevel(self)
        ventana.config(background=self.style.lookup('TFrame', 'background'))
        ventana.title('Agregar Usuario')
        ventana.iconbitmap('image/app-icon.ico')
        style = ThemedStyle(ventana)

        ventana.geometry("310x250")

        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (ventana.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (ventana.winfo_height() // 2)

        # Se actualiza la posición de la ventana secundaria
        ventana.geometry("+{}+{}".format(x, y))

        ventana.lift()

        ventana.overrideredirect(False)

        def destroy():
            ventana.destroy()

        label_sitio_web = ttk.Label(ventana, text='URL del sitio web')
        style.configure(style='Equilux.TLabel')
        label_sitio_web.config(
            width=17, font=('Segoe UI', 10))
        label_sitio_web.grid(row=0, padx=(1, 10), pady=(14, 4))

        label_nombre_usuario = ttk.Label(
            ventana, text='Nombre de usuario ')
        style.configure(style='Equilux.TLabel')
        label_nombre_usuario.config(
            width=17, font=('Segoe UI', 10))
        label_nombre_usuario.grid(row=2, padx=(1, 10), pady=(14, 4))

        label_contraseña = ttk.Label(ventana, text='Contraseña ')
        style.configure(style='Equilux.TLabel')
        label_contraseña.config(
            width=17, font=('Segoe UI', 10))
        label_contraseña.grid(row=4, padx=(1, 10), pady=(14, 4))

        # Entrys de cada campo
        self.mi_sitio_web_add = tk.StringVar()

        entry_sitio_web = ttk.Entry(
            ventana, textvariable=self.mi_sitio_web_add)
        style.configure(style='Equilux.TEntry')
        entry_sitio_web.config(width=30, font=('Segoe UI', 12))
        entry_sitio_web.grid(
            row=1, padx=(15, 16), columnspan=3)

        self.mi_nombre_usuario_add = tk.StringVar()

        entry_nombre_usuario = ttk.Entry(
            ventana, textvariable=self.mi_nombre_usuario_add)
        style.configure(style='Equilux.TEntry')
        entry_nombre_usuario.config(width=30,
                                    font=('Segoe UI', 12))
        entry_nombre_usuario.grid(
            row=3, padx=(16, 16), columnspan=3)

        mi_contrasena = generate_password()
        self.mi_contrasena_add = tk.StringVar()

        entry_contrasena = ttk.Entry(
            ventana, textvariable=self.mi_contrasena_add)
        entry_contrasena.insert(0, mi_contrasena)
        style.configure(
            style='Equilux.TEntry')

        entry_contrasena.config(width=30,
                                font=('Segoe UI', 12))
        entry_contrasena.grid(
            row=5, padx=(16, 16), columnspan=3)

        def guardar_datos():
            public_key_string=public_db_key()
            public_key_bytes = public_key_string.encode('utf-8')
            loaded_public_key = serialization.load_pem_public_key(public_key_bytes)

            encrypted_password = loaded_public_key.encrypt(
            self.mi_contrasena_add.get().encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
                )
            )

            user_data = user(
                self.mi_sitio_web_add.get(),
                self.mi_nombre_usuario_add.get(),
                encrypted_password)
            guardar(user_data)
            ventana.destroy()
            self.tabla_de_contrasenas()
            self.pop_menu()
            self.cuenta_contrasenas()

        boton_guardar = ttk.Button(
            ventana, text='Guardar', command=guardar_datos)

        style.configure("RoundedButton.TButton", width=25, font=('Segoe UI', 12, 'bold'),
                        cursor='hand2', focuscolor='none', borderwidth=2,
                        bd=2, relief="solid", anchor='center',
                        highlightcolor='#35BD6F', highlightbackground='#35BD6F')

        boton_guardar.grid(
            row=6, column=0,  padx=(30, 10), pady=(14, 10))

        boton_cancelar = ttk.Button(
            ventana, text='Cancelar', command=destroy)

        style.configure("RoundedButton.TButton", width=25, font=('Segoe UI', 12, 'bold'),
                        cursor='hand2', focuscolor='none', borderwidth=2,
                        bd=2, relief="solid", anchor='center',
                        highlightcolor='#35BD6F', highlightbackground='#35BD6F')

        boton_cancelar.grid(
            row=6, column=1,  padx=(0, 20), pady=(14, 10))

    def edit_user(self):
        self.ventana = tk.Toplevel(self)
        self.ventana.config(
            background=self.style.lookup('TFrame', 'background'))
        self.ventana.title('Editar Usuario')
        self.ventana.iconbitmap('image/app-icon.ico')
        self.style = ThemedStyle(self.ventana)

        self.ventana.geometry("310x250")

        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (self.ventana.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (self.ventana.winfo_height() // 2)

        # Se actualiza la posición de la ventana secundaria
        self.ventana.geometry("+{}+{}".format(x, y))

        self.ventana.lift()

        self.ventana.overrideredirect(False)

        def destroy():
            self.ventana.destroy()

        self.label_sitio_web = ttk.Label(
            self.ventana, text='URL del sitio web')
        self.style.configure(style='Equilux.TLabel')
        self.label_sitio_web.config(
            width=17, font=('Segoe UI', 10))
        self.label_sitio_web.grid(row=0, padx=(1, 10), pady=(14, 4))

        self.label_nombre_usuario = ttk.Label(
            self.ventana, text='Nombre de usuario ')
        self.style.configure(style='Equilux.TLabel')
        self.label_nombre_usuario.config(
            width=17, font=('Segoe UI', 10))
        self.label_nombre_usuario.grid(row=2, padx=(1, 10), pady=(14, 4))

        self.label_contraseña = ttk.Label(self.ventana, text='Contraseña ')
        self.style.configure(style='Equilux.TLabel')
        self.label_contraseña.config(
            width=17, font=('Segoe UI', 10))
        self.label_contraseña.grid(row=4, padx=(1, 10), pady=(14, 4))

        # Entrys de cada campo
        self.mi_sitio_web_edit = tk.StringVar()

        self.entry_sitio_web = ttk.Entry(
            self.ventana, textvariable=self.mi_sitio_web_edit)
        self.style.configure(style='Equilux.TEntry')
        self.entry_sitio_web.config(width=30, font=('Segoe UI', 12))
        self.entry_sitio_web.grid(
            row=1, padx=(15, 16), columnspan=3)

        self.mi_nombre_usuario_edit = tk.StringVar()

        self.entry_nombre_usuario = ttk.Entry(
            self.ventana, textvariable=self.mi_nombre_usuario_edit)
        self.style.configure(style='Equilux.TEntry')
        self.entry_nombre_usuario.config(width=30,
                                         font=('Segoe UI', 12))
        self.entry_nombre_usuario.grid(
            row=3, padx=(16, 16), columnspan=3)

        self.mi_contrasena_edit = tk.StringVar()

        self.entry_contrasena = ttk.Entry(
            self.ventana, textvariable=self.mi_contrasena_edit)
        self.style.configure(
            style='Equilux.TEntry')

        self.entry_contrasena.config(width=30,
                                     font=('Segoe UI', 12))
        self.entry_contrasena.grid(
            row=5, padx=(16, 16), columnspan=3)

        def guardar_datos():

            public_key_string=public_db_key()
            public_key_bytes = public_key_string.encode('utf-8')
            loaded_public_key = serialization.load_pem_public_key(public_key_bytes)

            encrypted_password = loaded_public_key.encrypt(
            self.mi_contrasena_edit.get().encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
                )
            )


            user_data = user(
                self.mi_sitio_web_edit.get(),
                self.mi_nombre_usuario_edit.get(),
                encrypted_password)
            id = self.id_user = self.tabla.item(self.tabla.selection())['text']
            editar(user_data, id)

            self.ventana.destroy()
            self.tabla_de_contrasenas()
            self.pop_menu()
            self.cuenta_contrasenas()
           

        self.boton_guardar = ttk.Button(
            self.ventana, text='Guardar', command=guardar_datos)

        self.style.configure("RoundedButton.TButton", width=25, font=('Segoe UI', 12, 'bold'),
                             cursor='hand2', focuscolor='none', borderwidth=2,
                             bd=2, relief="solid", anchor='center',
                             highlightcolor='#35BD6F', highlightbackground='#35BD6F')

        self.boton_guardar.grid(
            row=6, column=0,  padx=(30, 10), pady=(14, 10))

        self.boton_cancelar = ttk.Button(
            self.ventana, text='Cancelar', command=destroy)

        self.style.configure("RoundedButton.TButton", width=25, font=('Segoe UI', 12, 'bold'),
                             cursor='hand2', focuscolor='none', borderwidth=2,
                             bd=2, relief="solid", anchor='center',
                             highlightcolor='#35BD6F', highlightbackground='#35BD6F')

        self.boton_cancelar.grid(
            row=6, column=1,  padx=(0, 20), pady=(14, 10))

    def pop_menu(self):
        self.popup_menu = tk.Menu(
            self, type='normal', bg='#333', foreground='#D3D3D3', tearoff=0)
        self.popup_menu.config(activebackground='#555',
                               activeforeground='#D3D3D3', bd=0, activeborderwidth=0)

        self.popup_menu.add_command(label="Editar", command=lambda: (
            self.edit_user(), self.editar_datos()))
        self.popup_menu.add_command(
            label="Eliminar", command=self.eliminar_datos)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(
            label="Copiar", command=self.copiar_datos)

        self.tabla.bind("<Button-3>", self.mostrar_menu)

    def tabla_de_contrasenas(self):
        self.lista_usuario = listar()
        self.lista_usuario.reverse()

        self.tabla = ttk.Treeview(self,
                                  column=('Sitio Web', 'Usuario', 'Contraseña'))
        self.tabla.grid(row=4, column=0, columnspan=3,
                        sticky='nse', padx=10, pady=(0, 10))

        self.scroll = ttk.Scrollbar(self,
                                    orient='vertical', command=self.tabla.yview)
        self.scroll.grid(row=4, column=2, padx=(
            1, 10), pady=(0, 10), sticky='nse')
        self.tabla.configure(yscrollcommand=self.scroll.set)

        self.tabla.heading('#0', text='ID')
        self.tabla.heading('#1', text='Sitio Web')
        self.tabla.heading('#2', text='Usuario')
        self.tabla.heading('#3', text='Contraseña')

        private_key_string=private_table_key()
        private_key_bytes = private_key_string.encode('utf-8')
        loaded_private_key = serialization.load_pem_private_key(private_key_bytes,password=None)


        for p in self.lista_usuario:

            decrypted_password =loaded_private_key.decrypt(
            p[3],
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
                )
            )

            self.tabla.insert('', 0, text=p[0],
                              values=(p[1], p[2], decrypted_password.decode('utf-8')))
        self.tabla.column("#0", width=0, stretch=False)
        self.tabla.config(displaycolumns=(
            'Sitio Web', 'Usuario', 'Contraseña'))
        self.clear_search(self.tabla)

    def editar_datos(self):
        try:
            self.sitio = self.tabla.item(
                self.tabla.selection())['values'][0]
            self.username = self.tabla.item(
                self.tabla.selection())['values'][1]
            self.password = self.tabla.item(
                self.tabla.selection())['values'][2]

            self.entry_sitio_web.insert(0, self.sitio)
            self.entry_nombre_usuario.insert(0, self.username)
            self.entry_contrasena.insert(0, self.password)

        except:
            titulo = 'Edicion de datos'
            mensaje = 'No ha seleccionado ningun registro'
            messagebox.showerror(titulo, mensaje)

    def copiar_datos(self):
        try:
            self.password = self.tabla.item(
                self.tabla.selection())['values'][2]
            pyperclip.copy(self.password)

        except:
            titulo = 'Edicion de datos'
            mensaje = 'No ha seleccionado ningun registro'
            messagebox.showerror(titulo, mensaje)

    def input_code(self):
        self.root.withdraw()
        ventana = ctk.CTkToplevel(self.root)
        ventana.config(background=self.style.lookup('TFrame', 'background'))
        ventana.title('Acceder')
        ventana.iconbitmap('image/app-icon.ico')
        style = ThemedStyle(ventana)
        ventana.geometry("310x100")

        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - \
            (ventana.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - \
            (ventana.winfo_height() // 2)

        # Se actualiza la posición de la ventana secundaria
        ventana.geometry("+{}+{}".format(x, y))

        ventana.lift()
        ventana.grab_set()

        ventana.overrideredirect(False)

        label_sitio_web = ttk.Label(
            ventana, text='Ingresa tu codigo de acceso')
        style.configure(style='Equilux.TLabel')
        label_sitio_web.config(
            width=30, font=('Segoe UI', 10))
        label_sitio_web.grid(row=1, padx=(70, 10), pady=(10, 4))

        mi_codigo = tk.StringVar()

        entry_sitio_web = ttk.Entry(
            ventana, show="*", textvariable=mi_codigo)
        style.configure(style='Equilux.TEntry')
        entry_sitio_web.config(width=30, font=('Segoe UI', 12))
        entry_sitio_web.grid(
            row=2, padx=(15, 15), columnspan=3)

        def guardar_datos():
            codigo = str(mi_codigo.get())

            if check_code(codigo) is True:
                self.root.deiconify()
                ventana.destroy()
            else:
                title = 'Acceso Denegado'
                mensaje = 'El codgio ingresado es incorrecto'
                messagebox.showerror(
                    title, mensaje)

        boton_guardar = ttk.Button(
            ventana, text='Acceder', command=guardar_datos)

        style.configure("RoundedButton.TButton", width=25, font=('Segoe UI', 12, 'bold'),
                        cursor='hand2', focuscolor='none', borderwidth=2,
                        bd=2, relief="solid", anchor='center',
                        highlightcolor='#35BD6F', highlightbackground='#35BD6F')

        boton_guardar.grid(
            row=6, column=0,  padx=(50, 50), pady=(5, 15))

    def create_code(self):
        self.root.withdraw()
        ventana = ctk.CTkToplevel(self.root)
        ventana.config(background=self.style.lookup('TFrame', 'background'))
        ventana.title('Acceder')
        ventana.iconbitmap('image/app-icon.ico')
        style = ThemedStyle(ventana)
        ventana.geometry("310x160")

        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (ventana.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (ventana.winfo_height() // 2)

        # Se actualiza la posición de la ventana secundaria
        ventana.geometry("+{}+{}".format(x, y))

        ventana.lift()
        ventana.grab_set()

        ventana.overrideredirect(False)

        label_sitio_web = ttk.Label(
            ventana, text='Crea tu codigo de acceso')
        style.configure(style='Equilux.TLabel')
        label_sitio_web.config(
            width=30, font=('Segoe UI', 10))
        label_sitio_web.grid(row=1, padx=(70, 10), pady=(10, 4))

        label_confirmar = ttk.Label(
            ventana, text='Confirma tu codigo de acceso')
        style.configure(style='Equilux.TLabel')
        label_confirmar.config(
            width=30, font=('Segoe UI', 10))
        label_confirmar.grid(row=3, padx=(70, 10), pady=(10, 4))

        recibir_codigo = tk.StringVar()

        entry_sitio_web = ttk.Entry(
            ventana, show="*", textvariable=recibir_codigo)
        style.configure(style='Equilux.TEntry')
        entry_sitio_web.config(width=30, font=('Segoe UI', 12))
        entry_sitio_web.grid(
            row=2, padx=(15, 15), columnspan=3)

        confirmar_codigo = tk.StringVar()
        entry_confirmar = ttk.Entry(
            ventana, show="*", textvariable=confirmar_codigo)
        style.configure(style='Equilux.TEntry')
        entry_confirmar.config(width=30, font=('Segoe UI', 12))
        entry_confirmar.grid(
            row=4, padx=(15, 15), columnspan=3)

        def guardar_datos():
            codigo_1 = str(confirmar_codigo.get())
            codigo_2 = str(recibir_codigo.get())

            if len(codigo_1) > 0:
                if codigo_1.lower().strip() == codigo_2.lower().strip():
                    save_code(codigo_1)
                    self.root.deiconify()
                    ventana.destroy()
                else:
                    title = 'Creacion Codigo'
                    mensaje = 'Los codigos no coinciden'
                    messagebox.showerror(title, mensaje)
            else:
                title = 'Creacion Codigo'
                mensaje = 'Ingresa un codigo'
                messagebox.showerror(title, mensaje)

        boton_guardar = ttk.Button(
            ventana, text='Continuar', command=guardar_datos)

        style.configure("RoundedButton.TButton", width=25, font=('Segoe UI', 12, 'bold'),
                        cursor='hand2', focuscolor='none', borderwidth=2,
                        bd=2, relief="solid", anchor='center',
                        highlightcolor='#35BD6F', highlightbackground='#35BD6F')

        boton_guardar.grid(
            row=6, column=0,  padx=(50, 50), pady=(5, 15))

    def clear_search(self, tree):
        # limpiar selección y etiquetas de la tabla
        tree.selection_remove(tree.selection())
        tree.tag_configure("searched_row", background="#373737")

    def search_and_highlight(self, tree, search_string):
        if not search_string:
            self.clear_search(tree)
            return
        # limpiar selección y etiquetas de la tabla
        tree.selection_remove(tree.selection())
        tree.tag_configure("searched_row", background="#373737")

        for item in tree.get_children():
            if search_string.lower() in str(tree.item(item)["values"]).lower():
                # seleccionar y resaltar la fila
                tree.selection_add(item)
                tree.item(item, tags=("searched_row",))
"""
spec_content = """
# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['admin_contrasenas.py'],
    pathex=[],
    binaries=[],
    datas=[('/customtkinter;customtkinter/','customtkinter'), ('/cryptography;cryptography/','cryptography'), ('/bcrypt;bcrypt/','bcrypt'), ('/pyperclip;pyperclip/','pyperclip'), ('/ttkthemes;ttkthemes/','ttkthemes')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='admin_contrasenas',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon = ['app-icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='admin_contrasenas',
)
"""

app_icon = """
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
"""
if getattr(sys, 'frozen', False):
    # Running as a bundled executable
    base_dir = sys._MEIPASS
else:
    # Running as a normal script
    base_dir = os.path.dirname(os.path.abspath(__file__))

private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend)
public_key = private_key.public_key()

private_key1 = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend)
public_key1 = private_key1.public_key()


private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
            )

public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

private_key1_pem = private_key1.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
            )

public_key1_pem = public_key1.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

key = 'PvP7oSQbrKD8HNRYvWpPTJPmqgEMZfIeO5BuS1DqDUE='

bloqueo = threading.Lock()

f = Fernet(key)

class ConexionDB:
    def __init__(self, path):
        self.base_datos = path
        self.conexion = sqlite3.connect(self.base_datos)
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        self.conexion.commit()
        self.conexion.close()

class ConexionCodigo:
    def __init__(self, path):
        self.base_datos = path
        self.conexion = sqlite3.connect(self.base_datos)
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        self.conexion.commit()
        self.conexion.close()

def get_password(path):
    connect = ConexionDB(path)

    sql = "SELECT password FROM datos_cifrados"

    connect.cursor.execute(sql)

    passwords = connect.cursor.fetchall()
    connect.cerrar()

    return passwords

def get_id(path):
    connect = ConexionDB(path)

    sql = "SELECT id_user FROM datos_cifrados"

    connect.cursor.execute(sql)

    id_user = connect.cursor.fetchall()
    connect.cerrar()

    id_list = []

    for id in id_user:
        id = str(id)
        id =id.strip("()")
        id =id.strip(",")

        id_list.append(id)

    return id_list

def get_code(path):
    connect = ConexionCodigo(path)

    sql = "SELECT FROM codigo"

    connect.cursor.execute(sql)

    code = connect.cursor.fetchall()
    connect.cerrar()

    return code

def decode_passwords(path):
    passwords = get_password(path)

    uncrypted = []

    for password in passwords:
        password = str(password)
        password = password.strip("()")
        password = password.strip(",")
        password = password.strip("b")
        password = password.strip("'")
        password = password.encode()

        decrypyed_password = f.decrypt(password)

        uncrypted.append(decrypyed_password.decode())

    return uncrypted

def encode_passwords(path):
    
    passwords = decode_passwords(path)

    encrypted = []

    for password in passwords:
        encrypted_password = public_key1.encrypt(
        password.encode("utf-8"),
        padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        )
    )
        

        encrypted.append(encrypted_password)

    return encrypted

def update_passwords(path, id_user, password):
    connect = ConexionDB(path)

    sql = "UPDATE datos_cifrados SET password = ? WHERE id_user = ?"

    connect.cursor.execute(sql, (password, id_user,))
    connect.cerrar()

def store_passwords(path):
    passwords = encode_passwords(path)
    id_p = get_id(path)
    
    password_id = list(zip(id_p, passwords))

    for value in password_id:
        id, password = value

        update_passwords(path, id, password)

def ejecutar_pyinstaller(ruta_archivo,ruta_spec):
    
    ruta_directorio = os.path.dirname(ruta_archivo)
    os.chdir(ruta_directorio)
    nombre_archivo = os.path.basename(ruta_archivo)

    # env = 'python -m venv virtual'
    # subprocess.run(env, shell=True)

    # open_env = 'virtual/Scripts/activate'
    # subprocess.run(open_env, shell=True)


    install = 'pip install pyinstaller'
    subprocess.run(install, shell=True)

    customtk = 'pip install  customtkinter'
    subprocess.run(customtk,shell=True)

    cryptography  = 'pip install  cryptography '
    subprocess.run(cryptography ,shell=True)

    bcrypt  = 'pip install bcrypt'
    subprocess.run(bcrypt ,shell=True)

    pyperclip  = 'pip install pyperclip'
    subprocess.run(pyperclip ,shell=True)

    ttkthemes  = 'pip install ttkthemes'
    subprocess.run(ttkthemes ,shell=True)


    def create_spec():

        global spec_content

        locationctk =  subprocess.run('pip show customtkinter', capture_output=True, text=True)

        salida = locationctk.stdout

        lineas = salida.splitlines()

        location_linea = None
        for linea in lineas:
            if linea.startswith("Location"):
                location_linea = linea
                break

        if location_linea:
            location_linea = location_linea.replace("Location: ", "")

        ctk_path = location_linea.strip()

        ctk_path = ctk_path.replace("\\", "/")
        spec_lines = spec_content.splitlines()

        spec_lines[11] = f"    datas=[('{ctk_path}/customtkinter','customtkinter')],"

        spec_content = '\n'.join(spec_lines)

        main = ruta_directorio + '/admin_contrasenas.spec'

        with open(main, "w") as file:
                    
            file.write(spec_content)

    def dirs_to_pathex():

        global spec_content

        client = ruta_directorio + '/client'
        client = client.replace("\\", "/")

        model = ruta_directorio + '/model'
        model = model.replace("\\", "/")

        dirs = f"'{client}', '{model}'"

        pathex_lines = spec_content.splitlines()

        pathex_lines[9] = f"    pathex=[{dirs}],"

        spec_content = '\n'.join(pathex_lines)

        pathex_lines[12] = f"    hiddenimports=[{dirs}],"

        spec_content = '\n'.join(pathex_lines)

        main = ruta_directorio + '/admin_contrasenas.spec'

        with open(main, "w") as file:
                    
            file.write(spec_content)

    create_spec()
    dirs_to_pathex()


    run = f"""pyinstaller admin_contrasenas.spec""" 
    subprocess.run(run, shell=True)

def python_exists():
    check =  subprocess.run('python --version', capture_output=True, text=True)

    salida = check.stdout

    if salida.startswith("Python"):
        return True 

    return False

def instalar_python():
    webbrowser.open("https://www.python.org/downloads/")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class InstalacionApp:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.geometry("600x400")
        self.ventana.title("Asistente de Instalación")
        self.ventana.configure(bg="#f0f0f0")
        self.icon = os.path.join(base_dir, 'installer-icon.ico')
        self.ventana.iconbitmap(self.icon)

        self.ventana.resizable(0, 0)

        self.style = ThemedStyle(self.ventana)
        # self.style.set_theme("breeze")

        self.ubicacion_seleccionada = 'C:/Program Files'
        self.ubicacion_database = 'C:/Program Files/Administrador de contrasenas'
        self.count = 0
        self.count1 = 0
        self.count2 = 0
        
        self.image = os.path.join(base_dir, "code_image.jpg")


        self.introduccion()
        
        self.progreso_actual = tk.DoubleVar()
        self.radio_var = tk.IntVar(value=0)
        

    def seleccionar_ubicacion(self):
        self.ubicacion_seleccionada = filedialog.askdirectory()
        if self.ubicacion_seleccionada == "":
            self.ubicacion_seleccionada = 'C:/Program Files'
            self.ubicacion_entry.delete(0, 100)
            self.ubicacion_entry.insert(0, self.ubicacion_seleccionada)
            self.ubicacion_database = self.ubicacion_seleccionada + '/Administrador de contrasenas/database'

        else:
            self.ubicacion_entry.delete(0, 100)
            self.ubicacion_entry.insert(0, self.ubicacion_seleccionada)
            self.ubicacion_database = self.ubicacion_seleccionada + '/Administrador de contrasenas/database'

    def seleccionar_ubicacion_db(self):
        self.ubicacion_database = filedialog.askdirectory()
        if self.ubicacion_database == "":
            self.ubicacion_database = self.ubicacion_seleccionada + '/Administrador de contrasenas/database'
            self.actualizar_entry.delete(0, 100)
            self.actualizar_entry.insert(0, self.ubicacion_database)

        else:
            self.actualizar_entry.delete(0, 100)
            self.actualizar_entry.insert(0, self.ubicacion_database)

        with bloqueo:
            self.progreso_actual.set(0)  
            self.ventana.update()

    def graficos(self):
        self.regresar_1_button.destroy()
        self.boton_instalar.destroy()
        self.instalar_label.destroy()

        self.title_label.configure(text="Instalando")
        self.title_label.grid(row=0, column=0, padx=(0,175), pady=(10,0))
        self.title_message.configure(text="Espera hasta que el proceso de instalacion finalice")
        self.title_message.grid(row=1, column=0, padx=(20,0), pady=(5,0))
        
        self.instalar_progreso.grid(
                    row=0, column=0, padx=(0,  0), pady=(50, 0))

        self.progreso_label.configure(text="Instalando...")
        self.progreso_label.grid(
                    row=0, column=0, padx=(0, 435), pady=(0, 0))

        self.proceso = tk.Label(
        self.instalar_frame,width=71 ,  anchor="w")
        self.proceso.grid(
                    row=0, column=0, padx=(0, 0), pady=(100, 0))
        
        
        with bloqueo:
            self.progreso_actual.set(0)  
            self.ventana.update()

    def instalar(self):

        
        self.progreso_actual.set(0)

        self.graficos()
        self.crear_carpetas()
        self.copiar_archivos()
        self.crear_archivos_keys()
        self.crear_archivos_app()

        

        self.metodo_pyinstaller()
        
        self.mover_archivos()
        time.sleep(10)
        self.eliminar_archivos()
        self.proceso_db()
        self.write_version()
       


        self.exito()

    def metodo_pyinstaller(self):
        
        time.sleep(1)
        archivo_python = os.path.join(self.ubicacion_seleccionada, 'Administrador de contrasenas/app/admin_contrasenas.py')
        archivo_spec = 'admin_contrasenas.spec'
        ejecutar_pyinstaller(archivo_python, archivo_spec)
        with bloqueo:
            self.progreso_actual.set(60)  
            self.ventana.update()

    def proceso_db(self):
        self.proceso.configure(text="Copiando base de datos")   
        time.sleep(1)
        if self.check_version() is False:
            if self.radio_var.get() == 1:
                if self.ubicacion_database != self.ubicacion_seleccionada + '/Administrador de contrasenas/database':
                    store_passwords(self.ubicacion_database + '/datos_usuarios.db')

        with bloqueo:
            self.progreso_actual.set(90)
            self.ventana.update()
                      
    def mover_archivos(self):
        self.proceso.configure(text="Moviendo archivos")
        time.sleep(1)
        source_dir = os.path.join(self.ubicacion_seleccionada, 'Administrador de contrasenas/app/dist/admin_contrasenas')
        destination_dir = os.path.join(self.ubicacion_seleccionada, 'Administrador de contrasenas')

        contents = os.listdir(source_dir)

        for item in contents:
            source_item = os.path.join(source_dir, item)
            destination_item = os.path.join(destination_dir, item)
            shutil.move(source_item, destination_item)

        with bloqueo:
            self.progreso_actual.set(70)  
            self.ventana.update()

    def eliminar_archivos(self):
        self.proceso.configure(text="Eliminando archivos temporales")
        time.sleep(1)

        try:

            directory_path = os.path.join(self.ubicacion_seleccionada, 'Administrador de contrasenas/app')
            shutil.rmtree(directory_path)
            os.rmdir(directory_path)

        except PermissionError:
            print("[WinError 32] El proceso no tiene acceso al archivo porque está siendo utilizado por otro proceso")

        with bloqueo:
            self.progreso_actual.set(80)  
            self.ventana.update()

    def crear_carpetas(self):
        self.proceso.configure(text="Creando carpetas")
        time.sleep(1)  

        ruta_principal = os.path.join(
            self.ubicacion_seleccionada, "Administrador de contrasenas")
        os.makedirs(ruta_principal, exist_ok=True)

        ruta_basedatos = os.path.join(ruta_principal, "database")
        os.makedirs(ruta_basedatos, exist_ok=True)

        ruta_image = os.path.join(ruta_principal, "image")
        os.makedirs(ruta_image, exist_ok=True)

        ruta_respaldo = os.path.join(ruta_principal, "backup")
        os.makedirs(ruta_respaldo, exist_ok=True)

        ruta_version = os.path.join(ruta_principal, "version")
        os.makedirs(ruta_version, exist_ok=True)

        with bloqueo:
            self.progreso_actual.set(10)  
            self.ventana.update()

    def copiar_archivos(self):
        self.proceso.configure(text="Creando archivos de base de datos")
        time.sleep(1)

        def create_icon():
            icon_data = base64.b64decode(app_icon)

            ruta = self.ubicacion_seleccionada + '/Administrador de contrasenas/image/app-icon.ico'

            with open(ruta, 'wb') as f:
                f.write(icon_data)

        create_icon()
        ubicacion = Path(self.ubicacion_seleccionada + '/Administrador de contrasenas/database/codigo_acceso.db')
        try:
            if self.ubicacion_database != self.ubicacion_seleccionada + '/Administrador de contrasenas/database':
                
                archivo_basedatos = self.ubicacion_database
                ubicacion_db = self.ubicacion_seleccionada + '/Administrador de contrasenas/database' 
            
                for file in os.listdir(self.ubicacion_database):
                    shutil.copy2(os.path.join(self.ubicacion_database, file), ubicacion_db)

            if ubicacion.exists():
                print("Los archivos ya existen")

            else:
                db_codigo = open(self.ubicacion_seleccionada + '/Administrador de contrasenas/database/codigo_acceso.db', 'w')
                db_codigo.close()

                db_usuarios = open(self.ubicacion_seleccionada + '/Administrador de contrasenas/database/datos_usuarios.db', 'w')
                db_usuarios.close()
                
        except SameFileError:
            print("Los archivos ya existen")

        with bloqueo:
            self.progreso_actual.set(20)  
            self.ventana.update()

    def crear_archivos_keys(self):
        self.proceso.configure(text="Creando archivos de encriptacion")
        time.sleep(1)
        claves = {
        "PUBLIC_DB_KEY": public_key_pem.decode().replace('\n', ''),
        "PRIVATE_DB_KEY": private_key_pem.decode().replace('\n', ''),
        "PUBLIC_TABLE_KEY": public_key1_pem.decode().replace('\n', ''),
        "PRIVATE_TABLE_KEY": private_key1_pem.decode().replace('\n', '')
        }

        for key, value in claves.items():
            if value.startswith("-----BEGIN PUBLIC KEY-----") and "\n" not in value:
                claves[key] = value.replace("-----BEGIN PUBLIC KEY-----", "-----BEGIN PUBLIC KEY-----\n")

        for key, value in claves.items():
            if value.startswith("-----BEGIN PRIVATE KEY-----") and "\n" not in value:
                claves[key] = value.replace("-----BEGIN PRIVATE KEY-----", "-----BEGIN PRIVATE KEY-----\n")

        for key, value in claves.items():
            if value.endswith("-----END PUBLIC KEY-----"):
                claves[key] = value.replace("-----END PUBLIC KEY-----", "\n-----END PUBLIC KEY-----")

        for key, value in claves.items():
            if value.endswith("-----END PRIVATE KEY-----"):
                claves[key] = value.replace("-----END PRIVATE KEY-----", "\n-----END PRIVATE KEY-----")

        data = json.dumps(claves, separators=(',', ':'), indent=4)
        Path(self.ubicacion_seleccionada + '/Administrador de contrasenas/backup/keys.json').write_text(data)
        Path(self.ubicacion_seleccionada + '/Administrador de contrasenas/keys.json').write_text(data)

        with bloqueo:
            self.progreso_actual.set(30)  
            self.ventana.update()

    def crear_archivos_app(self):
        self.proceso.configure(text="Creando archivos para compilar")
        time.sleep(1)
        ruta_principal = os.path.join(
            self.ubicacion_seleccionada, "Administrador de contrasenas/app")
        os.makedirs(ruta_principal, exist_ok=True)

        ruta_client = os.path.join(ruta_principal, "client")
        os.makedirs(ruta_client, exist_ok=True)

        ruta_model = os.path.join(ruta_principal, "model")
        os.makedirs(ruta_model, exist_ok=True)

        def create(path,outside_text):
            main = ruta_principal + path

            with open(main, "w", encoding="utf-8") as file:
                    
                file.write(outside_text)

        def create_icon():
            icon_data = base64.b64decode(app_icon)

            ruta = ruta_principal + '/app-icon.ico'

            with open(ruta, 'wb') as f:
                f.write(icon_data)

        if self.check_version() is False:
            if self.radio_var.get() == 1:

                create('/admin_contrasenas.py', main_text)
                create('/model/__init__.py', '')
                create('/model/admin_dao.py', admin_dao_text)
                create('/model/conexion_db.py', conexion_db_text)
                create('/model/key.py', key_text)
                create('/client/__init__.py', '')
                create('/client/gui_app.py', gui_app_text)
                create_icon()
                


        with bloqueo:
            self.proceso.configure(text="Compilando archivos")
            self.progreso_actual.set(40)  
            self.ventana.update()
                
    def write_version(self):
        self.proceso.configure(text="Escribiendo version actual")
        time.sleep(1)
        version = self.ubicacion_seleccionada + '/Administrador de contrasenas/version/version.txt'
        archivo = Path(version)

        with open(version, "w") as file:
            texto= "Version 1.2.0"
            file.write(texto)
        with bloqueo:
            self.progreso_actual.set(100)  
            self.ventana.update()

    def renombrar_aplicacion(self, ruta_actual, nuevo_nombre): 

        ruta_absoluta = os.path.abspath(ruta_actual)

        ruta_directorio, nombre_archivo = os.path.split(ruta_absoluta)

        nombre_sin_extension, extension = os.path.splitext(nombre_archivo)

        nuevo_nombre_archivo = nuevo_nombre + extension

        nueva_ruta_absoluta = os.path.join(ruta_directorio, nuevo_nombre_archivo)

        os.rename(ruta_absoluta, nueva_ruta_absoluta)

    def crear_acceso_directo(self, nombre_acceso_directo, ruta_aplicacion):
        ruta_escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
        ruta_acceso_directo = os.path.join(ruta_escritorio, nombre_acceso_directo + ".lnk")

        shell = win32com.client.Dispatch("WScript.Shell")
        acceso_directo = shell.CreateShortcut(ruta_acceso_directo)
        acceso_directo.TargetPath = ruta_aplicacion
        acceso_directo.WorkingDirectory = os.path.dirname(ruta_aplicacion)
        acceso_directo.IconLocation = ruta_aplicacion
        acceso_directo.Save()

    def introduccion(self):

        def onclick(event=None):
            print("You clicked the button or pressed Enter")
            self.install_python()

        self.ventana.bind('<Return>', onclick)
        
        
        self.introduccion_frame = tk.Frame(
            self.ventana, width=600, height=600)
        self.introduccion_frame.grid(column=1, row=0)

        self.side_frame = tk.Frame(self.ventana, width=130, height=600)
        self.side_frame.grid(column=0, row=0)
        self.side_frame.grid_propagate(False)

        canvas = tk.Canvas(self.side_frame,width=130,bg="green" ,height=600)
        canvas.grid()
        

        imagen = Image.open(self.image)
        ancho = 130
        alto = 600
        imagen =  imagen.resize((ancho, alto), Image.LANCZOS)

        imagen_tk = ImageTk.PhotoImage(imagen)
        canvas.image = imagen_tk

        x = (130 - ancho) // 2
        y = (600 - alto) // 2

        
        canvas.create_image(x, y, anchor="nw", image=imagen_tk)
        text = "Created by"
        x = 50  # x-coordinate of text position
        y = 335  # y-coordinate of text position
        canvas.create_text(x, y, text=text, fill="White",font=(" Segoe 10"))

        text = "Edgar Arroyo"
        x = 58  # x-coordinate of text position
        y = 350  # y-coordinate of text position
        canvas.create_text(x, y, text=text, fill="White",font=(" Segoe 10"))


        self.introduccion_label = tk.Message(
            self.introduccion_frame,width=400, text="Bienvenido al asistente de instalacion del gestor de contraseñas\nlos pasos a continuacion te guiaran en el proceso de instalado,\nsi ya tienes alguna version instalada se actualizará.\nPresiona continuar para comenzar la instalación.")
        self.introduccion_label.grid(
            row=0, column=0, padx=(100, 0), pady=(0, 505))

        self.introduccion_button = ttk.Button(
            self.introduccion_frame, text="Continuar",width=10,command=self.install_python)
        self.introduccion_button.grid(
            row=0, column=0, padx=(273, 0), pady=(124, 0))

    def install_python(self):
        def onclick(event=None):
            print("You clicked the button or pressed Enter")
            self.ubicacion()

        self.ventana.bind('<Return>', onclick)

        if python_exists() is False:

            self.introduccion_frame.destroy()
            self.side_frame.destroy()

            self.upper_frame = tk.Frame(self.ventana,bg="#d9d9d9", width=600, height=70)
            self.upper_frame.grid(row=0, column=0)

            self.upper_frame.grid_propagate(False)

            self.title_label = tk.Label(self.upper_frame,bg="#d9d9d9", font=(" Segoe 10 bold"),text="Requisito Necesario")
            self.title_label.grid(row=0, column=0, padx=(0,200), pady=(10,0))

            self.title_message = tk.Message(self.upper_frame,bg="#d9d9d9",width=500,text="Es necesariao instalar lo siguiente para continuar con la instalación")
            self.title_message.grid(row=1, column=0, padx=(20,0), pady=(5,0))

            self.python_frame = tk.Frame(
                    self.ventana, width=600, height=600, )
            self.python_frame.grid(pady=(0,0))

                
            self.python_label = tk.Message(
                    self.python_frame, width=500,text="No tienes Python instalado en tu sistema operativo, preciona el boton debajo para instalarlo y poder seguir con la instalación. ")
            self.python_label.grid(
                    row=0, column=0, padx=(0, 20), pady=(13, 150))

            self.python_button = ttk.Button(
                    self.python_frame, text="Instalar Python", command=instalar_python)
            self.python_button.grid(
                    row=0, column=0, padx=(0, 0), pady=(0, 50))

            self.continuar_button = ttk.Button(
                    self.python_frame, text="Continuar",width=10,command=self.ubicacion)
            self.continuar_button.grid(
                    row=1, column=0, padx=(380, 0), pady=(75, 0))

        else:
            self.ubicacion()

    def ubicacion(self):
        def onclick(event=None):
            print("You clicked the button or pressed Enter")
            self.actualizar()

        self.ventana.bind('<Return>', onclick)

        if python_exists() is True:

            try:

                self.python_frame.destroy()

                self.count = self.count + 1 

                if self.count >= 2:
                    self.actualizar_frame.destroy()
                    self.side_frame.destroy()
                
                    
                self.upper_frame = tk.Frame(self.ventana,bg="#d9d9d9", width=600, height=70)
                self.upper_frame.grid(row=0, column=0)

                self.upper_frame.grid_propagate(False)

                self.title_label = tk.Label(self.upper_frame,bg="#d9d9d9", font=(" Segoe 10 bold"),text="Seleccionar ubicacion")
                self.title_label.grid(row=0, column=0, padx=(0,230), pady=(10,0))

                self.title_message = tk.Message(self.upper_frame,bg="#d9d9d9",width=500,text="A continuación selecciona donde se va a instalar el gestor de contraseñas")
                self.title_message.grid(row=1, column=0, padx=(20,0), pady=(5,0))

                self.ubicacion_frame = tk.Frame(
                    self.ventana, width=600, height=600,bg="#f0f0f0" )
                self.ubicacion_frame.grid(row=1)

                
                self.ubicacion_label = tk.Message(
                    self.ubicacion_frame, width=500,text="La ubicacion predeterminada es en archivos del programa, si decides cambiar la ubicacion recuerda que podria afectar el funcionamiento de algunas caracteristicas de la aplicacion." )
                self.ubicacion_label.grid(
                    row=0, column=0, padx=(0, 40), pady=(13, 150))

                self.ubicacion_entry = ttk.Entry(
                    self.ubicacion_frame, width=50)
                self.ubicacion_entry.grid(
                    row=0, column=0, padx=(0, 205), pady=(0, 50))

                self.ubicacion_entry.insert(0, self.ubicacion_seleccionada)

                self.ubicacion_button = ttk.Button(
                    self.ubicacion_frame, text="Seleccionar ubicacion",command=self.seleccionar_ubicacion)
                self.ubicacion_button.grid(
                    row=0, column=0, padx=(334, 0), pady=(0, 50))

                self.ubicacion_cont_button = ttk.Button(
                    self.ubicacion_frame, text="Continuar",width=10,command=self.actualizar)
                self.ubicacion_cont_button.grid(
                    row=1, column=0, padx=(380, 0), pady=(75, 0))

            except:
                self.introduccion_frame.destroy()
                self.side_frame.destroy()

                self.count = self.count + 1 

                if self.count >= 2:
                    self.actualizar_frame.destroy()
                
                    
                self.upper_frame = tk.Frame(self.ventana,bg="#d9d9d9", width=600, height=70)
                self.upper_frame.grid(row=0, column=0)

                self.upper_frame.grid_propagate(False)

                self.title_label = tk.Label(self.upper_frame,bg="#d9d9d9", font=(" Segoe 10 bold"),text="Seleccionar ubicacion")
                self.title_label.grid(row=0, column=0, padx=(0,230), pady=(10,0))

                self.title_message = tk.Message(self.upper_frame,bg="#d9d9d9",width=500,text="A continuación selecciona donde se va a instalar el gestor de contraseñas")
                self.title_message.grid(row=1, column=0, padx=(20,0), pady=(5,0))

                self.ubicacion_frame = tk.Frame(
                    self.ventana, width=600, height=600,bg="#f0f0f0" )
                self.ubicacion_frame.grid(row=1)

                
                self.ubicacion_label = tk.Message(
                    self.ubicacion_frame, width=500,text="La ubicacion predeterminada es en archivos del programa, si decides cambiar la ubicacion recuerda que podria afectar el funcionamiento de algunas caracteristicas de la aplicacion." )
                self.ubicacion_label.grid(
                    row=0, column=0, padx=(0, 40), pady=(13, 150))

                self.ubicacion_entry = ttk.Entry(
                    self.ubicacion_frame, width=50)
                self.ubicacion_entry.grid(
                    row=0, column=0, padx=(0, 205), pady=(0, 50))

                self.ubicacion_entry.insert(0, self.ubicacion_seleccionada)

                self.ubicacion_button = ttk.Button(
                    self.ubicacion_frame, text="Seleccionar ubicacion",command=self.seleccionar_ubicacion)
                self.ubicacion_button.grid(
                    row=0, column=0, padx=(334, 0), pady=(0, 50))

                self.ubicacion_cont_button = ttk.Button(
                    self.ubicacion_frame, text="Continuar",width=10,command=self.actualizar)
                self.ubicacion_cont_button.grid(
                    row=1, column=0, padx=(380, 0), pady=(75, 0))
        else:
            messagebox.showwarning("Requisito necesario","Es necesario que instales python para seguir con la instalación.")

    def actualizar(self):
        def onclick(event=None):
            print("You clicked the button or pressed Enter")
            self.encriptacion()

        self.ventana.bind('<Return>', onclick)

        self.ubicacion_frame.destroy()
        self.count = self.count + 1 


        if self.count1 >= 2:
            self.count1 = self.count1

        else:

            if self.count >= 2:
                self.count1 = 1
        if self.check_version() is False:
            if self.count1 >= 2:
                self.encriptacion_frame.destroy()
        else:
            if self.count1 >= 2:
                self.instalar_frame.destroy()

        self.title_label.configure(text="Ubicacion registro ")
        self.title_label.grid(row=0, column=0, padx=(0,150), pady=(10,0))
        self.title_message.configure(text="Selecciona la ubicacion del registro de tus contraseñas")
        self.title_message.grid(row=1, column=0, padx=(20,0), pady=(5,0))


        self.actualizar_frame = tk.Frame(
            self.ventana, width=600, height=600)
        self.actualizar_frame.grid()

        self.actualizar_label = tk.Message(
            self.actualizar_frame, width=500,text="Si anteriormente instalaste la aplicacion en otra ubicacion seleccionala a continuacion.\nSino preciona continuar.")
        self.actualizar_label.grid(
            row=0, column=0, padx=(0, 60), pady=(13, 150))

        self.actualizar_entry = ttk.Entry(
            self.actualizar_frame, width=50)
        self.actualizar_entry.grid(
            row=0, column=0, padx=(0, 205), pady=(0, 50))

        self.actualizar_entry.insert(
            0, self.ubicacion_database)

        self.continuar_button = ttk.Button(
            self.actualizar_frame, text="Seleccionar ubicacion",command=self.seleccionar_ubicacion_db)
        self.continuar_button.grid(
            row=0, column=0, padx=(334, 0), pady=(0, 50))

        self.continuar_button_cont_button = ttk.Button(
            self.actualizar_frame, text="Continuar", width=10,command=self.encriptacion)
        self.continuar_button_cont_button.grid(
            row=1, column=0, padx=(380, 0), pady=(75, 0))

        self.regresar_button = ttk.Button(
            self.actualizar_frame, text="Regresar",width=10 ,command=self.ubicacion)
        self.regresar_button.grid(
            row=1, column=0, padx=(0, 380), pady=(75, 0))

    def check_version(self):
        version = self.ubicacion_seleccionada + '/Administrador de contrasenas/version/version.txt'
        archivo =Path(version)

        if archivo.exists():
            with open(version, "r") as file:
                version = file.readlines()
                return version

        return False

    def encriptacion(self):
        def onclick(event=None):
            print("You clicked the button or pressed Enter")
            self.instalacion()

        self.ventana.bind('<Return>', onclick)


        if self.check_version() is False:

            self.actualizar_frame.destroy()
            self.count1 = self.count1 + 1
            

            if self.count2 >= 2:
                self.count2 = self.count2

            else:

                if self.count1 >= 2:
                    self.count2 = 1

            if self.count2 >= 2:
                self.instalar_frame.destroy()


            self.title_label.configure(text="Metodo de cifrado")
            self.title_label.grid(row=0, column=0, padx=(0,310), pady=(10,0))
            self.title_message.configure(text="Selecciona que metodo de cifrado quieres que se utilice para guardar tus contraseñas")
            self.title_message.grid(row=1, column=0, padx=(20,0), pady=(5,0))


            self.encriptacion_frame = tk.Frame(
                self.ventana, width=600, height=600)
            self.encriptacion_frame.grid()

            self.encriptacion_label = tk.Message(
                self.encriptacion_frame, width=600,text="Es recomendable actualizar al nuevo metodo de cifrado, pero si lo deseas puedes seguir usando el\nmetodo antigüo.")
            self.encriptacion_label.grid(
                row=0, column=0, padx=(0, 0), pady=(0, 120))


            self.new_encryption =ttk.Radiobutton(self.encriptacion_frame,variable= self.radio_var,value=1 ,text="Nuevo metodo de cifrado (recomendado)")
            self.new_encryption.grid(row=0, column=0, padx=(0, 250), pady=(0, 30))

            self.new_encryption_desc = tk.Message(self.encriptacion_frame,  width=500, text="El nuevo metodo usa cifrado asimetrico para incrementar la\nseguridad a la hora de guardar y acceder a tus contraseñas.")
            self.new_encryption_desc.grid(row=0, column=0, padx=(0, 105), pady=(20, 0))

            self.old_encryption = ttk.Radiobutton(self.encriptacion_frame,variable= self.radio_var,value=2 ,text="Antigüo metodo de cifrado")
            self.old_encryption.grid(row=0, column=0, padx=(0, 330), pady=(100, 0))

            self.old_encryption_desc = tk.Message(self.encriptacion_frame,  width=500, text="El viejo metodo usa cifrado simetrico lo que limita la \nseguridad a la hora de guardar y acceder a tus contraseñas.")
            self.old_encryption_desc.grid(row=0, column=0, padx=(0, 108), pady=(150, 0))

            self.continuar_encriptacion_button = ttk.Button(
                self.encriptacion_frame, text="Continuar",width=10,command=self.instalacion)
            self.continuar_encriptacion_button.grid(
                row=1, column=0, padx=(381, 0), pady=(90, 0))

            self.regresar_encriptacion_button = ttk.Button(
                self.encriptacion_frame, text="Regresar",width=10,command=self.actualizar)
            self.regresar_encriptacion_button.grid(
                row=1, column=0, padx=(0, 381), pady=(90, 0))
        else:
            self.instalacion()

    def instalacion(self):
        

        try:
            if self.radio_var.get() == 0:
                messagebox.showinfo("Seleccion necesaria", "Selecciona una opcion para la encriptacion de tus contraseñas.")

            else:

                def onclick(event=None):
                    print("You clicked the button or pressed Enter")
                    self.instalar()

                self.ventana.bind('<Return>', onclick)

                self.encriptacion_frame.destroy()

                self.count2 = self.count2 + 1

                self.title_label.configure(text="Instalar")
                self.title_label.grid(row=0, column=0, padx=(0,150), pady=(10,0))
                self.title_message.configure(text="A continuación comenzará la instalación")
                self.title_message.grid(row=1, column=0, padx=(20,0), pady=(5,0))


                self.instalar_frame = tk.Frame(
                    self.ventana, width=600, height=600)
                self.instalar_frame.grid()

                self.instalar_label = tk.Message(
                    self.instalar_frame,width=500, text="Presiona instalar para comenzar con la instalacion.")
                self.instalar_label.grid(
                    row=0, column=0, padx=(0, 250), pady=(15, 0))


                self.instalar_progreso = ttk.Progressbar (
                    self.instalar_frame,variable=self.progreso_actual, length=500,mode='determinate')

                self.progreso_label = tk.Message(
                    self.instalar_frame, width=100)
                

                self.boton_instalar = ttk.Button(
                    self.instalar_frame, text="Instalar", width=10,command=self.instalar)
                self.boton_instalar.grid(row=1, column=0, padx=(380, 0), pady=(240, 0))

                self.regresar_1_button = ttk.Button(
                    self.instalar_frame, text="Regresar", width=10,command= self.encriptacion)
                self.regresar_1_button.grid(
                    row=1, column=0, padx=(0,380), pady=(240, 0))

        except AttributeError:

            def onclick(event=None):
                print("You clicked the button or pressed Enter")
                self.instalar()

            self.ventana.bind('<Return>', onclick)

            print("Accediendo con version ")

            self.actualizar_frame.destroy()
            self.count1 = self.count1 + 1
            

            if self.count2 >= 2:
                self.count2 = self.count2

            else:

                if self.count1 >= 2:
                    self.count2 = 1

            self.title_label.configure(text="Instalar")
            self.title_label.grid(row=0, column=0, padx=(0,150), pady=(10,0))
            self.title_message.configure(text="A continuación comenzará la instalación")
            self.title_message.grid(row=1, column=0, padx=(20,0), pady=(5,0))


            self.instalar_frame = tk.Frame(
                    self.ventana, width=600, height=600)
            self.instalar_frame.grid()

            self.instalar_label = tk.Message(
                    self.instalar_frame,width=500, text="Presiona instalar para comenzar con la instalacion.")
            self.instalar_label.grid(
                    row=0, column=0, padx=(0, 250), pady=(15, 0))


            self.instalar_progreso = ttk.Progressbar (
                    self.instalar_frame,variable=self.progreso_actual, length=500,mode='determinate')

            self.progreso_label = tk.Message(
                    self.instalar_frame, width=100)
                

            self.boton_instalar = ttk.Button(
                    self.instalar_frame, text="Instalar", width=10,command=self.instalar)
            self.boton_instalar.grid(row=1, column=0, padx=(380, 0), pady=(240, 0))

            self.regresar_1_button = ttk.Button(
                    self.instalar_frame, text="Regresar", width=10,command= self.encriptacion)
            self.regresar_1_button.grid(
                    row=1, column=0, padx=(0,380), pady=(240, 0))

    def exito(self):
        self.check_var_dsk = tk.IntVar()
        self.check_var_ex = tk.IntVar()
        
        self.instalar_frame.destroy()
        self.upper_frame.destroy()

        self.exito_frame = tk.Frame(self.ventana, width=600, height=600)
        self.exito_frame.grid(column=1, row=0)
        self.exito_frame.grid_propagate(False)

        self.side_frame = tk.Frame(self.ventana, width=130, height=600)
        self.side_frame.grid(column=0, row=0)
        self.side_frame.grid_propagate(False)

        canvas = tk.Canvas(self.side_frame,width=130,bg="green" ,height=600)
        canvas.grid()

        imagen = Image.open(self.image)
        ancho = 130
        alto = 600
        imagen =  imagen.resize((ancho, alto), Image.LANCZOS)

        imagen_tk = ImageTk.PhotoImage(imagen)
        canvas.image = imagen_tk

        x = (130 - ancho) // 2
        y = (600 - alto) // 2

        
        canvas.create_image(x, y, anchor="nw", image=imagen_tk)
        text = "Created by"
        x = 50  # x-coordinate of text position
        y = 335  # y-coordinate of text position
        canvas.create_text(x, y, text=text, fill="White",font=(" Segoe 10"))

        text = "Edgar Arroyo"
        x = 58  # x-coordinate of text position
        y = 350  # y-coordinate of text position
        canvas.create_text(x, y, text=text, fill="White",font=(" Segoe 10"))


        self.exito_label = tk.Message(
            self.exito_frame, width=600,text="Instalacion completada con exito." )
        self.exito_label.grid(
            row=0, column=0, padx=(0, 0), pady=(0, 320))

        self.shortcut_dsk = ttk.Checkbutton(self.exito_frame, text="Agregar atajo al escritorio", variable=self.check_var_dsk)
        self.shortcut_dsk.grid(row=0, column=0, padx=(0, 0), pady=(0, 200))

        self.execute = ttk.Checkbutton(self.exito_frame, text="Abrir aplicacion al finalizar", variable=self.check_var_ex)
        self.execute.grid(row=0, column=0, padx=(0, 0), pady=(0, 100))

        self.close_button = ttk.Button(
            self.exito_frame, text="Terminar",width=10,command= self.terminar)
        self.close_button.grid(
            row=0, column=0, padx=(320, 0), pady=(350, 0))

    def variable_entorno(self):

        # Ruta al Registro del sistema
        HKEY_CURRENT_USER = winreg.HKEY_CURRENT_USER
        ENVIRONMENT_PATH = r"Environment"

        # Nombre y valor de la variable de entorno
        public_db_key = "Public_db_key"
        public_db_key_value = f"{public_key_pem.decode()}"

        # Nombre y valor de la variable de entorno
        private_db_key = "Private_db_key"
        private_db_key_value = f"{private_key_pem.decode()}"

        # Nombre y valor de la variable de entorno
        public_table_key = "Public_table_key"
        public_table_key_value = f"{public_key1_pem.decode()}"

        # Nombre y valor de la variable de entorno
        private_table_key = "Private_table_key"
        private_table_key_value = f"{private_key1_pem.decode()}"

        # Abrir la clave del Registro del sistema correspondiente a las variables de entorno
        clave_reg = winreg.OpenKey(
            HKEY_CURRENT_USER, ENVIRONMENT_PATH, 0, winreg.KEY_ALL_ACCESS)

        # Establecer el valor de la variable de entorno
        winreg.SetValueEx(clave_reg, public_db_key, 0,
                          winreg.REG_EXPAND_SZ, public_db_key_value)

        winreg.SetValueEx(clave_reg, private_db_key, 0,
                          winreg.REG_EXPAND_SZ, private_db_key_value)

        winreg.SetValueEx(clave_reg, public_table_key, 0,
                          winreg.REG_EXPAND_SZ, public_table_key_value)

        winreg.SetValueEx(clave_reg, private_table_key, 0,
                          winreg.REG_EXPAND_SZ, private_table_key_value)

        # Actualizar el entorno del proceso actual
        os.environ[public_db_key] = public_db_key_value
        os.environ[private_db_key] = private_db_key_value
        os.environ[public_table_key] = public_table_key_value
        os.environ[private_table_key] = private_table_key_value

        # Cerrar la clave del Registro del sistema
        winreg.CloseKey(clave_reg)

    def terminar(self):
        nombre_acceso_directo = "Administrador de contraseñas"
        ruta_aplicacion = os.path.join(self.ubicacion_seleccionada, 'Administrador de contrasenas/admin_contrasenas.exe')

        if self.check_var_dsk.get() == 1:
            self.crear_acceso_directo(nombre_acceso_directo,ruta_aplicacion)

        if self.check_var_ex.get() == 1:
            subprocess.run(ruta_aplicacion)


        self.ventana.destroy()

ventana = tk.Tk()

app = InstalacionApp(ventana)

if is_admin():
    ventana.mainloop()
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", "python", "main.py", None, 1)
