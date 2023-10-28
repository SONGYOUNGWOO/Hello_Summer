# 이것은 각 상태들을 객체로 구현한 것임.
from pico2d import (get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_w, SDLK_a,
                    SDLK_s, SDLK_d, SDLK_k)
from ball import Ball
import game_world
# state event check
# ( state event type, event value )
def D_down(e): #오른쪽
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d
def D_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d

def A_down(e): #왼쪽
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def A_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a

def W_down(e): #위
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w
def W_up(e): #위
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w

def S_down(e): #아래
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s
def S_up(e): #아래
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
def space_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_SPACE
def K_down(e): #아래
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_k


def time_out(e):
    return e[0] == 'TIME_OUT'


# time_out = lambda e : e[0] == 'TIME_OUT'

#1:왼쪽 2:오른쪽 3:위 4:아래 5:점프
class Idle:
    # 1:왼쪽 2:오른쪽 3:위 4:아래 5:점프
    @staticmethod
    def enter(boy, e):
        if boy.face_dir == -1:
            boy.action = 1
        elif boy.face_dir == 1:
            boy.action = 2
        boy.dir = 0
        boy.frame = 0
        boy.wait_time = get_time()  # pico2d import 필요
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 12
        if get_time() - boy.wait_time > 2:
            boy.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image_idle.clip_draw(boy.frame * 32, 0, 32, 43, boy.x, boy.y)

class Run:
    # 1:왼쪽 2:오른쪽 3:위 4:아래 5:점프
    @staticmethod
    def enter(boy, e):
        if A_down(e) or A_up(e):  # 왼쪽으로 RUN
            boy.dir, boy.face_dir, boy.action = -1, -1, 1
        elif D_down(e) or D_up(e):  # 오른쪽으로 RUN
            boy.dir, boy.face_dir, boy.action = 1, 1, 2
        elif W_down(e) or W_up(e):  # 오른쪽으로 RUN
            boy.dir, boy.face_dir, boy.action = 1, 1, 3
        elif S_down(e) or S_up(e):  # 오른쪽으로 RUN
            boy.dir, boy.face_dir, boy.action = -1, 1, 4

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 12
        if boy.action < 3:
            boy.x += boy.dir * 4
        else:
            boy.y += boy.dir * 4
        pass

    @staticmethod
    def draw(boy):
        if boy.dir == -1:  # 왼쪽
            boy.image_run.clip_composite_draw(boy.frame * 32, 0, 32, 43, 0, 'h',
                                              boy.x, boy.y, 32, 43)
        else:
            boy.image_run.clip_draw(boy.frame * 32, 0, 32, 43, boy.x, boy.y)


class Jump:
    @staticmethod
    def enter(boy, e):
        boy.dir, boy.face_dir, boy.action = 1, 1, 5
        boy.frame = 0
        global beg_y, end_y
        beg_y = boy.y
        end_y = beg_y + 100
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        if boy.y < end_y:
            boy.frame = (boy.frame + 1) % 13
            boy.y += boy.dir * 50
        else:
            boy.y = beg_y

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image_jump.clip_draw(boy.frame * 32, 0, 32, 50, boy.x, boy.y, 32,50)
        else:
            boy.image_jump.clip_composite_draw(boy.frame * 32, 0, 32, 50,
                                              0, 'h', boy.x , boy.y, 32, 50)
class Reception:
    @staticmethod
    def enter(boy, e):
        boy.dir, boy.face_dir, boy.action = 1, 1, 6
        boy.frame = 0
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 11


    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image_reception.clip_draw(boy.frame * 32, 0, 32, 43, boy.x, boy.y, 32, 43)
        else:
            boy.image_reception.clip_composite_draw(boy.frame * 32, 0, 32, 50,
                                              0, 'h', boy.x , boy.y, 32, 43)


class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Idle
        self.transitions = {
            Idle: {D_down: Run, A_down: Run, D_up:  Idle, A_up:  Idle,
                   W_down: Run, S_down: Run, W_up:  Idle, S_up:  Idle,
                   space_down: Jump, K_down: Reception},
            Run: {D_down: Idle, A_down: Idle, D_up: Idle, A_up: Idle,
                  W_down: Idle, S_down: Idle, W_up: Idle, S_up: Idle,
                  space_down: Jump,K_down: Reception},
            Jump: {space_up: Idle},
            Reception: {D_down: Run, A_down: Run, D_up:  Idle, A_up:  Idle,
                   W_down: Run, S_down: Run, W_up:  Idle, S_up:  Idle,
                   space_down: Jump}
        }

    def start(self):
        self.cur_state.enter(self.boy, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.boy)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.boy)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 40
        self.frame = 0
        self.action = 2 #1:왼쪽 2:오른쪽 3:위 4:아래 5:점프
        self.dir = 0
        self.face_dir = 1  # 얼굴이 바라보는 방향 1오른쪾 -1왼쪽
        self.image_idle = load_image('playerIdle.png') # 384 x 43
        self.image_run = load_image('playerRun.png') # 384 x 43
        self.image_jump = load_image('playerSmash.png') # 416 x 50
        self.image_reception = load_image('playerReception.png') # 352 x 43
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    def fire_ball(self):
        ball = Ball(self.x, self.y + 5, self.face_dir * 10)
        game_world.add_objects(ball, 0)

        if self.face_dir == -1:  # 왼쪽
            print('FIRE BALL to LEFT')
        elif self.face_dir == 1:  # 오른쪽
            print('FIRE BALL to RIGHT')
