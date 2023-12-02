# 이것은 각 상태들을 객체로 구현한 것임.
from pico2d import (get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_w, SDLK_a,
                    SDLK_s, SDLK_d, SDLK_k, SDLK_p, SDLK_i, SDLK_o,SDLK_m, SDLK_u, draw_rectangle, clamp)
from ball import Ball
import game_world
import game_framework
import play_mode
import random
import math
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

global win_w, win_h
win_w, win_h = 1000, 700

# state event check
# ( state event type, event value )
def D_down(e):  # 오른쪽
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d

def D_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d

def A_down(e):  # 왼쪽
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def A_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a

def W_down(e):  # 위
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w

def W_up(e):  # 위
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w

def S_down(e):  # 아래
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s

def S_up(e):  # 아래
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def space_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_SPACE
def K_down(e):  # 아래
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_k

def P_down(e):  # 리시브
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_p

def I_down(e):  # 슬라이드
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_i

def O_down(e):  # 스매쉬
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_o

def M_down(e): #bb on off
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_m

def U_down(e):  # 캐릭터 선택
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_u

def time_out(e):
    return e[0] == 'TIME_OUT'


# player Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 25.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 13


# time_out = lambda e : e[0] == 'TIME_OUT'
class Idle:
    @staticmethod
    def enter(player, e):

        if player.face_dir == '왼쪽':
            player.action = '좌'
            player.dir = -1
        elif player.face_dir == '오른쪽':
            player.action = '우'
            player.dir = 1

        player.dir = 0
        player.frame = 0
        player.wait_time = get_time()  # pico2d import 필요
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12
        if get_time() - player.wait_time > 2:
            player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        if player.face_dir == '오른쪽':
            Player.image_idle.clip_draw(int(player.frame) * 32, 0, 32, 43, player.x, player.y, 48, 65)
        else:
            Player.image_idle.clip_composite_draw(int(player.frame) * 32, 0, 32, 43,
                                                  0, 'h', player.x, player.y, 48, 65)
class RunRight:
    @staticmethod
    def enter(player, e):

        if player.face_dir == '오른쪽' :
            player.dir = 1
        else :
            player.dir = -1
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12
        player.x += RUN_SPEED_PPS * game_framework.frame_time
        player.x = clamp(10, player.x, win_w - 10)
        player.y = clamp(25, player.y, win_h - win_h / 3.3)
        pass

    @staticmethod
    def draw(player):
        if player.face_dir == '오른쪽':
            Player.image_run.clip_draw(int(player.frame) * 32, 0, 32, 43, player.x, player.y, 48, 65)
        else:
            Player.image_run.clip_composite_draw(int(player.frame) * 32,0, 32, 43, 0, 'h', player.x, player.y, 48, 65)


class RunRightUp:
    @staticmethod
    def enter(player, e):

        if player.face_dir == '오른쪽' :
            player.dir = 1
        else :
            player.dir = -1
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12
        player.x += RUN_SPEED_PPS * game_framework.frame_time * 0.8
        player.y += RUN_SPEED_PPS * game_framework.frame_time * 0.8
        player.x = clamp(10, player.x, win_w - 10)
        player.y = clamp(25, player.y, win_h - win_h / 3.3)
        pass

    @staticmethod
    def draw(player):
        if player.face_dir == '오른쪽':
            Player.image_run.clip_draw(int(player.frame) * 32, 0, 32, 43, player.x, player.y, 48, 65)
        else:
            Player.image_run.clip_composite_draw(int(player.frame) * 32,0, 32, 43, 0, 'h', player.x, player.y, 48, 65)



