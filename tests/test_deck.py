import unittest

from src.card import Card
from src.deck import Deck


class TestDeck(unittest.TestCase):

    def test_deck_has_40_cards(self):
        deck = Deck()

        self.assertEqual(len(deck.cards), 40)

    def test_shuffle_keeps_same_number_of_cards(self):
        deck = Deck()

        original_cards = deck.cards.copy()
        deck.shuffle()

        self.assertEqual(len(deck.cards), 40)
        self.assertCountEqual(deck.cards, original_cards)

    def test_draw_card(self):
        deck = Deck()

        card = deck.draw_card()

        self.assertIsInstance(card, Card)
        self.assertEqual(len(deck.cards), 39)


if __name__ == "__main__":
    unittest.main()