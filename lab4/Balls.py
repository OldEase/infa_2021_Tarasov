import pygame
from random import randint
pygame.init()

FPS = 30
x_screen_size = 1200
y_screen_size = 700
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
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
score_number = 0
target_amount = 10
amount = 0
ball_number = 0
x = []
y = []
r = []
dx = []
dy = []
color = []


def score(screen, font_coord, font_size, font_color):
    global score_number
    score_font = pygame.font.Font(None, font_size)
    score_result = score_font.render(str(score_number), True, font_color)
    screen.blit(score_result, font_coord)


def click(event):
    global score_number, amount, ball_number
    i = 0
    while i < len(x) - 1:
        i += 1
        delta_x = x[i] - event.pos[0]
        delta_y = y[i] - event.pos[1]
        if delta_x**2 + delta_y**2 <= r[i]**2:
            print('Nice!')
            score_number += 1
            ball_number -= 1
            amount -= 1
            x.pop(i)
            y.pop(i)
            dx.pop(i)
            dy.pop(i)
            color.pop(i)
            r.pop(i)
        else:
            print('Try again!')


def new_ball():
    '''рисует новый шарик '''
    global x, y, r, dx, dy, color, amount, ball_number
    x.append(randint(100, 1100))
    y.append(randint(100, 600))
    r.append(randint(10, 100))
    dx.append(randint(100, 300) / FPS)
    dy.append(randint(100, 300) / FPS)
    color.append(COLORS[randint(0, 5)])
    pygame.draw.circle(screen, color[ball_number], (x[ball_number], y[ball_number]), r[ball_number])
    ball_number += 1
    amount += 1


def old_ball():
    global x, y, dx, dy
    for i in range(len(x)):
        if x_screen_size < x[i] + r[i] + dx[i] or x[i] - r[i] + dx[i] < 0:
            dx[i] = -dx[i]
        if y_screen_size < y[i] + r[i] + dy[i] or y[i] - r[i] + dy[i] < 0:
            dy[i] = -dy[i]
        x[i] += dx[i]
        y[i] += dy[i]
        pygame.draw.circle(screen, color[i], (x[i], y[i]), r[i])


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
    if amount < target_amount:
        new_ball()
    else:
        old_ball()
    score(screen, (100, 100), 40, RED)
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()