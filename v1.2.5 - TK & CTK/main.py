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
    generator = KeyGeneration()
    
if __name__ == '__main__':
    create_table()
    create_table_codigo()
    create_keys()
    main()
