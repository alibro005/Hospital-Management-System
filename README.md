# 🏥 Hospital Management System

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Database](https://img.shields.io/badge/Database-MySQL-lightgrey)
![GUI](https://img.shields.io/badge/GUI-Tkinter-brightgreen)
![CLI](https://img.shields.io/badge/Interface-CLI-blueviolet)

A Python-based Hospital Management System that combines Object-Oriented Programming, a Tkinter GUI, CLI options, and MySQL integration. It enables users to manage patient data, doctor assignments, billing, and user authentication through a clean, modular architecture.

---

## 🚀 Features

- 🔐 Login Authentication System  
- ➕ Add / 🗑️ Delete Patients  
- 👨‍⚕️ Add Doctors & Assign Them to Patients  
- 📄 View Patient and Doctor Details  
- 💳 Generate Billing Information  
- 🖥️ GUI-based and CLI-based operation  
- 🛢️ MySQL Database Integration  

---

## 🧰 Tech Stack

- **Language:** Python  
- **GUI:** Tkinter & CustomTkinter  
- **Interface:** CLI and GUI  
- **Database:** MySQL (`hospital_db`)  
- **Design Pattern:** Object-Oriented Programming  

---

## 📁 Project Structure
```
Hospital-Management/
├── main.py      # CLI version
├── main_gui.py  # GUI interface
├── login.py     # Login window with GUI
├── database.py  # MySQL DB connection
├── model/ # OOP-based entity classes
│ ├── person.py
│ ├── patient.py
│ ├── doctor.py
│ └── billing.py
└── .venv/    # Optional virtual environment
```
---

## 🛠️ Setup Instructions

### 1. 📥 Clone the Repository

```bash
git clone https://github.com/yourusername/hospital-management-system.git
cd hospital-management-system/hospital-management
```

### 🐍 (Optional) Create a Virtual Environment

```
python -m venv .venv
source .venv/bin/activate  # For Windows: .venv\Scripts\activate
```
### 📦 Install Dependencies

```
pip install customtkinter mysql-connector-python
```
### 🛢️ Set Up MySQL Database

> Make sure your MySQL server is running.
> Open Database.txt and execute its SQL statements in your MySQL client (e.g., phpMyAdmin, MySQL Workbench, or terminal).
> This will create the hospital_db database and necessary tables.

### 🏃 Run the Application
Run the GUI version:
```
python login.py
```
Run the CLI version:
```
python main.py
```

### 🧪 Sample Credentials

> Username: admin@hms.com
> Password: 1234
(You can customize this in login.py)

### 📸 Screenshots





### 🧠 Concepts Demonstrated

> Object-Oriented Programming (Inheritance, Encapsulation)
> GUI development with Tkinter and CustomTkinter
> Integration of MySQL with Python using mysql-connector-python
> Functional separation between logic, database, and interface
> CLI and GUI support for managing hospital operations

### Author

Group Project
Muhammad Ali Siddiqui
Muhammad Sami
Object-Oriented Programming Final Project — Python + MySQL

### 📜 License

This project is licensed under the MIT License.


