from pico2d import *
from enum import Enum
import pygame
import time

# global variable
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 450
max_scroll_left = 400
max_scroll_right = 1600
clock = pygame.time.Clock()
admin = True
FPS = 90
running = True

# Rect
left = 0
bottom = 1
right = 2
top = 3


# player Status
class Status(Enum):
    Idle = 0
    Work = 1
    Jump = 2
    Fly = 3
    Drop = 4
    Run = 5


# object class
class object:
    def __init__(self, posX, posY, width, height, load_image_posY):
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.load_image_posY = load_image_posY
        self.frame = 0


# kirby class
class Kirby(object):
    def __init__(self):
        super().__init__(WINDOW_WIDTH / 2, 100, 22, 20, 0)
        self.rect = None
        self.Kirby = load_image("resource/Default_Kirby.png")
        self.dx = 0
        self.dy = 0
        self.screen_posX = 400

    def draw(self):
        self.Kirby.clip_draw(self.frame * self.width, self.load_image_posY, self.width, self.height,
                             self.screen_posX, self.posY, self.width * 2, self.height * 2)
        if admin: admin_key()

    def move(self):
        self.posX += self.dx  # player position X on the game world
        self.posY += self.dy  # player position Y on the game world
        self.screen_posX += self.dx  # player position on the screen : we can see
        self.rect = (self.screen_posX - self.width, self.posY - self.height,
                     self.screen_posX + self.width, self.posY + self.height)  # player's rect [left, bottom, right, top]

    def update(self):
        self.move()
        self.check_screen()
        self.frame = (self.frame + 1) % 6

    def check_screen(self):
        if self.rect[right] > WINDOW_WIDTH or self.rect[left] < 0:  # if player leaves the screen
            self.screen_posX -= self.dx
            self.posX -= self.dx
        if self.rect[top] > WINDOW_HEIGHT:  # if player leaves the screen
            self.posY -= self.dy
        if max_scroll_left <= self.posX <= max_scroll_right:  # if position is end of map, player moves, the stage pixed
            self.screen_posX = WINDOW_WIDTH / 2


# stage class
class stage:
    def __init__(self):
        self.stage1_background = load_image("resource/stage1_background.png")
        self.stage1_land = load_image("resource/stage1_land.png")

        self.bg_posX = WINDOW_WIDTH - 300
        self.bg_posY = WINDOW_HEIGHT / 2
        self.bg_width = 1100
        self.bg_height = WINDOW_HEIGHT

        self.land_posX = 1000
        self.land_posY = 150
        self.land_width = self.land_posX * 2
        self.land_height = self.land_posY * 2

    def draw(self):
        self.stage1_background.draw(self.bg_posX, self.bg_posY, self.bg_width, self.bg_height)
        self.stage1_land.draw(self.land_posX, self.land_posY, self.land_width, self.land_height)

    def move(self):
        self.bg_posX -= p.dx / 5
        self.land_posX -= p.dx

    def update(self):
        self.move()
        self.check_screen()

    def check_screen(self):
        if p.posX <= max_scroll_left or p.posX >= max_scroll_right:
            self.bg_posX += p.dx / 5
            self.land_posX += p.dx


def handle_events():
    global running
    global admin
    event_s = get_events()

    for event in event_s:

        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                p.dx += 3
            elif event.key == SDLK_LEFT:
                p.dx -= 3
            elif event.key == SDLK_UP:
                p.dy += 2
            elif event.key == SDLK_DOWN:
                p.dy -= 2
            elif event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_o:
                if admin: admin = False
                else: admin = True

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                p.dx -= 3
            elif event.key == SDLK_LEFT:
                p.dx += 3
            elif event.key == SDLK_UP:
                p.dy -= 2
            elif event.key == SDLK_DOWN:
                p.dy += 2


def admin_key():
    if p.dx != 0:
        print("p.posX = ", p.posX)
        print("p.screen_posX = ", p.screen_posX)
    draw_rectangle(p.screen_posX - p.width, p.rect[bottom], p.screen_posX + p.width, p.rect[top])


open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)

# initialization code
p = Kirby()
s = stage()

# game main loop code
while running:
    # simulation
    mt = clock.tick(FPS) / 1000
    handle_events()
    p.update()
    s.update()

    # rendering
    clear_canvas()
    s.draw()
    p.draw()

    update_canvas()

    delay(0.01)
# finalization code
close_canvas()
