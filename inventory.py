import pandas as pd
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from data import load_sales, save_sales
from data import load_inventory, save_inventory, save_cars



# ----------------------------- #
# Admin Menu Inventory Options
# ----------------------------- #

# ==VIEW INVENTORY==
def view_inventory(root):
    """Displays the inventory of cars WITH the CAR ID column."""

    # Create a new window specifically for viewing the car inventory
    inventory_window = tk.Toplevel(root)
    inventory_window.title("AUTOHUB") #Set window title
    inventory_window.geometry("1000x600") #Set window size

    # Add sub-title at the top of the window as "AutoHUb:"
    title_label = tk.Label(inventory_window, text="AutoHub:", font=("Serif", 14, "bold italic"))
    title_label.pack(pady=10)

    # Load the data from the inventory file and sort by Car ID
    df = load_inventory().sort_values(by="Car ID")

    # Create a table for the Inventory data
    inventory_table = ttk.Treeview(inventory_window, columns=list(df.columns), show="headings")
    for col in df.columns:
        inventory_table.heading(col,text=col)
        inventory_table.column(col, width=100, anchor="center")

    inventory_table.pack(fill=tk.BOTH, expand=True)

    # Insert rows
    for _, row in df.iterrows():
        inventory_table.insert("", tk.END, values=list(row)) #no index

    # Add vertical scrollbar
    scrollbar = ttk.Scrollbar(inventory_window, orient="vertical", command=inventory_table.yview)
    inventory_table.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Home Button
    home_button = tk.Button(inventory_window, text="Home", font=("Arial", 11),command=inventory_window.destroy)
    home_button.pack(pady=10)

