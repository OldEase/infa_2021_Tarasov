import pygame
from random import randint

print('Введите ваш ник')
name = input()
print(name)

pygame.init()

pygame.mixer.music.load('m.ogg')

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

def text(
        screen,
        font_coord,
        font_size,
        font_color,
        text_to_draw
):
    '''
    function to draw text
    :param screen: screen to draw
    :param font_coord: (x, y) - coordinates for place to draw on screen
    :param font_size: size of text
    :param font_color: color of text
    :param text_to_draw: text to draw on screen
    :return: None
    '''
    text_font = pygame.font.Font(None, font_size)
    text_result = text_font.render(str(text_to_draw), True, font_color)
    screen.blit(text_result, font_coord)


def interface(
        screen,
        font_coord_score,
        font_size_score,
        font_color_score,
        score,
        font_coord_time,
        font_size_time,
        font_color_time,
        time
):
    '''
    Function to draw interface
    :param screen: screen to draw
    :param font_coord_score: (x,y) - coordinates of scores
    :param font_size_score: size of score's text
    :param font_color_score: color os score's text
    :param score: number of score
    :param font_coord_time: (x,y) - coordinates of time
    :param font_size_time: size of time's text
    :param font_color_time: color os time's text
    :param time: number of time
    :return: None
    '''
    text(screen, font_coord_score, font_size_score, font_color_score, score)
    text(screen, font_coord_time, font_size_time, font_color_time, time)


def end(
        screen,
        font_coord,
        font_size,
        font_color,
        score_number
):
    '''
    Function to draw at ending screen
    :param screen: screen to draw
    :param font_coord: (x, y) - coordinates of text
    :param font_size: size of text
    :param font_color: color of text
    :param score_number: number of score
    :return: None
    '''
    text(screen, font_coord, font_size, font_color, 'Очки:' + str(score_number))


def title(
        screen,
        font_coord1,
        font_coord2,
        font_coord3,
        font_size,
        font_color
):
    '''
    Function to draw title on first screen
    :param screen: screen to draw title
    :param font_coord1: (x, y) - coordinates of 'ОПАСНО ДЛЯ ЭПИЛЕПТИКОВ'
    :param font_coord2: (x, y) - coordinates of 'КЛИКНИТЕ ДЛЯ ПРОДОЛЖЕНИЯ'
    :param font_coord3: (x, y) - coordinates of 'ГРОМКАЯ МУЗЫКА'
    :param font_size: size of text
    :param font_color: color of text
    :return: None
    '''
    text(screen, font_coord1, font_size, font_color, 'ОПАСНО ДЛЯ ЭПИЛЕПТИКОВ')
    text(screen, font_coord2, font_size, font_color, 'КЛИКНИТЕ ДЛЯ ПРОДОЛЖЕНИЯ')
    text(screen, font_coord3, font_size, font_color, 'ГРОМКАЯ МУЗЫКА')


def click(
        event
):
    '''
    Funtion to check click on balls and objects
    :param event: current event to check position of mouse
    :return: None
    '''
    global score_number, amount_balls, square_number, amount_square, object_number, amount_object
    i = 0
    clicked = True
    while i < len(balls) and clicked == True:
        if balls[i].click(event):
            score_number += 1
            amount_balls -= 1
            clicked = False
            balls.pop(i)
        i += 1
    i = 0
    clicked = True
    while i < len(fallens) and clicked == True:
        if fallens[i].click(event):
            score_number += 10
            amount_object -= 1
            clicked = False
            fallens.pop(i)
        i += 1
    i = 0


class Ball:
    def __init__(
            self
    ):
        '''
        creating and drawing ball
        return: object of class
        '''
        self.x_ball = (randint(100, 1100))
        self.y_ball = (randint(100, 600))
        self.r_ball = (randint(40, 100))
        self.dx_ball = (randint(100, 300) / FPS)
        self.dy_ball = (randint(100, 300) / FPS)
        self.color_ball = (COLORS[randint(0, 22)])
        pygame.draw.circle(screen, self.color_ball,
                           (self.x_ball, self.y_ball),
                           self.r_ball)

    def move(
            self
    ):
        '''
        Moving ball
        :return: None
        '''
        if x_screen_size < self.x_ball + self.r_ball + self.dx_ball or self.x_ball - self.r_ball + self.dx_ball < 0:
            self.dx_ball = -self.dx_ball
        if y_screen_size < self.y_ball + self.r_ball + self.dy_ball or self.y_ball - self.r_ball + self.dy_ball < 0:
            self.dy_ball = -self.dy_ball
        self.x_ball += self.dx_ball
        self.y_ball += self.dy_ball
        pygame.draw.circle(screen, self.color_ball, (self.x_ball, self.y_ball), self.r_ball)

    def click(
            self,
            event
    ):
        '''
        Function to check of click on ball
        :param event: event to get actual position of cursor
        :return: True if get, False if miss
        '''
        delta_x = self.x_ball - event.pos[0]
        delta_y = self.y_ball - event.pos[1]
        return delta_x ** 2 + delta_y ** 2 <= self.r_ball ** 2


