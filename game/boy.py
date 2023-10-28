# 이것은 각 상태들을 객체로 구현한 것임.
from pico2d import (get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_w, SDLK_a,
                    SDLK_s, SDLK_d)
from ball import Ball
import game_world

# state event check
# ( state event type, event value )

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'


# time_out = lambda e : e[0] == 'TIME_OUT'


class Idle:
    @staticmethod
    def enter(boy, e):
        if boy.face_dir == -1:
            boy.action = 2
        elif boy.face_dir == 1:
            boy.action = 3
        boy.dir = 0
        boy.frame = 0
        boy.wait_time = get_time()  # pico2d import 필요
        pass

    @staticmethod
    def exit(boy, e):
        if space_down(e):
            boy.fire_ball()
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

    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            boy.dir, boy.face_dir, boy.action = 1, 1, 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            boy.dir, boy.face_dir, boy.action = -1, -1, 0

    @staticmethod
    def exit(boy, e):
        if space_down(e):
            boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 12
        boy.x += boy.dir * 5
        pass

    @staticmethod
    def draw(boy):
        if boy.dir == 1:  # 오른쪽
            boy.image_run.clip_draw(boy.frame * 32, 0, 32, 43, boy.x, boy.y)
        else:
            boy.image_run.clip_composite_draw(boy.frame * 32, 0, 32, 43, 0, 'h', boy.x, boy.y,32,43)


class Sleep:

    @staticmethod
    def enter(boy, e):
        boy.frame = 0
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 12

    @staticmethod
    def draw(boy):
        if boy.face_dir == -1:
            boy.image_idle.clip_composite_draw(boy.frame * 32, 0, 32, 43,
                                               -3.141592 / 2, '', boy.x + 25, boy.y - 25, 32,43)
        else:
            boy.image_idle.clip_composite_draw(boy.frame * 32, 0, 32, 43,
                                               3.141592 / 2, '', boy.x - 25, boy.y - 25, 32,43)


class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Sleep, space_down: Idle},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Run},
            Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run}
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
        self.action = 3
        self.dir = 0
        self.face_dir = 1  # 얼굴이 바라보는 방향 1오른쪾 -1왼쪽
        self.image_idle = load_image('playerIdle.png') # 384 x 43
        self.image_run = load_image('playerRun.png') # 384 x 43
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