class RunRightDown:
    @staticmethod
    def enter(player, e):

        if player.face_dir == '오른쪽' :
            player.dir = 1
        else :
            player.dir = -1
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12
        player.x += RUN_SPEED_PPS * game_framework.frame_time * 0.8
        player.y -= RUN_SPEED_PPS * game_framework.frame_time * 0.8
        player.x = clamp(10, player.x, win_w - 10)
        player.y = clamp(25, player.y, win_h - win_h / 3.3)
        pass

    @staticmethod
    def draw(player):
        if player.face_dir == '오른쪽':
            Player.image_run.clip_draw(int(player.frame) * 32, 0, 32, 43, player.x, player.y, 48, 65)
        else:
            Player.image_run.clip_composite_draw(int(player.frame) * 32,0, 32, 43, 0, 'h', player.x, player.y, 48, 65)



class RunLeft:
    @staticmethod
    def enter(player, e):

        if player.face_dir == '오른쪽' :
            player.dir = 1
        else :
            player.dir = -1
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12
        player.x -= RUN_SPEED_PPS * game_framework.frame_time
        player.x = clamp(10, player.x, win_w - 10)
        player.y = clamp(25, player.y, win_h - win_h / 3.3)
        pass

    @staticmethod
    def draw(player):
        if player.face_dir == '오른쪽':
            Player.image_run.clip_composite_draw(int(player.frame) * 32, 0, 32, 43, 0, 'h',
                                                 player.x, player.y, 48, 65)
        else:
            Player.image_run.clip_composite_draw(int(player.frame) * 32,0, 32, 43, player.x, player.y, 48, 65)


class RunLeftUp:
    @staticmethod
    def enter(player, e):

        if player.face_dir == '오른쪽' :
            player.dir = 1
        else :
            player.dir = -1
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12
        player.x -= RUN_SPEED_PPS * game_framework.frame_time * 0.8
        player.y += RUN_SPEED_PPS * game_framework.frame_time * 0.8
        player.x = clamp(10, player.x, win_w - 10)
        player.y = clamp(25, player.y, win_h - win_h / 3.3)


    @staticmethod
    def draw(player):
        if player.face_dir == '오른쪽':
            Player.image_run.clip_composite_draw(int(player.frame) * 32, 0, 32, 43, 0, 'h',
                                                 player.x, player.y, 48, 65)
        else:
            Player.image_run.clip_composite_draw(int(player.frame) * 32,0, 32, 43, player.x, player.y, 48, 65)



class RunLeftDown:
    @staticmethod
    def enter(player, e):

        if player.face_dir == '오른쪽' :
            player.dir = 1
        else :
            player.dir = -1
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12
        player.x -= RUN_SPEED_PPS * game_framework.frame_time * 0.8
        player.y -= RUN_SPEED_PPS * game_framework.frame_time * 0.8

        player.x = clamp(10, player.x, win_w - 10)
        player.y = clamp(25, player.y, win_h - win_h / 3.3)


    @staticmethod
    def draw(player):
        if player.face_dir == '오른쪽':
            Player.image_run.clip_composite_draw(int(player.frame) * 32, 0, 32, 43, 0, 'h',
                                                 player.x, player.y, 48, 65)
        else:
            Player.image_run.clip_composite_draw(int(player.frame) * 32,0, 32, 43, player.x, player.y, 48, 65)



class RunUp:
    @staticmethod
    def enter(player, e):

        if player.face_dir == '오른쪽' :
            player.dir = 1
        else :
            player.dir = -1
        pass


    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12
        player.y += RUN_SPEED_PPS * game_framework.frame_time

        player.x = clamp(10, player.x, win_w - 10)
        player.y = clamp(25, player.y, win_h - win_h / 3.3)
        pass

    @staticmethod
    def draw(player):
        if player.face_dir == '오른쪽':
            Player.image_run.clip_draw(int(player.frame) * 32, 0, 32, 43, player.x, player.y, 48, 65)
        else:
            Player.image_run.clip_composite_draw(int(player.frame) * 32,0, 32, 43,
                                                   0, 'h', player.x, player.y, 48, 65)


