from model.person import Person
from model.patient import Patient
from model.doctor import Doctor
from model.billing import Billing
from database import conn, cursor

# ________CLI Based________


def menu():

    while True:

        print("\n---------Hospital Management System--------")
        print("1. Add Patient")
        print("2. Delete Patient")
        print("3. Add Doctor")
        print("4. Assign Doctor to patient")
        print("5. Show Patient Details")
        print("6. Show Doctor Details")
        print("7. Generate Bill")
        print("8. Exit")

        choice = input("Enter your choice : ")

        if choice == "1":
            name = input("Patient Name: ")
            age = int(input("Age: "))
            gender = input("Gender: ")
            patient_id = input("Patient ID: ")
            disease = input("Disease: ")
            p = Patient(name, age, gender, patient_id, disease)
            p.save_to_db(cursor, conn)

            print("Patient added successfully.")

        elif choice == "2":
            pid = input("Enter Patient ID to delete: ")
            try:
                pid = int(pid)
                Patient.delete_from_db(cursor, conn, pid)
            except ValueError:
                print("Invalid Patient ID. Please enter a number.")

        elif choice == "3":
            name = input("Doctor Name: ")
            age = int(input("Age: "))
            gender = input("Gender: ")
            doctor_id = input("Doctor ID: ")
            specialization = input("Specialization: ")
            d = Doctor(name, age, gender, doctor_id, specialization)
            d.save_to_db(cursor, conn)
            print("Doctor added successfully.")

        elif choice == "4":

            try:
                pid = int(input("Enter Patient ID: "))
                did = int(input("Enter Doctor ID: "))
                Patient.assign_doctor(cursor, conn, pid, did)
            except ValueError:
                print("❌ Please enter valid numeric IDs.")

        elif choice == "5":
            cursor.execute("SELECT * FROM patients")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print("-------Patient Details -----")
                    print(f"Patient ID  : {row[0]}")
                    print(f"Patient Name : {row[1]}")
                    print(f"Age :{row[2]}")
                    print(f"Gender : {row[3]}")
                    print(f"Disease : {row[4]}")
                    print(f"Assigned doctor ID: {row[5]}")
            else:
                print("No Record found")

        elif choice == "6":
            cursor.execute("SELECT * FROM doctors")
            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    print("------ Doctor Details------")
                    print(f"Doctor ID : {row[0]}")
                    print(f"Doctor Name : {row[1]}")
                    print(f"Age :{row[2]}")
                    print(f"Gender : {row[3]}")
                    print(f"Specialization : {row[4]}")
            else:
                print("No record Found")

        elif choice == "7":

            pid = input("Enter Patient ID: ")

            cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (pid,))
            patient = cursor.fetchone()
            if patient:
                days = int(input("Enter Number of Days Admitted : "))
                daily_charge = float(input("Enter Daily charges : "))

                bill = Billing(pid, days, daily_charge)
                bill.generate_bill()
            else:
                print(f"No Patient found")

        elif choice == "8":
            print("Exiting system.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()
