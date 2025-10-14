from datetime import datetime

from animals import Animal, Dog, Cat, Bird
from exceptions import (
    AnimalException,
    AnimalNotFoundException,
    AnimalAlreadyExistsException
)


class Zoo:    
    def __init__(self, name):
        self.name = name
        self.animals = []
    
    def add_animal(self, animal):
        try:
            # Check if animal already exists
            for a in self.animals:
                if a.name == animal.name:
                    raise AnimalAlreadyExistsException(
                        f"Animal '{animal.name}' already exists!"
                    )
            
            self.animals.append(animal)
            print(f"✓ Added: {animal.name}")
        
        except AnimalAlreadyExistsException as e:
            print(f"✗ Error: {e}")
    
    def find_animal(self, name):
        for animal in self.animals:
            if animal.name == name:
                return animal
        raise AnimalNotFoundException(f"Animal '{name}' not found!")
    
    def feed_animal(self, name):
        try:
            animal = self.find_animal(name)
            message = animal.eat()
            print(f"✓ {message}")
        except AnimalNotFoundException as e:
            print(f"✗ {e}")
    
    def make_animal_speak(self, name):
        try:
            animal = self.find_animal(name)
            sound = animal.speak()
            print(f"✓ {animal.name} says: {sound}")
        except AnimalNotFoundException as e:
            print(f"✗ {e}")
    
    def show_all_animals(self):
        print(f"\n{'='*50}")
        print(f"  {self.name} - All Animals")
        print(f"{'='*50}")
        
        if not self.animals:
            print("No animals in the zoo.")
            return
        
        # Polymorphism: each animal displays differently
        for animal in self.animals:
            print(animal.get_info())


def main():    
    print("="*50)
    print("  ANIMAL SYSTEM - OOP Assignment")
    print("="*50)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    zoo = Zoo("Python Zoo")
    
    print("\n--- Creating Animals ---")
    dog = Dog("Buddy", 3, "Golden Retriever")
    cat = Cat("Whiskers", 2, "Orange")
    bird = Bird("Tweety", 1, True)
    
    print("\n--- Adding Animals ---")
    zoo.add_animal(dog)
    zoo.add_animal(cat)
    zoo.add_animal(bird)
    zoo.add_animal(dog)  
    
    zoo.show_all_animals()
    
    print("\n--- Animals Speaking ---")
    zoo.make_animal_speak("Buddy")
    zoo.make_animal_speak("Whiskers")
    zoo.make_animal_speak("Tweety")
    zoo.make_animal_speak("Rex")  
    
    print("\n--- Feeding Animals ---")
    zoo.feed_animal("Buddy")
    zoo.feed_animal("Whiskers")
    zoo.feed_animal("Unknown") 
    
    zoo.show_all_animals()
    
    print("\n" + "="*50)
    print("✓ Inheritance: Dog, Cat, Bird inherit from Animal")
    print("✓ Polymorphism: Each animal speaks and displays differently")
    print("✓ Modules: animals.py, exceptions.py, main.py")
    print("✓ Imports: from animals import Dog, Cat, Bird")
    print("✓ Exception Handling: Custom exceptions with try-except")
    print("="*50)


if __name__ == "__main__":
    main()