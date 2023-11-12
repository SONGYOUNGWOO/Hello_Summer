from pico2d import load_image, draw_rectangle, get_time, clamp
import game_world
import game_framework
import random

global win_w, win_h
win_w ,win_h = 1000, 700

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 100.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Ball:
    image = None

    def __init__(self,x= 30, y= win_h - 100,velocity = 1): #초기값
        if Ball.image == None:
            Ball.image = load_image('./ball/ballRoll.png') # 120x 70

        self.wait_time = get_time()
        self.ball_hit_time = get_time()
        self.x, self.y, self.velocity ,self.frame = x, y, velocity, 0
        self.dx, self.dy = 0, -1

    def update(self):
        #print(get_time(),self.wait_time)
        if (get_time() - self.wait_time < 1):
            self.y += self.dy * RUN_SPEED_PPS * game_framework.frame_time * self.velocity / 2
            self.x += self.dx * RUN_SPEED_PPS * game_framework.frame_time * self.velocity / 2
        if(get_time() - self.ball_hit_time < 2):
            self.y += self.dy * RUN_SPEED_PPS * game_framework.frame_time * self.velocity / 2
            self.x += self.dx * RUN_SPEED_PPS * game_framework.frame_time * self.velocity / 2
            self.wait_time = get_time()

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.y = max(10, min(self.y, win_h - 10))
        self.x = max(10, min(self.x, win_w - 10))

    def get_bb(self):
        return self.x - 12, self.y - 25, self.x + 12, self.y + 8

    def draw(self):
        self.image.clip_draw(int(self.frame)* 15, 0, 15, 70, self.x, self.y, 30, 50)
        draw_rectangle(*self.get_bb())

    def handle_collision(self, group, other):
        if group == 'ball:ball':
            self.ball_hit_time = get_time()
            self.dy *= -1
            self.dx = 1
            self.velocity = 2

def player_smash(s):
    return s[0]

class Idle:
    @staticmethod
    def enter(ball, e):
        ball.dir, ball.action = 1, '스매쉬'
        ball.frame = 0
        global beg
        beg = ball.y
        ball.wait_time = get_time()  # pico2d import 필요
        pass

    @staticmethod
    def exit(ball, e):
        pass

    @staticmethod
    def do(ball):
        ball.frame = (ball.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 13
        ball.y += ball.dir * RUN_SPEED_PPS * game_framework.frame_time * 3
        if get_time() - ball.wait_time > 0.3: #시간으로 속도 조정
            ball.y -= (ball.dir * RUN_SPEED_PPS * game_framework.frame_time) * 6
        if get_time() - ball.wait_time > 0.6:
            ball.state_machine.handle_event(('TIME_OUT', 0))


    @staticmethod
    def draw(ball):
        if ball.face_dir == '오른쪽':
            ball.image_smash.clip_draw(int(ball.frame)* 32, 0, 32, 50, ball.x, ball.y, 48, 75)
        else:
            ball.image_smash.clip_composite_draw(int(ball.frame)* 32, 0, 32, 50,
                                              0, 'h', ball.x , ball.y, 48, 75)



class StateMachine:
    def __init__(self, ball):
        self.ball = ball
        self.cur_state = Idle
        self.transitions = {
            Idle: { Smash: },
        }

    def start(self):
        self.cur_state.enter(self.ball, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.ball)

    def state(self, s):
        for check_state, next_state in self.transitions[self.cur_state].items():
            if check_state(s):
                self.cur_state.exit(self.ball, s)
                self.cur_state = next_state
                self.cur_state.enter(self.ball, s)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.ball)


class Ball:
    def __init__(self):
        self.x, self.y = 50, win_h / 2.6
        self.frame = 0
        self.action = '우'
        self.dir = 0
        self.face_dir = '오른쪽'
        self.image_idle = load_image('./ball/ballRoll.png') # 120x 70, 8 , 15
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def Ball_state(self, cur_state):
        self.state_machine.state(cur_state)

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())  # 튜플을 풀어헤쳐서 인자로 전달.

    def get_bb(self):
        return self.x - 12, self.y - 25, self.x + 12, self.y + 8

    def handle_collision(self, group, other):
        pass






