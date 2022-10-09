from pico2d import *
from random import *

from background import *
from Default_Kirby import *
from globals import *

# --- open canvas
WinWidth = 800
WinHeight = 450
open_canvas(WinWidth, WinHeight)

# --- host key
hit_box = False
frame_cnt = 0

# --- player Kirby information
running = True
p1 = Kirby()
jmp_cnt = 0

# --- background information
background = background(WinWidth, WinHeight)


# --- player handle
def handle_events():
    global running
    global hit_box
    global p1

    event_s = get_events()

    for event in event_s:
        if event.type == SDL_QUIT:
            running = False
        # --- key dow events
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                p1.change_status(Status.Work)
                p1.dir_x += 1
            elif event.key == SDLK_LEFT:
                p1.change_status(Status.Work)
                p1.dir_x -= 1
            elif event.key == SDLK_SPACE:
                p1.dir_y += 0.5
                p1.change_status(Status.Jump)
            elif event.key == SDLK_ESCAPE:
                running = False
            # --- show hit box
            elif event.key == SDLK_h:
                if hit_box:
                    hit_box = False
                else:
                    hit_box = True
        # --- key up events
        elif SDL_KEYUP == event.type:
            if event.key == SDLK_RIGHT:
                p1.dir_x -= 1
                p1.change_status(Status.Idle)
            elif event.key == SDLK_LEFT:
                p1.dir_x += 1
                p1.change_status(Status.Idle)


# --- framework function
def framework():
    global p1
    global jmp_cnt
    global frame_cnt

    # --- moving background
    background.move_pos(p1.dir_x)

    # --- jump animation
    if frame_cnt % 2 == 0:
        if p1.status == Status.Jump:
            jmp_cnt += 1
            if jmp_cnt > 6:
                p1.frame = (p1.frame + 1) % p1.div_frame
                if jmp_cnt == 8:
                    p1.dir_y -= 1.0
                if p1.posy < 100:
                    p1.frame = 3
                    p1.posy = 100
                    jmp_cnt = 0
                    p1.dir_y += 0.5
                    if p1.dir_x == 0:
                        p1.change_status(Status.Idle)
                    else:
                        p1.change_status(Status.Work)
        elif p1.status == Status.Idle:
            if frame_cnt % 20 == 0:
                p1.frame = (p1.frame + 1) % p1.div_frame
        else:
            p1.frame = (p1.frame + 1) % p1.div_frame


while running:
    clear_canvas()

    background.draw_background()
    background.draw_land()
    p1.draw()
    frame_cnt += 1

    if hit_box:
        draw_rectangle(p1.posx - p1.width, p1.posy - p1.height, p1.posx + p1.width, p1.posy + p1.height)

    update_canvas()
    handle_events()

    # --- frame
    framework()

    # --- if press and hold to fly
    if p1.status == Status.Take_off and p1.frame < 5:
        p1.frame = 5

    p1.posy += p1.dir_y * 15
    delay(globals.delay_time)
close_canvas()
