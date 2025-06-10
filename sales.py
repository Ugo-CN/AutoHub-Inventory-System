import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from data import load_sales, save_sales
from data import load_inventory, save_inventory



#-------------------------#
#ADMIN MENU SALES OPTIONS
#-------------------------#

# ==SALE OVERVIEW==
def sales_overview(root):
    """Displays all sales records."""

    # Load sales data
    df_sales = load_sales()

    # Create Sales Window
    sales_window = tk.Toplevel(root)
    sales_window.title("AUTOHUB")
    sales_window.geometry("1000x600")

    #Set Subtiitle ====
    title_label = tk.Label(sales_window, text="AutoHub Sales:", font=("Serif", 14, "bold italic"))
    title_label.pack(pady=10)

    # Create Treeview(table) to display Sales
    sales_table = ttk.Treeview(sales_window)
    sales_table.pack(fill=tk.BOTH, expand=True)

    #Set Table Columns names to be same as DataFrame column names
    sales_table["columns"] = list(df_sales.columns)
    sales_table["show"] = "headings"
    for col in df_sales.columns:
        sales_table.heading(col, text=col)
        sales_table.column(col, width=120, anchor="center")

    # Insert each row of data from the DataFrame into the sales table
    for _, row in df_sales.iterrows():
        sales_table.insert("", tk.END, values=list(row))

    # Add Scrollbar
    scrollbar = ttk.Scrollbar(sales_window, orient="vertical", command=sales_table.yview)
    sales_table.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Home Button
    home_button = tk.Button(sales_window, text="Home", font=("Arial", 11), command=sales_window.destroy)
    home_button.pack(pady=10)


#==RECORD SALE==
def record_sale(root):
    """Records a new sale into the sales file. And saves result to the inventory automatically"""

    # Create sales window
    sale_window = tk.Toplevel(root)
    sale_window.title("AUTOHUB") #Set window title
    sale_window.geometry("500x500") #Set window size

    # Subtitle
    window_subtitle = tk.Label(sale_window, text="Record Sale:", font=("Serif", 14, "bold italic"))
    window_subtitle.pack(pady=15)

    # ===== Frame to show sales form =====
    form_frame = tk.Frame(sale_window)
    form_frame.pack(pady=5)

    #Sale ID Label and Entry
    tk.Label(form_frame, text="Sale ID (4 digits):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_sale_id = tk.Entry(form_frame)
    entry_sale_id.grid(row=0, column=1, padx=10, pady=5)

    #Car ID Label and Entry
    tk.Label(form_frame, text="Car ID:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_car_id = tk.Entry(form_frame)
    entry_car_id.grid(row=1, column=1, padx=10, pady=5)

    #Customer Name Label and Entry
    tk.Label(form_frame, text="Customer Name:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_customer_name = tk.Entry(form_frame)
    entry_customer_name.grid(row=2, column=1, padx=10, pady=5)

    #Price Label and Entry
    tk.Label(form_frame, text="Price Sold:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_price_sold = tk.Entry(form_frame)
    entry_price_sold.grid(row=3, column=1, padx=10, pady=5)

    #Sales Person Label and Entry
    tk.Label(form_frame, text="Sales Person:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    entry_sales_person = tk.Entry(form_frame)
    entry_sales_person.grid(row=4, column=1, padx=10, pady=5)

    #Date Label and Entry
    tk.Label(form_frame, text="Date (DD/MM/YYYY):").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    entry_date = tk.Entry(form_frame)
    entry_date.grid(row=5, column=1, padx=10, pady=5)

    #==Record Sale Logic==
    def new_sale():

        #Retrieve Sales Details
        sale_id = entry_sale_id.get().strip()
        car_id = entry_car_id.get().strip()
        customer_name = entry_customer_name.get().strip()
        price_sold = entry_price_sold.get().strip()
        sales_person = entry_sales_person.get().strip()
        date_input = entry_date.get().strip()

        df_sales = load_sales()
        df_inventory = load_inventory()

        # Sales ID  Details validation
        if not sale_id:
            messagebox.showerror("ERROR", "Sale ID cannot be empty!")
            return
        elif sale_id in df_sales["Sales ID"].values:
            messagebox.showerror("ERROR", "Sale ID already exists!")
            return
        elif len(sale_id) != 4 or not sale_id.isdigit():
            messagebox.showerror("ERROR", "Sale ID must be 4 digits!")
            return

        # Car ID validation
        if car_id not in df_inventory["Car ID"].values:
            messagebox.showerror("ERROR", "Car ID Not found")
            return

        if not customer_name or not sales_person:
            messagebox.showerror("ERROR", "Please Fill In All Sales Details")
            return

        if not price_sold.isdigit():
            messagebox.showerror("ERROR", "Price Must Be A Number")
            return

        # Update car status to Sold in the inventory
        df_inventory.loc[df_inventory["Car ID"] == car_id, "Status"] = "Sold"
        save_inventory(df_inventory)

        # Date validation
        try:
            datetime.strptime(date_input, "%d/%m/%Y") #Check that  input date perfectly fits the date format
        except ValueError:
            messagebox.showerror("Input Error", "Invalid Date format! Use DD/MM/YYYY.")
            return

        # Create a dictionary for the new sale with the sale details
        new_sales = {
            "Sales ID": sale_id,
            "Date": date_input,
            "Car ID": car_id,
            "Customer Name": customer_name,
            "Price Sold": price_sold,
            "Sales Person": sales_person
        }

        #Save the new sale to the existing data frame
        df_sales = pd.concat([df_sales, pd.DataFrame([new_sales])], ignore_index=True)
        save_sales(df_sales)
        messagebox.showinfo("Success", f"Sale {sale_id} successfully recorded!")
        sale_window.destroy()

    # Buttons
    btn_record_sale = tk.Button(form_frame, text="Record Sale", font=("Arial", 12), command=new_sale)
    btn_record_sale.grid(row=6, columnspan=2, pady=15)
    btn_home = tk.Button(form_frame, text="Home", font=("Arial", 12), command=sale_window.destroy)
    btn_home.grid(row=7, columnspan=2, pady=10)
