import random
from .card import Card

SPECIAL_CARDS = [
    {"value":"reverse", "number_per_color":1},
]

class Deck:
    def __init__(self):
        self.cards:list[Card] = []
        self.create_deck()

    def add_card(self, card):
        self.cards.append(card)

    def create_deck(self):
        colors = ["red", "blue", "green", "yellow"]

        for color in colors:
            for value in range(10):
                card = Card(color, value)
                self.add_card(card)
            for special_card in SPECIAL_CARDS:
                for _ in range(special_card["number_per_color"]):
                    card = Card(color,special_card["value"] )
                    self.add_card(card)

        #print([card for card in self.cards if card.value =='reverse'])
        
            
        # addd reverse card         
    
    def shuffle(self):
        random.shuffle(self.cards)  

    def draw_card(self) -> Card:
        if not self.cards:
            raise ValueError("The deck is empty.")

        return self.cards.pop()
    