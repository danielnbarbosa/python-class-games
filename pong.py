# Implementation of classic arcade game Pong
# Also available at http://www.codeskulptor.org/#user38_Y2lv4giWBo_7.py

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
PADDLE_VEL = 5

# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [ WIDTH / 2, HEIGHT / 2 ]
    x_vel = float(random.randrange(120, 240)) / 60.0
    y_vel = float(random.randrange(60, 180)) / 60.0
    if direction == LEFT:
        ball_vel = [ -x_vel, -y_vel ]
    elif direction == RIGHT:
        ball_vel = [ x_vel, -y_vel ]
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball(RIGHT)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # if ball hits left gutter
    if ball_pos[0] - BALL_RADIUS < 0:
        # if it hits the left paddle
        if paddle1_pos - HALF_PAD_HEIGHT < ball_pos[1] < paddle1_pos + HALF_PAD_HEIGHT:
            # deflect the ball back a little faster
            ball_vel[0] = -(1.1 * ball_vel[0])
        else:
            # give player 2 a point and start new round
            score2 += 1
            spawn_ball(RIGHT)
 
    # if ball hits right gutter
    elif ball_pos[0] + BALL_RADIUS > WIDTH:
        # if it hits the right paddle
        if paddle2_pos - HALF_PAD_HEIGHT < ball_pos[1] < paddle2_pos + HALF_PAD_HEIGHT:
            # deflect the ball back a little faster
            ball_vel[0] = - (1.1 * ball_vel[0])
        else:
            # givel player 1 a point and start new round
            score1 += 1
            spawn_ball(LEFT)
    
    # handle top and bottom bounce detection
    if ball_pos[1] - BALL_RADIUS < 0:
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] + BALL_RADIUS > HEIGHT:
        ball_vel[1] = -ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos - HALF_PAD_HEIGHT > 0 and paddle1_vel < 0 \
    or paddle1_pos + HALF_PAD_HEIGHT < HEIGHT and paddle1_vel > 0:
        paddle1_pos += paddle1_vel
    if paddle2_pos - HALF_PAD_HEIGHT > 0 and paddle2_vel < 0 \
    or paddle2_pos + HALF_PAD_HEIGHT < HEIGHT and paddle2_vel > 0:
        paddle2_pos += paddle2_vel
    
    # draw paddles
    canvas.draw_line( [HALF_PAD_WIDTH, (paddle1_pos - HALF_PAD_HEIGHT)], [HALF_PAD_WIDTH, (paddle1_pos + HALF_PAD_HEIGHT) ], PAD_WIDTH, 'White')
    canvas.draw_line( [WIDTH - HALF_PAD_WIDTH, (paddle2_pos - HALF_PAD_HEIGHT)], [WIDTH - HALF_PAD_WIDTH, (paddle2_pos + HALF_PAD_HEIGHT) ], PAD_WIDTH, 'White')
    
    # draw scores
    canvas.draw_text(str(score1), (WIDTH / 2 - 100, HEIGHT / 5 ), 48, 'White', 'sans-serif')
    canvas.draw_text(str(score2), (WIDTH / 2 + 100, HEIGHT / 5 ), 48, 'White', 'sans-serif')
    
# move the paddle as long as the key remains pressed
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["W"]:
        paddle1_vel = -PADDLE_VEL
    elif key == simplegui.KEY_MAP["S"]:
        paddle1_vel = PADDLE_VEL

    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -PADDLE_VEL
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = PADDLE_VEL

# stop the paddle if the key is no longer pressed
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["W"] or key == simplegui.KEY_MAP["S"]:
        paddle1_vel = 0        
    if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

def reset_button_handler():
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Reset', reset_button_handler, 200)


# start frame
new_game()
frame.start()
