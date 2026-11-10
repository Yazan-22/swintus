import tkinter as tk
from tkinter import messagebox

from .game import Game

DEFAULT_PLAYERS = ["", ""]
MAX_PLAYERS = 10
CARDS_PER_PLAYER = 8

# Color palette
BG = "#0B1020"
PANEL = "#141E32"
PANEL_LIGHT = "#1C2943"
BORDER = "#293854"
TEXT = "#F7F9FF"
MUTED = "#A2B1CE"
GOLD = "#F8BE60"
GREEN = "#7CE7A5"

CARD_COLORS = {
    "red": "#D64F62",
    "blue": "#477ADB",
    "green": "#2A9F7C",
    "yellow": "#EEC65A",
}


class SwintusGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SWINTUS | Card Game")
        self.root.geometry("1120x800")
        self.root.minsize(900, 690)
        self.root.configure(bg=BG)

        self.player_vars = [tk.StringVar(value=name) for name in DEFAULT_PLAYERS]
        self.game = None
        self.game_over = False
        self.screen = None
        self._show_setup()

    def _clear_screen(self):
        if self.screen is not None:
            self.screen.destroy()
        self.screen = tk.Frame(self.root, bg=BG)
        self.screen.pack(fill="both", expand=True)

    @staticmethod
    def _button(parent, text, command, bg=PANEL_LIGHT, fg=TEXT, **kwargs):
        options = dict(
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=BORDER,
            activeforeground=TEXT,
            disabledforeground=MUTED,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Arial", 11, "bold"),
            padx=16,
            pady=10,
        )
        options.update(kwargs)
        return tk.Button(parent, **options)

    def _show_setup(self):
        """Player setup. More players means more entries, not new GUI code."""
        self._clear_screen()

        tk.Label(
            self.screen, text="SWINTUS", bg=BG, fg=GOLD,
            font=("Arial", 38, "bold"),
        ).pack(pady=(56, 8))
        tk.Label(
            self.screen, text="A card game night starts here",
            bg=BG, fg=MUTED, font=("Arial", 14),
        ).pack(pady=(0, 34))

        panel = tk.Frame(self.screen, bg=PANEL, padx=28, pady=24)
        panel.pack(fill="x", padx=80)

        tk.Label(
            panel, text="SET UP YOUR TABLE", bg=PANEL, fg=TEXT,
            font=("Arial", 18, "bold"),
        ).pack(anchor="w", pady=(0, 7))
        tk.Label(
            panel,
            text="Add players, enter their names, and start playing.",
            bg=PANEL, fg=MUTED, font=("Arial", 11),
        ).pack(anchor="w", pady=(0, 16))

        entry_area = tk.Frame(panel, bg=PANEL)
        entry_area.pack(fill="both", expand=True)

        # Keep a manageable height when there are many players.
        columns = 2 if len(self.player_vars) > 5 else 1
        for i, name_var in enumerate(self.player_vars):
            column = i % columns
            row = i // columns
            item = tk.Frame(entry_area, bg=PANEL)
            item.grid(row=row, column=column, sticky="ew", padx=(0, 18), pady=5)
            entry_area.grid_columnconfigure(column, weight=1)

            tk.Label(
                item, text=f"{i + 1:02d}", bg=PANEL, fg=GOLD,
                font=("Arial", 12, "bold"), width=3,
            ).pack(side="left")
            entry = tk.Entry(
                item, textvariable=name_var, font=("Arial", 12),
                bg=PANEL_LIGHT, fg=TEXT, insertbackground=TEXT,
                relief="flat", highlightthickness=1,
                highlightbackground=BORDER, highlightcolor=GOLD,
            )
            entry.pack(side="left", fill="x", expand=True, ipady=7, padx=9)
            if len(self.player_vars) > 2:
                self._button(
                    item, "Remove", lambda index=i: self._remove_player(index),
                    bg=PANEL_LIGHT, fg=MUTED, padx=8, pady=7,
                ).pack(side="left")

        controls = tk.Frame(panel, bg=PANEL)
        controls.pack(fill="x", pady=(20, 0))
        add_btn = self._button(
            controls, "+ Add player", self._add_player,
            bg=PANEL_LIGHT, fg=TEXT,
        )
        add_btn.pack(side="left")
        if len(self.player_vars) >= MAX_PLAYERS:
            add_btn.config(state="disabled")

        self._button(
            controls, "START GAME", self._start_game,
            bg=GOLD, fg=BG, padx=26,
        ).pack(side="right")

        tk.Label(
            self.screen,
            text=f"{len(self.player_vars)} players selected  •  {CARDS_PER_PLAYER} cards each  •  2–{MAX_PLAYERS} players supported",
            bg=BG, fg=MUTED, font=("Arial", 10),
        ).pack(pady=20)

    def _add_player(self):
        if len(self.player_vars) < MAX_PLAYERS:
            self.player_vars.append(
                tk.StringVar(value=f"Player {len(self.player_vars) + 1}")
            )
            self._show_setup()

    def _remove_player(self, index):
        if len(self.player_vars) > 2:
            del self.player_vars[index]
            self._show_setup()

    def _start_game(self):
        names = [var.get().strip() for var in self.player_vars]
        if any(not name for name in names):
            messagebox.showwarning("Player names", "Please enter a name for every player.")
            return
        if len(set(name.lower() for name in names)) != len(names):
            messagebox.showwarning("Player names", "Please use different names for each player.")
            return

        self.game = Game()
        for name in names:
            self.game.add_player(name)

        # The current project deck has 40 cards. For larger groups, combine
        # enough 40-card sets to deal 8 per player and start the discard pile.
        cards_needed = len(names) * CARDS_PER_PLAYER + 1
        while len(self.game.deck.cards) < cards_needed:
            self.game.deck.create_deck()

        self.game.start()
        self.game_over = False
        self._build_game_screen()
        self.refresh_gui()

    def _build_game_screen(self):
        self._clear_screen()
        page = tk.Frame(self.screen, bg=BG)
        page.pack(fill="both", expand=True, padx=26, pady=18)

        header = tk.Frame(page, bg=BG)
        header.pack(fill="x", pady=(0, 13))
        titles = tk.Frame(header, bg=BG)
        titles.pack(side="left")
        tk.Label(
            titles, text="SWINTUS", fg=GOLD, bg=BG,
            font=("Arial", 26, "bold"),
        ).pack(anchor="w")
        tk.Label(
            titles, text="THE CARD TABLE", fg=MUTED, bg=BG,
            font=("Arial", 9, "bold"),
        ).pack(anchor="w")

        self._button(
            header, "NEW GAME", self._show_setup, bg=PANEL_LIGHT,
        ).pack(side="right", padx=(12, 0))
        tk.Label(
            header, text=f"{len(self.game.players)} PLAYERS", bg=BG,
            fg=MUTED, font=("Arial", 11, "bold"),
        ).pack(side="right", padx=10)

        tk.Label(
            page, text="PLAYERS", bg=BG, fg=MUTED,
            font=("Arial", 10, "bold"),
        ).pack(anchor="w", pady=(2, 4))
        self.players_frame = tk.Frame(page, bg=BG)
        self.players_frame.pack(fill="x", pady=(0, 14))

        table = tk.Frame(page, bg=PANEL, padx=20, pady=17)
        table.pack(fill="both", expand=True)
        tk.Label(
            table, text="MATCH THE COLOR OR THE NUMBER",
            bg=PANEL, fg=MUTED, font=("Arial", 10, "bold"),
        ).pack(pady=(0, 14))

        middle = tk.Frame(table, bg=PANEL)
        middle.pack(expand=True)
        draw_section = tk.Frame(middle, bg=PANEL)
        draw_section.pack(side="left", padx=20)
        self.draw_button = self._button(
            draw_section, "SWINTUS\n\nDRAW CARD", self.draw_card,
            bg="#304366", fg=TEXT, width=12, height=5,
        )
        self.draw_button.pack()
        tk.Label(
            draw_section, text="DRAW PILE", bg=PANEL, fg=MUTED,
            font=("Arial", 10, "bold"),
        ).pack(pady=(8, 0))

        discard_section = tk.Frame(middle, bg=PANEL)
        discard_section.pack(side="left", padx=20)
        self.discard_label = tk.Label(
            discard_section, text="", bg=PANEL_LIGHT, fg=TEXT,
            font=("Arial", 26, "bold"), width=10, height=4,
            relief="flat",
        )
        self.discard_label.pack()
        tk.Label(
            discard_section, text="DISCARD PILE", bg=PANEL, fg=MUTED,
            font=("Arial", 10, "bold"),
        ).pack(pady=(8, 0))

        self.status_label = tk.Label(
            table, text="", bg=PANEL, fg=GREEN,
            font=("Arial", 12, "bold"),
        )
        self.status_label.pack(pady=(13, 1))

        hand_panel = tk.Frame(page, bg=PANEL, padx=18, pady=13)
        hand_panel.pack(fill="x", pady=(14, 0))
        self.hand_title = tk.Label(
            hand_panel, text="", bg=PANEL, fg=TEXT,
            font=("Arial", 16, "bold"),
        )
        self.hand_title.pack(anchor="w", pady=(0, 10))

        self.hand_canvas = tk.Canvas(
            hand_panel, bg=PANEL, height=102,
            highlightthickness=0, bd=0,
        )
        self.hand_canvas.pack(fill="x")
        self.hand_content = tk.Frame(self.hand_canvas, bg=PANEL)
        self.hand_canvas.create_window(
            (0, 0), window=self.hand_content, anchor="nw",
        )
        self.hand_content.bind(
            "<Configure>",
            lambda event: self.hand_canvas.configure(
                scrollregion=self.hand_canvas.bbox("all")
            ),
        )
        scroll = tk.Scrollbar(
            hand_panel, orient="horizontal", command=self.hand_canvas.xview,
        )
        scroll.pack(fill="x", pady=(5, 0))
        self.hand_canvas.configure(xscrollcommand=scroll.set)
        tk.Label(
            hand_panel, text="Playable cards are highlighted. Scroll to see more cards.",
            bg=PANEL, fg=MUTED, font=("Arial", 10),
        ).pack(anchor="w", pady=(6, 0))

    def _draw_player_tiles(self):
        for child in self.players_frame.winfo_children():
            child.destroy()
        players = self.game.players
        columns = min(len(players), 5)
        for col in range(columns):
            self.players_frame.grid_columnconfigure(col, weight=1, uniform="player")

        for index, player in enumerate(players):
            active = index == self.game.current_player_index
            tile = tk.Frame(
                self.players_frame,
                bg=PANEL_LIGHT if active else PANEL,
                highlightthickness=2 if active else 1,
                highlightbackground=GOLD if active else BORDER,
                padx=11, pady=10,
            )
            tile.grid(
                row=index // columns, column=index % columns,
                padx=4, pady=4, sticky="nsew",
            )
            tk.Label(
                tile, text=("● YOUR TURN" if active else "PLAYER"),
                bg=tile["bg"], fg=GOLD if active else MUTED,
                font=("Arial", 9, "bold"),
            ).pack(anchor="w")
            tk.Label(
                tile, text=player.name, bg=tile["bg"], fg=TEXT,
                font=("Arial", 13, "bold"), anchor="w",
            ).pack(anchor="w", pady=(4, 2))
            tk.Label(
                tile, text=f"{len(player.hand)} cards remaining",
                bg=tile["bg"], fg=MUTED, font=("Arial", 10),
            ).pack(anchor="w")

    def refresh_gui(self, notice=None):
        current = self.game.get_current_player()
        top_card = self.game.discard_pile[-1]
        self._draw_player_tiles()

        card_bg = CARD_COLORS.get(top_card.color, PANEL_LIGHT)
        card_fg = BG if top_card.color == "yellow" else TEXT
        self.discard_label.config(
            text=f"{top_card.value}\n{top_card.color.upper()}",
            bg=card_bg, fg=card_fg,
        )
        self.hand_title.config(
            text=f"{current.name}'s hand  •  {len(current.hand)} cards"
        )

        for child in self.hand_content.winfo_children():
            child.destroy()
        for card in current.hand:
            playable = not self.game_over and card.can_play_on(top_card)
            card_bg = CARD_COLORS.get(card.color, PANEL_LIGHT)
            card_fg = BG if card.color == "yellow" else TEXT
            card_text = f"{card.value}\n{card.color.upper()}"
            tile = self._button(
                    self.hand_content,
                    card_text,
                    lambda chosen=card: self.play_card(chosen),
                    bg=card_bg,
                    fg=card_fg,
                    activeforeground=card_fg,
                    width=8,
                    height=2,
                    font=("Arial", 13, "bold"),
                    highlightthickness=2 if playable else 0,
                    highlightbackground=GOLD if playable else BORDER,
                )
            if self.game_over:
                    tile.config(state="disabled")
            tile.pack(side="left", padx=(0, 9), pady=4)

        self.hand_canvas.xview_moveto(0)
        self.draw_button.config(state="disabled" if self.game_over else "normal")
        self.status_label.config(
            text=notice or f"{current.name}'s turn — choose a matching card or draw"
        )

    def play_card(self, card):
        if self.game_over:
            return
        player = self.game.get_current_player()
        if not self.game.play_card(player, card):
            messagebox.showinfo(
                "Invalid move", "Choose a card matching the color or number."
            )
            return

        winner = self.game.has_winner()
        if winner:
            self.game_over = True
            self.refresh_gui(f"{winner.name} wins! Congratulations!")
            messagebox.showinfo("Game over", f"{winner.name} wins!")
            return

        self.game.next_player()
        self.refresh_gui()

    def draw_card(self):
        if self.game_over:
            return
        player = self.game.get_current_player()
        top_card = self.game.discard_pile[-1]
        if player.get_playable_cards(top_card):
            messagebox.showinfo(
                "Playable cards", "You already have a matching card. Play it first!"
            )
            return

        try:
            drawn = self.game.draw_card_for_player(player)
        except ValueError:
            self.game.next_player()
            self.refresh_gui("No cards left to draw. Turn passed.")
            return

        if drawn.can_play_on(top_card):
            self.refresh_gui(f"{player.name} drew a playable card — you can play it now!")
        else:
            self.game.next_player()
            self.refresh_gui()


def main():
    root = tk.Tk()
    SwintusGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
