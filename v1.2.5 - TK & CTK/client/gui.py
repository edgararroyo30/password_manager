"""
All the sections in the menu 
"""
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from ttkthemes import ThemedStyle
from client.frame_builder import FrameBuilder
from model.admin_dao import cuenta_id, listar_usuarios, save, user
from protect.password_generator import generate_password


class Gui():
    """
    Creates the main GUI
    """
    main_color = "black"
    text_color = "#ffffff"
    hover_color = '#808080'
    label_font = ("Segoe UI", 11, "bold")
    label_foreground = 'black'

    def __init__(self, frame):
        """
        Stablish the frame that is given as the self.frame and call main content functions
        """
        self.frame = frame
        self.detached_items = []
        self.content()

    def styles(self):
        """
        Defines the styles for ttk objects

        """
        self.style = ThemedStyle(self.frame)
        self.style.set_theme("equilux")
        self.style.configure("TButton", width=10, font=('Segoe UI', 8),
                             cursor='hand2', focuscolor='none', borderwidth=2,
                             bd=2, relief="solid", anchor='center',
                             highlightcolor='#35BD6F', highlightbackground='#35BD6F')
        
    def table(self, frame):
        """
        Creates a ttk Treeview to store user's data
        """
        self.tabla = ttk.Treeview(frame,
                                  column=('Web Site', 'Username', 'Password'))
        self.tabla.grid(row=4, column=0, columnspan=3,
                        sticky='nse', padx=10, pady=(0, 10))

        scroll = ttk.Scrollbar(frame,
                                    orient='vertical', command=self.tabla.yview)
        scroll.grid(row=4, column=2, padx=(
            1, 10), pady=(0, 10), sticky='nse')
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.heading('#1', text='Web Site')
        self.tabla.heading('#2', text='Username')
        self.tabla.heading('#3', text='Password')

        self.tabla.column("#0", width=0, stretch=False)
        self.tabla.config(displaycolumns=(
            'Web Site', 'Username', 'Password'))
        self.update_table()

    def update_table(self):
        children = self.tabla.get_children()
        

        if not children:

            try:
                for p in listar_usuarios(0):

                    self.tabla.insert('', 0,iid=p[0],
                       values=(p[1], p[2], p[3]))
            except TypeError as e:
                if "'NoneType' object is not iterable" in str(e):
                    print("Error: Tried to iterate on a None object.")
                else:
                    print(f"Unexpected error: {e}")
        else:
            try:
                last_item = self.tabla.get_children()[0]

                for p in listar_usuarios(int(last_item)):

                    self.tabla.insert('', 0, iid=p[0],
                       values=(p[1], p[2], p[3]))
            except TypeError as e:
                if "'NoneType' object is not iterable" in str(e):
                    print("Error: Tried to iterate on a None object.")
                else:
                    print(f"Unexpected error: {e}")

    def content(self):
        """
        Creates the main frame where table and buttons are stored
        """
        content_frame = FrameBuilder(self.frame)
        content_frame.configure( width=624, height=250)
        content_frame.grid(row=0, column=0, padx=(0, 0), pady=(0, 0))

        boton_nuevo = ttk.Button( content_frame, text='Add User', command=self.new_user,width=15)

        boton_nuevo.grid(row=3, column=2,
                              padx=(2, 10), pady=(10, 2))

        mi_busqueda = tk.StringVar()
        entry_buscar = ttk.Entry(content_frame, textvariable=mi_busqueda)
        entry_buscar.config(width=25, font=('Segoe UI', 9))
        entry_buscar.grid(
            row=3, padx=(250, 0), pady=(10, 2), columnspan=1)

        def search(*args):
            self.search_and_highlight(self.tabla, mi_busqueda.get())

        mi_busqueda.trace_add("write", search)

        boton_buscar = ttk.Button(content_frame, text='Search', command=search)

        boton_buscar.grid(row=3, column=1,
                               padx=(2, 0), pady=(10, 2))

        self.label_usuarios = ttk.Label(content_frame)
       
        self.label_usuarios.grid(row=3, padx=(10, 180), pady=(12, 2))

        self.update_users_count()

        self.table(content_frame)

        self.styles()

    def update_users_count(self):
        user_count = (f"{cuenta_id()} saved passwords")
        self.label_usuarios.config(
            width=30, font=('Segoe UI', 10, 'bold'),text=user_count)

    def new_user(self):
        """
        Window for new users
        """
        new_user_window = tk.Toplevel(self.frame)
        new_user_window.config(background=self.style.lookup('TFrame', 'background'))
        new_user_window.title('Add User')
        new_user_window.iconbitmap('image/app-icon.ico')
        style = ThemedStyle(new_user_window)

        new_user_window.geometry("310x250")

        x = self.frame.winfo_x() + (self.frame.winfo_width() // 2) - \
            (new_user_window.winfo_width() // 2)
        y = self.frame.winfo_y() + (self.frame.winfo_height() // 2) - \
            (new_user_window.winfo_height() // 2)

        new_user_window.geometry("+{}+{}".format(x, y))

        new_user_window.lift()

        new_user_window.overrideredirect(False)

        def save_data():
            
            user_data = user(
                self.mi_sitio_web_add.get(),
                self.mi_nombre_usuario_add.get(),
               self.mi_contrasena_add.get())
            save(user_data)
            new_user_window.destroy()
            self.update_table()
            self.update_users_count()

        def destroy():
            new_user_window.destroy()

        def new_user_content():

            label_sitio_web = ttk.Label(new_user_window, text='Web site')
            style.configure(style='Equilux.TLabel')
            label_sitio_web.config(
            width=17, font=('Segoe UI', 10))
            label_sitio_web.grid(row=0, padx=(1, 10), pady=(14, 4))

            label_nombre_usuario = ttk.Label(
            new_user_window, text='Username ')
            style.configure(style='Equilux.TLabel')
            label_nombre_usuario.config(
            width=17, font=('Segoe UI', 10))
            label_nombre_usuario.grid(row=2, padx=(1, 10), pady=(14, 4))

            label_contraseña = ttk.Label(new_user_window, text='Password ')
            style.configure(style='Equilux.TLabel')
            label_contraseña.config(
            width=17, font=('Segoe UI', 10))
            label_contraseña.grid(row=4, padx=(1, 10), pady=(14, 4))

        
            self.mi_sitio_web_add = tk.StringVar()

            entry_sitio_web = ttk.Entry(
            new_user_window, textvariable=self.mi_sitio_web_add)
            style.configure(style='Equilux.TEntry')
            entry_sitio_web.config(width=30, font=('Segoe UI', 12))
            entry_sitio_web.grid(
            row=1, padx=(15, 16), columnspan=3)

            self.mi_nombre_usuario_add = tk.StringVar()

            entry_nombre_usuario = ttk.Entry(
            new_user_window, textvariable=self.mi_nombre_usuario_add)
            style.configure(style='Equilux.TEntry')
            entry_nombre_usuario.config(width=30,
                                    font=('Segoe UI', 12))
            entry_nombre_usuario.grid(
            row=3, padx=(16, 16), columnspan=3)

            mi_contrasena = generate_password()
            self.mi_contrasena_add = tk.StringVar()

            entry_contrasena = ttk.Entry(
            new_user_window, textvariable=self.mi_contrasena_add)
            entry_contrasena.insert(0, mi_contrasena)
            style.configure(
            style='Equilux.TEntry')

            entry_contrasena.config(width=30,
                                font=('Segoe UI', 12))
            entry_contrasena.grid(
            row=5, padx=(16, 16), columnspan=3)

            boton_guardar = ttk.Button(
            new_user_window, text='Save', command=save_data)

            style.configure("RoundedButton.TButton", width=25, font=('Segoe UI', 12, 'bold'),
                        cursor='hand2', focuscolor='none', borderwidth=2,
                        bd=2, relief="solid", anchor='center',
                        highlightcolor='#35BD6F', highlightbackground='#35BD6F')

            boton_guardar.grid(
            row=6, column=0,  padx=(30, 10), pady=(14, 10))

            boton_cancelar = ttk.Button(
            new_user_window, text='Cancel', command=destroy)

            style.configure("RoundedButton.TButton", width=25, font=('Segoe UI', 12, 'bold'),
                        cursor='hand2', focuscolor='none', borderwidth=2,
                        bd=2, relief="solid", anchor='center',
                        highlightcolor='#35BD6F', highlightbackground='#35BD6F')

            boton_cancelar.grid(
            row=6, column=1,  padx=(0, 20), pady=(14, 10))

        new_user_content()




    def search_and_highlight(self, tree, search_string):
        
        if search_string == "":
            for item in self.detached_items:
                tree.reattach(item,'','end')
        else:

            for item in self.detached_items:
                tree.reattach(item,'','end')

            for item in tree.get_children():
                if search_string.lower() in str(tree.item(item)["values"]).lower():
                    tree.reattach(item,'','end')

                else:
                    self.detached_items.append(item)
                    tree.detach(item)
                

