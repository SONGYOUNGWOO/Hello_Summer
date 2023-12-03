from pico2d import load_image, draw_rectangle, get_time, clamp
import game_world
import game_framework
import random
import play_mode

global win_w, win_h
win_w, win_h = 1000, 600

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

DECELERATION = 0.05  # 매 프레임마다 속도가 감소하는 양
MAX_VELOCITY = 3    # 공의 최대 속도
def time_out(e):
    return e[0] == 'TIME_OUT'
class Jumping:
    def enter(ball, e):
        ball.action_start_time = get_time()
        ball.velocity = 2  # 초기 상승 속도

    @staticmethod
    def do(ball):
        time_since_action = get_time() - ball.action_start_time

        # 초기에는 위로 상승
        if time_since_action < 0.5:
            ball.dy = -1
            ball.velocity = max(ball.velocity - DECELERATION, 0)
        else:
            # 이후 아래로 하강
            ball.dy = 1
            ball.velocity = min(ball.velocity + ball.GRAVITY * game_framework.frame_time, MAX_VELOCITY)

        # 위치 업데이트
        ball.y += ball.dy * RUN_SPEED_PPS * game_framework.frame_time * ball.velocity

    def exit(ball, e):
        pass

    @staticmethod
    def draw(ball):
        ball.image.clip_draw(int(ball.frame) * 15, 0, 15, 70, ball.x, ball.y, 30, 50)
class Idle:
    @staticmethod
    def enter(ball, e):
        ball.action_start_time = get_time()
        ball.velocity = 2  # 초기 상승 속도


    @staticmethod
    def do(ball):
        time_since_action = get_time() - ball.action_start_time

        # 초기에는 위로 상승
        if time_since_action < 0.5:
            ball.dy = -1
            ball.velocity = max(ball.velocity - DECELERATION, 0)
        else:
            # 이후 아래로 하강
            ball.dy = 1
            ball.velocity = min(ball.velocity + ball.GRAVITY * game_framework.frame_time, MAX_VELOCITY)

        # 위치 업데이트
        ball.y += ball.dy * RUN_SPEED_PPS * game_framework.frame_time * ball.velocity

    def exit(ball, e):
        pass

    @staticmethod
    def draw(ball):
        ball.image.clip_draw(int(ball.frame) * 15, 0, 15, 70, ball.x, ball.y, 30, 50)
        # if ball.face_dir == '오른쪽':
        #     ball.image_idle.clip_draw(int(ball.frame) * 32, 0, 32, 43, ball.x, ball.y, 48, 65)
        # else:
        #     ball.image_idle.clip_composite_draw(int(ball.frame) * 32, 0, 32, 43,
        #                                           0, 'h', ball.x, ball.y, 48, 65)
