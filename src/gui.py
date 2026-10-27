
import tkinter as tk
from tkinter import messagebox

from .game import Game


COLORS = {
    "red": "#741717",
    "blue": "#0f327e",
    "green": "#106930",
    "yellow": "#ddcb26",
}


class SwintusGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Swintus")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1f2937")

        self.game = Game()
        self.game.add_player("Yazan")
        self.game.add_player("Ahmad")
        self.game.add_player("Bashar")
        self.game.start()

        self.game_over = False

        tk.Label(
            root,
            text="SWINTUS",
            font=("Arial", 28, "bold"),
            bg="#1f2937",
            fg="white",
        ).pack(pady=12)
        
        self.opponent_label = tk.Label(
            root,
            font=("Arial", 16),
            bg="#1f2937",
            fg="white",
        )
        self.opponent_label.pack(pady=10)

        center = tk.Frame(root, bg="#1f2937")
        center.pack(pady=20)

        self.draw_button = tk.Button(
            center,
            text="DRAW\nCARD",
            font=("Arial", 14, "bold"),
            width=10,
            height=4,
            bg="#374151",
            fg="white",
            command=self.draw_card,
        )
        self.draw_button.pack(side="left", padx=25)

        self.discard_label = tk.Label(
            center,
            font=("Arial", 20, "bold"),
            width=8,
            height=4,
            fg="white",
        )
        self.discard_label.pack(side="left", padx=25)

        self.player_label = tk.Label(
            root,
            font=("Arial", 16, "bold"),
            bg="#1f2937",
            fg="#4ade80",
        )
        self.player_label.pack(pady=10)

        self.hand_frame = tk.Frame(root, bg="#1f2937")
        self.hand_frame.pack(pady=10)

        self.status_label = tk.Label(
            root,
            text="",
            font=("Arial", 13),
            bg="#1f2937",
            fg="white",
        )
        self.status_label.pack(pady=12)

        self.refresh_gui()

    def refresh_gui(self):
        current = self.game.get_current_player()
        print(self.game.players)
        opponents = [p for p in self.game.players if p.name != current.name]
        opponent = self.game.players[
            1 - self.game.current_player_index
        ]
        top_card = self.game.discard_pile[-1]

        self.opponent_label.config(
            text=f"{opponent.name} — {len(opponent.hand)} cards"
        )

        self.player_label.config(
            text=f"{current.name}'s hand — {len(current.hand)} cards"
        )

        self.discard_label.config(
            text=f"{top_card.value}",
            bg=COLORS[top_card.color],
        )

        for widget in self.hand_frame.winfo_children():
            widget.destroy()

        for card in current.hand:
            button = tk.Button(
                self.hand_frame,
                text=f"{card.value}",
                font=("Arial", 15, "bold"),
                width=8,
                height=3,
                bg=COLORS[card.color],
                fg="white",
                command=lambda selected_card=card: self.play_card(
                    selected_card
                ),
            )
            button.pack(side="left", padx=3, pady=3)

        self.status_label.config(
            text=f"{current.name}'s turn — select a card or draw"
        )

    def play_card(self, card):
        if self.game_over:
            return

        player = self.game.get_current_player()

        success = self.game.play_card(player, card)

        if not success:
            messagebox.showinfo(
                "Invalid move",
                "Choose a card matching the color or number "
                "of the top discard card.",
            )
            return

        winner = self.game.has_winner()

        if winner:
            self.game_over = True
            self.refresh_gui()
            self.status_label.config(text=f"{winner.name} wins!")
            self.draw_button.config(state="disabled")
            messagebox.showinfo("Game over", f"{winner.name} wins!")
            return

        self.game.next_player()
        self.refresh_gui()

    def draw_card(self):
        if self.game_over:
            return
        
        player = self.game.get_current_player()
        top_card = self.game.discard_pile[-1]
        playable_cards = player.get_playable_cards(top_card) 
        if playable_cards:
            messagebox.showinfo("Error", "You have playable cards!")
            return    
        card = self.game.draw_card_for_player(player)
        if not card.can_play_on(top_card):
            self.game.next_player()  
        self.refresh_gui()

                
        


def main():
    root = tk.Tk()
    SwintusGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
