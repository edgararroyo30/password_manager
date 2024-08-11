"""
All the sections in the menu 
"""
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from client.frame_builder import FrameBuilder


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
        Stablish the frame that is given as the self.frame
        """
        self.frame = frame
        self.searchbar()
        self.content()

    def searchbar(self):
        """
        Creates de search bar including the buttons to search and add an account
        And the count of current account on the DB
        """
        search_frame = FrameBuilder(self.frame)
        search_frame.configure(
            width=624, height=40, fg_color=self.main_color)
        search_frame.grid(
            row=0, column=0, padx=0, pady=(10, 0))

        search_entry = ctk.CTkEntry(search_frame)
        search_entry.configure(border_color=self.text_color, width=250, height=20,
                               bg_color=self.main_color, text_color=self.text_color,
                               placeholder_text="", placeholder_text_color=self.text_color,
                               font=("Segoe UI", 9, "bold"), fg_color=self.main_color, border_width=1)
        search_entry.grid(row=0, column=1, padx=(
            70, 0), pady=(0, 0))

        search_button = ctk.CTkButton(search_frame)
        search_button.configure(width=30, bg_color=self.main_color,
                                hover_color=self.hover_color, height=2,
                                text="  Search  ", text_color=self.text_color,
                                font=("Segoe UI", 9, "bold"),  fg_color=self.main_color)
        search_button.grid(row=0, column=3, padx=(
            0, 60), pady=(0, 0))

        add_button = ctk.CTkButton(search_frame)
        add_button.configure(width=30, bg_color=self.main_color,
                             hover_color=self.hover_color, height=2,
                             text="Add account", text_color=self.text_color,
                             font=("Segoe UI", 9, "bold"),  fg_color=self.main_color)
        add_button.grid(row=0, column=3, padx=(
            80, 0), pady=(0, 0))

        saved_label = ctk.CTkLabel(search_frame)
        saved_label.configure(
            text="Saved Passwords", text_color=self.text_color,  font=("Segoe UI", 9, "bold"),
            fg_color=self.main_color)
        saved_label.grid(
            row=0, column=0, padx=(70, 0), pady=(0, 0))

    def content(self):
        """
        Creates the table where the content is located
        Includes all main interactions to modify, delete and copy account data
        """
        content_frame = FrameBuilder(self.frame)
        content_frame.configure(
            fg_color=self.main_color, width=624, height=250)
        content_frame.grid(row=3, column=0, padx=(0, 0), pady=(0, 0))

        scrollable_frame = ctk.CTkScrollableFrame(content_frame)
        scrollable_frame.configure(fg_color='white', width=580, height=150)
        scrollable_frame.grid(row=2, padx=(11, 0), pady=(0, 0))

        website_label = ctk.CTkLabel(content_frame)
        website_label.configure(fg_color=self.label_foreground,
                                text='Website', width=50, height=5,  font=self.label_font)
        website_label.grid(row=1, column=0, padx=(0, 460), pady=(5, 5))

        user_label = ctk.CTkLabel(content_frame)
        user_label.configure(fg_color=self.label_foreground,
                             text='Username', width=50, height=5,  font=self.label_font)
        user_label.grid(row=1, column=0, padx=(0, 0), pady=(5, 5))

        password_label = ctk.CTkLabel(content_frame)
        password_label.configure(fg_color=self.label_foreground,
                                 text='Password', width=50, height=5,  font=self.label_font)
        password_label.grid(row=1, column=0, padx=(500, 0), pady=(5, 5))
