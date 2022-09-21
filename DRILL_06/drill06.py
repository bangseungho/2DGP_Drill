from pico2d import *
import math

open_canvas(800, 600)
grass = load_image('grass.png')
character = load_image('character.png')

x = 400
y = 90
cnt = False
dir = 0
cir = 0
rot = 0

while(True):
    clear_canvas_now()
    grass.draw_now(400, 30)
    character.draw_now(x, y)


    if cir == 0 or cir == 1:
        if x > 770:
            x -= 1
            dir = 1
        if y > 550:
            y -= 1
            dir = 2
        if x < 20:
            x += 1
            dir = 3
        if y < 90:
            cir = 1
            y += 1
            dir = 0
        if dir == 0:
            x = x + 2
        if dir == 1:
            y = y + 2
        if dir == 2:
            x = x - 2
        if dir == 3:
            y = y - 2
    if cir == 2:
        x = 400 + math.sin(360 / 360 * 2 * math.pi)
        y = 90 + math.cos(360 / 360 * 2 * math.pi)
        rot += 1

    delay(0.01)


close_canvas()