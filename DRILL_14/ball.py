import random
from pico2d import *
import game_world
import server

class Ball:
    image = None

    def __init__(self):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y = random.randint(0, 1600), random.randint(0, 1000)

    def draw(self):
        self.sx, self.sy = self.x - server.background.window_left, self.y - server.background.window_bottom
        self.image.draw(self.sx, self.sy)
        draw_rectangle(self.sx - 10, self.sy - 10, self.sx + 10, self.sy + 10)

    def update(self):
        pass

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10
    
    def handle_collision(self, other, group):
        game_world.remove_object(self)

