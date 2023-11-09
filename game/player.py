# 이것은 각 상태들을 객체로 구현한 것임.
from pico2d import (get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_w, SDLK_a,
                    SDLK_s, SDLK_d, SDLK_k, SDLK_p,draw_rectangle)
from ball import Ball
import game_world
import game_framework

# state event check
# ( state event type, event value )
def D_down(e): #오른쪽
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d
def D_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d

def A_down(e): #왼쪽
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def A_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a

def W_down(e): #위
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w
def W_up(e): #위
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w

def S_down(e): #아래
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s
def S_up(e): #아래
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
def space_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_SPACE
def K_down(e): #아래
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_k
def P_down(e): #아래
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_p

def time_out(e):
    return e[0] == 'TIME_OUT'


# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 12




# time_out = lambda e : e[0] == 'TIME_OUT'

#1:왼쪽 2:오른쪽 3:위 4:아래 5:점프
class Idle:
    # 1:왼쪽 2:오른쪽 3:위 4:아래 5:점프
    @staticmethod
    def enter(player, e):
        if player.face_dir == -1:
            player.action = 1
        elif player.face_dir == 1:
            player.action = 2
        player.dir = 0
        player.frame = 0
        player.wait_time = get_time()  # pico2d import 필요
        pass

    @staticmethod
    def exit(player, e):
        if P_down(e):
            player.fire_ball()
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12
        if get_time() - player.wait_time > 2:
            player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        player.image_idle.clip_draw(int(player.frame) * 32, 0, 32, 43, player.x, player.y, 48, 65)

class Run:
    # 1:왼쪽 2:오른쪽 3:위 4:아래 5:점프
    @staticmethod
    def enter(player, e):
        if A_down(e) or A_up(e):  # 왼쪽으로 RUN
            player.dir, player.face_dir, player.action = -1, -1, 1
        elif D_down(e) or D_up(e):  # 오른쪽으로 RUN
            player.dir, player.face_dir, player.action = 1, 1, 2
        elif W_down(e) or W_up(e):  # 오른쪽으로 RUN
            player.dir, player.face_dir, player.action = 1, 1, 3
        elif S_down(e) or S_up(e):  # 오른쪽으로 RUN
            player.dir, player.face_dir, player.action = -1, 1, 4

    @staticmethod
    def exit(player, e):
        if P_down(e):
            player.fire_ball()
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12
        if player.action < 3:
            player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time
        else:
            player.y += player.dir * RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(player):
        if player.dir == -1:  # 왼쪽
            player.image_run.clip_composite_draw(int(player.frame) * 32, 0, 32, 43, 0, 'h',
                                              player.x, player.y, 48, 65)
        else:
            player.image_run.clip_draw(int(player.frame) * 32, 0, 32, 43, player.x, player.y, 48, 65)


class Jump:
    @staticmethod
    def enter(player, e):
        player.dir, player.face_dir, player.action = 1, 1, 5
        player.frame = 0
        global beg
        beg = player.y
        player.wait_time = get_time()  # pico2d import 필요
        pass

    @staticmethod
    def exit(player, e):
        if P_down(e):
            player.fire_ball()
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 13
        player.y += player.dir * RUN_SPEED_PPS * game_framework.frame_time * 3
        if get_time() - player.wait_time > 0.2: #시간으로 속도 조정
            player.y -= (player.dir * RUN_SPEED_PPS * game_framework.frame_time) * 6
        if get_time() - player.wait_time > 0.4:
            player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image_block.clip_draw(32 * 7, 0, 32, 46, player.x, player.y, 48, 65)
        else:
            player.image_block.clip_composite_draw(32 * 7, 0, 32, 46,
                                              0, 'h', player.x , player.y, 48, 65)
class Reception:
    @staticmethod
    def enter(player, e):
        player.dir, player.face_dir, player.action = 1, 1, 6
        player.frame = 0
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12


    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image_reception.clip_draw(int(player.frame) * 32, 0, 32, 43, player.x, player.y, 48, 65)
        else:
            player.image_reception.clip_composite_draw(int(player.frame) * 32, 0, 32, 50,
                                              0, 'h', player.x , player.y, 48, 65)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {D_down: Run, A_down: Run, D_up:  Idle, A_up:  Idle,
                   W_down: Run, S_down: Run, W_up:  Idle, S_up:  Idle,
                   space_down: Jump, K_down: Reception},
            Run: {D_down: Idle, A_down: Idle, D_up: Idle, A_up: Idle,
                  W_down: Idle, S_down: Idle, W_up: Idle, S_up: Idle,
                  space_down: Jump, K_down: Reception},
            Jump: {time_out: Idle},
            Reception: {D_down: Run, A_down: Run, D_up:  Idle, A_up:  Idle,
                   W_down: Run, S_down: Run, W_up:  Idle, S_up:  Idle,
                   space_down: Jump}
        }

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.player)


class Player:
    def __init__(self):
        self.x, self.y = 400, 40
        self.frame = 0
        self.action = 2 #1:왼쪽 2:오른쪽 3:위 4:아래 5:점프
        self.dir = 0
        self.face_dir = 1  # 얼굴이 바라보는 방향 1오른쪾 -1왼쪽
        self.image_idle = load_image('./player/playerIdle.png') # 384 x 43
        self.image_run = load_image('./player/playerRun.png') # 384 x 43
        self.image_jump = load_image('./player/playerSmash.png') # 416 x 50
        self.image_block = load_image('./player/playerBlock.png') # 416 x 46
        self.image_reception = load_image('./player/playerReception.png') # 352 x 43
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        # self.font.draw(self.x - 10, self.y + 50, f'{self.ball_count:02d}', (255, 255, 0))
        # # 디버그용 바운딩박스 그리기
        draw_rectangle(*self.get_bb())  # 튜플을 풀어헤쳐서 인자로 전달.

    def get_bb(self):
        return self.x - 20, self.y - 30, self.x + 20, self.y + 30  # 튜플

    def handle_collision(self, group, other):
        pass
        # if group == 'boy:ball':  # 아... 볼과 충돌했구나...
        #     self.ball_count += 1
        # if group == 'boy:zombie':
        #     exit(1)

    def fire_ball(self):
        ball = Ball(self.x, self.y + 5, self.face_dir * 10)
        game_world.add_objects(ball, 0)

        if self.face_dir == -1:  # 왼쪽
            print('FIRE BALL to LEFT')
        elif self.face_dir == 1:  # 오른쪽
            print('FIRE BALL to RIGHT')
