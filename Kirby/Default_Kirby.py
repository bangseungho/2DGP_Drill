from pico2d import *


class Kirby:
    def __init__(self):
        self.work = load_image('resource/work.png')
        self.jump = load_image('resource/jump.png')
        self.take_off = load_image('resource/take_off.png')
        self.land = load_image('resource/land.png')
        self.status = 3

    def draw(self, frame):
        if self.status == 0:
            self.work.clip_draw(23 * frame, 0, 23, 21, 400, 450/2, 48, 44)
        elif self.status == 1:
            self.jump.clip_draw(27 * frame, 0, 27, 22, 400, 450/2, 48, 44)
        elif self.status == 2:
            self.take_off.clip_draw(28 * frame, 0, 28, 27, 400, 450 / 2, 48, 44)
        elif self.status == 3:
            self.land.clip_draw(27 * frame, 0, 27, 24, 400, 450/2, 48, 44)

        update_canvas()
