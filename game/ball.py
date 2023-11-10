from pico2d import load_image,  draw_rectangle
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

    def __init__(self,x= 200, y= 400,velocity = 1):
        if Ball.image == None:
            Ball.image = load_image('./ball/ballRoll.png') # 120x 70
        self.x, self.y, self.velocity = x, y, velocity


    def update(self):
        self.y += self.velocity * 100 * game_framework.frame_time
        self.x += self.velocity * 100 * game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if self.y > 70:
            self.y -= random.randint(1, 30)
        self.y = max(10, min(self.y, win_h - 10))
        self.x = max(10, min(self.x, win_w - 10))

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def draw(self):
        self.image.clip_draw(int(self.frame)* 15, 0, 15, 70, self.x, self.y, 15, 70)
        draw_rectangle(*self.get_bb())

    def handle_collision(self, group, other):
        pass






