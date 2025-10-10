from datetime import datetime


class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.fed = False
    
    def speak(self):
        return "Some sound"
    
    def eat(self):
        self.fed = True
        return f"{self.name} is eating."
    
    def get_info(self):
        status = "Fed" if self.fed else "Hungry"
        return f"{self.name} (Age: {self.age}, Status: {status})"


class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed
    
    # Polymorphism - Method Overriding
    def speak(self):
        return "Woof! Woof!"
    
    def get_info(self):
        return f"🐕 Dog: {super().get_info()}, Breed: {self.breed}"


class Cat(Animal):
    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color
    
    # Polymorphism - Method Overriding
    def speak(self):
        return "Meow!"
    
    def get_info(self):
        return f"🐱 Cat: {super().get_info()}, Color: {self.color}"


class Bird(Animal):
    def __init__(self, name, age, can_fly):
        super().__init__(name, age)
        self.can_fly = can_fly
    
    # Polymorphism - Method Overriding
    def speak(self):
        return "Chirp! Chirp!"
    
    def get_info(self):
        fly_status = "Can fly" if self.can_fly else "Cannot fly"
        return f"🐦 Bird: {super().get_info()}, {fly_status}"
