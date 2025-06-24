# Person CLass

class Person:
    def __init__(self, name, age, gender):

        self.name = name
        self.age = age
        self.gender = gender

    def show_details(self):
        
        print(f"Name : {self.name}")
        print(f"Age : {self.age}")
        print(f"Gender : {self.gender}")
    
