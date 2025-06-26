# Billing Class


class Billing:
    def __init__(self, pid, days, daily_charge):
        self.pid = pid
        self.days = days
        self.daily_charge = daily_charge

    def generate_bill(self):

        print(f"---------BILL-------")
        print(f"Patient ID : {self.pid}")
        print(f"Total bill for {self.pid} is : {self.days*self.daily_charge} ")
        print("----------------------")
