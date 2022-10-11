import pico2d
from pico2d import *
from enum import Enum
import pygame
import time

# global variable
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 450
VELOCITY = 25
MASS = 0.04
running = True
clock = pygame.time.Clock()
FPS = 90
start = 0
finish = 0


class Status(Enum):
    Idle = 0
    Work = 1
    Jump = 2
    Fly = 3
    Drop = 4
    Run = 5


class object:
    def __init__(self, posX, posY, width, height, image_bottom):
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.image_bottom = image_bottom


class Kirby(object):
    def __init__(self):
        super().__init__(WINDOW_WIDTH / 2, 100, 22, 20, 0)
        self.idle = load_image("resource/Default_Kirby.png")
        self.dx = 0
        self.dy = 0
        self.isJump = 0
        self.v = VELOCITY
        self.m = MASS
        self.hit_box = True
        self.frame = 0
        self.div_frame = 6
        self.look_at_left = False
        self.current_time = 0
        self.animation_time = 0
        self.width_size = 44
        self.height_size = 40
        self.status = Status.Idle
        self.animating = False
        self.fly_flag = False
        self.collide_land = False
        self.can_dash = False

    # draw player
    def draw(self):
        self.idle.clip_draw(self.frame * self.width, self.look_at_left * self.height + self.image_bottom, self.width,
                            self.height, self.posX, self.posY, self.width_size, self.height_size)
        # hit_box
        if self.hit_box:
            draw_rectangle(player.posX - self.width, player.posY - self.height, player.posX + self.width,
                           player.posY + self.height)

    # move player
    def move(self):
        if stage.move_map == 0 or stage.move_map == 1200:
            self.posX += self.dx

    def move_change_stat(self, dx, dy, look_at_left):
        self.dx += dx
        self.dy += dy
        self.look_at_left = look_at_left


    # player screen collider
    def check_screen(self):
        if self.posX + player.width > WINDOW_WIDTH or self.posX - player.width < 0:
            self.posX -= self.dx
        if self.posY + player.height > WINDOW_HEIGHT:
            self.posY = WINDOW_HEIGHT - player.height

    # jump flag
    def jump(self, j):
        # if isJump  == 1 -> jump
        # if isJump  == 2 -> Fly
        self.isJump = j

    def set_status(self, width, height, width_size, height_size, div_frame, image_bottom):
        self.width = width
        self.height = height
        self.width_size = width_size
        self.height_size = height_size
        self.div_frame = div_frame
        self.image_bottom = image_bottom

    def check_status(self):
        if self.status == Status.Idle:
            self.set_status(22, 20, 44, 40, 6, 0)
        if self.status == Status.Idle:
            self.set_status(22, 20, 44, 40, 6, 0)
        elif self.status == Status.Jump:
            self.set_status(27, 22, 54, 44, 10, 40)
        elif self.status == Status.Fly:
            self.set_status(28, 27, 56, 54, 13, 84)
        elif self.status == Status.Drop:
            self.set_status(27, 24, 54, 48, 18, 138)
        elif self.status == Status.Work:
            self.set_status(23, 21, 46, 42, 10, 186)
        elif self.status == Status.Run:
            self.set_status(25, 23, 50, 46, 8, 228)

    def change_status(self, status):
        self.status = status
        self.frame = 0
        self.m = MASS
        self.animating = False
        self.fly_flag = False
        self.collide_land = False

    def exception(self):
        # exception - if status is land
        if self.status == Status.Drop:
            # When it falls to the floor, it rolls only once.
            if self.frame >= 15:
                self.frame = 15
                if self.posY <= 110:
                    self.change_status(Status.Idle)
            # if self.frame == self.div_frame - 1:
            #     self.change_status(Status.Idle)
            # When it falls to the floor, constant motion
            if not self.collide_land:
                if self.frame >= 8:
                    self.frame = 8

    # Fly player
    def flying(self):
        if self.isJump == 2:
            self.v = 0
            self.posY += self.dy
            self.posY -= 1.0
            if self.frame == 5:
                self.fly_flag = True
            if self.fly_flag:
                if self.frame <= 5:
                    self.frame = 5

    # update player
    def update(self, m_t):
        # animation velocity
        self.animation_time = round(100 / (self.div_frame * 100), 2)
        self.current_time += m_t

        # move player
        self.check_status()
        self.move()
        self.check_screen()
        self.exception()
        # move animation

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

            if self.posY < 100:
                self.posY = 100
                self.isJump = 0
                self.v = VELOCITY
                self.collide_land = True
                if self.status == Status.Drop:
                    self.frame = 7
                    self.jump(1)
                if not self.animating:
                    if player.dx != 0:
                        self.change_status(Status.Work)
                    else:
                        self.change_status(Status.Idle)
                        self.collide_land = False


class stage(object):
    def __init__(self):
        super().__init__(WINDOW_WIDTH - 300, WINDOW_HEIGHT / 2, 1100, WINDOW_HEIGHT, 0)
        self.stage1_background = load_image("resource/stage1_background.png")
        self.stage1_land = load_image("resource/stage1_land.png")
        self.move_map = 0

    def draw(self):
        self.stage1_background.draw(self.posX - self.move_map / 5, self.posY, self.width, self.height)
        self.stage1_land.draw(1000 - self.move_map, 150, 2000, 300)

    def update(self):
        if 390 <= player.posX <= 410:
            self.move_map += player.dx
        if self.move_map < 0:
            self.move_map = 0
        if self.move_map > 1200:
            self.move_map = 1200
        if player.isJump == 2:
            player.posY += player.dy


def handle_events():
    global running
    global start
    global finish
    event_s = get_events()
    for event in event_s:
        if event.type == SDL_QUIT:
            running = False
        # --- key dow events
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                if player.posY == 100:
                    player.change_status(Status.Work)
                player.move_change_stat(3, 0, False)
            elif event.key == SDLK_LEFT:
                if player.posY == 100:
                    player.change_status(Status.Work)
                player.move_change_stat(-3, 0, True)
            elif event.key == SDLK_UP:
                player.dy += 2
            elif event.key == SDLK_DOWN:
                player.dy -= 2
            elif event.key == SDLK_h:
                if player.hit_box:
                    player.hit_box = False
                elif not player.hit_box:
                    player.hit_box = True
            elif event.key == SDLK_SPACE:
                if player.isJump == 0:
                    player.jump(1)
                    player.change_status(Status.Jump)
                elif player.isJump == 1:
                    player.jump(2)
                    player.change_status(Status.Fly)
            elif event.key == SDLK_ESCAPE:
                running = False
        # --- key up events
        elif SDL_KEYUP == event.type:
            if event.key == SDLK_RIGHT:

                player.move_change_stat(-3, 0, player.look_at_left)
                if player.posY == 100:
                    player.change_status(Status.Idle)
            elif event.key == SDLK_LEFT:
                player.move_change_stat(3, 0, player.look_at_left)
                if player.posY == 100:
                    player.change_status(Status.Idle)
            elif event.key == SDLK_UP:
                player.dy -= 2
            elif event.key == SDLK_DOWN:
                player.dy += 2
            elif event.key == SDLK_SPACE:
                if player.isJump == 2:
                    player.jump(1)
                    player.change_status(Status.Drop)
                    player.animating = True


open_canvas(800, 450)

# initialization code
player = Kirby()
stage = stage()

# game main loop code
while running:
    mt = clock.tick(FPS) / 1000

    # simulation
    handle_events()
    player.update(mt)
    stage.update()

    # rendering
    clear_canvas()
    stage.draw()
    player.draw()

    update_canvas()

    delay(0.01)
# finalization code
close_canvas()
