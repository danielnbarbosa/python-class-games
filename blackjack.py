# Mini-project #6 - Blackjack
# Also available at http://www.codeskulptor.org/#user38_CfoPqPVnDy_9.py

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
money = 200
bet = 5

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = list()

    def __str__(self):
        result = ''
        for card in self.cards:
            result += card.get_suit() + card.get_rank() + ' '
        return "hand contains " + result
            
    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        has_ace = False
        result = 0
        for card in self.cards:
            if card.get_rank() == 'A':
                has_ace = True
            result += VALUES[card.get_rank()]
        if has_ace and result < 12:
            result += 10
        return result
        
    def draw(self, canvas, pos):
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += 100
 
# define deck class 
class Deck:
    def __init__(self):
        self.cards = list()
        for suit in SUITS:
            for rank in RANKS:
                new_card = Card(suit, rank)
                self.cards.append(new_card)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
    
    def cards_left(self):
        return len(self.cards)
    
    def __str__(self):
        result = ''
        for card in self.cards:
            result += card.get_suit() + card.get_rank() + ' '
        return "deck contains " + result


#define event handlers for buttons
def deal():
    global outcome, in_play, score, money, bet, deck, dealer_hand, player_hand
    
    if money <= 0:
        outcome = "You're broke!"
        in_play = False
    else:
        if in_play:
            outcome = 'You forfeited the round'
            money -= bet
        else:
            outcome = 'Hit or stand?'
    
        deck = Deck()
        deck.shuffle()
    
        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
    
        player_hand = Hand()
        player_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())

        in_play = True
    


def hit():
    global outcome, in_play, score, money, bet, deck, dealer_hand, player_hand
    
    if in_play:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = "You have busted"
            in_play = False
            money -= bet
        else:
            outcome = 'Hit or stand?'
               
def stand():
    global outcome, in_play, score, money, bet, deck, dealer_hand, player_hand
    
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value() > 21:
            outcome = "Dealer busted"
            in_play = False
            money += bet
        else:
            if player_hand.get_value() > dealer_hand.get_value():
                outcome = "You win!"
                in_play = False
                money += bet
            else:
                outcome = "Dealer wins"
                in_play = False
                money -= bet
    else:
        outcome = "You are already busted"

def raise_bet():
    global bet
    bet += 5

def lower_bet():
    global bet
    bet -= 5
        
# draw handler    
def draw(canvas):
    global outcome, in_play, score, money, bet, deck, dealer_hand, player_hand

    dealer_hand.draw(canvas, [20, 30])
    if in_play:
        canvas.draw_text("Dealer: ", (20, 20), 24, 'White')
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_SIZE, (CARD_BACK_CENTER[0] + 20, CARD_BACK_CENTER[1] + 30), CARD_SIZE)
    else:
        canvas.draw_text("Dealer: " + str(dealer_hand.get_value()), (20, 20), 24, 'White')

    canvas.draw_text("Player: " + str(player_hand.get_value()), (20, 190), 24, 'White')
    player_hand.draw(canvas, [20, 200])
    
    canvas.draw_text(outcome, (20, 400), 36, 'Yellow')
    canvas.draw_text("Money: $" + str(money), (450, 400), 24, 'White')
    canvas.draw_text("Bet: $" + str(bet), (450, 430), 24, 'White')
    canvas.draw_text("Blackjack", (200, 550), 48, 'White')


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_button("Raise Bet", raise_bet, 100)
frame.add_button("Lower Bet", lower_bet, 100)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