class Receive:
    @staticmethod
    def enter(ball, e):
        ball.action_start_time = get_time()
        ball.velocity = 2  # 초기 속도 설정

    @staticmethod
    def exit(ball, e):
        # 리시브 상태에서 나갈 때 필요한 로직
        pass

    @staticmethod
    def do(ball):
        ball.frame = (ball.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        # 리시브 상태에서의 공의 움직임을 구현
        time_since_action = get_time() - ball.action_start_time
        if time_since_action < 0.5:
            ball.dy = -1  # 위로 이동
        else:
            ball.dy = 1  # 아래로 이동
        ball.y += ball.dy * ball.velocity


    @staticmethod
    def draw(ball):
        # 리시브 상태에서의 공 그리기 로직
        ball.image.clip_draw(int(ball.frame) * 15, 0, 15, 70, ball.x, ball.y, 30, 50)


class Smash:
    def enter(ball, e):
        ball.action_start_time = get_time()
        ball.velocity = 4 # 초기 속도 설정

    @staticmethod
    def exit(ball, e):
        pass

    @staticmethod
    def do(ball):
        ball.frame = (ball.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        # 리시브 상태에서의 공의 움직임을 구현
        ball.dy, ball.dx = 1, 1
        ball.x += ball.dx * ball.velocity
        ball.y += ball.dy * ball.velocity

    @staticmethod
    def draw(ball):
        # 리시브 상태에서의 공 그리기 로직
        ball.image.clip_draw(int(ball.frame) * 15, 0, 15, 70, ball.x, ball.y, 30, 50)

# 상태 머신 클래스

class StateMachine:
    def __init__(self, ball):
        self.ball = ball
        self.cur_state = Idle

        self.transitions = {
            Idle: {'RECEIVE': Receive, 'SMASH': Smash, 'JUMPING':Jumping},
            Receive: {'TIME_OUT': Idle},
            Smash: {'TIME_OUT': Idle},
            Jumping:{'RECEIVE': Receive, 'SMASH': Smash}
        }

    def update(self):
        self.cur_state.do(self.ball)
        #
        # if self.player in play_mode.enemy_team:
        #     if get_time() - self.last_state_change > self.state_duration:
        #         self.change_state()
        #         self.last_state_change = get_time()

    def handle_event(self, event_type):
        if event_type in self.transitions[self.cur_state]:
            new_state = self.transitions[self.cur_state][event_type]
            self.cur_state.exit(self.ball, event_type)
            self.cur_state = new_state
            self.cur_state.enter(self.ball, event_type)
        pass

    def draw(self):
        self.cur_state.draw(self.ball)



class Ball:
    image = None
    GRAVITY = -5

    def __init__(self, x=30, y=win_h - 100, velocity=1):  # 초기값
        if Ball.image == None:
            Ball.image = load_image('./ball/ballRoll.png')  # 120x 70
        self.current_state = None  # 현재 상태를 저장하는 변수
        self.state_machine = StateMachine(self)
        self.wait_time = get_time()
        self.action_start_time = 0
        self.x, self.y, self.velocity, self.frame = x, y, velocity, 0
        self.dx, self.dy = 0, 1
        self.hit = False
        self.mode = 'idle'

    def update(self):
        self.state_machine.update()
        if self.y <= 10:
            self.y = 10  # 공의 y 위치를 바닥에 고정
            self.velocity = 0  # 공의 속도를 0으로 설정하여 멈춤


    def get_bb(self):
        return self.x - 12, self.y - 25, self.x + 12, self.y + 8

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def handle_collision(self, group, other):
        if group == 'player:ball':
            if other.action == '스매쉬':
                self.state_machine.handle_event('SMASH')
            elif other.action == '슬라이드' or other.action == '리시브':
                self.state_machine.handle_event('RECEIVE')
            else:
                self.state_machine.handle_event('JUMPING')
            self.hit = True

        # MAX_VELOCITY = 2
        # DECELERATION = 0.2
        # time_since_action = get_time() - self.action_start_time
        #
        # if self.mode == '스매쉬':
        #     self.dy, self.dx = 1, 1  # 대각선 아래로 이동
        #     self.velocity = min(self.velocity + DECELERATION, MAX_VELOCITY)
        #
        # elif self.mode == '리시브':
        #     if time_since_action < 0.5:
        #         self.y += 1  # 위로 상승
        #     else:
        #         self.dy = 1  # 아래로 하강
        #         self.dx = 1  # 오른쪽으로 이동
        #         self.velocity = min(self.velocity + DECELERATION, MAX_VELOCITY)
        #
        # else:
        #     self.dx, self.dy = 0, 1
        #     self.velocity += self.GRAVITY * game_framework.frame_time
        #     self.velocity = max(-MAX_VELOCITY, min(self.velocity, MAX_VELOCITY))
        #
        # # 볼의 위치 업데이트
        # self.x += self.dx * RUN_SPEED_PPS * game_framework.frame_time * self.velocity
        # self.y += self.dy * RUN_SPEED_PPS * game_framework.frame_time * self.velocity
        #
        # self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        # self.y = clamp(10, self.y, win_h - 10)
        # self.x = clamp(10, self.x, win_w - 10)