import pygame
from random import randint
import numpy


pygame.init()

FPS = 144
x_screen_size = 1200
y_screen_size = 700
board_for_counter = FPS * 2
screen = pygame.display.set_mode((x_screen_size, y_screen_size))

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
fallens = []
counter_for_new_ball = 1000
amount_object = 0
target_amount_object = 4
counter_for_new_object = 1000


def text(
        screen,
        font_coord,
        font_size,
        font_color,
        text
):
    '''
    function to draw text
    :param screen: screen to draw on
    :param font_coord: (x, y) - position of text
    :param font_size: size of text
    :param font_color: color of text
    :param text: text to render
    :return: None
    '''
    score_font = pygame.font.Font(None, font_size)
    score_result = score_font.render(str(text), True, font_color)
    screen.blit(score_result, font_coord)


def score(
        screen,
        font_coord,
        font_size,
        font_color,
        score_number
):
    '''
    function to draw scores
    :param screen: screen to draw on
    :param font_coord: (x, y) - position of scores
    :param font_size: size of scores
    :param font_color: color of scores
    :param score_number: amount of score to render
    :return: None
    '''
    text(screen, font_coord, font_size, font_color, score_number)


def restart_button(
        screen,
        font_coord,
        font_size,
        font_color
):
    '''
    Function to draw button
    :param screen: screen to draw on
    :param font_coord: (x, y) - coordinates of button
    :param font_size: size of text 'Restart'
    :param font_color: color of 'Restart'
    :return: None
    '''
    pygame.draw.rect(screen, LIGHTSTEELBLUE, font_coord + (100, 50), 0)
    text(screen, font_coord, font_size, font_color, 'Restart')


def collision_check(
        checking,
        bullet,
        amount_object,
        score_number,
        tank
):
    func_amount_object = amount_object
    func_score_number = score_number
    temporary_checking = checking
    if checking and tank.health_points > 0:
        bullet.move(fallens, tank)
        temporary_checking = bullet.collision_check
        if temporary_checking == False:
            func_amount_object -= 1
            func_score_number += 1
    return temporary_checking, func_amount_object, func_score_number


def restart(
        event,
        fallens,
        amount_object,
        score_number
):
    '''
    Function to restart game
    :param event: actual event to get position of cursor
    :param fallens: array of object to annihilate
    :param amount_object: counter of objects to destroy
    :param score_number: counter of score to make zero
    :return: array = [], 0, 0
    '''
    if 50 < event.pos[0] < 150 and 630 < event.pos[1] < 680:
        fallens = []
        amount_object = 0
        score_number = 0
    return fallens, amount_object, score_number


class Tank:
    def __init__(self, color=WHITE):
        self.x_position = 400
        self.y_position = 670
        self.x_size = 100
        self.y_size = 30
        self.speed = 1
        self.score = 0
        self.color = color
        self.health_points = 3
        pygame.draw.rect(screen, self.color, (self.x_position, self.y_position, self.x_size, self.y_size), 0)

    def draw(self):
        if self.health_points > 0:
            pygame.draw.rect(screen, self.color, (self.x_position, self.y_position, self.x_size, self.y_size), 0)

    def move(self, button_left_check, button_right_check):
        if self.health_points > 0:
            if button_left_check and self.x_position > 0:
                self.x_position -= self.speed
            if button_right_check and self.x_position + self.x_size < x_screen_size:
                self.x_position += self.speed
            self.draw()


