from pico2d import *
from enum import Enum
import pygame
import time
import datetime
import math

from pygame.draw import rect

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
cr_ob = [0, 0, 0, 0]

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
        self.Life = load_image("resource/life_hud.png")
        self.Life_0 = load_image("resource/0_hud.png")
        self.Life_1 = load_image("resource/1_hud.png")
        self.Life_2 = load_image("resource/2_hud.png")
        self.Hp = load_image("resource/hp_hud.png")
        self.Life_x = load_image("resource/x_hud.png")
        self.breath = load_image("resource/breath.png")
        self.lifes = 2
        self.hps = 6
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
        self.suck_flag = False
        self.work_flag = True
        self.breath_flag = False
        self.status = Status.Idle
        self.L_suck_range = None
        self.R_suck_range = None
        self.on_the_ob = False
        self.breath_posX = None
        self.breath_posY = None
        self.breath_frame = 0

    def draw(self):
        self.Kirby.clip_draw(self.frame * self.width, self.look_at_left * self.height + self.load_image_posY,
                             self.width, self.height, self.screen_posX, self.posY, self.width * 2, self.height * 2)

        if self.breath_flag:
            if not self.look_at_left:
                self.breath.clip_draw(self.breath_frame * 32, 0, 32, 21, p.breath_posX + 20 + self.breath_frame * 5, p.breath_posY)
            else:
                self.breath.clip_draw(self.breath_frame * 32, 21, 32, 21, p.breath_posX - 20 - self.breath_frame * 5, p.breath_posY)
            if self.breath_frame == 5:
                self.breath_flag = False

        self.Life.draw(40, 420, 32, 25)

        self.Life_x.draw(69, 419, 15.5, 16)

        if self.lifes == 2:
            self.Life_0.draw(90, 420, 16, 22)
            self.Life_2.draw(106, 420, 16, 22)
        if self.lifes == 1:
            self.Life_0.draw(90, 420, 16, 22)
            self.Life_1.draw(106, 420, 16, 22)
        if self.lifes == 0:
            self.Life_0.draw(90, 420, 16, 22)
            self.Life_0.draw(106, 420, 16, 22)

        for hp in range(self.hps):
            self.Hp.draw(130 + hp * 18, 420, 18, 29.5)

        if admin: admin_key()

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
        self.L_suck_range = (self.rect[left], self.rect[bottom], self.rect[left] - 60, self.rect[top])
        self.R_suck_range = (self.rect[right], self.rect[bottom], self.rect[right] + 60, self.rect[top])

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
            if self.frame == 12:
                self.frame = 5

    def sucktion(self):
        if self.suck_flag:
            self.dx = 0
            if self.frame == 4:
                self.frame = 2

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
            self.suck_flag = False
            self.work_flag = False
        elif self.status == Status.Jump:
            self.set_status(27, 22, 10, 40)
            self.on_the_ob = False
        elif self.status == Status.Fly:
            self.fly_flag = True
            self.set_status(28, 27, 13, 84)
        elif self.status == Status.Drop:
            self.set_status(27, 24, 18, 138)
        elif self.status == Status.Work:
            self.work_flag = True
            self.set_status(23, 21, 10, 186)
        elif self.status == Status.Dash:
            self.set_status(26, 21, 8, 228)
        elif self.status == Status.Suck:
            self.set_status(25, 21, 5, 270)
            self.suck_flag = True

    def check_screen(self):
        global cr_ob
        for ob in s.obstacles:
            if self.rect[left] <= ob[right] and self.rect[right] >= ob[left] and self.rect[bottom] <= ob[top] and self.rect[top] >= ob[bottom]:
                cr_ob = ob

                if self.rect[right] >= ob[left] and self.rect[left] <= ob[right]:
                    if self.rect[bottom] + 5 <= ob[top]:
                        self.dx = 0

                if self.rect[bottom] >= cr_ob[top] - 10:
                    self.on_the_ob = True
                    self.posY = cr_ob[top] + 20
                    s.under_player = cr_ob[top] + 20
        if self.rect[right] <= cr_ob[left] or self.rect[left] >= cr_ob[right]:
            s.under_player = 100
            if self.on_the_ob:
                if self.posY != s.under_player and self.status != Status.Drop:
                    if not self.fly_flag:
                        self.posY -= 5
                elif self.posY == 100:
                    self.on_the_ob = False
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
            self.breath_frame = (self.breath_frame + 1) % 6

        self.flying()
        self.sucktion()

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
                if not self.animating and not p.suck_flag:
                    if dash:
                        self.change_status(Status.Dash)
                    if p.dx != 0 and not dash:
                        self.change_status(Status.Work)
                    elif not dash and not self.suck_flag:
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

        self.obstacles = [[555, 79, 610, 110], [1065, 79, 1250, 110], [1390, 79, 2000, 110],
                          [1580, 110, 1630, 240], [1630, 110, 1665, 180]]

    def draw(self):
        self.stage1_background.draw(self.bg_posX, self.bg_posY, self.bg_width, self.bg_height)
        self.stage1_land.draw(self.land_posX, self.land_posY, self.land_width, self.land_height)

    def move(self):
        if -200 < self.land_posX <= 1000:
            self.bg_posX -= p.dx / 5
            self.land_posX -= p.dx

            for ob in self.obstacles:
                ob[0] -= p.dx
                ob[2] -= p.dx

    def update(self):
        self.move()
        self.check_screen()

    def check_screen(self):
        if p.posX <= max_scroll_left or p.posX >= max_scroll_right:
            self.bg_posX += p.dx / 5
            self.land_posX += p.dx

            for ob in self.obstacles:
                ob[0] += p.dx
                ob[2] += p.dx


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
                if p.posY == s.under_player:
                    if measure_time():
                        p.change_status(Status.Dash)
                    else:
                        p.change_status(Status.Work)
            elif event.key == SDLK_LEFT:
                p.set_dir(-3, 0, True)

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
                p.work_flag = False
                p.dx = 0
                if p.posY == s.under_player:
                    p.change_status(Status.Idle)
                dash = False
            elif event.key == SDLK_LEFT:
                p.dx = 0
                p.work_flag = False
                if p.posY == s.under_player:
                    p.change_status(Status.Idle)
                dash = False
            elif event.key == SDLK_UP:
                p.set_dir(0, -3, p.look_at_left)
            elif event.key == SDLK_DOWN:
                p.set_dir(0, 2, p.look_at_left)
            elif event.key == SDLK_LCTRL:
                p.suck_flag = False
                if p.work_flag and p.posY == s.under_player:
                    p.change_status(Status.Work)
                    if p.look_at_left:
                        p.set_dir(-3, 0, True)
                    else:
                        p.set_dir(3, 0, False)
                else:
                    p.change_status(Status.Idle)
            elif event.key == SDLK_SPACE:
                p.breath_posX = p.screen_posX
                p.breath_posY = p.posY
                if p.isJump == 2:
                    p.jump(1)
                    p.change_status(Status.Drop)
                    p.animating = True
                    p.breath_flag = True
                    p.breath_frame = 0


def admin_key():
    if p.dx != 0:
        print(p.status)
    draw_rectangle(p.screen_posX - p.width, p.rect[bottom], p.screen_posX + p.width, p.rect[top])
    if p.suck_flag:
        if p.look_at_left:
            draw_rectangle(p.L_suck_range[0], p.L_suck_range[1], p.L_suck_range[2], p.L_suck_range[3])
        else:
            draw_rectangle(p.R_suck_range[0], p.R_suck_range[1], p.R_suck_range[2], p.R_suck_range[3])
    draw_rectangle(0, 0, 800, 79)

    for ob in s.obstacles:
        draw_rectangle(ob[0], ob[1], ob[2], ob[3])


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
