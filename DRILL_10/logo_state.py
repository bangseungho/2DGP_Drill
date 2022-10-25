from pico2d import *
import game_framework
import play_state
import title_state

logo_time = 0.0
image = None


def enter():
    global image
    image = load_image('tuk_credit.png')


def exit():
    global image
    del image


def update():
    global logo_time
    delay(0.01)
    logo_time += 0.01
    if logo_time >= 0.5:
        logo_time = 0
        game_framework.change_state(title_state)


def draw():
    global image
    clear_canvas()
    image.draw(400, 300)
    update_canvas()


def handle_events():
    events = get_events()
