from pico2d import *
from random import *
from Default_Kirby import *

WinWidth = 800
WinHeight = 450

open_canvas(WinWidth, WinHeight)

p1 = Kirby()

frame = 0

while True:
    clear_canvas()
    p1.draw(frame)
    frame = (frame + 1) % 18
    delay(0.1)
    get_events()

close_canvas()
