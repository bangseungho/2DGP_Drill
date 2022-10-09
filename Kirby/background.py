from pico2d import *


class background:
    def __init__(self, WinWidth, WinHeight):
        self.stage1_background = load_image('resource/stage1_background.png')
        self.stage1_land = load_image('resource/stage1_land.png')
        self.WinWidth, self.WinHeight = WinWidth, WinHeight
        self.move = 0
        self.posX = 1000

    def draw_background(self):
        self.stage1_background.draw(self.WinWidth / 2, self.WinHeight / 2, self.WinWidth, self.WinHeight)

    def draw_land(self):
        self.stage1_land.draw(self.posX, 150, 2000, 300)

    def move_pos(self, value):
        self.posX -= value * 5
