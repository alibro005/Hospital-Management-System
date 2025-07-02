import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, Toplevel
from tkinter import simpledialog
from database import cursor, conn
from PIL import Image, ImageTk

## GUI based

class HospitalGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1540x800+0+0")
        self.create_gui()
        self.cursor = cursor
        self.conn = conn

# ------------------------- GUI Creation ----------------------------------

    def create_gui(self):

        lbltitle = Label(
            self.root,
            bd=7,
            relief=RIDGE,
            text="Hospital MANAGEMENT SYSTEM",
            fg="green",
            bg="white",
            font=("poppins", 30, "bold"),
        )
        lbltitle.pack(side=TOP, fill="x")

# -------------------------- Left data frame -----------------------
        Dataframe = Frame(self.root, bd=9, relief=RIDGE)
        Dataframe.place(x=0, y=60, width=1270, height=360)

        self.Dataframeleft = LabelFrame(
            Dataframe,
            bd=9,
            relief=RIDGE,
            padx=10,
            font=("poppins", 10, "bold"),
            text="Information Panel",
        )
        self.Dataframeleft.place(x=0, y=5, width=880, height=340)

# ---------------- Right data frame --------------------------
        Dataframeright = LabelFrame(
            Dataframe,
            bd=9,
            relief=RIDGE,
            padx=10,
            font=("poppins", 10, "bold"),
            text="Bill",
        )
        Dataframeright.place(x=875, y=5, width=374, height=340)

# ----------------- Buttton frame -----------------------------

        Buttonframe = Frame(self.root, bd=9, relief=RIDGE)
        Buttonframe.place(x=0, y=409, width=1270, height=50)

# --------------- Details frame -----------------------------

        self.Detailsframe = Frame(self.root, bd=9, relief=RIDGE)
        self.Detailsframe.place(x=0, y=455, width=1270, height=200)

# -------------------------------------------------------------------
        self.notebook = ttk.Notebook(self.Detailsframe)
        self.notebook.pack(expand=True, fill=BOTH)

        self.patient_tab = Frame(self.notebook)
        self.doctor_tab = Frame(self.notebook)

        self.notebook.add(self.patient_tab, text="Patients")
        self.notebook.add(self.doctor_tab, text="Doctors")

        self.create_patient_tree()
        self.create_doctor_tree()

        self.current_form = "patient"
        self.create_patient_form()

# ----------------- Buttons ----------------------------------------

        Button(
            Buttonframe,
            text="Add Patient",
            bg="grey",
            fg="white",
            font=("Arial", 10, "bold"),
            width=21,
            command=lambda: self.switch_form("patient"),
        ).grid(row=0, column=0)

        Button(
            Buttonframe,
            text="Delete Patient",
            bg="grey",
            fg="white",
            font=("Arial", 10, "bold"),
            width=21,
            command=lambda: self.switch_form("delete"),
        ).grid(row=0, column=1)

        Button(
            Buttonframe,
            text="Add Doctor",
            bg="grey",
            fg="white",
            font=("Arial", 10, "bold"),
            width=21,
            command=lambda: self.switch_form("doctor"),
        ).grid(row=0, column=2)

        Button(
            Buttonframe,
            text="Assign Doctor",
            bg="grey",
            fg="white",
            font=("Arial", 10, "bold"),
            width=21,
            command=lambda: self.switch_form("assign"),
        ).grid(row=0, column=3)

        Button(
            Buttonframe,
            text="Show Patients",
            bg="grey",
            fg="white",
            font=("Arial", 10, "bold"),
            width=21,
            command=self.show_patients,
        ).grid(row=0, column=4)

        Button(
            Buttonframe,
            text="Show Doctors",
            bg="grey",
            fg="white",
            font=("Arial", 10, "bold"),
            width=21,
            command=self.show_doctors,
        ).grid(row=0, column=5)

        Button(
            Buttonframe,
            text="Exit",
            bg="grey",
            fg="white",
            font=("Arial", 10, "bold"),
            width=20,
            command=self.root.quit,
        ).grid(row=0, column=6)

