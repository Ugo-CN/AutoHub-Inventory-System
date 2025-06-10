import tkinter as tk


# -------------------------- #
# Re-used Functions
# -------------------------- #
def close_window(root):
    """Clears all widgets from the root window."""
    for widget in root.winfo_children():
        widget.destroy()

def leave_program(root,main_menu):
    root.destroy()