class Fallen:
    def __init__(
            self,
            array_balls
    ):
        '''
        function to create object with random parameters and to draw it
        :param array_balls: [array] - already existing balls
        '''
        inside_check = True
        self.r_object = 40
        while inside_check:
            inside_check = False
            self.x_object = randint(300, 1140)
            self.y_object = randint(60, 640)
            for ball in array_balls:
                if (ball.x_object - self.x_object) ** 2 + (ball.y_object - self.y_object) ** 2 <= (
                        4 * self.r_object) ** 2:
                    inside_check = True
        self.dx_object = randint(200, 400) / FPS
        self.dy_object = randint(200, 400) / FPS
        self.color_object = COLORS[randint(0, 22)]
        #self.vy_object = randint(-10, 10) / FPS
        #self.vx_object = randint(-10, 10) / FPS
        pygame.draw.circle(screen,
                           self.color_object,
                           (self.x_object, self.y_object),
                           self.r_object
                           )

    def collision(
            self,
            array_balls
    ):
        '''
        function for checking collisions with walls and another balls
        :param array_balls: [array] - already existing balls
        :return: None
        '''
        for ball in array_balls:
            if ball != self and (ball.x_object - self.x_object) ** 2 + (ball.y_object - self.y_object) ** 2 < (
                    2 * self.r_object) ** 2:
                delta_x = self.x_object - ball.x_object
                delta_y = self.y_object - ball.y_object
                dx_system = self.dx_object
                dy_system = self.dy_object
                dx_relative = ball.dx_object - dx_system
                dy_relative = ball.dy_object - dy_system
                scalar = (dx_relative * delta_x + dy_relative * delta_y) / (delta_x ** 2 + delta_y ** 2)
                if scalar > 0:
                    dx_projection = scalar * delta_x
                    dy_projection = scalar * delta_y
                    self.dx_object = dx_projection + dx_system
                    self.dy_object = dy_projection + dy_system
                    dx_ortogonal = dx_relative - dx_projection
                    dy_ortogonal = dy_relative - dy_projection
                    ball.dx_object = dx_ortogonal + dx_system
                    ball.dy_object = dy_ortogonal + dy_system
                #self.collision_check = 5
                #ball.collision_check = 5
        #if self.collision_check > 0:
         #   self.collision_check -= 1

    def move(
            self,
            array_balls
    ):
        '''
        function to move balls
        :param array_balls: [array] - already existing balls
        :return: None
        '''
        self.collision(array_balls)
        if self.x_object - self.r_object < 300:
            self.dx_object = abs(self.dx_object) #+ abs(self.vx_object)
            self.dx_object = 0.99 * self.dx_object
        if x_screen_size < self.x_object + self.r_object:
            self.dx_object = -(abs(self.dx_object)) #+ abs(self.vx_object))
            self.dx_object = 0.99 * self.dx_object
        if self.y_object - self.r_object < 0:
            self.dy_object = abs(self.dy_object)# + abs(self.vy_object)
            self.dy_object = 0.99 * self.dy_object
        if y_screen_size - 100 < self.y_object + self.r_object:
            self.dy_object = -(abs(self.dy_object))# + abs(self.vy_object))
            self.dy_object = 0.99 * self.dy_object
        self.x_object += self.dx_object
        self.y_object += self.dy_object
        #self.dx_object += self.vx_object
        #self.dy_object += self.vy_object
        pygame.draw.circle(
            screen,
            self.color_object,
            (self.x_object, self.y_object),
            self.r_object
        )


class Gravity_Balls(Fallen):
    def __init__(self, array_balls):
        super().__init__(array_balls)
        self.vy_object = randint(-10, 10) / FPS
        self.vx_object = randint(-10, 10) / FPS
        self.color_object = RED_COLORS[randint(0, 3)]

    def move(
            self,
            array_balls
    ):
        '''
        function to move balls
        :param array_balls: [array] - already existing balls
        :return: None
        '''
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
        if y_screen_size - 100 < self.y_object + self.r_object:
            self.dy_object = -(abs(self.dy_object) + abs(self.vy_object))
            self.dy_object = 0.99 * self.dy_object
        self.x_object += self.dx_object
        self.y_object += self.dy_object
        self.dx_object += self.vx_object
        self.dy_object += self.vy_object
        pygame.draw.circle(
            screen,
            self.color_object,
            (self.x_object, self.y_object),
            self.r_object
        )


class Gun:
    def __init__(self, tank_arrow, color=WHITE):
        '''
        creating and drawing gun
        '''
        self.x_fixed = tank_arrow.x_position + tank_arrow.x_size / 2
        self.y_fixed = tank_arrow.y_position + tank_arrow.y_size / 2
        self.length = 50
        self.k_proportion = 1
        self.x_length = 25
        self.y_length = -numpy.sqrt(self.length**2 - self.x_length**2)
        self.x_width = self.y_length / 10
        self.y_width = self.x_length / 10
        self.k_holding = 1
        self.x_turn_speed = 0.3
        self.color = color
        self.life_check = True
        pygame.draw.polygon(
            screen,
            self.color,
            (
                (self.x_fixed, self.y_fixed),
                (self.x_fixed + self.x_length, self.y_fixed + self.y_length),
                (self.x_fixed + self.x_length + self.x_width,
                 self.y_fixed + self.y_length - self.y_width
                 ),
                (self.x_fixed + self.x_width, self.y_fixed - self.y_width)
            ),
            0
        )

    def draw(self):
        '''
        function to draw gun
        :return: None
        '''
        pygame.draw.polygon(
            screen,
            self.color,
            (
                (self.x_fixed, self.y_fixed),
                (self.x_fixed + self.x_length * self.k_holding,
                 self.y_fixed + self.y_length * self.k_holding
                 ),
                (self.x_fixed + self.x_length * self.k_holding + self.x_width,
                 self.y_fixed + self.y_length * self.k_holding - self.y_width
                 ),
                (self.x_fixed + self.x_width, self.y_fixed - self.y_width)
            ),
            0
        )

    '''def still(self, tank_arrow):
        
        function to draw gun when mouse doesn't move
        :return: None
        
        self.x_fixed = tank_arrow.x_position + tank_arrow.x_size / 2
        self.y_fixed = tank_arrow.y_position + tank_arrow.y_size / 2
        self.x_width = self.y_length / 1000 * self.length
        self.y_width = self.x_length / 1000 * self.length
        self.draw()'''

    def move(self,
             tank_arrow,
             button_up_check,
             button_down_check
             ):
        if tank_arrow.health_points > 0:
            self.x_fixed = tank_arrow.x_position + tank_arrow.x_size / 2
            self.y_fixed = tank_arrow.y_position + tank_arrow.y_size / 2
            if self.y_length < -45:
                if button_up_check:
                    self.x_length += self.x_turn_speed
                    self.y_length = -numpy.sqrt(self.length**2 - self.x_length**2)
                if button_down_check:
                    self.x_length -= self.x_turn_speed
                    self.y_length = -numpy.sqrt(self.length**2 - self.x_length**2)
            else:
                if self.x_length < 0:
                   self.x_length += self.x_turn_speed
                   self.y_length = -numpy.sqrt(self.length ** 2 - self.x_length ** 2)
                if self.x_length > 0:
                    self.x_length -= self.x_turn_speed
                    self.y_length = -numpy.sqrt(self.length ** 2 - self.x_length ** 2)
            self.x_width = self.y_length / 10
            self.y_width = self.x_length / 10
            self.draw()
        else:
            self.life_check = False