class RunDown:
    @staticmethod
    def enter(player, e):
        if player.face_dir == '오른쪽' :
            player.dir = 1
        else :
            player.dir = -1
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12
        player.y -= RUN_SPEED_PPS * game_framework.frame_time

        player.x = clamp(10, player.x, win_w - 10)
        player.y = clamp(25, player.y, win_h - win_h / 3.3)
        pass

    @staticmethod
    def draw(player):
        if player.face_dir == '오른쪽':
            Player.image_run.clip_draw(int(player.frame) * 32, 0, 32, 43, player.x, player.y, 48, 65)
        else:
            Player.image_run.clip_composite_draw(int(player.frame) * 32,0, 32, 43,
                                                   0, 'h', player.x, player.y, 48, 65)

class Jump:
    @staticmethod
    def enter(player, e):
        player.shadow_y = player.y - 35
        player.action = '점프'
        if player.face_dir == '오른쪽' :
            player.dir = 1
        else :
            player.dir = -1
        player.frame = 0

        player.wait_time = get_time()  # pico2d import 필요
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 13
        player.y += player.dir * RUN_SPEED_PPS * game_framework.frame_time * 3
        if get_time() - player.wait_time > 0.2:  # 시간으로 속도 조정
            player.y -= (player.dir * RUN_SPEED_PPS * game_framework.frame_time) * 6
        if get_time() - player.wait_time > 0.4:
            player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        if player.face_dir == '오른쪽':
            Player.image_block.clip_draw(32 * 7, 0, 32, 46, player.x, player.y, 48, 65)
        else:
            Player.image_block.clip_composite_draw(32 * 7, 0, 32, 46,
                                                   0, 'h', player.x, player.y, 48, 65)

class Reception:  # 352 x 43 , 11, 32
    @staticmethod
    def enter(player, e):
        player.action = '리시브'
        player.frame = 0
        player.wait_time = get_time()  # pico2d import 필요

        if player.face_dir == '오른쪽' :
            player.dir = 1
        else :
            player.dir = -1
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 11
        if get_time() - player.wait_time > 0.5:  # 시간으로 속도 조정
            player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        if player.face_dir == '오른쪽':
            Player.image_reception.clip_draw(int(player.frame) * 32, 0, 32, 43, player.x, player.y, 48, 65)
        else:
            Player.image_reception.clip_composite_draw(int(player.frame) * 32, 0, 32, 43,
                                                       0, 'h', player.x, player.y, 48, 65)

class Slide:  # 352 x 43 , 11, 32
    @staticmethod
    def enter(player, e):
        player.action = '슬라이드'
        player.frame = 0
        player.wait_time = get_time()  # pico2d import 필요

        if player.face_dir == '오른쪽' :
            player.dir = 1
        else :
            player.dir = -1
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 15
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time * 2
        if get_time() - player.wait_time > 0.3:  # 시간으로 속도 조정
            player.state_machine.handle_event(('TIME_OUT', 0))

        player.y = max(0, min(player.y, win_h - win_h / 3.3))
        player.x = max(10, min(player.x, win_w / 2 - 40))

    @staticmethod
    def draw(player):
        if player.face_dir == '오른쪽':
            Player.image_slide.clip_draw(int(player.frame) * 43, 0, 43, 43, player.x, player.y, 64, 65)
        else:
            Player.image_slide.clip_composite_draw(int(player.frame) * 43, 0, 43, 43,
                                                   0, 'h', player.x, player.y, 64, 65)