#==ADD CAR==
def add_car(root):
    """Adds a new car to the inventory data."""

    # Create a new window for adding cars
    add_window = tk.Toplevel(root)
    add_window.title("AUTOHUB") #Set window title
    add_window.geometry("500x450") #Set window size

    # Subtitle
    window_subtitle = tk.Label(add_window, text="Add New Car:", font=("Serif", 14, "bold italic"))
    window_subtitle.pack(pady=15)

    # ===Create Form Frame to hold car details===
    form_frame = tk.Frame(add_window)
    form_frame.pack(pady=5)

    #Add Car ID label and Entry
    tk.Label(form_frame, text="Car ID (4 digits):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    carid_entry = tk.Entry(form_frame)
    carid_entry.grid(row=0, column=1, padx=10, pady=5)

    #Add Brand label and Entry
    tk.Label(form_frame, text="Brand:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    brand_entry = tk.Entry(form_frame)
    brand_entry.grid(row=1, column=1, padx=10, pady=5)

    #Add Model label and Entry
    tk.Label(form_frame, text="Model:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    model_entry = tk.Entry(form_frame)
    model_entry.grid(row=2, column=1, padx=10, pady=5)

    #Add Year label and dropdown (combo box for year)
    tk.Label(form_frame, text="Year:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    year_var = tk.StringVar()
    year_dropdown = ttk.Combobox(
        form_frame,
        textvariable=year_var,
        values=[str(y) for y in range(1990, 2031)],
        state="readonly"
    )
    year_dropdown.set("2025")
    year_dropdown.grid(row=3, column=1, padx=10, pady=5)

    #Add Price label and Entry
    tk.Label(form_frame, text="Price:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    price_entry = tk.Entry(form_frame)
    price_entry.grid(row=4, column=1, padx=10, pady=5)

    #Add Colour label and Entry
    tk.Label(form_frame, text="Colour:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    colour_entry = tk.Entry(form_frame)
    colour_entry.grid(row=5, column=1, padx=10, pady=5)

    #Add Status label and dropdown for status
    tk.Label(form_frame, text="Status:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
    status_var = tk.StringVar()
    status_dropdown = ttk.Combobox(form_frame, textvariable=status_var,
                                   values=["On Sale", "Unavailable"],
                                   state="readonly")

    status_dropdown.set("On Sale")
    status_dropdown.grid(row=6, column=1, padx=10, pady=5)

    #==Add Car Logic==
    def submit_car():

        #Retrieve Input Details
        car_id = carid_entry.get().strip()
        brand = brand_entry.get().capitalize().strip()
        model = model_entry.get().capitalize().strip()
        year = year_var.get().strip()
        price = price_entry.get().strip()
        colour = colour_entry.get().capitalize().strip()
        status = status_var.get()

        #Load Inventory Data
        df = load_inventory()

        # Error Check Each User Input
        if not car_id or len(car_id) != 4 or not car_id.isdigit():
            messagebox.showerror("ERROR", "Car ID must be exactly 4 digits.")
            return
        if car_id in df["Car ID"].values:
            messagebox.showerror("ERROR", "Car ID already exists.")
            return
        if not price.isdigit():
            messagebox.showerror("ERROR", "Price must be a number.")
            return
        if not brand or not model or not colour:
            messagebox.showerror("ERROR", "Please Fill in All Car Details")
            return

        # Create a dictionary for the new car with the user details
        new_car = {
            "Car ID": car_id,
            "Brand": brand,
            "Model": model,
            "Year": year,
            "Price": price,
            "Colour": colour,
            "Status": status
        }

        # Add the new car entry to the existing DataFrame
        df = pd.concat([df, pd.DataFrame([new_car])], ignore_index=True)
        save_inventory(df) # Save the new inventory DataFrame
        messagebox.showinfo("SUCCESS", f"Car {car_id} Successfully Added.")
        add_window.destroy()

    # Create Add button and Home button
    add_button = tk.Button(form_frame, text="Add Car", command=submit_car, font=("Arial", 12))
    add_button.grid(row=7, columnspan=2, pady=15)
    home_button = tk.Button(form_frame, text="Home", command=add_window.destroy, font=("Arial", 11), width=10)
    home_button.grid(row=8, columnspan=2, pady=15)

#==UPDATE CAR==
def update_car(root):
    """Updates an existing car's data in the inventory."""

    # Create a new window for updating cars
    update_window = tk.Toplevel(root)
    update_window.title("AUTOHUB")
    update_window.geometry("500x450")

    # Subtitle
    window_subtitle = tk.Label(update_window, text="Update Car Details:", font=("Serif", 14, "bold italic"))
    window_subtitle.pack(pady=15)

    # ===Create a frame to Hold Car ID Search label===
    carid_frame = tk.Frame(update_window)
    carid_frame.pack(pady=5)

    #Card ID search label
    tk.Label(carid_frame, text="Enter Car ID:").grid(row=0, column=0, padx=10, pady=10)
    entry_car_id = tk.Entry(carid_frame)
    entry_car_id.grid(row=0, column=1, padx=10)

    # ===== Create a frame to Hold Updatable Fields =====
    frame_updates = tk.Frame(update_window)

    #New Price Label and Entry
    tk.Label(frame_updates, text="New Price:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_price = tk.Entry(frame_updates)
    entry_price.grid(row=0, column=1, padx=5, pady=5)

    #New Colour Label and Entry
    tk.Label(frame_updates, text="New Colour:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_colour = tk.Entry(frame_updates)
    entry_colour.grid(row=1, column=1, padx=5, pady=5)

    #New Year Label and Dropdown option
    tk.Label(frame_updates, text="New Year:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    year_var = tk.StringVar()
    year_dropdown = ttk.Combobox(frame_updates, textvariable=year_var,
                                 values=[str(year) for year in range(1900, 2031)],
                                 state="readonly")
    year_dropdown.set("2025") #set year to be 2025
    year_dropdown.grid(row=2, column=1, padx=5, pady=5)

    #===Update Logic===
    def find_car():
        #Check if Car ID exists
        car_id = entry_car_id.get().strip()
        df = load_inventory()
        if car_id not in df["Car ID"].values:
            messagebox.showerror("ERROR", "Car ID Not Found")
            return

        # If Car ID found, Disable previous search and Car ID label.Show update options
        idx = df[df["Car ID"] == car_id].index[0] #Retrieves df index of inputted Car ID
        entry_car_id.config(state="disabled")
        btn_search.config(state="disabled")
        frame_updates.pack(pady=10) #Shows the update options (the section to update car details)

        def apply_update():
            new_price = entry_price.get().strip()
            new_colour = entry_colour.get().capitalize().strip()
            new_year = year_var.get()

            if new_price and not new_price.isdigit():
                messagebox.showerror("ERROR", "Price must be a number.")
                return

            if new_price:
                df.at[idx, "Price"] = new_price
            if new_colour:
                df.at[idx, "Colour"] = new_colour
            if new_year != "Select Year":
                df.at[idx, "Year"] = new_year

            save_inventory(df)
            messagebox.showinfo("Success", f"Car {car_id} updated successfully.")
            update_window.destroy()

        # Button to Apply Updates
        btn_apply = tk.Button(frame_updates, text="Apply Update")
        btn_apply.grid(row=3, columnspan=2, pady=10)  # Use grid, not pack
        btn_apply.config(command=apply_update)

        # Home Button
        btn_home = tk.Button(frame_updates, text="Home", font=("Arial", 11), command=update_window.destroy)
        btn_home.grid(row=4, columnspan=2, pady=10)

    #Button to Search
    btn_search = tk.Button(carid_frame, text="Search", command=find_car)
    btn_search.grid(row=1, column=0, columnspan=2, pady=5)


#==REMOVE CAR==
def remove_car(root):
    """Removes a car from inventory."""

    # New Window for Removing Cars
    remove_window = tk.Toplevel(root)
    remove_window.title("AUTOHUB")  # Set window title
    remove_window.geometry("450x300")  # Set window size

    # Subtitle
    title_label = tk.Label(remove_window, text="Delete Car Details:", font=("Serif", 14, "bold italic"))
    title_label.pack(pady=15)

    # ===== Frame for Car Id Entry =====
    input_frame = tk.Frame(remove_window)
    input_frame.pack(pady=5)

    # Car ID Label and Entry
    tk.Label(input_frame, text="Enter Car ID to Remove:").grid(row=0, column=0, padx=5, pady=5)
    entry_car_id = tk.Entry(input_frame)
    entry_car_id.grid(row=0, column=1, padx=5)

    #==Remove Car Logic==
    def delete_car():
        car_id = entry_car_id.get().strip()
        df = load_inventory()

        if car_id not in df["Car ID"].values:
            messagebox.showerror("ERROR", "Car ID Not Found")
            return

        # Remove car
        df = df[df["Car ID"] != car_id]
        save_inventory(df)
        messagebox.showinfo("Success", f"Car {car_id} removed successfully.")

    # Remove Button
    btn_remove = tk.Button(remove_window, text="Remove Car", command=delete_car)
    btn_remove.pack(pady=15)
    # Add Empty Space between buttons
    spacer = tk.Label(remove_window)
    spacer.pack(expand=True)
    # Home Button at Bottom
    home_button = tk.Button(remove_window, text="Home", font=("Arial", 11), command=remove_window.destroy)
    home_button.pack(pady=10, side="bottom")
