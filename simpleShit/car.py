class Car:
    def __init__(self, brand, color, choice):
        self.brand = brand
        self.color = color
        self.choice = choice

    def display(self, choice):
        return f"My car is a {self.brand} that is color {self.color}"

if __name__ == "__main__":
    my_car = Car("Toyota", "red")
    print(my_car.display())