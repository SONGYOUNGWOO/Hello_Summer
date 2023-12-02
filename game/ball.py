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
        MAX_VELOCITY = 2
        DECELERATION = 0.2

        self.velocity += self.GRAVITY * game_framework.frame_time
        self.velocity = clamp(-MAX_VELOCITY, self.velocity, MAX_VELOCITY)

        if self.hit:
            if self.mode == '스매쉬':
                self.dx = 1 if play_mode.players else -1
                self.velocity = 3
            elif self.mode == '리시브':
                self.dx = 0
                self.dy *= -1

        else:
            pass



        self.x += self.dx * RUN_SPEED_PPS * game_framework.frame_time * self.velocity
        self.y += RUN_SPEED_PPS * game_framework.frame_time * self.velocity

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
            elif other.action == '슬라디드' or other.action == '리시브':
                self.mode = '리시브'
            self.ball_hit_time = get_time()
            self.velocity = 2
            self.hit = True
