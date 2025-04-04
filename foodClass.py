class Food:
    def __init__(self, name, calories, protein, carbs):
        self.name = name
        self.calories = calories
        self.protein = protein
        self.carbs = carbs

    def __str__(self):
        return f"{self.name} has {self.calories} calories"


