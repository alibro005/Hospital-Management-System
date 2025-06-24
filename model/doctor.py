from .person import Person


class Doctor(Person):
    def __init__(self, name, age, gender, doctor_id, specialization):
        super().__init__(name, age, gender)

        self.doctor_id = doctor_id
        self.specialization = specialization
        self.assigned_doctor_id = None
  

    def save_to_db(self, cursor, conn):
        query = "INSERT INTO doctors (name, age, gender, doctor_id,specialization) VALUES (%s, %s, %s, %s,%s)"
        values = (self.name, self.age, self.gender, self.doctor_id,self.specialization)
        cursor.execute(query, values)
        conn.commit()
    
   
