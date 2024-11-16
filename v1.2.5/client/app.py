"""
Create the Graphic user interface 
"""

import customtkinter as ctk
from client.gui import Gui
import os


class App(ctk.CTk):
    """
    Call the main GUI modules and methods,
    Inherit from ctk.CTk to display the interface
    """

    def __init__(self):
        super().__init__()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        

        self.title('Password Manager')
        self.geometry("624x280")
        self.resizable(0, 0)
        self.iconbitmap(os.path.join(base_dir,'..','image', 'app-icon.ico')) #Reference to found the image on the working directory
        self.configure(fg_color="Black")
        Gui(self)
