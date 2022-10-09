from pico2d import *
from enum import Enum

import globals
from globals import *


class Status(Enum):
    Idle = 0
    Work = 1
    Jump = 2
    Take_off = 3
    Land = 4


class Kirby:
    def __init__(self):
        self.idle = load_image('resource/idle.png')
        self.work = load_image('resource/work.png')
        self.jump = load_image('resource/jump.png')
        self.take_off = load_image('resource/take_off.png')
        self.land = load_image('resource/land.png')
        self.status = Status.Idle
        self.posx = 400
        self.posy = 100
        self.dir_x = 0
        self.dir_y = 0
        self.frame = 0
        self.div_frame = 6
        self.width = 0
        self.height = 0

    def draw(self):
        if self.status == Status.Idle:
            self.width = 22
            self.height = 20
            self.idle.clip_draw(22 * self.frame, 0, self.width, self.height, self.posx, self.posy, 40, 36)
        elif self.status == Status.Work:
            self.width = 23
            self.height = 21
            self.work.clip_draw(23 * self.frame, 0, self.width, self.height, self.posx, self.posy, 44, 39)
        elif self.status == Status.Jump:
            self.width = 27
            self.height = 22
            self.jump.clip_draw(27 * self.frame, 0, self.width, self.height, self.posx, self.posy, 44, 39)
        elif self.status == Status.Take_off:
            self.width = 28
            self.height = 27
            self.take_off.clip_draw(28 * self.frame, 0, self.width, self.height, self.posx, self.posy, 48, 44)
        elif self.status == Status.Land:
            self.width = 27
            self.height = 24
            self.land.clip_draw(27 * self.frame, 0, self.width, self.height, self.posx, self.posy, 48, 44)

    def change_status(self, to_change_status):
        self.frame = 0
        self.status = to_change_status
        if to_change_status == Status.Idle:
            self.div_frame = 6
        elif to_change_status == Status.Work:
            self.div_frame = 10
        elif to_change_status == Status.Jump:
            self.div_frame = 10
        elif to_change_status == Status.Take_off:
            self.div_frame = 13
        elif to_change_status == Status.Land:
            self.div_frame = 18
