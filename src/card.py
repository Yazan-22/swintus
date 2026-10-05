class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __str__(self):
        return f"{self.color} {self.value}"
    
    def can_play_on(self, other_card):
        return self.color == other_card.color or self.value == other_card.value