import tkinter as tk                    #Tkinter est la bibliotheque d interface graphique de python. On import la bibliotheque de tkinter.
from tkinter import messagebox          #Messagebox permet d afficher le resultat de la partie.
import random
                                         #Creation  de la logique du jeu.
class Blackjack:                         
    def __init__(self, master):
        self.master = master
        self.master.title("Blackjack")
        
        self.deck = Deck()             #creation du deck de carte pour la partie et de l'interface graphique.
        self.deck.shuffle()
        
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        
        self.create_widgets()
        self.deal_cards()
        
    def create_widgets(self):
        self.player_label = tk.Label(self.master, text="Joueur")       #La fonction Label permet de pouvoir afficher des textes dans le jeu, ici on affiche les textes suivants : 
        self.player_label.grid(row=0, column=0)                        # Joueur , score ,croupier. 
        
        self.player_score_label = tk.Label(self.master, text="Score: ")
        self.player_score_label.grid(row=0, column=1)
        
        self.player_hand_label = tk.Label(self.master, text="")
        self.player_hand_label.grid(row=1, column=0, columnspan=2)
        
        self.dealer_label = tk.Label(self.master, text="Croupier")
        self.dealer_label.grid(row=2, column=0)
        
        self.dealer_score_label = tk.Label(self.master, text="Score: ")
        self.dealer_score_label.grid(row=2, column=1)
        
        self.dealer_hand_label = tk.Label(self.master, text="")
        self.dealer_hand_label.grid(row=3, column=0, columnspan=2)
        
        self.hit_button = tk.Button(self.master, text="hit", command=self.hit)     #creation de bouton 'Hit' aui permet au joueur de tirer une carte si il le souhaite.
        self.hit_button.grid(row=4, column=0)
        
        self.stand_button = tk.Button(self.master, text="Stand", command=self.stand)
        self.stand_button.grid(row=4, column=1)
        
    def deal_cards(self):
        for _ in range(2):
            self.player_hand.add_card(self.deck.deal())
            self.dealer_hand.add_card(self.deck.deal())
        self.update_display()
        
    def update_display(self):
        self.player_hand_label.config(text=str(self.player_hand))
        self.player_score_label.config(text="Score: {}".format(self.player_hand.get_value()))
        
        self.dealer_hand_label.config(text=str(self.dealer_hand))
        self.dealer_score_label.config(text="Score: {}".format(self.dealer_hand.get_value()))
        
    def hit(self):
        self.player_hand.add_card(self.deck.deal())       #Creation du bouton 'hit' qui va permet au joueur de tirer une carte si il le veut.
        self.update_display()                             #En fonction de la carte tiree et du resultat cela affichera si le joueur gagne ou non.
        player_score = self.player_hand.get_value()
        if player_score > 21:
            messagebox.showinfo("Résultat", "Vous avez dépassé 21. Croupier gagne!")
            self.reset_game()
        
    def stand(self):
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.deal())
            self.update_display()
        player_score = self.player_hand.get_value()
        dealer_score = self.dealer_hand.get_value()
        if dealer_score > 21 or player_score > dealer_score:
            messagebox.showinfo("Résultat", "Vous gagnez!")
        elif dealer_score > player_score:
            messagebox.showinfo("Résultat", "Croupier gagne!")
        else:
            messagebox.showinfo("Résultat", "Égalité!")
        self.reset_game()
        
    def reset_game(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand.clear()
        self.dealer_hand.clear()
        self.deal_cards()

class Card:
    def __init__(self, suit, value):                                   #Definition du deck de carte avec les valeurs(value), et les classes (suit). 
        self.suit = suit                                               #La fonction .append va permet d ajouter une valeur et une classe a chaque carte du deck.
        self.value = value                                             #la fonction str permet d afficher une chaine de caractere, ici on veut afficher la valeur et la classe de la carte.
        
    def __str__(self):
        return "{}{}".format(self.value, self.suit)

class Deck:                                                
    def __init__(self):
        self.cards = []
        suits = ['♠', '♥', '♦', '♣']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for suit in suits:
            for value in values:
                self.cards.append(Card(suit, value))
                
    def shuffle(self):
        random.shuffle(self.cards)
        
    def deal(self):
        return self.cards.pop()
    
class Hand:
    def __init__(self):
        self.cards = []
        
    def add_card(self, card):
        self.cards.append(card)
        
    def get_value(self):
        value = 0
        num_aces = 0
        for card in self.cards:
            if card.value.isdigit():
                value += int(card.value)
            elif card.value in ['J', 'Q', 'K']:
                value += 10
            elif card.value == 'A':
                num_aces += 1
                value += 11
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1
        return value
    
    def clear(self):
        self.cards = []
        
    def __str__(self):
        return ", ".join(str(card) for card in self.cards)

if __name__ == "__main__":
    root = tk.Tk()
    game = Blackjack(root)
    root.mainloop()                                    #La fonction mainloop permet de repeter l operation.