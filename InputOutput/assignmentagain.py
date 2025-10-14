from functools import wraps
from time import sleep

# DECORATORS

def log_growth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"🌱 Starting: {func.__name__.replace('_', ' ').title()}")
        result = func(*args, **kwargs)
        print(f"✓ Completed: {func.__name__.replace('_', ' ').title()}\n")
        return result
    return wrapper


def water_required(amount):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.water_level < amount:
                print(f"⚠️  Not enough water! Need {amount}ml, have {self.water_level}ml")
                return None
            self.water_level -= amount
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


# GENERATORS

def growth_stages(plant_name):
    stages = [
        f"{plant_name} seed is germinating...",
        f"{plant_name} sprout has emerged!",
        f"{plant_name} is growing leaves...",
        f"{plant_name} is developing stems...",
        f"{plant_name} is budding...",
        f"{plant_name} is flowering! 🌸",
        f"{plant_name} is producing fruit! 🍅"
    ]
    
    for stage in stages:
        yield stage


def seasonal_water_needs(base_amount):
    seasons = ['Spring', 'Summer', 'Fall', 'Winter']
    multipliers = [1.2, 1.5, 1.0, 0.8]
    
    while True:
        for season, mult in zip(seasons, multipliers):
            water_needed = base_amount * mult
            yield season, water_needed


# PLANT CLASS

class Plant:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        self.water_level = 100
        self.height = 0
        self.growth_stage = 0
    
    @log_growth
    def add_water(self, amount):
        self.water_level += amount
        print(f"💧 Added {amount}ml of water. Total: {self.water_level}ml")
    
    @log_growth
    @water_required(20)
    def grow(self):
        self.height += 5
        self.growth_stage += 1
        print(f"📏 {self.name} grew to {self.height}cm (Stage {self.growth_stage})")
    
    @log_growth
    @water_required(15)
    def photosynthesize(self):
        print(f"☀️  {self.name} is converting sunlight to energy!")
        self.height += 2
    
    def __repr__(self):
        return f"Plant('{self.name}', species='{self.species}', height={self.height}cm)"

def main():
    print("=" * 50)
    print("🌿 PLANT GROWTH SIMULATOR 🌿")
    print("=" * 50)
    print()
    
    tomato = Plant("Lance", "Tomato")
    print(f"Created plant: {tomato}\n")
    
    print("--- Growth Stages ---")
    stages = growth_stages(tomato.name)
    for i in range(4):
        print(f"Stage {i+1}: {next(stages)}")
    print()
    
    print("--- Seasonal Water Needs ---")
    seasons = seasonal_water_needs(base_amount=50)
    for _ in range(4):
        season, water = next(seasons)
        print(f"{season}: {water:.1f}ml needed")
    print()
    
    print("--- Growing the Plant ---")
    tomato.grow() 
    
    tomato.add_water(50)  
    
    tomato.grow()
    tomato.photosynthesize()
    tomato.grow()
    
    print(f"\nFinal state: {tomato}")
    print(f"Remaining water: {tomato.water_level}ml")


if __name__ == "__main__":
    main()