# ---------------- bill area ---------------------------------------------------

        self.bill_text = Text(Dataframeright, font=("Arial", 12), width=40, height=15)
        self.bill_text.pack()

        Button(
            Dataframeright,
            text="Generate Bill",
            bg="grey",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.create_bill_form,
        ).pack(side=BOTTOM, pady=2)

# ------------------- Show Details ----------------------------------------------

    def create_patient_tree(self):
        self.patient_tree = ttk.Treeview(
            self.patient_tab,
            columns=("ID", "Name", "Age", "Gender", "Disease", "Doctor ID"),
            show="headings",
        )
        for col in self.patient_tree["columns"]:
            self.patient_tree.heading(col, text=col)
        for col, w in zip(self.patient_tree["columns"], [100, 150, 50, 80, 150, 100]):
            self.patient_tree.column(col, width=w)
        scrollbar = ttk.Scrollbar(
            self.patient_tab, orient="vertical", command=self.patient_tree.yview
        )
        self.patient_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.patient_tree.pack(expand=True, fill=BOTH)

    def create_doctor_tree(self):
        self.doctor_tree = ttk.Treeview(
            self.doctor_tab,
            columns=("ID", "Name", "Age", "Gender", "Specialization"),
            show="headings",
        )
        for col in self.doctor_tree["columns"]:
            self.doctor_tree.heading(col, text=col)
        for col, w in zip(self.doctor_tree["columns"], [100, 150, 50, 80, 200]):
            self.doctor_tree.column(col, width=w)
        scrollbar = ttk.Scrollbar(
            self.doctor_tab, orient="vertical", command=self.doctor_tree.yview
        )
        self.doctor_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.doctor_tree.pack(expand=True, fill=BOTH)

    def clear_form(self):
        for widget in self.Dataframeleft.winfo_children():
            widget.destroy()

