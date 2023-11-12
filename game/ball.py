from pico2d import load_image,  draw_rectangle
import game_world
import game_framework
import random

global win_w, win_h
win_w ,win_h = 1000, 700

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

    def __init__(self,x= 30, y= win_h - 100,velocity = 1):
        if Ball.image == None:
            Ball.image = load_image('./ball/ballRoll.png') # 120x 70
        self.x, self.y, self.velocity ,self.frame = x, y, velocity, 0


    def update(self):
        if (self.y > 100):
            self.y -= RUN_SPEED_PPS * game_framework.frame_time
        # self.x = RUN_SPEED_PPS * game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.y = max(10, min(self.y, win_h - 10))
        self.x = max(10, min(self.x, win_w - 10))

    def get_bb(self):
        return self.x - 12, self.y - 25, self.x + 12, self.y + 8

    def draw(self):
        self.image.clip_draw(int(self.frame)* 15, 0, 15, 70, self.x, self.y, 30, 50)
        draw_rectangle(*self.get_bb())

    def handle_collision(self, group, other):
        pass






