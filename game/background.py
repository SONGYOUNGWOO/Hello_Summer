from pico2d import load_image, get_time, delay, draw_rectangle
import game_framework

global win_w, win_h

win_w, win_h = 1000, 700

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 1  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6


# 700-490,600-430, 500-360 약 3.3
class Beach:
    def __init__(self):
        self.image_grass = load_image('./background/beachbkg2.png')

    def draw(self):
        self.image_grass.draw(win_w / 2, win_h / 2, win_w, win_h)

    def update(self):
        pass


class Net:
    def __init__(self):
        self.bool = False
        self.frame = 0
        self.x, self.y = win_w / 2, 180
        self.image = load_image('./background/net3.png')  # 270, 375

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

    def get_bb(self):
        return self.x - 20, self.y - win_h / 2.4, self.x + 20, self.y + win_h / 2.4  # 튜플

    def draw(self):
        self.image.clip_composite_draw(int(self.frame) * 45, 0, 45, 375, - 3.141592 / 100, '', self.x, self.y, 45,
                                       win_h/2)
        #draw_rectangle(*self.get_bb())

    def handle_collision(self, group, other):
        pass
