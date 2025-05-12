# theme.py
import tkinter as tk
from tkinter import ttk

class UITheme:
    BG_COLOR = "#f9f9f9"
    FONT = ("Segoe UI", 11)
    TITLE_FONT = ("Segoe UI", 14, "bold")
    BUTTON_FONT = ("Segoe UI", 11, "bold")

    BUTTON_COLOR = "#4CAF50"
    BUTTON_HOVER = "#45a049"
    BUTTON_STYLE = "Accent.TButton"

    @staticmethod
    def apply_theme(root):
        root.configure(bg=UITheme.BG_COLOR)

        style = ttk.Style()
        style.theme_use("clam")  # smoother and modern look
        style.configure(
            UITheme.BUTTON_STYLE,
            font=UITheme.BUTTON_FONT,
            background=UITheme.BUTTON_COLOR,
            foreground="white",
            padding=8,
            borderwidth=0
        )
        style.map(
            UITheme.BUTTON_STYLE,
            background=[("active", UITheme.BUTTON_HOVER)],
            relief=[("pressed", "flat"), ("!pressed", "flat")]
        )
