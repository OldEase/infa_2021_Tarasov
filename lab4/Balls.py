import pygame
from random import randint
pygame.init()

FPS = 144
x_screen_size = 1200
y_screen_size = 700
counter_for_new_ball = 0
board_for_counter = FPS * 3
screen = pygame.display.set_mode((x_screen_size, y_screen_size))

score_font = pygame.font.Font(None, 60)
score_result = score_font.render('10', True, (255, 255, 255))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, WHITE]
score_number = 0
target_amount_balls = 5
amount_balls = 0
ball_number = 0
x_ball = []
y_ball = []
r_ball = []
dx_ball = []
dy_ball = []
color_ball = []
x_square = []
y_square = []
color_square = []
square_inf = 10
square_sup = 200
dr_square = (square_sup - square_inf) / (FPS * 2)
square_number = 0
amount_square = 0
target_amount_square = 5



def score(screen, font_coord, font_size, font_color):
    global score_number
    score_font = pygame.font.Font(None, font_size)
    score_result = score_font.render(str(score_number), True, font_color)
    screen.blit(score_result, font_coord)


def click(event):
    global score_number, amount_balls, ball_number
    i = 0
    clicked = True
    while i < len(x_ball) and clicked == True:
        delta_x = x_ball[i] - event.pos[0]
        delta_y = y_ball[i] - event.pos[1]
        if delta_x**2 + delta_y**2 <= r_ball[i]**2:
            print('Nice!')
            score_number += 1
            ball_number -= 1
            amount_balls -= 1
            clicked = False
            x_ball.pop(i)
            y_ball.pop(i)
            dx_ball.pop(i)
            dy_ball.pop(i)
            color_ball.pop(i)
            r_ball.pop(i)
        else:
            print('Try again!')
        i += 1


def new_ball():
    '''рисует новый шарик '''
    global x_ball, y_ball, r_ball, dx_ball, dy_ball, color_ball, amount_balls, ball_number, counter_for_new_ball
    x_ball.append(randint(100, 1100))
    y_ball.append(randint(100, 600))
    r_ball.append(randint(40, 100))
    dx_ball.append(randint(100, 300) / FPS)
    dy_ball.append(randint(100, 300) / FPS)
    color_ball.append(COLORS[randint(0, 6)])
    pygame.draw.circle(screen, color_ball[ball_number], (x_ball[ball_number], y_ball[ball_number]), r_ball[ball_number])
    ball_number += 1
    amount_balls += 1
    counter_for_new_ball = 0


def new_square():
    global x_square, y_square
    x_square.append(randint(0, 1000))
    y_square.append(randint(0, 500))
    pygame.draw.rect(screen, WHITE, (x_square[square_number], y_square[square_number], square_inf, square_inf))



def old_ball():
    global x_ball, y_ball, dx_ball, dy_ball
    for i in range(len(x_ball)):
        if x_screen_size < x_ball[i] + r_ball[i] + dx_ball[i] or x_ball[i] - r_ball[i] + dx_ball[i] < 0:
            dx_ball[i] = -dx_ball[i]
        if y_screen_size < y_ball[i] + r_ball[i] + dy_ball[i] or y_ball[i] - r_ball[i] + dy_ball[i] < 0:
            dy_ball[i] = -dy_ball[i]
        x_ball[i] += dx_ball[i]
        y_ball[i] += dy_ball[i]
        pygame.draw.circle(screen, color_ball[i], (x_ball[i], y_ball[i]), r_ball[i])



pygame.display.update()
clock = pygame.time.Clock()
finished = False
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event)
            click(event)
    if amount_balls < target_amount_balls and counter_for_new_ball > board_for_counter:
        new_ball()
        new_square()
    else:
        old_ball()
    score(screen, (100, 100), 40, RED)
    pygame.display.update()
    screen.fill(BLACK)
    counter_for_new_ball += 1

pygame.quit()