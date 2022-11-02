from os import stat
from pico2d import *


# 2. 이벤트 정의
# RD, LD, RU, LU = 0, 1, 2, 3, 4, 5
RD, LD, RU, LU, TIMER, AR = range(6)

# 키 입력 확인을 단순화 시켜서 이벤트로 해석
key_evenet_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,
    (SDL_KEYDOWN, SDLK_a): AR,
}

# 1. 상태 정의


class IDLE:
    def enter(self, event):  # 상태에 들어갈 때 행하는 액션
        print('Enter Idle')
        self.dir = 0
        self.timer = 1000

    def exit(self):  # 상태를 나올 때 행하는 액션, 고개 들기
        print('Exit Idle')

    def do(self):  # 상태에 있을 때 지속적으로 행하는 행위, 숨쉬기
        self.frame = (self.frame + 1) % 8
        self.timer -= 1
        if self.timer == 0:
             self.add_event(TIMER)

    def draw(self):
        if self.face_dir == 1:
            self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)


class RUN:
    @staticmethod  # 이 함수는 객체용이 아니라 클래스 함수이다.
    def enter(self, event):
        print('Enter Run')
        # 방향 결정해야 하는데, 어떤 키가 눌린 것에 근거로 하여
        # 키 이벤트 정보가 필요
        if event == RD:
            self.dir += 1
        elif event == LD:
            self.dir -= 1
        elif event == RU:
            self.dir -= 1
        elif event == LU:
            self.dir += 1
        pass

    @staticmethod  # 이 함수는 객체용이 아니라 클래스 함수이다.
    def exit(self):
        self.face_dir = self.dir
        print('Exit Run')
        pass

    @staticmethod  # 이 함수는 객체용이 아니라 클래스 함수이다.
    def do(self):
        self.frame = (self.frame + 1) % 8
        # x 좌표 변경, 달리기
        self.x += self.dir
        self.x = clamp(0, self.x, 800)

    @staticmethod  # 이 함수는 객체용이 아니라 클래스 함수이다.
    def draw(self):
        if self.dir == -1:
            self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)
        elif self.dir == 1:
            self.image.clip_draw(self.frame*100, 100, 100, 100, self.x, self.y)


class AUTORUN:
    def enter(self, event):
        self.dir = self.face_dir
        print('Enter AutoRun')

    def exit(self):
        self.dir = 0
        print('Exit AutoRun')

    def do(self): 
        if(self.x == 800 or self.x == 0): self.dir *= -1
        self.frame = (self.frame + 1) % 8
        self.x += self.dir
        self.x = clamp(0, self.x, 800)

    def draw(self):
        if self.dir == -1:
            self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y + 25, 200, 200)
        else:
            self.image.clip_draw(self.frame * 100, 100, 100, 100, self.x, self.y + 25, 200, 200)


class SLEEP:
    def enter(self, event):  # 상태에 들어갈 때 행하는 액션
        print('Enter Sleep')
        # self.dir = 0 # idle에서 오는데 굳이 self.dir = 0 을 또 쓸 필요가 없다.
        pass

    def exit(self):  # 상태를 나올 때 행하는 액션, 고개 들기
        print("Exit Sleep")
        pass

    def do(self):  # 상태에 있을 때 지속적으로 행하는 행위, 숨쉬기
        self.frame = (self.frame + 1) % 8
        pass

    def draw(self):
        if self.face_dir == -1:
            self.image.clip_composite_draw(self.frame * 100, 200, 100, 100, -3.141592/2, '', self.x + 25, self.y - 25, 100, 100)
        else:
            self.image.clip_composite_draw(self.frame * 100, 300, 100, 100, 3.141592/2, '',self.x + 25, self.y - 25, 100, 100)


# 3. 상태 변환 기술
next_state = {
    SLEEP: {RU: RUN, LU: RUN, RD: RUN, LD: RUN, TIMER: SLEEP, AR : AUTORUN},
    IDLE: {RU: RUN, LU: RUN, RD: RUN, LD: RUN, TIMER: SLEEP, AR: AUTORUN},
    RUN: {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE, AR: AUTORUN},
    AUTORUN : {RU: AUTORUN, LU: AUTORUN, RD: RUN, LD: RUN, AR : IDLE}
    
}


class Boy:

    def add_event(self, event):
        self.q.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_evenet_table:
            key_evenet = key_evenet_table[(event.type, event.key)]
            self.add_event(key_evenet)

        # if event.type == SDL_KEYDOWN:
        #     match event.key:
        #         case pico2d.SDLK_LEFT:
        #             boy.dir -= 1
        #         case pico2d.SDLK_RIGHT:
        #             boy.dir += 1
        # elif event.type == SDL_KEYUP:
        #     match event.key:
        #         case pico2d.SDLK_LEFT:
        #             boy.dir += 1
        #             boy.face_dir = -1
        #         case pico2d.SDLK_RIGHT:
        #             boy.dir -= 1
        #             boy.face_dir = 1

    def __init__(self):
        self.x, self.y = 0, 90
        self.frame = 0
        self.dir, self.face_dir = 0, 1
        self.image = load_image('animation_sheet.png')

        self.q = []  # 이벤트 큐 초기화
        self.cur_state = IDLE
        self.cur_state.enter(self, None)  # 초기 상태의 entry 액션 수행

    def update(self):
        self.cur_state.do(self)  # 현재 상태의 do 액션 수행

        # 이벤트를 확인해서, 이벤트가 있으면 이벤트 변환 처리
        if self.q:  # 큐에 이벤트가 있으면, 이벤트가 발생했으면,
            event = self.q.pop()
            self.cur_state.exit(self)  # 현재 상태를 나가야하고
            self.cur_state = next_state[self.cur_state][event]  # 다음 상태를 구한다.
            self.cur_state.enter(self, event)

        # self.frame = (self.frame + 1) % 8
        # self.x += self.dir * 1
        # self.x = clamp(0, self.x, 800)

    def draw(self):
        self.cur_state.draw(self)
