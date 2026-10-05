import random
from .card import Card


class Deck:
    def __init__(self):
        self.cards = []
        self.create_deck()

    def add_card(self, card):
        self.cards.append(card)

    def create_deck(self):
        colors = ["red", "blue", "green", "yellow"]

        for color in colors:
            for value in range(10):
                card = Card(color, value)
                self.add_card(card) 
    
    def shuffle(self):
        random.shuffle(self.cards)  

    def draw_card(self):
        if not self.cards:
            raise ValueError("The deck is empty.")

        return self.cards.pop()
    