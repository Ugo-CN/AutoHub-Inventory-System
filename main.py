# Standard library imports
import os
from datetime import datetime

# Third-party library imports
import pandas as pd

# Tkinter GUI components
import tkinter as tk
from tkinter import messagebox, ttk

# Local application imports
from auth import sign_up, user_login, admin_login
from showroom import *
from inventory import *
from sales import *
from data import create_inventory_file, create_sales_file, create_cars_file
from utils import *


# -------------------------------------- #
#  AutoHub Menus
# ---------------------------------------#
root = tk.Tk()
root.title("AUTOHUB INVENTORY")
root.geometry("600x400")

def main_menu():
    close_window(root) # Close the current window (if any)

    # Title label for the main menu at the top of the window
    tk.Label(root, text="Welcome to AutoHub", font=("Helvetica", 16, "bold")).pack(pady=20)

    # Button for user login
    tk.Button(root, text="User", width=30, command=lambda: user_login(root, main_menu,user_menu)).pack(pady=5)
    # Button for admin login
    tk.Button(root, text="Admin", width=30, command=lambda: admin_login(root,main_menu,admin_menu)).pack(pady=5)
    # Button to exit the program
    tk.Button(root, text="Leave", width=30, command=lambda: leave_program(root,main_menu)).pack(pady=50)

    # Sign-up option at the bottom for new users
    signup_frame = tk.Frame(root)
    signup_frame.pack(pady=20)

    tk.Label(signup_frame, text="New user?").pack(side="left")
    tk.Button(signup_frame, text=" Sign up", fg="blue", font="italic", cursor="plus", command=lambda root=root: sign_up
    (root, main_menu)).pack(side="left")

def user_menu(username):
    close_window(root) # Close any existing window

    # Title label for the user menu
    tk.Label(root, text=f"Welcome, {username}", font=("Arial", 16)).pack(pady=10)

    # Buttons for user options
    tk.Button(root, text="View Cars", width=30, command=lambda: view_cars(root)).pack(pady=5)
    tk.Button(root, text="Search Car", width=30, command=lambda: search_cars(root,username)).pack(pady=5)
    tk.Button(root, text="Sort Cars", width=30, command=lambda: sort_cars(root,username)).pack(pady=5)

    # Back button to return to the main menu
    tk.Button(root, text="Back to Home Menu", width=30, command=main_menu).pack(pady=70)

def admin_menu(admin_id):
    close_window(root) # Close any existing window

    tk.Label(root,text=f" Welcome, {admin_id}",font=("Arial",16)).pack(pady=10)

    # Create a container frame for organizing the UI layout
    admin_frame = tk.Frame(root)
    admin_frame.pack()

    # Create left and right frames within the container
    left_frame = tk.Frame(admin_frame)
    right_frame = tk.Frame(admin_frame)

    # Grid the left and right frames
    left_frame.grid(row=0, column=0, padx=40, pady=20, sticky="n")
    right_frame.grid(row=0, column=1, padx=40, pady=20, sticky="n")

    # Left-side buttons for admin functions
    tk.Button(left_frame, text="View Inventory", width=20, command=lambda: view_inventory(root)).pack(pady=10)
    tk.Button(left_frame, text="Add Car", width=20, command=lambda: add_car(root)).pack(pady=10)
    tk.Button(left_frame, text="Remove Car", width=20, command=lambda: remove_car(root)).pack(pady=10)
    tk.Button(left_frame, text="Update Car", width=20, command=lambda: update_car(root)).pack(pady=10)

    # Right-side buttons for admin sales functions
    tk.Button(right_frame, text="Record Sale", width=20, command=lambda: record_sale(root)).pack(pady=10)
    tk.Button(right_frame, text="View Sales", width=20, command=lambda: sales_overview(root)).pack(pady=10)

    # Back button at the bottom of the screen to return to the home menu
    tk.Button(root, text="Back to Home Menu", width=30, command=main_menu).pack(pady=40)



if __name__ == "__main__":
    # ------------------------- #
    # Startup initialization
    # ------------------------- #
    create_inventory_file()
    create_sales_file()
    create_cars_file()

    # ------------------------------ #
    # Run Main Loop
    # ------------------------------ #
    main_menu()
    root.mainloop()
