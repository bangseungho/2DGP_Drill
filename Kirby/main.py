from pico2d import *
from enum import Enum
import pygame
import time
import datetime
import math

# global variable
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 450
max_scroll_left = 400
max_scroll_right = 1600
clock = pygame.time.Clock()
admin = True
FPS = 90
VELOCITY = 25
MASS = 0.04
running = True
start = False
start_sec = 0
end_sec = 0
dash = False
temp_look_at_left = None

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
    Dash = 5
    Suck = 6


# object class
class object:
    def __init__(self, posX, posY, width, height, load_image_posY, div_frame):
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.load_image_posY = load_image_posY
        self.frame = 0
        self.div_frame = div_frame


# kirby class
class Kirby(object):
    def __init__(self):
        super().__init__(WINDOW_WIDTH / 2, 100, 22, 20, 0, 6)
        self.rect = None
        self.Kirby = load_image("resource/Default_Kirby.png")
        self.dx = 0
        self.dy = 0
        self.screen_posX = 400
        self.current_time = 0
        self.animation_time = 0
        self.look_at_left = False
        self.v = 25
        self.m = 0.04
        self.isJump = 0
        self.animating = False
        self.collide_land = False
        self.fly_flag = False
        self.status = Status.Idle

    def draw(self):
        self.Kirby.clip_draw(self.frame * self.width, self.look_at_left * self.height + self.load_image_posY,
                             self.width, self.height, self.screen_posX, self.posY, self.width * 2, self.height * 2)
        # if admin: admin_key()

    def exception(self):
        # exception - if status is land
        if self.status == Status.Drop:
            # When it falls to the floor, it rolls only once.
            if self.frame >= 15:
                self.frame = 15
                if self.posY <= s.under_player + 10:
                    self.change_status(Status.Idle)
            # if self.frame == self.div_frame - 1:
            #     self.change_status(Status.Idle)
            # When it falls to the floor, constant motion
            if not self.collide_land:
                if self.frame >= 8:
                    self.frame = 8

    def move(self):
        self.posX += self.dx  # player position X on the game world
        self.screen_posX += self.dx  # player position on the screen : we can see
        self.rect = (self.screen_posX - self.width, self.posY - self.height,
                     self.screen_posX + self.width, self.posY + self.height)  # player's rect [left, bottom, right, top]

    def jump(self, j):
        # if isJump  == 1 -> jump
        # if isJump  == 2 -> Fly
        self.isJump = j

    # Fly player
    def flying(self):
        if self.isJump == 2:
            self.v = 0
            self.posY += self.dy
            self.posY -= 0.8
            if self.frame == 5:
                self.fly_flag = True
            if self.fly_flag:
                if self.frame <= 5:
                    self.frame = 5

    def set_dir(self, dx, dy, look_at_left):
        self.dx += dx
        self.dy += dy
        self.look_at_left = look_at_left

    def set_status(self, width, height, div_frame, load_image_posY):
        self.width = width
        self.height = height
        self.div_frame = div_frame
        self.load_image_posY = load_image_posY

    def change_status(self, status):
        self.status = status
        self.frame = 0
        self.m = MASS
        self.animating = False
        self.fly_flag = False
        self.collide_land = False

    def check_status(self):
        global dash
        if self.status == Status.Idle:
            self.set_status(22, 20, 6, 0)
            dash = False
        elif self.status == Status.Jump:
            self.set_status(27, 22, 10, 40)
        elif self.status == Status.Fly:
            self.set_status(28, 27, 13, 84)
        elif self.status == Status.Drop:
            self.set_status(27, 24, 18, 138)
        elif self.status == Status.Work:
            self.set_status(23, 21, 10, 186)
        elif self.status == Status.Dash:
            self.set_status(26, 21, 8, 228)
        elif self.status == Status.Suck:
            self.set_status(25, 21, 5, 270)

    def check_screen(self):
        if self.rect[right] > WINDOW_WIDTH or self.rect[left] < 0:  # if player leaves the screen
            self.screen_posX -= self.dx
            self.posX -= self.dx
        if self.rect[top] > WINDOW_HEIGHT:  # if player leaves the screen
            self.posY -= self.dy
        if max_scroll_left <= self.posX <= max_scroll_right:  # if position is end of map, player moves, the stage pixed
            self.screen_posX = WINDOW_WIDTH / 2

    def update(self, ms):
        self.animation_time = round(100 / (self.div_frame * 100), 2)
        self.current_time += ms
        self.check_status()
        self.move()

        self.check_screen()
        self.exception()

        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.frame = (self.frame + 1) % self.div_frame

        self.flying()

        # jump player
        if self.isJump > 0:
            # FORCE = 1/2 * MASS * VELOCITY ** 2
            if self.animating:
                self.m = 0.02
            if self.v > 0:
                FORCE = (0.5 * self.m * (self.v ** 2))
            elif self.status == Status.Jump:
                FORCE = -(0.5 * self.m * (self.v ** 2)) / 4
            else:
                FORCE = -(0.5 * self.m * (self.v ** 2)) / 2
            self.posY += round(FORCE)
            self.v -= 1
            self.m = MASS

            if self.posY < s.under_player:
                self.posY = s.under_player
                self.isJump = 0
                self.v = VELOCITY
                self.collide_land = True
                if self.status == Status.Drop:
                    self.frame = 7
                    self.jump(1)
                if not self.animating:
                    if dash:
                        self.change_status(Status.Dash)
                    if p.dx != 0 and not dash:
                        self.change_status(Status.Work)
                    elif not dash:
                        self.change_status(Status.Idle)
                        self.collide_land = False


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

        self.under_player = 100

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


