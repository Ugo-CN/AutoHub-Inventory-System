import pandas as pd
import os

# --------------------------------- #
# FILES,SAMPLE DATA & FILE FUNCTIONS
# -------------------------------- #


# == File Constants ==
INVENTORY_FILE = "AutoHub Inventory.csv"
SALES_FILE = "AutoHub Sales.csv"
CARS_FILE = "AutoHub Cars.csv"
USERS_FILE = "Users.txt"
ADMINS_FILE = "Admins.txt"

# == Sample Data for Cars and Sales Files ==
SAMPLE_CARS = [
    {'Car ID': '0001', 'Brand': 'Toyota', 'Model': 'Camry', 'Year': '2019',
     'Price': '22593', 'Colour': 'Black', 'Status': 'Sold'},
    {'Car ID': '0002', 'Brand': 'Honda', 'Model': 'Civic', 'Year': '2016',
     'Price': '34075', 'Colour': 'White', 'Status': 'On-Sale'},
    {'Car ID': '0003', 'Brand': 'Ford', 'Model': 'Focus', 'Year': '2015',
     'Price': '21655', 'Colour': 'Blue', 'Status': 'On-Sale'},
    {'Car ID': '0004', 'Brand': 'Nissan', 'Model': 'Altima', 'Year': '2022',
     'Price': '28000', 'Colour': 'Red', 'Status': 'On-Sale'},
    {'Car ID': '0005', 'Brand': 'Chevrolet', 'Model': 'Malibu', 'Year': '2020',
     'Price': '23000', 'Colour': 'Silver', 'Status': 'Unavailable'},
    {'Car ID': '0006', 'Brand': 'Hyundai', 'Model': 'Elantra', 'Year': '2018',
     'Price': '19500', 'Colour': 'Gray', 'Status': 'Unavailable'},
    {'Car ID': '0007', 'Brand': 'BMW', 'Model': '3 Series', 'Year': '2021',
     'Price': '41000', 'Colour': 'Black', 'Status': 'On-Sale'},
    {'Car ID': '0008', 'Brand': 'Kia', 'Model': 'Optima', 'Year': '2017',
     'Price': '18000', 'Colour': 'Blue', 'Status': 'Unavailable'},
    {'Car ID': '0009', 'Brand': 'Mercedes-Benz', 'Model': 'C-Class', 'Year': '2019',
     'Price': '43000', 'Colour': 'White', 'Status': 'On-Sale'},
    {'Car ID': '0010', 'Brand': 'Volkswagen', 'Model': 'Jetta', 'Year': '2016',
     'Price': '17000', 'Colour': 'Red', 'Status': 'Unavailable'}
]

SAMPLE_SALES = [
    {"Sales ID": "0100", "Date": "10/03/2024", "Car ID": "0100",
     "Customer Name": "John Doe", "Price Sold": "24000", "Sales Person": "Alice Brown"},
    {"Sales ID": "0101", "Date": "12/03/2024", "Car ID": "0101",
     "Customer Name": "Jane Smith", "Price Sold": "54000", "Sales Person": "Bob Green"},
    {"Sales ID": "0102", "Date": "15/03/2024", "Car ID": "0102",
     "Customer Name": "Michael Johnson", "Price Sold": "47000", "Sales Person": "Charlie White"},
    {"Sales ID": "0103", "Date": "17/03/2024", "Car ID": "0103",
     "Customer Name": "Emily Davis", "Price Sold": "25000", "Sales Person": "David Lee"},
    {"Sales ID": "0104", "Date": "20/03/2024", "Car ID": "0104",
     "Customer Name": "Lucas Brown", "Price Sold": "37000", "Sales Person": "Eva Black"},
    {"Sales ID": "0105", "Date": "22/03/2024", "Car ID": "0105",
     "Customer Name": "Sophia Wilson", "Price Sold": "42000", "Sales Person": "Frank Green"},
    {"Sales ID": "0106", "Date": "24/03/2024", "Car ID": "0106",
     "Customer Name": "Oliver Martinez", "Price Sold": "31000", "Sales Person": "Grace White"},
    {"Sales ID": "0107", "Date": "26/03/2024", "Car ID": "0107",
     "Customer Name": "Isabella Moore", "Price Sold": "39000", "Sales Person": "Harry Brown"},
    {"Sales ID": "0108", "Date": "28/03/2024", "Car ID": "0108",
     "Customer Name": "Elijah Taylor", "Price Sold": "46000", "Sales Person": "Ivy Green"},
    {"Sales ID": "0109", "Date": "30/03/2024", "Car ID": "0109",
     "Customer Name": "Amelia Harris", "Price Sold": "53000", "Sales Person": "Jack White"}
]


# == Create each file(inventory,sales,cars) ==
def create_inventory_file():
    """Create inventory file if it does not exist or is empty."""
    if not os.path.exists(INVENTORY_FILE) or os.stat(INVENTORY_FILE).st_size == 0:
        df = pd.DataFrame(SAMPLE_CARS).sort_values(by="Car ID")
        df.to_csv(INVENTORY_FILE, index=False)

def create_sales_file():
    """Create sales file if it does not exist or is empty."""
    if not os.path.exists(SALES_FILE) or os.stat(SALES_FILE).st_size == 0:
        df = pd.DataFrame(SAMPLE_SALES)
        df.to_csv(SALES_FILE, index=False)

def create_cars_file():
    """Create car display file (without Car ID column) if not present."""
    df = load_inventory()
    if not os.path.exists(CARS_FILE) or os.stat(CARS_FILE).st_size == 0:
        df.drop(columns=["Car ID"]).to_csv(CARS_FILE, index=False)

# == Load and Save the data in each file ==
def load_inventory() -> pd.DataFrame:
    """Load the car inventory CSV file."""
    return pd.read_csv(INVENTORY_FILE, dtype=str)

def save_inventory(df: pd.DataFrame) -> None:
    """Save updated inventory to CSV."""
    df.to_csv(INVENTORY_FILE, index=False)

def load_sales() -> pd.DataFrame:
    """Load the sales CSV file."""
    df = pd.read_csv(SALES_FILE, dtype=str)
    return df.sort_values(by="Sales ID")

def save_sales(df: pd.DataFrame) -> None:
    """Sort and save sales to sales CSV file."""
    df.sort_values(by="Sales ID").to_csv(SALES_FILE, index=False)

def save_cars(df: pd.DataFrame) -> None:
    """Save sample car listings (without CAR ID) to  cars file."""
    df.to_csv(CARS_FILE, index=False)

def load_details(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as file:
        lines=file.readlines()
        return dict (line.strip(). split (":") for line in lines)

def save_details(file_path, dtls):
    with open(file_path, "w") as file:
        for key, value in dtls.items():
            file.write(f"{key}:{value}\n")

def valid_admin_id(admin_id):
        return admin_id in {"AD001", "AD002", "AD003"}