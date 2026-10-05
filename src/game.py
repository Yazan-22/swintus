from .deck import Deck
from .player import Player


class Game:
    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.current_player_index = 0
        self.discard_pile = []

    def get_current_player(self):
        return self.players[self.current_player_index]    
    
    def next_player(self):
        self.current_player_index = (
            self.current_player_index + 1
        ) % len(self.players)

    def add_player(self, name):
        player = Player(name)
        self.players.append(player)

    def deal_cards(self, cards_per_player=8):
        self.deck.shuffle()

        for player in self.players:
            for _ in range(cards_per_player):
                card = self.deck.draw_card()
                player.add_card(card)

    def start_discard_pile(self):
        card = self.deck.draw_card()
        self.discard_pile.append(card)
    
    def refill_deck(self):
        top_card = self.discard_pile[-1]
        cards_to_shuffle = self.discard_pile[:-1]
        self.deck.cards = cards_to_shuffle
        self.discard_pile = [top_card]
        self.deck.shuffle()

    def play_card(self, player, card):
        top_card = self.discard_pile[-1]

        if not card.can_play_on(top_card):
            return False
        played_card = player.play_card(card)
        self.discard_pile.append(played_card)
        return True
    
    def draw_card_for_player(self, player):
        if not self.deck.cards:
            self.refill_deck()

        card = self.deck.draw_card()
        player.add_card(card)
        return card
    
    def take_turn(self):
        player = self.get_current_player()
        top_card = self.discard_pile[-1]

        playable_cards = player.get_playable_cards(top_card)

        if playable_cards:
            card = playable_cards[0]
            self.play_card(player, card)
            result = f"{player.name} played {card}"
        else:
            card = self.draw_card_for_player(player)
            result = f"{player.name} drew {card}"

        self.next_player()

        return result
    
    def has_winner(self):
        for player in self.players:
            if len(player.hand) == 0:
                return player

        return None
    
    def start(self):
        self.deal_cards()
        self.start_discard_pile()
        self.current_player_index = 0

    def play_game(self):
        while self.has_winner() is None:
            result = self.take_turn()
            print(result)

        winner = self.has_winner()
        print(f"Winner: {winner.name}")    