class piece:
    def __init__(self, color, name):
        self.color = color
        self.name = name

    def __str__(self):
        return f"{self.color} {self.name}"