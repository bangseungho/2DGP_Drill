from pico2d import *
from enum import Enum

open_canvas()


class Status(Enum):
    Work = 1
    Jump = 2
    Punch = 3


class Player:
    def __init__(self):
        self.image = load_image('Golem.png')
        self.frame = -1
        self.width = 0
        self.status = Status.Work
        self.bottom = 0
        self.height = 120
        self.posX = 100
        self.posY = 100
        self.image_num = 0

    def draw(self):
        self.image.clip_draw(self.frame * self.width, self.bottom, self.width, self.height, self.posX, self.posY)

    def set_option(self, bottom, width, image_num):
        self.bottom = bottom
        self.width = width
        self.image_num = image_num

    def status_option(self):
        self.frame = -1
        if self.status == Status.Work:
            self.set_option(240, 120, 8)
        elif self.status == Status.Jump:
            self.set_option(120, 120, 12)
        elif self.status == Status.Punch:
            self.set_option(0, 160, 12)

    def re_status(self, status):
        self.status = status
        self.status_option()


p1 = Player()

x = 0
p1.status = Status.Work
p1.status_option()
background = load_image('background.png')
jump_cnt = 0
punch_cnt = 0

while p1.posX < 800:
    clear_canvas()
    background.draw(400, 300, 800, 600)
    p1.frame = (p1.frame + 1) % p1.image_num
    p1.draw()

    if p1.posX == 200:
        p1.re_status(Status.Jump)
    if p1.posX == 400:
        p1.posX += 1
        p1.re_status(Status.Punch)

    if p1.status == Status.Work:
        p1.posX += 2
    if p1.status == Status.Jump:
        jump_cnt += 1
        p1.posX += 5
        if jump_cnt > 6:
            p1.posY -= 10
            if jump_cnt == 12:
                p1.re_status(Status.Work)
        else:
            p1.posY += 10
    if p1.status == Status.Punch:
        punch_cnt += 1
        if punch_cnt == 36:
            p1.re_status(Status.Work)

    update_canvas()
    delay(0.05)
    get_events()

close_canvas()
