import pandas as pd
import os
import tkinter as tk
from tkinter import messagebox
from data import *
from utils import *



# --------------------------------------#
# AUTHENTICATION SYSTEM
# --------------------------------------#

# == Sign up process ==
def sign_up(root,main_menu_callback):
    close_window(root)


    # Function to register a new user when 'Sign Up' button is pressed
    def register_user():
        username = user_entry.get()
        password = pass_entry.get()
        users = load_details(USERS_FILE)# Load the existing user details from the USERS_FILE

        if not username:
            messagebox.showerror("Error", "Please Username Cannot Be Empty")
            return
        if not password:
            messagebox.showerror("Error", "Please Password Cannot Be Empty")
            return

        # Check if the username already exists in the users dictionary
        if username in users:
            # If the username exists, show an error message
            messagebox.showerror("Error", "Username already exists.")
        else:
            # If username does not exist, add it to the dictionary with the password
            users[username] = password
            save_details(USERS_FILE, users)   # Save the updated user data back to the USERS_FILE
            messagebox.showinfo("Success", f"User '{username}' registered!")
            main_menu_callback()


    signup_frame = tk.Frame(root)
    signup_frame.pack(pady=30)

    # Place Title label at the top of the signup window
    tk.Label(signup_frame, text="Sign Up Details:", font=("Arial", 14, "italic")).pack(pady=10)

    # Button for the user registration
    tk.Button(signup_frame, text="Sign Up", command=register_user).pack(side="bottom", pady=10)

    # Label and entry field for creating a username
    tk.Label(signup_frame, text="Create Username").pack()
    user_entry = tk.Entry(signup_frame)
    user_entry.pack()

    # Label and entry field for creating a password
    tk.Label(signup_frame, text="Create Password").pack()
    pass_entry = tk.Entry(signup_frame, show="*")
    pass_entry.pack()

        # Back button at the top-left to go back to the previous screen (e.g., main menu)
    (tk.Button(signup_frame, text="Back", fg="gray", command=main_menu_callback)
     .pack(pady=20))

# == User login authentication functions ==
def user_login(root,main_menu_callback,user_menu_callback):
    close_window(root)

    # Title label for the user login screen
    tk.Label(root, text="User Login", font=("Arial", 18)).pack(pady=10)

    # Create a frame to hold the login widgets
    ulogin_frame = tk.Frame(root)
    ulogin_frame.pack(pady=50)

    # Label and entry field for the username input
    tk.Label(ulogin_frame, text="Username").pack()
    username_entry = tk.Entry(ulogin_frame,bg="lightgray", fg="black", insertbackground="black")
    username_entry.pack(pady=5)

    # Label and entry field for the password input
    tk.Label(ulogin_frame, text="Password").pack()
    password_entry = tk.Entry(ulogin_frame, show="*" , bg="lightgray", fg="black", insertbackground="black")
    password_entry.pack(pady=5)

    # Function to authenticate the user
    def user_auth():
        username = username_entry.get().strip() # Get username from user, and strip any extra spaces
        password = password_entry.get().strip()  # Get username from user, and strip any extra spaces

        # Load the user details from the USERS_FILE
        users = load_details(USERS_FILE)

        # Check that neither username of password field is empty
        if not username:
            messagebox.showerror("Input Error", "Please Username cannot be empty.")
            return

        if not password:
            messagebox.showerror("Input Error", "Please Password cannot be empty.")
            return

        # Check if the username exists and if the password matches
        if username in users and users[username] == password:
            ulogin_success(username)
            user_menu_callback(username)
            return

        messagebox.showerror("Unsuccessful Login", "Invalid Login\n(New Users,Please Sign Up First)")

    # Button to trigger the user authentication
    tk.Button(ulogin_frame, text="Login", command=user_auth).pack(pady=10)
    tk.Button(root, text="Back",fg="gray", command=main_menu_callback).place(x="10",y="10") # To return to the main menu


def ulogin_success(username):
    # Display a success message when login is successful
    messagebox.showinfo("Login Successful", f"User Login Successful: {username}")


# == Admin Login Authentication Functions ==
def admin_login(root,main_menu_callback,admin_menu_callback):

    close_window(root) # Close the previous window (if any).

    # Title Label for Admin Login screen
    tk.Label(root, text="Admin Login", font=("Arial", 18)).pack(pady=10)

    # Create a frame to hold the admin login widgets
    alogin_frame = tk.Frame(root)
    alogin_frame.pack(pady=50)

    # Instruction label explaining the format for Admin ID
    tk.Label(alogin_frame, text="Admin ID \n (Please enter 'AD' then the three digits e.g AD123)").pack()
    # Entry widget for the admin to enter their Admin ID
    admin_entry = tk.Entry(alogin_frame,bg="lightgray", fg="black", insertbackground="black")
    admin_entry.pack(pady=5)

    # Label and entry field for entering the password
    tk.Label(alogin_frame, text="Password").pack()
    pass_entry = tk.Entry(alogin_frame, show="*", bg="lightgray", fg="black", insertbackground="black")
    pass_entry.pack(pady=5)

    # Function to authenticate the admin when the "Login" button is pressed
    def admin_auth():
        admin_id = admin_entry.get()
        password = pass_entry.get()

        # Check that Admind ID field is not empty
        if not admin_id:
            messagebox.showerror("Input Error", "Please Admin ID cannot be empty.")
            return

        # Check if the Admin ID is valid using the valid_admin_id function
        if not valid_admin_id(admin_id):
            # Show an error if the Admin ID is not in the specified range (AD001–AD003)
            messagebox.showerror(
                "Error",
                "Admin ID can only be AD001–AD003.\n"
                "Contact Chukwubuikem to allow more IDs."
            )
            return

        # Check that Password field is not empty if ID is valid
        if not password:
            messagebox.showerror("Input Error", "Please Password cannot be empty.")
            return

        # Load the existing admin details from a file
        admins = load_details(ADMINS_FILE)

        # Check if the Admin ID exists in the loaded data
        if admin_id in admins:
            if admins[admin_id] == password:
                alogin_success(admin_id) # Show a success message if login is successful
                admin_menu_callback(admin_id) # Open the admin menu
            else:
                messagebox.showerror("Error", "Incorrect Password.") # Show error if password is incorrect
        else:
         # Allow new admin registration if the Admin ID does not exist
            if messagebox.askyesno("New Admin", f"Admin ID {admin_id} not found. Register as new admin?"):
                admins[admin_id] = password  # Add the new admin with passwrod to the admin list
                save_details(ADMINS_FILE, admins) # Save the new admin data to the file
                messagebox.showinfo("Registered", f"Admin {admin_id} Registered!")
                admin_menu_callback(admin_id) # Open the admin menu for the newly registered admin

    # Button to trigger the admin authentication process
    tk.Button(alogin_frame, text="Login", command=admin_auth).pack(pady=5)

    # Back button at the top-left to return to the main menu
    tk.Button(root, text="Back",fg="gray", command=main_menu_callback).place(x="20",y="20")

def alogin_success(admin_id):
    # Display a success message upon successful admin login
    messagebox.showinfo("Login Successful", f"Admin Login Successful: {admin_id}")