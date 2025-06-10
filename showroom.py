import pandas as pd
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from data import load_inventory, save_inventory, save_cars



# -------------------------- #
# User Menu Showroom Options
# -------------------------- #

#== VIEW CARS==
def view_cars(root):
    """Displays cars in the inventory file as a table but without the 'Car ID' column."""

    # Create a new window specifically for viewing the car inventory table
    cars_window = tk.Toplevel(root)
    cars_window.title("AUTOHUB") # Sets the tile of the window
    cars_window.geometry("1000x600") # Sets the size of the search window

    # Add the sub-title at the top of the car window as "AutoHub Cars:"
    window_subtitle = tk.Label(cars_window, text="AutoHub Cars:", font=("Serif", 14, "bold italic"))
    window_subtitle.pack(pady=10)

    # Load the data from the inventory file and remove the "Car ID" column
    df = load_inventory().drop(columns=["Car ID"])

    # Create a car table( using tree view) and set the columns to be same as the inventory data frame columns
    car_table = ttk.Treeview(cars_window, columns=list(df.columns), show="headings")
    for col in df.columns:
        car_table.heading(col, text=col) #iterate over columns and set each column header in table to be same as df columns
        car_table.column(col, width=100, anchor="center")

    # Add new rows to the bottom of the car table and start index from 1 instead of 0
    for idx, row in df.iterrows():
        # Insert row data without index to maintain correct column alignment
        car_table.insert("", "end", values=tuple(row))

    # Add the table(tree view) to the cars window and make it exapnd to empty spaces
    car_table.pack(fill="both", expand=True)

    # Add a vertical scrollbar to the  tree view and link it to the tbale
    scrollbar = ttk.Scrollbar(cars_window, orient="vertical", command=car_table.yview)
    car_table.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Home button to take you back to the user menu(i.e closes the window)
    home_button = tk.Button(cars_window, text="Home", font=("Arial", 11), command=cars_window.destroy)
    home_button.pack(pady=20)

#==SEARCH CARS==
def search_cars(root,username):

    # Creates a new window to search through the cars
    search_window = tk.Toplevel(root)
    search_window.title("AUTOHUB")   # Sets the tile of the window
    search_window.geometry("800x600")  # Sets the size of the search window

    # Add sub-title at the top of the window as "Search Cars"
    window_subtitle = tk.Label(search_window, text="Search Cars:", font=("Serif", 14, "bold italic"))
    window_subtitle.pack(pady=10)

    # Create a parent search frame to hold both the left and right search input sections
    search_frame = tk.Frame(search_window)
    search_frame.pack(pady=10)

    # -- Left input section (Brand and Year)--
    left_frame = tk.Frame(search_frame)
    left_frame.grid(row=0, column=0, padx=10)

    # Create labels and entries for Brand and dropdown list for Year
    tk.Label(left_frame, text="Brand:", font=("Arial", 12)).grid(row=0, column=0, sticky="e")
    brand_entry = tk.Entry(left_frame) # Create brand entry in the left frame
    brand_entry.grid(row=0, column=1, padx=5)

    tk.Label(left_frame, text="Year:", font=("Arial", 12)).grid(row=1, column=0, sticky="e")
    # Dropdown (Combobox) instead of entry for the car's year (also in the left frame)
    year_entry = ttk.Combobox(left_frame, values=[str(i) for i in range(1990, 2031)],state="readonly")
    year_entry.grid(row=1, column=1, padx=5)

    # -- Right input section (Min Price, Max Price)--
    right_frame = tk.Frame(search_frame)
    right_frame.grid(row=0, column=1, padx=10)

    # Create labels and entries for Min and Max Price
    tk.Label(right_frame, text="Min Price:", font=("Arial", 12)).grid(row=0, column=0, sticky="e")
    min_price_entry = tk.Entry(right_frame) # Create min price entry in the right frame
    min_price_entry.grid(row=0, column=1, padx=5)

    tk.Label(right_frame, text="Max Price:", font=("Arial", 12)).grid(row=1, column=0, sticky="e")
    max_price_entry = tk.Entry(right_frame) # Create max price entry in the right frame
    max_price_entry.grid(row=1, column=1, padx=5)

    # --Create another frame to hold the Treeview (table) displaying search results--
    results_frame = tk.Frame(search_window)
    results_frame.pack(pady=(10, 0), fill=tk.BOTH, expand=True)
    results_table = ttk.Treeview(results_frame, show="headings", height=20)
    results_table.pack(fill=tk.BOTH, expand=True)

    #Add Scrollbar
    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=results_table.yview)
    results_table.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # ==== Search Logic ====
    def search_logic():

        #Get and clean user input values for brand, year, and price range
        brand = brand_entry.get().strip().lower()
        year = year_entry.get().strip()
        min_price = min_price_entry.get().strip()
        max_price = max_price_entry.get().strip()

        ## Load the inventory, remove "Car ID" column, and process data for display
        df = load_inventory().drop(columns=["Car ID"])
        df = df[df["Brand"].str.contains(brand, case=False)]  # case=False for case-insensitive match
        df["Price"] = df["Price"].astype(float) # Convert price to float
        df["Year"] = df["Year"].astype(int) # Ensure year is in integer

        # Apply search filters to the inventory
        # Filter based on the brand if a brand is provided
        if brand:
            # Perform case-insensitive search using `str.contains` for partial match
            df = df[df["Brand"].str.contains(brand, case=False)]  # case=False makes it case-insensitive
        # Filter based on the selected year from the dropdown (no error messgae needed)
        if year:
            df = df[df["Year"] == int(year)]  # Filter inventory by the selected year

        # Ensure that the entered prices are numbers
        try:
            if min_price:
                df = df[df["Price"] >= float(min_price)]
            if max_price:
                df = df[df["Price"] <= float(max_price)]
        except ValueError:
            messagebox.showerror("ERROR", "Enter Valid Digits for Prices")
            return

        # Clear existing rows from the Table before displaying new results
        results_table.delete(*results_table.get_children())

        # Check if df is not empty based on filters
        if not df.empty:
            # Set the columns to the correct headers, excluding the index column
            results_table["columns"] = list(df.columns)

            for col in results_table["columns"]:
                # Set the column header to the column names
                results_table.heading(col, text=col)
                results_table.column(col, width=100, anchor="center")

                # Add new rows to the bottom of the results table and start index from 1 instead of 0
            for _, row in df.iterrows():
            # Insert row data without index to maintain correct column alignment
                results_table.insert("", "end", values=tuple(row))

        else:
            messagebox.showinfo("No Results", "No cars found")

    # Create a separate frame for search and home button to place them side by side
    buttom_frame = tk.Frame(search_window)
    buttom_frame.pack(pady=10)
    tk.Button(buttom_frame, text="Search", command=search_logic).grid(row=0, column=0, padx=10)
    tk.Button(buttom_frame, text="Home", command=search_window.destroy).grid(row=0, column=1, padx=10)