class Fallen:
    def __init__(
            self
    ):
        '''
        Creating and drawing ball with gravity
        '''
        self.x_object = randint(50, 1150)
        self.y_object = randint(50, 650)
        self.r_object = 40
        self.dx_object = randint(100, 300) / FPS
        self.dy_object = randint(100, 300) / FPS
        self.color_object = RED_COLORS[randint(0, 3)]
        self.vy_object = randint(-15, 15) / FPS
        self.vx_object = randint(-15, 15) / FPS
        pygame.draw.circle(screen, self.color_object,
                           (self.x_object, self.y_object),
                           self.r_object)

    def move(
            self
    ):
        '''
        Function to move ball with gravity
        :return: None
        '''
        if self.x_object - self.r_object < 0:
            self.dx_object = abs(self.dx_object) + abs(self.vx_object)
        if x_screen_size < self.x_object + self.r_object:
            self.dx_object = -(abs(self.dx_object) + abs(self.vx_object))
        if self.y_object - self.r_object < 0:
            self.dy_object = abs(self.dy_object) + abs(self.vy_object)
        if y_screen_size < self.y_object + self.r_object:
            self.dy_object = -(abs(self.dy_object) + abs(self.vy_object))
        self.dy_object += self.vy_object
        self.dx_object += self.vx_object
        self.x_object += self.dx_object
        self.y_object += self.dy_object
        pygame.draw.circle(screen, self.color_object, (self.x_object, self.y_object), self.r_object)

    def click(
            self,
            event
    ):
        '''
        Function to check if ball with gravity was clicked
        :param event: actual event to get position of cursor
        :return: True if get a ball, False if miss
        '''
        delta_x = self.x_object - event.pos[0]
        delta_y = self.y_object - event.pos[1]
        return delta_x ** 2 + delta_y ** 2 <= self.r_object ** 2


def new_ball():
    '''
    Function to draw new ball
    :return: None
    '''
    balls.append(Ball())


def old_ball():
    '''
    Function to move existing balls
    :return: None
    '''
    for ball in balls:
        if megalovania_check == False and change_color_count >= FPS / 8:
            ball.color_ball = (randint(0, 255), randint(0, 255), randint(0, 255))
        ball.move()


def new_object():
    '''
    Function to draw new object
    :return: None
    '''
    fallens.append(Fallen())


def old_object():
    '''
        Function to move existing objects
        :return: None
        '''
    for fallen in fallens:
        if megalovania_check == False and change_color_count >= FPS / 8:
            fallen.color_object = (randint(0, 255), randint(0, 255), randint(0, 255))
        fallen.move()


time_count = 0

pygame.display.update()
clock = pygame.time.Clock()
finished = False
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            finished = True
    title(screen, (120, 300), (180, 560), (100, 450), 80, RED)
    pygame.display.update()
finished = False
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play()
while not finished:
    clock.tick(FPS)
    fps = clock.get_fps()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)
    if amount_balls < target_amount_balls and counter_for_new_ball > board_for_counter:
        new_ball()
        counter_for_new_ball = 0
        amount_balls += 1
    else:
        old_ball()
    if amount_object < target_amount_object and counter_for_new_object > board_for_counter:
        new_object()
        amount_object += 1
        counter_for_new_object = 0
    else:
        old_object()
    interface(screen, (100, 100), 40, BLACK, score_number, (100, 50), 40, RED, time_number)
    time_count += 1
    if time_count >= FPS:
        time_number -= 1
        time_count = 0
    if time_number == 0:
        finished = True
    if megalovania_check == True and time_number == 19:
        megalovania_check = False

    pygame.display.update()
    screen.fill(WHITE)
    if change_color_count >= FPS / 4:
        change_color_count = 0
        if WHITE == (255, 255, 255) and megalovania_check == False:
            WHITE = (randint(0, 255), randint(0, 255), randint(0, 255))
        else:
            WHITE = (255, 255, 255)
    change_color_count += 1
    counter_for_new_ball += 4
    counter_for_new_object += 4
finished = False
sans_surf = pygame.image.load('mn.png')
screen.fill((255, 255, 255))
screen.blit(sans_surf, (500, 0))
end(screen, (100, 400), 100, BLACK, score_number)
data = open("score.txt", "r").readlines()
data.append(name + '. ' + str(score_number) + '. \n')
sort_check = True
while sort_check:
    sort_check = False
    for i in range(len(data)):
        if i != 0 and int(data[i].split('. ')[1]) > int(data[i - 1].split('. ')[1]):
            sort_check = True
            temporary = data[i]
            data[i] = data[i - 1]
            data[i - 1] = temporary
file = open("score.txt", "w")
for place in data:
    file.write(place)
file.close()
volume = 1
while not finished:
    clock.tick(FPS)
    volume *= 0.99
    pygame.mixer.music.set_volume(volume)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    pygame.display.update()

pygame.quit()