class Smash:
    @staticmethod
    def enter(player, e):
        player.shadow_y = player.y - 35
        player.action = '스매쉬'
        if player.face_dir == '오른쪽' :
            player.dir = 1
        else :
            player.dir = -1
        player.frame = 0

        player.wait_time = get_time()  # pico2d import 필요



    @staticmethod
    def exit(player, e):
        play_mode.ball_mode = 'smash'
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 13
        player.y += player.dir * RUN_SPEED_PPS * game_framework.frame_time * 3
        if get_time() - player.wait_time > 0.3:  # 시간으로 속도 조정
            player.y -= (player.dir * RUN_SPEED_PPS * game_framework.frame_time) * 6
        if get_time() - player.wait_time > 0.6:
            player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        if player.face_dir == '오른쪽':
            Player.image_smash.clip_draw(int(player.frame) * 32, 0, 32, 50, player.x, player.y, 48, 75)
        else:
            Player.image_smash.clip_composite_draw(int(player.frame) * 32, 0, 32, 50,
                                                   0, 'h', player.x, player.y, 48, 75)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.state_duration = 2

        self.transitions = {
            Idle: {D_down: RunRight, A_down: RunLeft, A_up: RunRight, D_up: RunLeft, W_down: RunUp,
                   S_down: RunDown, W_up: RunDown, S_up: RunUp,
                   space_down: Jump, P_down: Reception, O_down: Smash},
            RunRight: {D_up: Idle, A_down: Idle, W_down: RunRightUp, W_up: RunRightDown,
                       S_down: RunRightDown, S_up: RunRightUp,space_down: Jump,
                       P_down: Reception, I_down: Slide, O_down: Smash},
            RunRightUp: {W_up: RunRight, D_up: RunUp, A_down: RunUp, S_down: RunRight,
                         space_down: Jump, P_down: Reception, I_down: Slide, O_down: Smash},
            RunUp: {W_up: Idle, A_down: RunLeftUp, S_down: Idle, D_down: RunRightUp,
                    A_up: RunRightUp, D_up: RunLeftUp, space_down: Jump, P_down: Reception, I_down: Slide, O_down: Smash},
            RunLeftUp: {D_down: RunUp, S_down: RunLeft, A_up: RunUp, W_up: RunLeft,
                        space_down: Jump, P_down: Reception, I_down: Slide, O_down: Smash},
            RunLeft: {A_up: Idle, W_down: RunLeftUp, D_down: Idle, S_down: RunLeftDown,
                      W_up: RunLeftDown, S_up: RunLeftUp,
                      space_down: Jump, P_down: Reception, I_down: Slide, O_down: Smash},
            RunLeftDown: {A_up: RunDown, S_up: RunLeft, W_down: RunLeft, D_down: RunDown,
                          space_down: Jump, P_down: Reception, I_down: Slide, O_down: Smash},
            RunDown: {S_up: Idle, A_down: RunLeftDown, W_down: Idle, D_down: RunRightDown,
                      A_up: RunRightDown, D_up: RunLeftDown,space_down: Jump, P_down: Reception, I_down: Slide, O_down: Smash},
            RunRightDown: {D_up: RunDown, S_up: RunRight, A_down: RunDown, W_down: RunRight
                           ,space_down: Jump, P_down: Reception, I_down: Slide, O_down: Smash},
            Jump: {time_out: Idle},
            Reception: {D_down: RunRight, A_down: RunLeft, D_up: Idle, A_up: Idle,
                        W_down: RunUp, S_down: RunDown, W_up: Idle, S_up: Idle,
                        space_down: Jump, time_out: Idle, O_down: Smash},
            Slide: {time_out: Idle},
            Smash: {time_out: Idle}
        }

    def start(self, initial_state_name="Idle"):
        initial_state = self.get_state_by_name(initial_state_name)
        self.cur_state = initial_state
        self.cur_state.enter(self.player, ('NONE', 0))
        self.last_state_change = get_time()

    def update(self):
        self.cur_state.do(self.player)

        if self.player in play_mode.enemy_team:
            if get_time() - self.last_state_change > self.state_duration:
                self.change_state()
                self.last_state_change = get_time()

    def get_state_by_name(self, state_name):
        return {
            "Idle": Idle,
            "RunUp": RunUp,
            "RunDown": RunDown,
            # 기타 상태 이름과 클래스 매핑...
        }.get(state_name, Idle)

    def change_state(self):
        if self.cur_state == RunUp:
            next_state = RunDown
        else:
            next_state = RunUp
        self.cur_state.exit(self.player, None)
        self.cur_state = next_state
        self.cur_state.enter(self.player, None)


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
    image_idle = None
    image_run = None
    image_jump = None
    image_block = None
    image_reception = None
    image_slide = None
    image_smash = None
    image_shadow0 = None


    def __init__(self, x = 50, y = win_h / 2.6 , initial_state_name="Idle"):
        self.x, self.y = x, y
        self.frame = 0
        self.action = '우'
        self.dir = 0
        self.face_dir = '오른쪽'
        self.current_state = None  # 현재 상태를 저장하는 변수
        self.state_machine = StateMachine(self)
        self.state_machine.start(initial_state_name)
        self.state_machine.last_state_change = get_time()  # 마지막 상태 변경 시간 초기화
        self.shadow_y = self.y - 35

        self.tx, self.ty = 100, 100
        self.difp = None
        # self.build_behavior_tree()

        if Player.image_idle == None:
            Player.image_idle = load_image('./player/playerIdle.png')  # 384 x 43
        if Player.image_run == None:
            Player.image_run = load_image('./player/playerRun.png')  # 384 x 43
        if Player.image_jump == None:
            Player.image_jump = load_image('./player/playerSmash.png')  # 416 x 50
        if Player.image_block == None:
            Player.image_block = load_image('./player/playerBlock.png')  # 416 x 46
        if Player.image_reception == None:
            Player.image_reception = load_image('./player/playerReception.png')  # 352 x 43 , 11, 32
        if Player.image_slide == None:
            Player.image_slide = load_image('./player/playerSlide.png')  # 645 x 43 , 15, 43
        if Player.image_smash == None:
            Player.image_smash = load_image('./player/playerSmash.png')  # 416 x 50 , 13, 32
        if Player.image_shadow0 == None:
            Player.image_shadow0 = load_image('./player/shadow0.png')  # 23 x 10



    def update(self):
        if self in play_mode.enemy_team:
            self.state_machine.update()
            self.x = clamp(win_w / 2 + 10, self.x, win_w - 10)
            self.y = clamp(50, self.y, win_h/2 + 50)
        else:
            # 일반 플레이어 업데이트 로직
            self.state_machine.update()
        # if play_mode.player_slect != self:
        #     self.bt.run()

    def handle_event(self, event):
        # if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
        #     self.shadow_y = self.y - 35  # 점프 시작 Y 좌표 업데이트

        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        if self.state_machine.cur_state == Jump or self.state_machine.cur_state == Smash:
            self.image_shadow0.clip_draw(0,0,23,10,self.x,  self.shadow_y ,22,10)  # 그림자의 위치를 플레이어 아래로 조정
        # self.font.draw(self.x - 10, self.y + 50, f'{self.ball_count:02d}', (255, 255, 0))
        # # 디버그용 바운딩박스 그리기
        draw_rectangle(*self.get_bb())  # 튜플을 풀어헤쳐서 인자로 전달.

    def get_bb(self):
        return self.x - 20, self.y - 30, self.x + 20, self.y + 30  # 튜플

    def handle_collision(self, group, other):
        if group == 'player:net':
            if other.x > self.x:
                self.x = clamp(0, self.x, other.x - 20)
            else:
                self.x = clamp(other.x + 20, self.x, win_w)
            # self.x -= self.dir * RUN_SPEED_PPS * game_framework.frame_time
        # if group == 'player:ball':  # 아... 볼과 충돌했구나...
        #     self.ball_count += 1
        # if group == 'player:zombie':
        #     exit(1)


    def set_target_location(self, x=None, y=None):
        if not x or not y :
            raise ValueError('위치를 지정을 해야 합니다.')
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS
        pass

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2)**2 + (y1 - y2)**2
        return distance2 < (r * PIXEL_PER_METER) ** 2
        pass

    # dir = radian
    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

    #조금씩 움직이면서 기준 안쪽으로 들어오면
    def move_to(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING


    def set_random_location(self):
        self.tx, self.ty = random.randint(100,1000-100), random.randint(100, 800-100)
        pass

    def is_boy_nearby(self, r):
        if self.distance_less_than(play_mode.boy.x, play_mode.boy.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass

    def move_to_boy(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(play_mode.boy.x, play_mode.boy.y)
        if self.distance_less_than(play_mode.boy.x, play_mode.boy.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def run_away_to_boy(self, r=0.5):
        self.state = 'Walk'

        # 소년과 좀비 사이의 (방향)을 계산
        dx = self.x - play_mode.boy.x
        dy = self.y - play_mode.boy.y

        # 도망칠 위치 설정 (현재 좀비 위치에서 소년과의 차이만큼 더 이동)
        escape_x = self.x + dx
        escape_y = self.y + dy

        # 도망칠 위치로 이동
        self.move_slightly_to(escape_x, escape_y)

        # 소년과의 거리가 충분히 멀어졌는지 체크
        if self.distance_less_than(play_mode.boy.x, play_mode.boy.y, self.x, self.y, r) > 7:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING


    def get_patrol_location(self):
        self.tx, self.ty = self.patrol_locations[self.loc_no]
        self.loc_no = (self.loc_no + 1) % len(self.patrol_locations)
        return BehaviorTree.SUCCESS
        pass

    def is_player_substitution(self):
        if play_mode.player_slect != self:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_ball_ground(self):
        if play_mode.ball.y == 10:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL


    def move_relatively(self):
        self.sp_w, self.sp_h = win_w/4, win_w/4
        if self.difp == None :
            for player in play_mode.players:
                if player != self:
                    self.difp = player

    def next_round(self):
        return BehaviorTree.SUCCESS

    def close_to_the_ball(self):
        p1x, p1y =  play_mode.player[0].x,  play_mode.player[0].y
        p2x, p2y =  play_mode.player[1].x,  play_mode.player[1].y
        ball_x, ball_y = play_mode.ball.x, play_mode.ball.y

        distance_to_p1 = math.sqrt((ball_x - p1x) ** 2 + (ball_y - p1y) ** 2)
        distance_to_p2 = math.sqrt((ball_x - p2x) ** 2 + (ball_y - p2y) ** 2)

        if distance_to_p1 < distance_to_p2:
            return play_mode.player[0]
        elif distance_to_p2 < distance_to_p1:
            return play_mode.player[1]
        else: #거리가 같음
            return play_mode.player[0]

    def is_ball_net_over(self):
        if play_mode.ball.x > win_w/2: #우측 라인
            return BehaviorTree.SUCCESS

    def jump_spike(self):
        # 벽에 가장 가까운 플레이어 찾기
        closest_player = min(play_mode.player, key=lambda p: p.x)

        # 이 플레이어의 StateMachine 상태를 Smash로 설정
        closest_player.state_machine.cur_state = Smash
        closest_player.state_machine.cur_state.enter(closest_player, ('NONE', 0))

        # 공의 위치와 방향 설정
        play_mode.ball.x = closest_player.x
        play_mode.ball.y = closest_player.y + 50  # 플레이어의 높이 위로 설정

        # 공을 상대 진형으로 넘기기 위한 속도 및 방향 설정
        # 예시: 공에 대한 속도와 방향 벡터 설정
        play_mode.ball.velocity_x = 300  # X축 속도
        play_mode.ball.velocity_y = 400  # Y축 속도 (양의 값이면 위로, 음의 값이면 아래로)

        # 스매쉬 동작에 필요한 추가 애니메이션 또는 상태 변화 로직
        # 예: 애니메이션 프레임 설정, 특정 시간 후 상태 변경 등
    def do_serve(self):
        pass




    def build_behavior_tree(self):
        c1 = Condition('공이 땅에 닿았는가?', self.is_ball_ground)
        a1 = Action('다음 라운드', self.next_round)

        SEQ_next_round = Sequence('다음라운드 ', c1, a1)

        c2 = Condition('서브인가?', self.is_ball_net_over)
        SEQ_ATTACK = Sequence('공격',)

        # self.bt = BehaviorTree(root)
