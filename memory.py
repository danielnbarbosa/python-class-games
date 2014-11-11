# implementation of card game - Memory
# Also available at http://www.codeskulptor.org/#user38_KfGDUKP3he_10.py

"""
Explanation of game states:
0: start of the game, all cards face down
1: a single exposed, unpaired card
2: end of a turn, two cards exposed
"""

import simplegui
import random

# define constants
X_CARDS = 4
Y_CARDS = 4
CARDS = X_CARDS * Y_CARDS
CARD_WIDTH = 150
CARD_HEIGHT = 175
X_PAD = 20
Y_PAD = 20
SLOT_WIDTH = CARD_WIDTH + X_PAD
SLOT_HEIGHT = CARD_HEIGHT + Y_PAD

# define media assets
FRONT_IMAGE = simplegui.load_image('http://i.istockimg.com/file_thumbview_approve/6910013/2/stock-illustration-6910013-slot-symbols.jpg')
FRONT_IMAGE_BW = simplegui.load_image('https://dl.dropboxusercontent.com/u/1237849/stock-illustration-6910013-slot-symbols-black-and-white.jpg')
FRONT_IMAGE_POS = { 0: (67, 70), 1: (193, 69), 2: (310, 69),
                   3: (65, 191), 4: (311, 313), 5: (311, 191),
                   6: (66, 313), 7: (190, 313) }
BACK_IMAGE = simplegui.load_image('http://media-hearth.cursecdn.com/attachments/2/101/cardback-rankedladder.png')
CARD_FLIP_SOUND = simplegui.load_sound('http://www.soundrangers.com/demos/gambling/card_deal02.mp3')

# helper function to initialize globals
def new_game():
    global cards, exposed, state, card_clicked, card1, card2, match, turns, matched
    cards = list(range(CARDS / 2)) + list(range(CARDS / 2))
    random.shuffle(cards)
    exposed = [False for i in range(CARDS)]
    matched = [False for i in range(CARDS)]
    state = 0
    turns = 0
    card_clicked = None
    card1 = None
    card2 = None
    match = False
    
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, card_clicked, card1, card2, match, turns, exposed, matched
    card_clicked = (pos[0] // SLOT_WIDTH) + (pos[1] // SLOT_HEIGHT * Y_CARDS)
    # if everything is matched, turn everything color
    if matched.count(False) == 2:
        exposed = [True for i in range(CARDS)]
        matched = [False for i in range(CARDS)] 
    # evaluate the click only if the card is face down
    if exposed[card_clicked] == False:
        exposed[card_clicked] = True
        # transition from state 0 to state 1
        if state == 0:
            state = 1
            #CARD_FLIP_SOUND.play()
            card1 = card_clicked
        # transition from state 1 to state 2
        elif state == 1:
            state = 2
            #CARD_FLIP_SOUND.play()
            card2 = card_clicked
            turns += 1
            if cards[card1] == cards[card2]:
                match = True
            else:
                match = False
        # transition from state 2 to state 1
        else:
            state = 1
            # flip over unmatched cards
            if match == True:
                matched[card1] = True
                matched[card2] = True
            else:
                exposed[card1] = False
                exposed[card2] = False
            #CARD_FLIP_SOUND.play()
            card1 = card_clicked
  
def draw(canvas):
    global cards, exposed, card_clicked, state
    # update turns
    label.set_text("Turns = " + str(turns))
    # display cards either face up or face down accordingly
    for i in range(CARDS):
        if exposed[i] == True:
            if matched[i] == True:
                # show black and white image if matched
                canvas.draw_image(FRONT_IMAGE_BW,
                                  FRONT_IMAGE_POS[cards[i]],
                                  (125, 125),
                                  ((i * SLOT_WIDTH + SLOT_WIDTH / 2) % (SLOT_WIDTH * X_CARDS), (SLOT_HEIGHT / 2) + ( i // Y_CARDS * SLOT_HEIGHT)),
                                  (CARD_WIDTH, CARD_HEIGHT))
            else:
                # show color image if not matched
                canvas.draw_image(FRONT_IMAGE,
                                  FRONT_IMAGE_POS[cards[i]],
                                  (125, 125),
                                  ((i * SLOT_WIDTH + SLOT_WIDTH / 2) % (SLOT_WIDTH * X_CARDS), (SLOT_HEIGHT / 2) + ( i // Y_CARDS * SLOT_HEIGHT)),
                                  (CARD_WIDTH, CARD_HEIGHT))
        else:
            # show back of playing card if face down
            canvas.draw_image(BACK_IMAGE,
                              (628 // 2, 934 // 2),
                              (628, 934),
                              ((i * SLOT_WIDTH + SLOT_WIDTH / 2) % (SLOT_WIDTH * X_CARDS), (SLOT_HEIGHT / 2) + ( i // Y_CARDS * SLOT_HEIGHT)),
                              (CARD_WIDTH, CARD_HEIGHT))
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", CARDS * SLOT_WIDTH / X_CARDS, CARDS * SLOT_HEIGHT / Y_CARDS)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