#==SORT CARS==
def sort_cars(root, username):

    # Create a new window for sorting
    sort_window = tk.Toplevel(root)
    sort_window.title("AUTOHUB")   #Set window title
    sort_window.geometry("800x600")  # Set window size

    # Window sub-title as "Sort By"
    tk.Label(sort_window, text="Sort By:", font=("Serif", 14, "bold italic")).pack(pady=10)

    # Buttons for Price and Year side by side
    button_frame = tk.Frame(sort_window)
    button_frame.pack(pady=5)

    tk.Button(button_frame, text="Price", command=lambda: perform_sort("Price")).grid(row=0, column=0, padx=10)
    tk.Button(button_frame, text="Year", command=lambda: perform_sort("Year")).grid(row=0, column=1, padx=10)

    # Create frame for sorted results
    table_frame = tk.Frame(sort_window)
    table_frame.pack(pady=(10, 0), fill=tk.BOTH, expand=True)

    #Add Tree view to the table frame
    car_table = ttk.Treeview(table_frame, show="headings")
    car_table.pack(fill=tk.BOTH, expand=True)

    #Add vertical scrollbar
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=car_table.yview)
    car_table.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # === Sorting Logic===
    def perform_sort(option):

        df = load_inventory().drop(columns=["Car ID"])
        #  Sort data frame in descending order, either by 'Price' or 'Year'
        if option == "Price":
            df["Price"] = df["Price"].astype(float) # Convert price column values to float
            sorted_df = df.sort_values(by="Price", ascending=False)
        elif option == "Year":
            sorted_df = df.sort_values(by="Year", ascending=False)
        else:
            sorted_df = df
        save_cars(sorted_df) #save the sorted data frame

        # Clear table before inserting new data
        for item in car_table.get_children():
            car_table.delete(item)

        # Setup Table columns if df is not empty.
        if not sorted_df.empty:
            car_table["columns"] = ["Index"] + list(sorted_df.columns)
            for col in car_table["columns"]:
                car_table.heading(col, text=col)
                car_table.column(col, width=100, anchor="center")

            # Insert each row from the sorted DataFrame into the Treeview with a row number
            row_no = 1
            for _, row in sorted_df.iterrows():
                car_table.insert("", "end", values=(row_no, *row)) # Add row number as the first column
                row_no += 1 #Increase after each insertion

        else:
            messagebox.showinfo("ERROR", "Error Occurred") #just incase

    # Home button
    tk.Button(sort_window, text="Home", command=sort_window.destroy).pack(pady=10)