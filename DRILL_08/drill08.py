from pico2d import *

KPU_WIDTH, KPU_HEIGHT = 1280, 1024

def handle_events():
    global running
    global dir, diry
    global status
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir += 1
                status = 2
            elif event.key == SDLK_LEFT:
                dir -= 1
                status = 3
            if event.key == SDLK_UP:
                diry += 1
            elif event.key == SDLK_DOWN:
                diry -= 1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir -= 1
                status = 0
            elif event.key == SDLK_LEFT:
                dir += 1
                status = 1
            elif event.key == SDLK_UP:
                diry -= 1
            elif event.key == SDLK_DOWN:
                diry += 1

open_canvas(KPU_WIDTH, KPU_HEIGHT)
kpu_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')

status = 0
running = True
x = 1280 // 2
y = 1024 // 2
frame = 0
dir = 0
diry = 0

while running:
    clear_canvas()
    global statis
    kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)

    if status == 0:
        character.clip_draw(frame * 100, 100 * 3, 100, 100, x, y)
    elif status == 1:
        character.clip_draw(frame * 100, 100 * 2, 100, 100, x, y)
    elif status == 2:
        character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)
    elif status == 3:
        character.clip_draw(frame * 100, 100 * 0, 100, 100, x, y)

    update_canvas()
    handle_events()
    frame = (frame + 1) % 8

    x += dir * 5
    y += diry * 5

    if x > 1260:
        x = 1260 - 1
    if x < 20:
        x = 20 + 1
    if y > 1004:
        y = 1004 - 1
    if y < 20:
        y = 20 + 1

    delay(0.01)

close_canvas()