class Bullet:
    def __init__(self,
                 gun
                 ):
        '''
        create bullet_arrow on the end of the gun
        :param gun: which gun is shooting
        '''
        if gun.life_check:
            self.x_object = gun.x_fixed + gun.x_length * gun.k_holding
            self.y_object = gun.y_fixed + gun.y_length * gun.k_holding
            self.r_object = 10
            self.dx_object = gun.x_length / FPS * 13 * gun.k_holding
            self.dy_object = gun.y_length / FPS * 13 * gun.k_holding
            self.color_object = gun.color
            self.vy_object = 10 / FPS
            self.collision_check = True
            self.life_check = True
            pygame.draw.circle(screen, self.color_object,
                               (self.x_object, self.y_object),
                               self.r_object)
        else:
            self.life_check = False
            self.collision_check = False

    def collision(self,
                  array_balls,
                  tank
                  ):
        '''
        function to check and work with collision
        :param array_balls: [array] - with which balls collision is checking
        :return: None
        '''
        if self.life_check:
            i = 0
            for ball in array_balls:
                if (ball.x_object - self.x_object) ** 2 + (ball.y_object - self.y_object) ** 2 < (
                        self.r_object + ball.r_object) ** 2:
                    array_balls.pop(i)
                    self.collision_check = False
                i += 1
            if tank.x_position < self.x_object < tank.x_position + tank.x_size and self.y_object > tank.y_position:
                tank.health_points -= 1
                self.collision_check = False

    def draw(self):
        '''
        function to draw bullet_arrow
        :return: None
        '''
        if self.life_check:
            pygame.draw.circle(screen, self.color_object, (self.x_object, self.y_object), self.r_object)

    def move(self,
             array_balls,
             tank
             ):
        '''
        Function to move bullet_arrow
        :param array_balls:
        :return:None
        '''
        if self.life_check:
            self.collision(array_balls, tank)
            self.dy_object += self.vy_object
            self.x_object += self.dx_object
            self.y_object += self.dy_object
            self.draw()


class Bomb(Bullet):
    def __init__(self, gun, event):
        if gun.life_check:
            self.x_object = event.pos[0]
            self.y_object = event.pos[1]
            self.r_object = 30
            self.dx_object = 0
            self.dy_object = 0
            self.color_object = CRIMSON
            self.vy_object = 10 / FPS
            self.collision_check = True
            self.life_check = True
            pygame.draw.circle(screen, self.color_object,
                               (self.x_object, self.y_object),
                               self.r_object)
        else:
            self.life_check = False
            self.collision_check = False

    def collision(self,
                  tank1,
                  tank2
                  ):
        if self.life_check:
            if tank1.x_position < self.x_object < tank1.x_position + tank1.x_size and self.y_object > tank1.y_position:
                tank1.health_points -= 1
                self.collision_check = False
            if tank2.x_position < self.x_object < tank2.x_position + tank2.x_size and self.y_object > tank2.y_position:
                tank2.health_points -= 1
                self.collision_check = False

    def move(self,
             tank1,
             tank2
             ):
        if self.life_check:
            self.collision(tank1, tank2)
            self.dy_object += self.vy_object
            self.x_object += self.dx_object
            self.y_object += self.dy_object
            self.draw()


def new_object():
    '''
    function to create ball
    :return: None
    '''
    fallens.append(Fallen(fallens))
    fallens.append(Gravity_Balls(fallens))