# ---------------------  Forms -------------------------------------------

    def create_patient_form(self):
        self.clear_form()
        self.current_form = "patient"
        self.Dataframeleft.config(text="Patient Information")

        self.patient_id = StringVar()
        self.patient_name = StringVar()
        self.patient_age = StringVar()
        self.patient_gender = StringVar()
        self.patient_disease = StringVar()

        labels = ["Patient ID", "Patient Name", "Age", "Gender", "Disease"]
        variables = [
            self.patient_id,
            self.patient_name,
            self.patient_age,
            self.patient_gender,
            self.patient_disease,
        ]
        for i, (label, var) in enumerate(zip(labels, variables)):
            Label(
                self.Dataframeleft,
                text=label + ":",
                font=("poppins", 10, "bold"),
                padx=24,
                pady=12,
            ).grid(row=i, column=0)
            Entry(
                self.Dataframeleft, font=("poppins", 10), width=35, textvariable=var
            ).grid(row=i, column=1)

        Button(
            self.Dataframeleft,
            text="Submit",
            bg="green",
            fg="white",
            font=("Arial", 12, "bold"),
            width=15,
            command=self.submit_patient,
        ).grid(row=6, columnspan=2, pady=10)

    def create_doctor_form(self):
        self.clear_form()
        self.current_form = "doctor"
        self.Dataframeleft.config(text="Doctor Information")

        self.doctor_id = StringVar()
        self.doctor_name = StringVar()
        self.doctor_age = StringVar()
        self.doctor_gender = StringVar()
        self.doctor_specialization = StringVar()

        labels = ["Doctor ID", "Doctor Name", "Age", "Gender", "Specialization"]
        variables = [
            self.doctor_id,
            self.doctor_name,
            self.doctor_age,
            self.doctor_gender,
            self.doctor_specialization,
        ]
        for i, (label, var) in enumerate(zip(labels, variables)):
            Label(
                self.Dataframeleft,
                text=label + ":",
                font=("poppins", 10, "bold"),
                padx=24,
                pady=12,
            ).grid(row=i, column=0)
            Entry(
                self.Dataframeleft, font=("poppins", 10), width=35, textvariable=var
            ).grid(row=i, column=1)

        Button(
            self.Dataframeleft,
            text="Submit",
            bg="green",
            fg="white",
            font=("Arial", 12, "bold"),
            width=15,
            command=self.submit_doctor,
        ).grid(row=5, columnspan=2, pady=10)

    def create_delete_patient_form(self):
        self.clear_form()
        self.Dataframeleft.config(text="Delete Patient")
        self.delete_patient_id = StringVar()

        Label(
            self.Dataframeleft,
            text="Enter Patient ID:",
            font=("poppins", 10, "bold"),
            padx=24,
            pady=12,
        ).grid(row=0, column=0)
        Entry(
            self.Dataframeleft,
            font=("poppins", 10),
            width=35,
            textvariable=self.delete_patient_id,
        ).grid(row=0, column=1)

        Button(
            self.Dataframeleft,
            text="Delete",
            bg="red",
            fg="white",
            font=("Arial", 12, "bold"),
            width=15,
            command=self.delete_patient_from_form,
        ).grid(row=1, columnspan=2, pady=10)

    def create_assign_doctor_form(self):
        self.clear_form()
        self.Dataframeleft.config(text="Assign Doctor")
        self.assign_patient_id = StringVar()
        self.assign_doctor_id = StringVar()

        Label(
            self.Dataframeleft,
            text="Patient ID:",
            font=("poppins", 10, "bold"),
            padx=24,
            pady=12,
        ).grid(row=0, column=0)
        Entry(
            self.Dataframeleft,
            font=("poppins", 10),
            width=35,
            textvariable=self.assign_patient_id,
        ).grid(row=0, column=1)

        Label(
            self.Dataframeleft,
            text="Doctor ID:",
            font=("poppins", 10, "bold"),
            padx=24,
            pady=12,
        ).grid(row=1, column=0)
        Entry(
            self.Dataframeleft,
            font=("poppins", 10),
            width=35,
            textvariable=self.assign_doctor_id,
        ).grid(row=1, column=1)

        Button(
            self.Dataframeleft,
            text="Assign",
            bg="blue",
            fg="white",
            font=("Arial", 12, "bold"),
            width=15,
            command=self.assign_doctor_from_form,
        ).grid(row=2, columnspan=2, pady=10)

    def create_bill_form(self):

        self.clear_form()
        self.Dataframeleft.config(text="Billing Form")

        self.bill_pid = StringVar()
        self.bill_days = StringVar()
        self.bill_rate = StringVar()

        Label(self.Dataframeleft, text="Patient ID:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, padx=10, pady=10
        )
        Entry(self.Dataframeleft, textvariable=self.bill_pid, width=30).grid(
            row=0, column=1
        )

        Label(
            self.Dataframeleft, text="Days Admitted:", font=("Arial", 10, "bold")
        ).grid(row=1, column=0, padx=10, pady=10)
        Entry(self.Dataframeleft, textvariable=self.bill_days, width=30).grid(
            row=1, column=1
        )

        Label(
            self.Dataframeleft, text="Daily Charge:", font=("Arial", 10, "bold")
        ).grid(row=2, column=0, padx=10, pady=10)
        Entry(self.Dataframeleft, textvariable=self.bill_rate, width=30).grid(
            row=2, column=1
        )

        Button(
            self.Dataframeleft,
            text="Generate",
            bg="green",
            fg="white",
            command=self.calculate_bill,
        ).grid(row=3, columnspan=2, pady=10)

    def switch_form(self, form_type):
        if form_type == "patient":
            self.create_patient_form()
        elif form_type == "doctor":
            self.create_doctor_form()
        elif form_type == "delete":
            self.create_delete_patient_form()
        elif form_type == "assign":
            self.create_assign_doctor_form()
        elif form_type == "bill":
            self.create_bill_form()

    def submit_patient(self):
        try:
            query = "INSERT INTO patients (name, age, gender, disease) VALUES (%s, %s, %s, %s)"
            values = (
                self.patient_name.get(),
                self.patient_age.get(),
                self.patient_gender.get(),
                self.patient_disease.get(),
            )
            self.cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("Success", "Patient added successfully")
            self.clear_patient_fields()
            self.show_patients()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def submit_doctor(self):
        try:
            query = "INSERT INTO doctors VALUES (%s, %s, %s, %s, %s)"
            values = (
                self.doctor_id.get(),
                self.doctor_name.get(),
                self.doctor_age.get(),
                self.doctor_gender.get(),
                self.doctor_specialization.get(),
            )
            self.cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("Success", "Doctor added successfully")
            self.clear_doctor_fields()
            self.show_doctors()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ----------------------------------------------------------------

    def assign_doctor_from_form(self):
        pid = self.assign_patient_id.get()
        did = self.assign_doctor_id.get()
        if pid and did:
            try:
                self.cursor.execute(
                    "UPDATE patients SET assigned_doctor_id = %s WHERE patient_id = %s",
                    (did, pid),
                )
                self.conn.commit()
                if self.cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Doctor assigned successfully")
                    self.show_patients()
                    self.assign_patient_id.set("")
                    self.assign_doctor_id.set("")
                else:
                    messagebox.showinfo("Not Found", "No patient found with that ID")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def delete_patient_from_form(self):
        pid = self.delete_patient_id.get()
        if pid:
            try:
                self.cursor.execute(
                    "DELETE FROM patients WHERE patient_id = %s", (pid,)
                )
                self.conn.commit()
                if self.cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Patient deleted successfully")
                    self.show_patients()
                    self.delete_patient_id.set("")
                else:
                    messagebox.showinfo("Not Found", "No patient found with that ID")
            except Exception as e:
                messagebox.showerror("Error", str(e))

