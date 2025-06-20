# AutoHub Inventory System

**Technologies:** Python | Tkinter | Pandas | CSV/TXT File I/O  


## Overview

**AutoHub Inventory System** is a modular, API-driven desktop application for managing automotive inventory and sales in a corporate in-house environment. With a clear separation of concerns, it exposes an internal API layer for core functions like inventory tracking, user authentication, and role-based access control.

Built with the **Python’s standard Tk GUI toolkit**, it provides a modern, responsive interface tailored for administrators and sales staff. `pandas` powers efficient handling of structured data and CSV integration.

Developed iteratively under SDLC principles, AutoHub prioritizes modularity, data integrity, and long-term maintainability—delivering a professional-grade system that meets real operational needs.

---

## Core Features

- **Role-Based Authentication**  
  Verifies stored credentials for customers and restricts admin functions to validated admin IDs.

- **Inventory Management (Admin)**  
  Enables administrators to add, update, and remove vehicles using VIN as the unique identifier.

- **Sales Processing**  
  Records completed transactions, auto-updates inventory status, and stores historical data in structured formats.

- **Customer Showroom API**  
  Displays a filtered, dynamic car listing interface for customers, supporting interactive browsing and selection.

- **Modular Design**  
  Each module (auth, inventory, sales, etc.) encapsulates specific logic to promote separation of concerns and testability.

- **Optimized File I/O**  
  Data is persisted through `.csv` and `.txt` files, with `pandas` powering high-performance data manipulation and structure validation.

- **Iterative Development & Testing**  
  The system was built and verified in cycles, with continuous testing of modules, user flows, and data consistency.

---

## Project Structure

- **`main.py`**  
  Entry point of the application. Initializes the API and contains navigable submenus for customers and administrators.

- **`auth.py`**  
  Manages authentication logic — verifying login credentials against stored user/admin records. Enforces access control via valid admin IDs.

- **`showroom.py`**  
  Handles all user-side display of vehicle listings. Provides a responsive interface for browsing available cars using a dynamic, event-driven API.

- **`inventory.py`**  
  Encapsulates administrative functions for managing the backend vehicle database — including adding, editing, and removing entries by VIN.

- **`sales.py`**  
  Facilitates recording and viewing of vehicle sales. Handles the synchronization of inventory status upon successful transactions.

- **`data.py`**  
  Core data layer. Abstracts CSV and TXT file I/O for all modules, ensuring safe and consistent access to cars, users, admins, and sales records.

- **`utils.py`**  
  Contains reusable Tkinter utilities for API transitions and cleanup — enhancing code reusability and interface responsiveness.

---

## Installation & Usage

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Ugo-CN/AutoHub-Inventory-System.git
   cd AutoHub-Inventory-System