def measure_time():
    global start_sec
    global end_sec
    global start
    global dash
    global temp_look_at_left

    if not start:
        start_sec = time.time()
        start = True
    elif start:
        end_sec = time.time()
        start = False

    if not start and end_sec - start_sec < 0.1:
        dash = True
        if not p.look_at_left:
            p.set_dir(3.2, 0, p.look_at_left)
        else:
            p.set_dir(-3.2, 0, p.look_at_left)
        return True
    else:
        return False



def handle_events():
    global running
    global admin
    global start
    global start_sec
    global end_sec
    global dash
    event_s = get_events()

    for event in event_s:

        if event.type == SDL_KEYDOWN:
            end_sec = time.time()
            if end_sec - start_sec > 0.2:
                start = False
            if event.key == SDLK_RIGHT:
                p.set_dir(3, 0, False)
                print(start)
                print("temp", temp_look_at_left)
                print("player", p.look_at_left)
                if p.posY == s.under_player:
                    if measure_time():
                        p.change_status(Status.Dash)
                    else:
                        p.change_status(Status.Work)
            elif event.key == SDLK_LEFT:
                p.set_dir(-3, 0, True)
                print(start)
                print("temp",temp_look_at_left)
                print("player", p.look_at_left)

                if p.posY == s.under_player:
                    if measure_time():
                        p.change_status(Status.Dash)
                    else:
                        p.change_status(Status.Work)
            elif event.key == SDLK_UP:
                p.set_dir(0, 3, p.look_at_left)
            elif event.key == SDLK_DOWN:
                p.set_dir(0, -2, p.look_at_left)
            elif event.key == SDLK_SPACE:
                if p.isJump == 0:
                    p.jump(1)
                    p.change_status(Status.Jump)
                elif p.isJump == 1:
                    p.jump(2)
                    p.change_status(Status.Fly)
            elif event.key == SDLK_LCTRL:
                p.change_status(Status.Suck)
            elif event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_o:
                if admin:
                    admin = False
                else:
                    admin = True
        elif event.type == SDL_KEYUP:
            start_sec = time.time()
            if event.key == SDLK_RIGHT:
                p.dx = 0
                if p.posY == s.under_player:
                    p.change_status(Status.Idle)
                dash = False
            elif event.key == SDLK_LEFT:
                p.dx = 0
                if p.posY == s.under_player:
                    p.change_status(Status.Idle)
                dash = False
            elif event.key == SDLK_UP:
                p.set_dir(0, -3, p.look_at_left)
            elif event.key == SDLK_DOWN:
                p.set_dir(0, 2, p.look_at_left)
            elif event.key == SDLK_LCTRL:
                p.change_status(Status.Idle)
            elif event.key == SDLK_SPACE:
                if p.isJump == 2:
                    p.jump(1)
                    p.change_status(Status.Drop)
                    p.animating = True


def admin_key():
    if p.dx != 0:
        print("p.posX = ", p.posX)
        print("p.posY = ", p.posY)
        print("p.screen_posX = ", p.screen_posX)
    draw_rectangle(p.screen_posX - p.width, p.rect[bottom], p.screen_posX + p.width, p.rect[top])


open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)

# initialization code
p = Kirby()
s = stage()

# game main loop code
while running:
    # simulation
    m_t = clock.tick(FPS) / 1000

    handle_events()
    p.update(m_t)
    s.update()

    # rendering
    clear_canvas()
    s.draw()
    p.draw()

    update_canvas()

    delay(0.01)
# finalization code
close_canvas()
