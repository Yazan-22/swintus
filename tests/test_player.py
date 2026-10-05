import unittest

from src.card import Card
from src.player import Player


class TestPlayer(unittest.TestCase):

    def test_add_card(self):
        player = Player("Yazan")
        card = Card("red", 5)

        player.add_card(card)

        self.assertEqual(len(player.hand), 1)
        self.assertEqual(player.hand[0], card)

    def test_get_playable_cards(self):
        player = Player("Yazan")

        card1 = Card("red", 5)
        card2 = Card("blue", 5)
        card3 = Card("green", 8)

        player.add_card(card1)
        player.add_card(card2)
        player.add_card(card3)

        top_card = Card("red", 9)

        playable_cards = player.get_playable_cards(top_card)

        self.assertEqual(len(playable_cards), 1)
        self.assertEqual(playable_cards[0], card1)

    def test_play_card(self):
        player = Player("Yazan")
        card = Card("red", 5)

        player.add_card(card)

        played_card = player.play_card(card)

        self.assertEqual(played_card, card)
        self.assertEqual(len(player.hand), 0)


if __name__ == "__main__":
    unittest.main()