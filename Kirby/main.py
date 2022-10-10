import textwrap

from pico2d import *

# global variable
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 450
VELOCITY = 25
MASS = 0.05
running = True


class object:
    def __init__(self, posX, posY, width, height):
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height


class Kirby(object):
    def __init__(self):
        super().__init__(WINDOW_WIDTH / 2, 100, 22, 20)
        self.idle = load_image("resource/idle.png")
        self.dx = 0
        self.dy = 0
        self.isJump = 0
        self.v = VELOCITY
        self.m = MASS
        self.hit_box = True
        self.frame = 0
        self.add_frame = 0.1
        self.div_frame = 6

    # draw player
    def draw(self):
        self.idle.clip_draw(self.frame * self.width, 0, self.width, self.height, self.posX, self.posY, 44, 40)
        # hit_box
        if self.hit_box:
            draw_rectangle(player.posX - self.width, player.posY - self.height, player.posX + self.width,
                           player.posY + self.height)

    # move player
    def move(self):
        if stage.move_map == 0 or stage.move_map == 1200:
            self.posX += self.dx

    # player screen collider
    def check_screen(self):
        if self.posX + 22 > WINDOW_WIDTH or self.posX - 22 < 0:
            self.posX -= self.dx
        if self.posY + 20 > WINDOW_HEIGHT or self.posY - 20 < 0:
            self.posY -= self.dy

    # jump flag
    def jump(self, j):
        # if isJump  == 1 -> jump
        # if isJump  == 2 -> fly
        self.isJump = j

    # update player
    def update(self):
        # move player
        self.move()
        self.check_screen()
        self.frame = (self.frame + 1) % self.div_frame

        # jump player
        if self.isJump > 0:
            if self.isJump == 2 and self.posY < WINDOW_HEIGHT - 20:
                self.v = 0
                self.posY += self.dy
                self.posY -= 1.0
            # FORCE = 1/2 * MASS * VELOCITY ** 2
            if self.v > 0:
                FORCE = (0.5 * self.m * (self.v ** 2))
            else:
                FORCE = -(0.5 * self.m * (self.v ** 2))
            self.posY += round(FORCE)
            self.v -= 1
            if self.posY < 100:
                self.posY = 100
                self.isJump = 0
                self.v = VELOCITY


class stage(object):
    def __init__(self):
        super().__init__(WINDOW_WIDTH - 300, WINDOW_HEIGHT / 2, 1100, WINDOW_HEIGHT)
        self.stage1_background = load_image("stage1_background.png")
        self.stage1_land = load_image("stage1_land.png")
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
            elif event.key == SDLK_h:
                if player.hit_box:
                    player.hit_box = False
                elif not player.hit_box:
                    player.hit_box = True
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


open_canvas(800, 450)

# initialization code
player = Kirby()
stage = stage()

# game main loop code
while running:
    # simulation
    handle_events()
    player.update()
    stage.update()

    # rendering
    clear_canvas()
    stage.draw()
    player.draw()

    update_canvas()

    delay(0.01)

# finalization code
close_canvas()
