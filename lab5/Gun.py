import pygame
from random import randint
import numpy
'''
print('Введите ваш ник')
name = input()
print(name)
'''
pygame.init()

FPS = 144
x_screen_size = 1200
y_screen_size = 700
board_for_counter = FPS * 2
screen = pygame.display.set_mode((x_screen_size, y_screen_size))

score_font = pygame.font.Font(None, 60)
score_result = score_font.render('10', True, (255, 255, 255))

RED = (255, 0, 0)
CRIMSON = (220, 20, 60)
FIREBRICK = (178, 34, 34)
DARKRED = (139, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
LIGHTCYAN = (224, 255, 255)
PALETURQUOISE = (175, 238, 238)
AQUAMARINE = (127, 255, 212)
TURQUOISE = (64, 224, 208)
MEDIUMTURQUOISE = (72, 209, 204)
DARKTURQUOISE = (0, 206, 209)
CADETBLUE = (95, 158, 160)
STEELBLUE = (70, 130, 180)
LIGHTSTEELBLUE = (176, 196, 222)
POWDERBLUE = (176, 224, 230)
LIGHTBLUE = (173, 216, 230)
SKYBLUE = (135, 206, 235)
LIGHTSKYBLUE = (135, 206, 250)
DEEPSKYBLUE = (0, 191, 255)
DODGERBLUE = (30, 144, 255)
CORNFLOWERBLUE = (100, 149, 237)
MEDIUMSTATEBLUE = (123, 104, 238)
MEDIUMBLUE = (0, 0, 205)
DARKBLUE = (0, 0, 139)
NAVY = (0, 0, 128)
MIDNIGHTBLUE = (25, 25, 112)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    BLUE, LIGHTCYAN, PALETURQUOISE,
    AQUAMARINE, CYAN, TURQUOISE,
    MEDIUMTURQUOISE, DARKTURQUOISE, CADETBLUE,
    STEELBLUE, LIGHTSTEELBLUE, POWDERBLUE,
    LIGHTBLUE, SKYBLUE, LIGHTSKYBLUE,
    DEEPSKYBLUE, DODGERBLUE, CORNFLOWERBLUE,
    MEDIUMSTATEBLUE, MEDIUMBLUE, DARKBLUE,
    NAVY, MIDNIGHTBLUE
]
RED_COLORS = [RED, CRIMSON, FIREBRICK, DARKRED]
score_number = 0
target_amount_balls = 5
amount_balls = 0
balls = []
fallens = []
counter_for_new_ball = 1000
amount_object = 0
target_amount_object = 5
counter_for_new_object = 1000
time_number = 36
change_color_count = 0
megalovania_check = True


def score(screen, font_coord, font_size, font_color):
    global score_number
    score_font = pygame.font.Font(None, font_size)
    score_result = score_font.render(str(score_number), True, font_color)
    screen.blit(score_result, font_coord)


class Fallen:
    def __init__(self, array_balls):
        in_check = True
        self.r_object = 40
        while in_check:
            in_check = False
            self.x_object = randint(300, 1140)
            self.y_object = randint(60, 640)
            for ball in array_balls:
                if (ball.x_object - self.x_object) ** 2 + (ball.y_object - self.y_object) ** 2 <= (
                        4 * self.r_object) ** 2:
                    in_check = True
        self.dx_object = randint(200, 400) / FPS
        self.dy_object = randint(200, 400) / FPS
        self.color_object = COLORS[randint(0, 22)]
        self.vy_object = randint(-10, 10) / FPS
        self.vx_object = randint(-10, 10) / FPS
        self.collision_check = 0
        pygame.draw.circle(screen, self.color_object,
                           (self.x_object, self.y_object),
                           self.r_object)

    def collision(self, array_balls):
        for ball in array_balls:
            if ball != self and (ball.x_object - self.x_object) ** 2 + (ball.y_object - self.y_object) ** 2 < (
                    2 * self.r_object) ** 2 and self.collision_check == 0:
                delta_x = self.x_object - ball.x_object
                delta_y = self.y_object - ball.y_object
                dx_system = self.dx_object
                dy_system = self.dy_object
                dx_relative = ball.dx_object - dx_system
                dy_relative = ball.dy_object - dy_system
                scalar = (dx_relative * delta_x + dy_relative * delta_y) / (delta_x ** 2 + delta_y ** 2)
                dx_projection = scalar * delta_x
                dy_projection = scalar * delta_y
                self.dx_object = dx_projection + dx_system
                self.dy_object = dy_projection + dy_system
                dx_ortogonal = dx_relative - dx_projection
                dy_ortogonal = dy_relative - dy_projection
                ball.dx_object = dx_ortogonal + dx_system
                ball.dy_object = dy_ortogonal + dy_system
                self.collision_check = 5
                ball.collision_check = 5
        if self.collision_check > 0:
            self.collision_check -= 1

    def move(self, array_balls):
        self.collision(array_balls)
        if self.x_object - self.r_object < 300:
            self.dx_object = abs(self.dx_object) + abs(self.vx_object)
            self.dx_object = 0.99 * self.dx_object
        if x_screen_size < self.x_object + self.r_object:
            self.dx_object = -(abs(self.dx_object) + abs(self.vx_object))
            self.dx_object = 0.99 * self.dx_object
        if self.y_object - self.r_object < 0:
            self.dy_object = abs(self.dy_object) + abs(self.vy_object)
            self.dy_object = 0.99 * self.dy_object
        if y_screen_size < self.y_object + self.r_object:
            self.dy_object = -(abs(self.dy_object) + abs(self.vy_object))
            self.dy_object = 0.99 * self.dy_object
        self.x_object += self.dx_object
        self.y_object += self.dy_object
        pygame.draw.circle(screen, self.color_object, (self.x_object, self.y_object), self.r_object)


