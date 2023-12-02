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


class Ball:
    image = None
    GRAVITY = -5

    def __init__(self, x=30, y=win_h - 100, velocity=1):  # 초기값
        if Ball.image == None:
            Ball.image = load_image('./ball/ballRoll.png')  # 120x 70

        self.wait_time = get_time()
        self.smash_start_time = 0
        self.x, self.y, self.velocity, self.frame = x, y, velocity, 0
        self.dx, self.dy = 0, 1
        self.hit = False
        self.mode = 'idle'

    def update(self):
        MAX_VELOCITY = 2
        DECELERATION = 0.2

        if self.hit and self.mode == '스매쉬':
            time_since_smash = get_time() - self.smash_start_time

            if time_since_smash  > 0.2:  # 0.5초 동안은 볼을 상승시킴
                self.dy = -1  # 위로 상승
            else:  # 이후에는 45도 각도로 아래로 떨어짐
                self.dy = 1  # 아래로 하강
                self.dx = 1  # 오른쪽으로 이동 (45도 각도)

            # 볼의 속도 조정
            self.velocity = 3
        elif self.mode == '리시브':
            time_since_smash = get_time() - self.smash_start_time

            if time_since_smash > 1:  # 0.5초 동안은 볼을 상승시킴\
                self.dy = -1  # 아래로 상승
                self.dx = 2 # 오른쪽으로 이동 (45도 각도)


        else:
            self.dx, self.dy = 0, 1
            # 볼이 스매쉬 상태가 아닐 때 일반적인 중력 영향을 받도록 함
            self.velocity += self.GRAVITY * game_framework.frame_time
            self.velocity = clamp(-MAX_VELOCITY, self.velocity, MAX_VELOCITY)

            # 볼의 위치 업데이트
        self.x += self.dx * RUN_SPEED_PPS * game_framework.frame_time
        self.y += self.dy * RUN_SPEED_PPS * game_framework.frame_time * self.velocity

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
                self.smash_start_time = get_time()
                self.mode = '스매쉬'
            elif other.action == '슬라디드' or other.action == '리시브':
                self.smash_start_time = get_time()
                self.mode = '리시브'
            self.ball_hit_time = get_time()
            self.velocity = 2
            self.hit = True
