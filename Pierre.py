import tkinter as tk
from tkinter import messagebox
import random

# Valeurs et types des cartes
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

# Créer un deck de cartes
def create_deck():
    return [(value, suit) for value in values for suit in suits]

# Tirer une carte du deck
def draw_card(deck):
    if len(deck) == 0:
        deck.extend(create_deck())
    card = random.choice(deck)
    deck.remove(card)
    return card

# Calculer le score d'une main
def calculate_score(hand):
    score = 0
    ace_count = 0
    for card in hand:
        value, suit = card
        if value in 'JQK':
            score += 10
        elif value == 'A':
            ace_count += 1
            score += 11
        else:
            score += int(value)
    while score > 21 and ace_count:
        score -= 10
        ace_count -= 1
    return score

class BlackjackGame:
    def __init__(self, master):
        self.master = master
        master.title('Blackjack')

        # État initial du jeu
        self.deck = create_deck()
        random.shuffle(self.deck)
        self.player_hand = [draw_card(self.deck), draw_card(self.deck)]
        self.dealer_hand = [draw_card(self.deck), draw_card(self.deck)]
        
        # Configuration de l'interface
        self.status_var = tk.StringVar()
        self.status_var.set("Hit or Stand?")
        self.label_status = tk.Label(master, textvariable=self.status_var)
        self.label_status.pack()

        self.player_score_var = tk.StringVar()
        self.player_score_var.set(f"Player Score: {calculate_score(self.player_hand)}")
        self.label_player_score = tk.Label(master, textvariable=self.player_score_var)
        self.label_player_score.pack()
        
        self.dealer_score_var = tk.StringVar()
        self.dealer_score_var.set("Dealer Score: ???")
        self.label_dealer_score = tk.Label(master, textvariable=self.dealer_score_var)
        self.label_dealer_score.pack()

        self.button_hit = tk.Button(master, text="Hit", command=self.hit)
        self.button_hit.pack(side=tk.LEFT)

        self.button_stand = tk.Button(master, text="Stand", command=self.stand)
       .button_stand.pack(side=tk.RIGHT)

    def hit(self):
        self.player_hand.append(draw_card(self.deck))
        score = calculate_score(self.player_hand)
        self.player_score_var.set(f"Player Score: {score}")
        if score > 21:
            self.status_var.set("Player busts! You lose.")
            self.end_game()

    def stand(self):
        dealer_score = calculate_score(self.dealer_hand)
        while dealer_score < 17:
            self.dealer_hand.append(draw_card(self.deck))
            dealer_score = calculate_score(self.dealer_hand)
        
        player_score = calculate_score(self.player_hand)
        self.dealer_score_var.set(f"Dealer Score: {dealer_score}")

        if dealer_score > 21 or dealer_score < player_score:
            self.status_var.set("Dealer busts or player wins!")
        elif dealer_score == player_score:
            self.status_var.set("Push! It's a tie.")
        else:
            self.status_var.set("Dealer wins!")
        self.end_game()

    def end_game(self):
        self.button_hit['state'] = 'disabled'
        self.button_stand['state'] = 'disabled'
        
# Créer et lancer la fenêtre principale
root = tk.Tk()
game = BlackjackGame(root)
root.mainloop()