class Gun:
    def __init__(self):
        self.x_fixed = x_screen_size / 10
        self.y_fixed = y_screen_size / 10 * 8
        self.length = 100
        self.k_proportion = 1
        self.x_length = 100
        self.y_length = 0
        self.x_width = self.y_length / 10
        self.y_width = self.x_length / 10
        self.k_holding = 1
        pygame.draw.polygon(screen, WHITE, ((self.x_fixed, self.y_fixed),
                                                (self.x_fixed + self.x_length, self.y_fixed + self.y_length),
                                                (self.x_fixed + self.x_length + self.x_width,
                                                 self.y_fixed + self.y_length - self.y_width),
                                                (self.x_fixed + self.x_width, self.y_fixed - self.y_width)), 0)

    def draw(self):
        pygame.draw.polygon(screen, WHITE, ((self.x_fixed, self.y_fixed),
                                            (self.x_fixed + self.x_length * self.k_holding,
                                             self.y_fixed + self.y_length * self.k_holding),
                                            (self.x_fixed + self.x_length * self.k_holding + self.x_width,
                                             self.y_fixed + self.y_length * self.k_holding - self.y_width),
                                            (self.x_fixed + self.x_width, self.y_fixed - self.y_width)), 0)

    def still(self):
        self.x_width = self.y_length / 1000 * self.length
        self.y_width = self.x_length / 1000 * self.length
        self.draw()

    def move(self, event):
        self.k_proportion = numpy.sqrt(
            ((event.pos[0] - self.x_fixed) ** 2 + (event.pos[1] - self.y_fixed) ** 2) / self.length ** 2)
        self.x_length = (event.pos[0] - self.x_fixed) / self.k_proportion
        self.y_length = (event.pos[1] - self.y_fixed) / self.k_proportion
        self.x_width = self.y_length / 10
        self.y_width = self.x_length / 10
        self.draw()


class Bullet:
    def __init__(self, gun):
        self.x_object = gun.x_fixed + gun.x_length * gun.k_holding
        self.y_object = gun.y_fixed + gun.y_length * gun.k_holding
        self.r_object = 10
        self.dx_object = gun.x_length / FPS * 8 * gun.k_holding
        self.dy_object = gun.y_length / FPS * 8 * gun.k_holding
        self.color_object = RED_COLORS[randint(0, 3)]
        self.vy_object = 10 / FPS
        self.collision_check = True
        pygame.draw.circle(screen, self.color_object,
                           (self.x_object, self.y_object),
                           self.r_object)

    def collision(self, array_balls):
        i = 0
        for ball in array_balls:
            if (ball.x_object - self.x_object) ** 2 + (ball.y_object - self.y_object) ** 2 < (
                    self.r_object + ball.r_object) ** 2:
                array_balls.pop(i)
                self.collision_check = False
            i += 1

    def draw(self):
        pygame.draw.circle(screen, self.color_object, (self.x_object, self.y_object), self.r_object)

    def move(self, array_balls):
        self.collision(array_balls)
        if self.x_object - self.r_object < 0:
            self.dx_object = abs(self.dx_object)
            self.dx_object = 0.5 * self.dx_object
        if x_screen_size < self.x_object + self.r_object:
            self.dx_object = -(abs(self.dx_object))
            self.dx_object = 0.5 * self.dx_object
        if self.y_object - self.r_object < 0:
            self.dy_object = abs(self.dy_object) + abs(self.vy_object)
            self.dy_object = 0.5 * self.dy_object
        if y_screen_size < self.y_object + self.r_object:
            self.dy_object = -(abs(self.dy_object) + abs(self.vy_object))
            self.dy_object = 0.5 * self.dy_object
        self.dy_object += self.vy_object
        self.x_object += self.dx_object
        self.y_object += self.dy_object
        self.draw()


def new_object():
    fallens.append(Fallen(fallens))


def old_object():
    for fallen in fallens:
        if megalovania_check == False and change_color_count >= FPS / 8:
            fallen.color_object = (randint(0, 255), randint(0, 255), randint(0, 255))
        fallen.move(fallens)


time_count = 0

pygame.display.update()
clock = pygame.time.Clock()
finished = False
checking = False
new_gun = Gun()
button_check = False
test = True
while not finished:
    clock.tick(FPS)
    fps = clock.get_fps()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEMOTION:
            new_gun.move(event)
        if event.type == pygame.MOUSEBUTTONUP:
            bullet = Bullet(new_gun)
            checking = True
            new_gun.length = 100
        keys = pygame.mouse.get_pressed()
        if keys[0]:
            button_check = True
        if keys[0] == False:
            button_check = False
    if amount_object < target_amount_object and counter_for_new_object > board_for_counter:
        new_object()
        amount_object += 1
        counter_for_new_object = 0
    else:
        old_object()
    if button_check:
        if new_gun.k_holding < 2:
            new_gun.k_holding *= 1.005
    else:
        new_gun.k_holding = 1
    new_gun.still()
    if checking:
        bullet.move(fallens)
        checking = bullet.collision_check
        if checking == False:
            amount_object -= 1
            score_number += 1
    score(screen, (100, 100), 40, WHITE)
    pygame.display.update()
    screen.fill(BLACK)
    counter_for_new_ball += 4
    counter_for_new_object += 4
finished = False
screen.fill((255, 255, 255))
'''
f = open('score.txt', 'r+')
f.read()
f.write('\n' + name + ' ' + str(score_number))
f.close()
'''
pygame.quit()
