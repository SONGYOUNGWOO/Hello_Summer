from pico2d import load_image, draw_rectangle, get_time, clamp
import game_world
import game_framework
import random
import play_mode

global win_w, win_h
win_w, win_h = 1000, 700

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 50.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Ball:
    image = None
    GRAVITY = -5

    def __init__(self, x=30, y=win_h - 100, velocity=1):  # 초기값
        if Ball.image == None:
            Ball.image = load_image('./ball/ballRoll.png')  # 120x 70

        self.wait_time = get_time()
        self.ball_hit_time = get_time()
        self.x, self.y, self.velocity, self.frame = x, y, velocity, 0
        self.dx, self.dy = 0, -1
        self.hit = False
        self.mode = 'idle'

    def update(self):
        # 최대 속도와 감속 값 설정
        MAX_VELOCITY = 2
        DECELERATION = 0.2

        # 중력에 의한 가속
        self.velocity += self.GRAVITY * game_framework.frame_time
        self.velocity = clamp(-MAX_VELOCITY, self.velocity, MAX_VELOCITY)

        # 공의 움직임 처리
        if self.hit:
            if self.mode == '스매쉬':
                self.dx = 1
                self.dy = -1
                self.y = play_mode.player_slect.y + 30
                self.velocity = 3



            # 히트된 상태일 때의 움직임 처리
            elif self.velocity > MAX_VELOCITY:
                self.velocity -= DECELERATION * game_framework.frame_time
        else:
            # 히트되지 않은 상태일 때의 움직임 처리
            if get_time() - self.wait_time < 1:
                self.dy = 1  # 위로 이동
            else:
                self.dy = -1  # 아래로 이동

        if self.y <= 11:
            self.hit = False
            self.dy = 0
            self.dx = 0
            self.velocity = 0

        # 속도 적용
        self.x += self.dx * RUN_SPEED_PPS * game_framework.frame_time * self.velocity
        self.y += self.dy * RUN_SPEED_PPS * game_framework.frame_time * self.velocity

        # 프레임 및 위치 제한
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.y = clamp(10, self.y, win_h - 10)
        self.x = clamp(10, self.x, win_w - 10)





    def get_bb(self):
        return self.x - 12, self.y - 25, self.x + 12, self.y + 8

    def draw(self):
        self.image.clip_draw(int(self.frame) * 15, 0, 15, 70, self.x, self.y, 30, 50)
        draw_rectangle(*self.get_bb())

    def handle_collision(self, group, other):
        if group == 'player:ball':
            if other.action == '스매쉬':
                self.mode = '스매쉬'
            self.ball_hit_time = get_time()
            self.velocity = 2
            self.hit = True

# def player_smash(s):
#     return s[0]
#
# class Idle:
#     @staticmethod
#     def enter(ball, e):
#         ball.dir, ball.action = 1, '스매쉬'
#         ball.frame = 0
#         global beg
#         beg = ball.y
#         ball.wait_time = get_time()  # pico2d import 필요
#         pass
#
#     @staticmethod
#     def exit(ball, e):
#         pass
#
#     @staticmethod
#     def do(ball):
#         ball.frame = (ball.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 13
#         ball.y += ball.dir * RUN_SPEED_PPS * game_framework.frame_time * 3
#         if get_time() - ball.wait_time > 0.3: #시간으로 속도 조정
#             ball.y -= (ball.dir * RUN_SPEED_PPS * game_framework.frame_time) * 6
#         if get_time() - ball.wait_time > 0.6:
#             ball.state_machine.handle_event(('TIME_OUT', 0))
#
#
#     @staticmethod
#     def draw(ball):
#         if ball.face_dir == '오른쪽':
#             ball.image_smash.clip_draw(int(ball.frame)* 32, 0, 32, 50, ball.x, ball.y, 48, 75)
#         else:
#             ball.image_smash.clip_composite_draw(int(ball.frame)* 32, 0, 32, 50,
#                                               0, 'h', ball.x , ball.y, 48, 75)
#
#
#
# class StateMachine:
#     def __init__(self, ball):
#         self.ball = ball
#         self.cur_state = Idle
#         self.transitions = {
#             Idle: { Smash: },
#         }
#
#     def start(self):
#         self.cur_state.enter(self.ball, ('NONE', 0))
#
#     def update(self):
#         self.cur_state.do(self.ball)
#
#     def state(self, s):
#         for check_state, next_state in self.transitions[self.cur_state].items():
#             if check_state(s):
#                 self.cur_state.exit(self.ball, s)
#                 self.cur_state = next_state
#                 self.cur_state.enter(self.ball, s)
#                 return True
#
#         return False
#
#     def draw(self):
#         self.cur_state.draw(self.ball)
#
#
# class Ball:
#     def __init__(self):
#         self.x, self.y = 50, win_h / 2.6
#         self.frame = 0
#         self.action = '우'
#         self.dir = 0
#         self.face_dir = '오른쪽'
#         self.image_idle = load_image('./ball/ballRoll.png') # 120x 70, 8 , 15
#         self.state_machine = StateMachine(self)
#         self.state_machine.start()
#
#     def update(self):
#         self.state_machine.update()
#
#     def Ball_state(self, cur_state):
#         self.state_machine.state(cur_state)
#
#     def draw(self):
#         self.state_machine.draw()
#         draw_rectangle(*self.get_bb())  # 튜플을 풀어헤쳐서 인자로 전달.
#
#     def get_bb(self):
#         return self.x - 12, self.y - 25, self.x + 12, self.y + 8
#
#     def handle_collision(self, group, other):
#         pass
#
#
