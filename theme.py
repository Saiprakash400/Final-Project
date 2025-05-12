import tkinter as tk
from tkinter import ttk

class UITheme:
    BG_COLOR = "#f0f0f0"
    FONT = ("Arial", 12)
    TITLE_FONT = ("Arial", 14, "bold")
    BUTTON_STYLE = "Accent.TButton"

    @staticmethod
    def apply_theme(root):
        root.configure(bg=UITheme.BG_COLOR)
        style = ttk.Style()
        style.theme_use("default")
        style.configure(UITheme.BUTTON_STYLE, font=("Arial", 11, "bold"), background="#4CAF50", foreground="white", padding=6)
        style.map(UITheme.BUTTON_STYLE, background=[('active', '#45a049')])
