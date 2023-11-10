from pico2d import load_image, get_time , delay, draw_rectangle
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 1  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6


class Beach:
    def __init__(self):
        self.image_grass = load_image('./background/beachbkg.png')

    def draw(self):
        self.image_grass.draw(400, 300, 800, 600)

    def update(self):
        pass


class Net:
    def __init__(self):
        self.bool = False
        self.frame = 0
        self.x, self.y = 400, 270
        self.image = load_image('./background/net.png') #270 x450 :6
    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

    def get_bb(self):
        return self.x - 20, self.y - 250, self.x + 20, self.y + 250  # 튜플


    def draw(self):
        self.image.clip_composite_draw(int(self.frame) * 45, 0, 45, 450,  - 3.141592 / 100, '', self.x, self.y, 45, 510)
        draw_rectangle(*self.get_bb())