import textwrap

from pico2d import *

open_canvas(800, 450)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 450
VELOCITY = 25
MASS = 0.05
running = True

class Kirby:
    def __init__(self):
        self.idle = load_image("Kirby.png")
        self.dx = 0
        self.dy = 0
        self.posX = 400
        self.posY = 100
        self.isJump = 0
        self.v = VELOCITY
        self.m = MASS

    def draw_image(self):
        self.idle.clip_draw(0, 0, 22, 20, self.posX, self.posY, 40, 36)

    def move(self):
        if stage.move_map == 0 or stage.move_map == 1200:
            self.posX += self.dx

    def jump(self, j):
        self.isJump = j

    def check_screen(self):
        if self.posX + 22 > WINDOW_WIDTH or self.posX - 22 < 0:
            self.posX -= self.dx
        if self.posY + 20 > WINDOW_HEIGHT or self.posY - 20 < 0:
            self.posY -= self.dy

    def update(self):
        if self.isJump > 0:
            if self.isJump == 2:
                self.v = 0
                self.posY += self.dy
                self.posY -= 1.0
            if self.v > 0:
                F = (0.5 * self.m * (self.v ** 2))
            else:
                F = -(0.5 * self.m * (self.v ** 2))
            self.posY += round(F)
            self.v -= 1
            if self.posY < 100:
                self.posY = 100
                self.isJump = 0
                self.v = VELOCITY


class stage:
    def __init__(self):
        self.stage1_background = load_image("stage1_background.png")
        self.stage1_land = load_image("stage1_land.png")
        self.move_map = 0

    def draw_image(self):
        self.stage1_background.draw(WINDOW_WIDTH - 300 - self.move_map / 5, WINDOW_HEIGHT / 2, 1100, WINDOW_HEIGHT)
        self.stage1_land.draw(1000 - self.move_map, 150, 2000, 300)

    def move(self):
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
    event_s = get_events()
    for event in event_s:
        if event.type == SDL_QUIT:
            running = False
        # --- key dow events
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                player.dx += 3
            elif event.key == SDLK_LEFT:
                player.dx -= 3
            elif event.key == SDLK_UP:
                player.dy += 2
            elif event.key == SDLK_DOWN:
                player.dy -= 2
            elif event.key == SDLK_SPACE:
                if player.isJump == 0:
                    player.jump(1)
                elif player.isJump == 1:
                    player.jump(2)

            elif event.key == SDLK_ESCAPE:
                running = False
        # --- key up events
        elif SDL_KEYUP == event.type:
            if event.key == SDLK_RIGHT:
                player.dx -= 3
            elif event.key == SDLK_LEFT:
                player.dx += 3
            elif event.key == SDLK_UP:
                player.dy -= 2
            elif event.key == SDLK_DOWN:
                player.dy += 2
            elif event.key == SDLK_SPACE:
                if player.isJump == 2:
                    player.jump(1)


player = Kirby()
stage = stage()

while running:
    clear_canvas()

    stage.draw_image()
    player.draw_image()

    handle_events()
    draw_rectangle(player.posX - 22, player.posY - 20, player.posX + 22, player.posY + 20)

    player.move()
    stage.move()

    player.update()
    player.check_screen()

    update_canvas()
    delay(0.01)
close_canvas()
