"""
Create the Graphic user interface 
"""

import customtkinter as ctk
from client.gui import Gui


class App(ctk.CTk):
    """
    Call the main GUI modules and methods,
    Inherit from ctk.CTk to display the interface
    """

    def __init__(self):
        super().__init__()

        self.title('Password Manager')
        self.geometry("624x280")
        self.resizable(0, 0)
        self.iconbitmap('image/app-icon.ico')
        self.configure(fg_color="Black")
        Gui(self)
