"""
Executes the the app and creates db tables if not exists
"""

import customtkinter as ctk
from model.admin_dao import crear_tabla, create_table_codigo
from client.gui_app import Frame


def main():
    """
    Loads all the GUI interface and creates the mainloop
    """
    root = ctk.CTk()
    root.title('Administrador de contraseñas')
    root.iconbitmap('image/app-icon.ico')
    root.resizable(0, 0)

    app = Frame(root=root)

    app.mainloop()


if __name__ == '__main__':
    create_table_codigo()
    crear_tabla()
    main()
