class Vehicle:
    def __init__(self, model, year):
        self.model = model
        self.year = year
    def start_message(self):
        return f"{self.model} is starting"
    def vehicle_details(self):
        return f"{self.model} {self.year}"

class Motorcycle(Vehicle):
    def start_engine(self):
        return f"{self.model} goes vroom!!!"
    
class Car(Vehicle):
    def start_engine(self):
        print(self.start_message())
        print(self.engine_sound())
    def start_message(self):
        return f"{self.model} is starting"
    def engine_sound(self):
        return "Vroom!"

class Truck(Vehicle):
    def start_engine(self):
        print(self.start_message())
        print(self.engine_sound())
    def start_message(self):
        return f"{self.model} is starting"
    def engine_sound(self):
        return "Putt-putt-chug!"

vehicles = [Vehicle("Vios", "2005"), Vehicle("Burger", "2005"), Vehicle("Tite", "2005")]
for vehicle in vehicles:
    print(Motorcycle.start_engine(vehicle))



                