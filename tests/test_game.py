import unittest

from src.card import Card
from src.game import Game


class TestGame(unittest.TestCase):

    def test_add_player(self):
        game = Game()

        game.add_player("Yazan")
        game.add_player("Ahmad")

        self.assertEqual(len(game.players), 2)
        self.assertEqual(game.players[0].name, "Yazan")
        self.assertEqual(game.players[1].name, "Ahmad")

    def test_deal_cards(self):
        game = Game()

        game.add_player("Yazan")
        game.add_player("Ahmad")

        game.deal_cards()

        self.assertEqual(len(game.players[0].hand), 8)
        self.assertEqual(len(game.players[1].hand), 8)
        self.assertEqual(len(game.deck.cards), 24)

    def test_start_discard_pile(self):
        game = Game()

        game.add_player("Yazan")
        game.add_player("Ahmad")
        game.deal_cards()

        game.start_discard_pile()

        self.assertEqual(len(game.discard_pile), 1)
        self.assertIsInstance(game.discard_pile[0], Card)
        self.assertEqual(len(game.deck.cards), 23)

    def test_play_card(self):
        game = Game()

        game.add_player("Yazan")

        player = game.players[0]

        top_card = Card("red", 5)
        playable_card = Card("red", 8)

        game.discard_pile.append(top_card)
        player.add_card(playable_card)

        result = game.play_card(player, playable_card)

        self.assertTrue(result)
        self.assertEqual(len(player.hand), 0)
        self.assertEqual(game.discard_pile[-1], playable_card)    

    def test_draw_card_for_player(self):
        game = Game()
        game.add_player("Yazan")
        player = game.players[0]
        cards_before = len(game.deck.cards)
        hand_before = len(player.hand)
        card = game.draw_card_for_player(player)
        self.assertIsInstance(card, Card)
        self.assertEqual(len(game.deck.cards), cards_before - 1)
        self.assertEqual(len(player.hand), hand_before + 1)
        self.assertIn(card, player.hand)

    def test_next_player(self):
        game = Game()
        game.add_player("Yazan")
        game.add_player("Ahmad")
        self.assertEqual(game.get_current_player().name, "Yazan")
        game.next_player()
        self.assertEqual(game.get_current_player().name, "Ahmad")
        game.next_player()
        self.assertEqual(game.get_current_player().name, "Yazan")

    def test_has_winner(self):
        game = Game()
        game.add_player("Yazan")
        game.add_player("Ahmad")
        game.players[0].add_card(Card("red", 5))
        game.players[1].add_card(Card("blue", 8))
        winner = game.has_winner()
        self.assertIsNone(winner)
        game.players[0].hand = []
        winner = game.has_winner()
        self.assertEqual(winner.name, "Yazan")

    def test_refill_deck(self):
        game = Game()
        top_card = Card("red", 5)
        discard_card_1 = Card("blue", 2)
        discard_card_2 = Card("green", 7)
        game.discard_pile = [
            discard_card_1,
            discard_card_2,
            top_card]

        game.deck.cards = []
        game.refill_deck()
        self.assertEqual(len(game.deck.cards), 2)
        self.assertEqual(game.discard_pile, [top_card])
        self.assertCountEqual(
            game.deck.cards,
            [discard_card_1, discard_card_2]
        )
        
if __name__ == "__main__":
    unittest.main()