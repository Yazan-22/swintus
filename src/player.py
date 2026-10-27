from src.card import Card

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
    def __str__(self):
        return f"{self.name}"
    def __repr__(self):
        return f"{self.name}"
    
    
    def add_card(self, card):
        self.hand.append(card)

    def get_playable_cards(self, top_card):
        return [card for card in self.hand if card.can_play_on(top_card)]     
    
    def play_card(self, card) -> Card:
        self.hand.remove(card)
        return card