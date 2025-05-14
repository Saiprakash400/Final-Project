
# theme.py
import tkinter as tk
from tkinter import ttk

class UITheme:
    BG_COLOR = "#e0f7fa" 
    FONT = ("Segoe UI", 11)
    TITLE_FONT = ("Segoe UI", 15, "bold")
    BUTTON_FONT = ("Segoe UI", 10, "bold")

    BUTTON_COLOR = "#03A9F4"         
    BUTTON_HOVER = "#0288D1"        
    BUTTON_STYLE = "Accent.TButton"

    @staticmethod
    def apply_theme(root):
        root.configure(bg=UITheme.BG_COLOR)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            UITheme.BUTTON_STYLE,
            font=UITheme.BUTTON_FONT,
            background=UITheme.BUTTON_COLOR,
            foreground="white",
            padding=(8, 4),
            relief="flat",
            borderwidth=0
        )

        style.map(
            UITheme.BUTTON_STYLE,
            background=[("active", UITheme.BUTTON_HOVER)],
            relief=[("pressed", "flat"), ("!pressed", "flat")]
        )
