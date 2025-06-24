import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from tkinter import simpledialog
from model.patient import Patient
from model.doctor import Doctor
from model.billing import Billing
from database import cursor, conn
from PIL import Image, ImageTk


class HospitalGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("950x600")
        self.fields = {}
        self.current_form = None
        self.form_widgets = []

        # Create base canvas first
        self.canvas = tk.Canvas(self.root, width=950, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Load and display background image
        bg_image = Image.open("images/background.png")
        bg_image = bg_image.resize((950, 600), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Add title label on canvas
        self.title_label = tk.Label(
            self.root,
            text="🏥 Hospital Management System",
            font=("Arial", 20, "bold"),
            fg="#004080",
            bg="#ffffff",
        )
        self.canvas.create_window(475, 30, window=self.title_label)

        # Bill display area
        self.bill_frame = tk.Frame(self.root, bg="white")
        self.bill_frame.place(x=450, y=350)

        # Sidebar buttons
        button_texts = [
            ("Add Patient", self.show_add_patient_form),
            ("Delete Patient", self.delete_patient),
            ("Add Doctor", self.add_doctor_form),
            ("Assign Doctor", self.build_assign_form),
            ("Show Patients", self.show_patients),
            ("Show Doctor", self.show_doctors),
            ("Generate Bill", self.generate_bill_form),
            ("Exit", self.root.quit),
        ]

        self.button_refs = []
        for i, (text, command) in enumerate(button_texts):
            btn = tk.Button(
                self.root,
                text=text,
                width=20,
                height=2,
                font=("Arial", 10),
                command=command,
                bg="#e0f7fa",
            )
            self.canvas.create_window(100, 100 + i * 50, window=btn)
            self.button_refs.append(btn)

        self.build_form()

    def clear_form(self):
        for widget in self.root.winfo_children():
            if isinstance(
                widget, (tk.Label, tk.Entry, tk.Button)
            ) and widget not in self.button_refs + [self.title_label]:
                widget.destroy()
        self.fields.clear()


    def build_form(self, patient_form=True):
        self.clear_form()
        self.fields = {}
        self.current_form = "patient" if patient_form else "doctor"

        labels = ["Name", "Age", "Gender"]
        if patient_form:
            labels.insert(0, "Patient ID")
            labels.append("Disease")
        else:
            labels.insert(0, "Doctor ID")
            labels.append("Specialization")

        for i, label in enumerate(labels):
            lbl = tk.Label(self.root, text=f"{label} :", font=("Arial", 12), bg="white")
            entry = tk.Entry(self.root, font=("Arial", 12), width=30)
            self.canvas.create_window(350, 100 + i * 40, window=lbl)
            self.canvas.create_window(550, 100 + i * 40, window=entry)
            self.fields[label.lower()] = entry

        submit_btn = tk.Button(
            self.root,
            text="Submit",
            font=("Arial", 12),
            width=10,
            command=self.submit_form,
            bg="#d9ead3",
        )
        self.canvas.create_window(500, 120 + len(labels) * 40, window=submit_btn)
     


    def show_add_patient_form(self):
        self.build_form(patient_form=True)

    def add_doctor_form(self):
        self.build_form(patient_form=False)

    def submit_form(self):
        if self.current_form == "patient":
            self.submit_patient()
        elif self.current_form == "doctor":
            self.submit_doctor()
        elif self.current_form == "assign":
            self.submit_assignment()
        elif self.current_form == "bill":
            self.submit_bill()

    def submit_patient(self):
        try:
            name = self.fields["name"].get().strip()
            age = int(self.fields["age"].get())
            gender = self.fields["gender"].get().strip()
            disease = self.fields["disease"].get().strip()
            patient_id = self.fields["patient id"].get().strip()
            if not all([name, age, gender, disease, patient_id]):
                raise ValueError("All fields are required.")
            p = Patient(name, age, gender, patient_id, disease)
            p.save_to_db(cursor, conn)
            messagebox.showinfo("Success", "Patient added successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def submit_doctor(self):
        try:
            name = self.fields["name"].get().strip()
            age = int(self.fields["age"].get())
            gender = self.fields["gender"].get().strip()
            specialization = self.fields["specialization"].get().strip()
            doctor_id = self.fields["doctor id"].get().strip()
            if not all([name, age, gender, specialization, doctor_id]):
                raise ValueError("All fields are required.")
            d = Doctor(name, age, gender, doctor_id, specialization)
            d.save_to_db(cursor, conn)
            messagebox.showinfo("Success", "Doctor added successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def build_assign_form(self):
        self.clear_form()
        self.fields = {}
        self.current_form = "assign"
        labels = ["Patient ID", "Doctor ID"]

        for i, label in enumerate(labels):
            lbl = tk.Label(self.root, text=f"{label} :", font=("Arial", 12), bg="white")
            entry = tk.Entry(self.root, font=("Arial", 12), width=30)
            self.canvas.create_window(350, 120 + i * 50, window=lbl)
            self.canvas.create_window(550, 120 + i * 50, window=entry)
            self.fields[label.lower()] = entry

        submit_btn = tk.Button(
            self.root,
            text="Submit",
            font=("Arial", 12),
            width=10,
            command=self.submit_form,
            bg="#d9ead3",
        )
        self.canvas.create_window(500, 250, window=submit_btn)

    def generate_bill_form(self):
        self.clear_form()
        self.fields = {}
        self.current_form = "bill"
        labels = ["Patient ID", "No. of days Admit", "Daily Charge"]

        for i, label in enumerate(labels):
            lbl = tk.Label(self.root, text=f"{label} :", font=("Arial", 12), bg="white")
            entry = tk.Entry(self.root, font=("Arial", 12), width=30)
            self.canvas.create_window(350, 120 + i * 50, window=lbl)
            self.canvas.create_window(580, 120 + i * 50, window=entry)
            self.fields[label.lower()] = entry

        submit_btn = tk.Button(
            self.root,
            text="Submit",
            font=("Arial", 12),
            width=10,
            command=self.submit_form,
            bg="#d9ead3",
        )
        self.canvas.create_window(500, 300, window=submit_btn)

    def submit_assignment(self):
        try:
            pid = self.fields["patient id"].get()
            did = self.fields["doctor id"].get()
            cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (pid,))
            patient = cursor.fetchone()

            cursor.execute("SELECT * FROM doctors WHERE doctor_id = %s", (did,))
            doctor = cursor.fetchone()

            if patient and doctor:
                query = "UPDATE patients SET assigned_doctor_id = %s WHERE patient_id = %s"
                cursor.execute(query, (did, pid))
                conn.commit()
                messagebox.showinfo(
                    "Success", f"Doctor {did} assigned to Patient {pid}."
                )
            else:
                raise ValueError("Both IDs are required.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_patient(self):
        pid = simpledialog.askstring("Delete Patient", "Enter Patient ID to delete:")
        if pid:
            try:
                Patient.delete_from_db(cursor, conn, int(pid))
                messagebox.showinfo("Success", "Patient deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def submit_bill(self):
        try:
            pid = self.fields["patient id"].get().strip()
            days = int(self.fields["no. of days admit"].get())
            rate = int(self.fields["daily charge"].get())
            total = days * rate
            cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (pid,))
            patient = cursor.fetchone()
            if not patient:
                raise ValueError(f"No patient found with ID {pid}.")
            messagebox.showinfo(
                "Bill Generated", f"Bill: {total} units for Patient {pid}."
            )

            for widget in self.bill_frame.winfo_children():
                widget.destroy()

            tk.Label(
                self.bill_frame,
                text=f"Patient ID : {pid}",
                font=("Arial", 12),
                bg="white",
            ).pack()
            tk.Label(
                self.bill_frame,
                text=f"Days Admitted : {days}",
                font=("Arial", 12),
                bg="white",
            ).pack()
            tk.Label(
                self.bill_frame,
                text=f"Charge per Day : {rate}",
                font=("Arial", 12),
                bg="white",
            ).pack()
            tk.Label(
                self.bill_frame,
                text=f"Total Bill : {total} units",
                font=("Arial", 12, "bold"),
                bg="white",
            ).pack()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_patients(self):
        cursor.execute("SELECT * FROM patients")
        records = cursor.fetchall()
        if records:
            win = Toplevel(self.root)
            win.title("Patients List")
            win.geometry("800x400")
            columns = (
                "Patient ID",
                "Name",
                "Age",
                "Gender",
                "Disease",
                "Assigned Doctor",
            )
            tree = ttk.Treeview(win, columns=columns, show="headings")
            tree.pack(expand=True, fill="both")
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor="center")
            for row in records:
                tree.insert("", "end", values=row)
        else:
            messagebox.showinfo("Patients", "No patients found.")

    def show_doctors(self):
        cursor.execute("SELECT * FROM doctors")
        records = cursor.fetchall()
        if records:
            win = Toplevel(self.root)
            win.title("Doctors List")
            win.geometry("700x400")
            columns = ("Doctor ID", "Name", "Age", "Gender", "Specialization")
            tree = ttk.Treeview(win, columns=columns, show="headings")
            tree.pack(expand=True, fill="both")
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=130, anchor="center")
            for row in records:
                tree.insert("", "end", values=row)
        else:
            messagebox.showinfo("Doctors", "No doctors found.")


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = HospitalGUI(root)
#     root.mainloop()
