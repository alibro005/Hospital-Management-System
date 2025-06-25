from .person import Person

# Patient Class

class Patient(Person):
    def __init__(self, name, age, gender, patient_id, disease):
        super().__init__(name, age, gender)

        self.patient_id = patient_id
        self.disease = disease

    @staticmethod
    def assign_doctor(cursor, conn, patient_id, doctor_id):
        # Check if both patient and doctor exist

        cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
        patient = cursor.fetchone()

        cursor.execute("SELECT * FROM doctors WHERE doctor_id = %s", (doctor_id,))
        doctor = cursor.fetchone()

        if patient and doctor:
            query = "UPDATE patients SET assigned_doctor_id = %s WHERE patient_id = %s"
            cursor.execute(query, (doctor_id, patient_id))
            conn.commit()
            print(f"Doctor with ID {doctor_id} assigned to patient {patient_id}.")
        else:
            print("Patient or Doctor not found.")


    def save_to_db(self, cursor, conn):
        query = (
            "INSERT INTO patients (name, age, gender, disease) VALUES (%s, %s, %s, %s)"
        )
        values = (self.name, self.age, self.gender, self.disease)
        cursor.execute(query, values)
        conn.commit()


    @staticmethod
    def delete_from_db(cursor, conn, patient_id):
        cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
        result = cursor.fetchone()
        if result:
            cursor.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
            conn.commit()
            print(f"Patient with ID {patient_id} deleted.")
        else:
            print("Patient ID not found.")
