"""
Execute the mainloop if file name is main
"""

from client.app import App
from model.admin_dao import create_table, create_table_codigo
from protect.key_generation import KeyGeneration

def main():
    """
    Create the main loop for the app interface
    """
    app = App()
    app.mainloop()

def create_keys():
    """
    Calls the function to generate the keys for DB encryption
    """
    generator = KeyGeneration()
    
if __name__ == '__main__':
    """
    Calls the main methods to start the app
    """
    create_table()
    create_table_codigo()
    create_keys()
    main()
