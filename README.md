# Swintus

Swintus is a Python card game with a graphical user interface (GUI) built using Tkinter. It supports local player-versus-player (PvP) gameplay.

## Objective

Be the first player to get rid of all the cards in your hand.

Players take turns playing cards that match the top card of the discard pile by color or number.

## Current Implementation

The current MVP includes:

- Object-oriented design using `Card`, `Deck`, `Player`, and `Game` classes.
- A 40-card deck with four colors and numbers from 0 to 9.
- Shuffling and dealing 8 cards to each player.
- A discard pile and a draw pile.
- Playing cards that match by color or number.
- Drawing a card when no playable card is available.
- Switching turns between two local players.
- Detecting the winner when a player's hand becomes empty.
- A graphical interface built with Tkinter.
- Unit tests for the core game logic.

**Note:** Special cards, scoring, the "Swintus!" announcement, and interception are not implemented in the current MVP.

## Requirements

- Python 3.10 or newer recommended.
- Tkinter (usually included with standard Python installations).

No external Python packages are required for the current implementation.

## How to Run

Open a terminal in the project root directory.

Run the game:

```bash
python -m src.main
```

Run the unit tests:

```bash
python -m unittest discover -s tests
```

## How to Play

1. Start the game.
2. Two players take turns using the same computer.
3. Look at the top card of the discard pile.
4. Select a playable card from your hand, or draw a card when you cannot play.
5. The turn switches to the other player.
6. The first player to empty their hand wins.

## Project Structure

```text
swintus/
├── src/
│   ├── __init__.py
│   ├── card.py
│   ├── deck.py
│   ├── game.py
│   ├── main.py
│   └── player.py
├── tests/
│   ├── test_card.py
│   ├── test_deck.py
│   ├── test_game.py
│   └── test_player.py
├── .gitignore
└── README.md
```

## Planned Features

The following features may be added in future versions:

- Special cards such as Grab, Snorer, Reverse, and Color Change.
- The "Swintus!" announcement and associated penalties.
- Interception and reaction cards.
- Scoring and additional game rules.
- Improvements to the graphical interface.

## Technologies

- Python
- Tkinter
- `unittest`
- Git and GitHub