# ----------------------------------------------------------------------------------

    def show_patients(self):
        try:
            for item in self.patient_tree.get_children():
                self.patient_tree.delete(item)
            self.cursor.execute("SELECT * FROM patients")
            for patient in self.cursor.fetchall():
                self.patient_tree.insert("", "end", values=patient)
            self.notebook.select(self.patient_tab)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_doctors(self):
        try:
            for item in self.doctor_tree.get_children():
                self.doctor_tree.delete(item)

            self.cursor.execute("SELECT * FROM doctors")
            for doctor in self.cursor.fetchall():
                self.doctor_tree.insert("", "end", values=doctor)
            self.notebook.select(self.doctor_tab)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def calculate_bill(self):
        try:
            pid = self.bill_pid.get()
            days = int(self.bill_days.get())
            rate = int(self.bill_rate.get())

            self.cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (pid,))
            patient = cursor.fetchone()

            if patient:
                total = days * rate
                self.bill_text.delete("1.0", END)
                self.bill_text.insert(END, f"         Patient ID: {patient[0]}\n")
                self.bill_text.insert(END, f"         Name: {patient[1]}\n")
                self.bill_text.insert(END, f"         Days Admitted: {days}\n")
                self.bill_text.insert(END, f"         Daily Charge: {rate}\n")
                self.bill_text.insert(END, f"\n        Total Bill: {total}\n")
            else:
                messagebox.showerror("Error", "Patient not found")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_patient_fields(self):
        self.patient_id.set("")
        self.patient_name.set("")
        self.patient_age.set("")
        self.patient_gender.set("")
        self.patient_disease.set("")

    def clear_doctor_fields(self):
        self.doctor_id.set("")
        self.doctor_name.set("")
        self.doctor_age.set("")
        self.doctor_gender.set("")
        self.doctor_specialization.set("")
