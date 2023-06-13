import customtkinter as ctk
from model.admin_dao import crear_tabla, create_table_codigo
from client.gui_app import Frame


def main():
    root = ctk.CTk()
    root.title('Administrador de contraseñas')
    root.iconbitmap('image/icono_candado.ico')
    root.resizable(0, 0)

    app = Frame(root=root)

    app.mainloop()


if __name__ == '__main__':
    create_table_codigo()
    crear_tabla()
    main()
