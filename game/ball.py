from pico2d import load_image, draw_rectangle, get_time, clamp, load_wav
import game_world
import game_framework
import random
import play_mode

global win_w, win_h
win_w, win_h = 1000, 600

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

DECELERATION = 0.05  # 매 프레임마다 속도가 감소하는 양
MAX_VELOCITY = 3   # 공의 최대 속도
def time_out(e):
    return e[0] == 'TIME_OUT'

class Idle:
    @staticmethod
    def enter(ball, e):
        ball.action_start_time = get_time()
        ball.velocity = 1  # 초기 상승 속도

    @staticmethod
    def do(ball):
        ball.x += ball.dx * ball.velocity * RUN_SPEED_PPS * game_framework.frame_time
        ball.y += ball.dy * ball.velocity * RUN_SPEED_PPS * game_framework.frame_time
        if (ball.dx < 0 and ball.left <= 10) or (ball.dx > 0 and ball.right >= win_w - 10):
            ball.dx *= -1
            ball.x += ball.dx * ball.velocity * RUN_SPEED_PPS * game_framework.frame_time

        if (ball.dy < 0 and ball.btm <= 0) or (ball.dy > 0 and ball.top >= win_h - 10):
            ball.dy *= -1
            ball.y += ball.dy * ball.velocity * RUN_SPEED_PPS * game_framework.frame_time

    def exit(ball, e):
        pass

    @staticmethod
    def draw(ball):
        ball.image.clip_draw(int(ball.frame) * 15, 0, 15, 70, ball.x, ball.y, 60, 100)

class Receive:
    @staticmethod
    def enter(ball, e):
        ball.action_start_time = get_time()
        ball.velocity = 1  # 초기 속도 설정

    @staticmethod
    def exit(ball, e):
        pass

    @staticmethod
    def do(ball):
        ball.x += ball.dx * ball.velocity * RUN_SPEED_PPS * game_framework.frame_time
        ball.y += ball.dy * ball.velocity * RUN_SPEED_PPS * game_framework.frame_time
        if (ball.dx < 0 and ball.left <= 10) or (ball.dx > 0 and ball.right >= win_w - 10):
            ball.dx *= -1
            ball.x += ball.dx * ball.velocity * RUN_SPEED_PPS * game_framework.frame_time
        if (ball.dy < 0 and ball.btm <= 0) or (ball.dy > 0 and ball.top >= win_h - 10):
            ball.dy *= -1
            ball.y += ball.dy * ball.velocity * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(ball):
        ball.image.clip_draw(int(ball.frame) * 15, 0, 15, 70, ball.x, ball.y, 60, 100)


class Smash:
    def enter(ball, e):
        ball.action_start_time = get_time()
        ball.velocity = 2 # 초기 속도 설정
        ball.dy = -1

    @staticmethod
    def exit(ball, e):
        pass

    @staticmethod
    def do(ball):
        ball.x += ball.dx * ball.velocity * RUN_SPEED_PPS * game_framework.frame_time
        ball.y += ball.dy * ball.velocity * RUN_SPEED_PPS * game_framework.frame_time
        # if (ball.dx < 0 and ball.left <= 10) or (ball.dx > 0 and ball.right >= win_w - 10):
        #     ball.dx *= -1
        #     ball.x += ball.dx * ball.velocity * RUN_SPEED_PPS * game_framework.frame_time
        #
        # if (ball.dy < 0 and ball.btm <= 0) or (ball.dy > 0 and ball.top >= win_h - 10):
        #     ball.dy *= -1
        #     ball.y += ball.dy * ball.velocity * RUN_SPEED_PPS * game_framework.frame_time

        if get_time() - ball.action_start_time > 1:  # 시간으로 속도 조정
            ball.velocity = 1
            ball.state_machine.handle_event(('TIME_OUT', 0))



    @staticmethod
    def draw(ball):
        ball.image.clip_draw(int(ball.frame) * 15, 0, 15, 70, ball.x, ball.y, 60, 100)

# 상태 머신 클래스

class StateMachine:
    def __init__(self, ball):
        self.ball = ball
        self.cur_state = Idle

        self.transitions = {
            Idle: {'RECEIVE': Receive, 'SMASH': Smash, },
            Receive: {'TIME_OUT': Idle},
            Smash: {'TIME_OUT': Idle},
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

enemy_score = 0
ally_score = 0



class Ball:
    image = None
    smashs_sound = None



    def __init__(self, x=30, y=win_h - 100, velocity=1):  # 초기값
        if Ball.image == None:
            Ball.image = load_image('./ball/ballRoll.png')  # 120x 70
        self.current_state = None  # 현재 상태를 저장하는 변수
        self.state_machine = StateMachine(self)
        self.wait_time = get_time()
        self.action_start_time = 0
        self.x, self.y, self.velocity, self.frame = x, y, velocity, 0
        self.btm ,self.top= self.y - 50, self.y + 6
        self.left,self.right = self.x - 24,self.x + 20
        self.dx, self.dy = 0, -1

        if not Ball.smashs_sound:
            Ball.smashs_sound = load_wav('./sound/smashs.wav') #동시에 여러 음악 재생시 wav로 진행
            Ball.smashs_sound.set_volume(24)



    def update(self):
        global enemy_score, ally_score  # 전역 변수 사용

        self.state_machine.update()
        if self.y >= win_h - 10:
            self.dy = -1  # 아래로 떨어지도록 방향 변경
        if self.y <= 20:  # 공이 바닥에 닿으면
            if self.x < win_w / 2:
                enemy_score += 1  # 적팀 점수 증가
            else:
                ally_score += 1  # 아군팀 점수 증가

            # 점수 업데이트 후 게임 재시작
            game_framework.change_mode(play_mode)
            return




    def get_bb(self):
        self.btm, self.top = self.y - 50, self.y + 6
        self.left, self.right = self.x - 24, self.x + 20
        return self.left, self.btm, self.right, self.top

    def draw(self):
        self.state_machine.draw()
        self.draw_score()  # 점수를 화면에 출력하는 함수 호출
        draw_rectangle(*self.get_bb())

    def draw_score(self):
        # 점수를 화면에 출력하는 함수
        # 여기에서는 font 라이브러리를 사용하여 점수를 출력합니다.
        # font = load_font(...)
        # font.draw(위치, f'Enemy: {enemy_score} Ally: {ally_score}')
        pass

    def handle_collision(self, group, other):
        if group == 'player:ball':
            if self.x < win_w / 2:
                self.dx, self.dy = 1, 1
            if other.action == '스매쉬':
                self.state_machine.handle_event('SMASH')
            elif other.action == '슬라이드' or other.action == '리시브':
                self.state_machine.handle_event('RECEIVE')

        elif group == 'enemy:ball':
            if self.x > win_w / 2:
                self.dx, self.dy = -1, 1
            if other.action == '스매쉬':
                Ball.smashs_sound.play()
                self.state_machine.handle_event('SMASH')
            elif other.action == '슬라이드' or other.action == '리시브':
                self.state_machine.handle_event('RECEIVE')


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