def old_object():
    '''
    function to move balls
    :return: None
    '''
    for fallen in fallens:
        fallen.move(fallens)


pygame.display.update()
clock = pygame.time.Clock()
finished = False
checking_arrow = False
checking_wasd = False
tank_arrow = Tank()
tank_wasd = Tank(RED)
gun_arrow = Gun(tank_arrow)
gun_wasd = Gun(tank_wasd, RED)
button_space_check = False
test = True
move_check = 0
aim_check = 0
bomb_exist_check = False
while not finished:
    clock.tick(FPS)
    fps = clock.get_fps()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            fallens, amount_object, score_number = restart(event, fallens, amount_object, score_number)
        if event.type == pygame.MOUSEBUTTONUP:
            bomb = Bomb(gun_wasd, event)
            bomb_exist_check = True
        button_space_check = pygame.key.get_pressed()[pygame.K_SPACE]
        button_left_check = pygame.key.get_pressed()[pygame.K_LEFT]
        button_right_check = pygame.key.get_pressed()[pygame.K_RIGHT]
        button_up_check = pygame.key.get_pressed()[pygame.K_UP]
        button_down_check = pygame.key.get_pressed()[pygame.K_DOWN]
        button_shift_check = pygame.key.get_pressed()[pygame.K_LSHIFT]
        button_a_check = pygame.key.get_pressed()[pygame.K_a]
        button_d_check = pygame.key.get_pressed()[pygame.K_d]
        button_w_check = pygame.key.get_pressed()[pygame.K_w]
        button_s_check = pygame.key.get_pressed()[pygame.K_s]
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and tank_arrow.health_points > 0:
                bullet_arrow = Bullet(gun_arrow)
                checking_arrow = True
                gun_arrow.length = 50
            if event.key == pygame.K_LSHIFT and tank_wasd.health_points > 0:
                bullet_wasd = Bullet(gun_wasd)
                checking_wasd = True
                gun_wasd.length = 50

    if amount_object < target_amount_object and counter_for_new_object > board_for_counter:
        new_object()
        amount_object += 2
        counter_for_new_object = 0
    else:
        old_object()
    tank_arrow.move(button_left_check, button_right_check)
    if button_space_check:
        if gun_arrow.k_holding < 2:
            gun_arrow.k_holding *= 1.005
    else:
        gun_arrow.k_holding = 1
    gun_arrow.move(tank_arrow, button_up_check, button_down_check)
    tank_wasd.move(button_a_check, button_d_check)
    if button_shift_check:
        if gun_wasd.k_holding < 2:
            gun_wasd.k_holding *= 1.005
    else:
        gun_wasd.k_holding = 1
    gun_wasd.move(tank_wasd, button_w_check, button_s_check)
    if bomb_exist_check:
        bomb.move(tank_wasd, tank_arrow)
        bomb_exist_check = bomb.collision_check
    if checking_arrow:
        checking_arrow, amount_object, tank_arrow.score = collision_check(checking_arrow, bullet_arrow, amount_object, tank_arrow.score, tank_wasd)
    if checking_wasd:
        checking_wasd, amount_object, tank_wasd.score = collision_check(checking_wasd, bullet_wasd, amount_object, tank_wasd.score, tank_arrow)
    score(screen, (50, 100), 40, WHITE, tank_arrow.health_points)
    score(screen, (100, 100), 40, WHITE, tank_arrow.score)
    score(screen, (50, 150), 40, RED, tank_wasd.health_points)
    score(screen, (100, 150), 40, RED, tank_wasd.score)
    restart_button(screen, (50, y_screen_size - 70), 40, BLACK)
    pygame.display.update()
    screen.fill(BLACK)
    counter_for_new_ball += 4
    counter_for_new_object += 4
    if tank_arrow.health_points <= 0 or tank_wasd.health_points <= 0:
        finished = True
finished = False
if tank_arrow.health_points <= 0:
    tank_wasd.score += 10
if tank_wasd.health_points <= 0:
    tank_arrow.score += 10
while not finished:
    clock.tick(FPS)
    fps = clock.get_fps()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    screen.fill(BLACK)
    text(screen, (100, 100), 100, RED, 'WASD: ' + str(tank_wasd.score))
    text(screen, (100, 210), 100, WHITE, 'Arrow: ' + str(tank_arrow.score))
    if tank_arrow.score > tank_wasd.score:
        text(screen, (100, 350), 100, RED, 'Arrow - Winner')
    if tank_arrow.score < tank_wasd.score:
        text(screen, (100, 350), 100, RED, 'WASD - Winner')
    if tank_arrow.score == tank_wasd.score:
        text(screen, (100, 350), 100, RED, 'Draw')

    pygame.display.update()
pygame.quit()
