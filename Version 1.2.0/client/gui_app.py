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
    """
    Esta funcion genera una contrasena segura
    """
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
        ventana.iconbitmap('image/icono_candado.ico')
        style = ThemedStyle(ventana)

        ventana.geometry("310x250")

        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - \
            (ventana.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - \
            (ventana.winfo_height() // 2)

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
        self.ventana.iconbitmap('image/icono_candado.ico')
        self.style = ThemedStyle(self.ventana)

        self.ventana.geometry("310x250")

        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - \
            (self.ventana.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - \
            (self.ventana.winfo_height() // 2)

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
        ventana.iconbitmap('image/icono_candado.ico')
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
        ventana.iconbitmap('image/icono_candado.ico')
        style = ThemedStyle(ventana)
        ventana.geometry("310x160")

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
