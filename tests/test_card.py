import unittest

from src.card import Card


class TestCard(unittest.TestCase):

    def test_same_color(self):
        card1 = Card("red", 5)
        card2 = Card("red", 8)

        self.assertTrue(card1.can_play_on(card2))

    def test_same_value(self):
        card1 = Card("red", 5)
        card2 = Card("blue", 5)

        self.assertTrue(card1.can_play_on(card2))

    def test_different_color_and_value(self):
        card1 = Card("red", 5)
        card2 = Card("blue", 8)

        self.assertFalse(card1.can_play_on(card2))


if __name__ == "__main__":
    unittest.main()