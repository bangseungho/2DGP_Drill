from pico2d import *


class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)


class Boy:
    def __init__(self):
        self.x, self.y = 0, 90
        self.frame = 0
        self.image = load_image('run_animation.png')

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += 1

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


team = []
grass = None
running = True
number = 1


# 초기화
def enter():
    global team, grass, running
    team = [Boy() for i in range(number)]
    grass = Grass()
    running = True


# 종료
def exit():
    global boy, grass
    del boy
    del grass


# 월드에 존재하는 객체들을 업데이트 한다.
def update():
    for boy in team:
        boy.update()
    # grass는 업데이트가 필요 없음


def draw():
    clear_canvas()
    grass.draw()

    for boy in team:
        boy.draw()
    update_canvas()


open_canvas()
enter()

# game main loop code
while running:
    handle_events()

    update()
    draw()

    delay(0.05)
exit()

# finalization code
close_canvas()
