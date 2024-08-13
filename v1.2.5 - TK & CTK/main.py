"""
Execute the mainloop if file name is main
"""

from client.app import App
from model.admin_dao import create_table, create_table_codigo

def main():
    """
    Create the main loop for the app interface
    """
    app = App()
    app.mainloop()


if __name__ == '__main__':
    create_table()
    create_table_codigo()
    main()
