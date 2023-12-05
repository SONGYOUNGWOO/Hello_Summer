# 이것은 각 상태들을 객체로 구현한 것임.
from pico2d import (get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_w, SDLK_a,
                    SDLK_s, SDLK_d, SDLK_k, SDLK_p, SDLK_i, SDLK_o,SDLK_m, SDLK_u, draw_rectangle, clamp, load_wav)
from ball import Ball
import game_world
import game_framework
import play_mode
import random
import math
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

global win_w, win_h
win_w, win_h = 1000, 600

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
        player.face_dir = '오른쪽'
        player.dir = 1


    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12
        player.x += RUN_SPEED_PPS * game_framework.frame_time
        player.x = clamp(20, player.x, win_w - 10)
        player.y = clamp(50, player.y, win_h / 3)
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
        player.face_dir = '오른쪽'
        player.dir = 1
        # if player.face_dir == '오른쪽' :
        #     player.dir = 1
        # else :
        #     player.dir = -1
        # pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12
        player.x += RUN_SPEED_PPS * game_framework.frame_time * 0.8
        player.y += RUN_SPEED_PPS * game_framework.frame_time * 0.8
        player.x = clamp(20, player.x, win_w - 10)
        player.y = clamp(50, player.y, win_h / 3)
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
        player.face_dir = '오른쪽'
        player.dir = 1
        # if player.face_dir == '오른쪽' :
        #     player.dir = 1
        # # else :
        #     player.dir = -1
        # pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12
        player.x += RUN_SPEED_PPS * game_framework.frame_time * 0.8
        player.y -= RUN_SPEED_PPS * game_framework.frame_time * 0.8
        player.x = clamp(20, player.x, win_w - 10)
        player.y = clamp(50, player.y, win_h / 3)
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
        player.face_dir = '왼쪽'
        player.dir = -1
        #
        # if player.face_dir == '오른쪽' :
        #     player.dir = 1
        # else :
        #     player.dir = -1
        # pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12
        player.x -= RUN_SPEED_PPS * game_framework.frame_time
        player.x = clamp(20, player.x, win_w - 10)
        player.y = clamp(50, player.y, win_h / 3)
        pass

    @staticmethod
    def draw(player):
        if player.face_dir == '오른쪽':
            Player.image_run.clip_composite_draw(int(player.frame) * 32, 0, 32, 43, player.x, player.y, 48, 65)
        else:
            Player.image_run.clip_composite_draw(int(player.frame) * 32, 0, 32, 43, 0, 'h',
                                                 player.x, player.y, 48, 65)



class RunLeftUp:
    @staticmethod
    def enter(player, e):
        player.face_dir = '왼쪽'
        player.dir = -1
        # if player.face_dir == '오른쪽' :
        #     player.dir = 1
        # else :
        #     player.dir = -1
        # pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12
        player.x -= RUN_SPEED_PPS * game_framework.frame_time * 0.8
        player.y += RUN_SPEED_PPS * game_framework.frame_time * 0.8
        player.x = clamp(20, player.x, win_w - 10)
        player.y = clamp(50, player.y, win_h / 3)


    @staticmethod
    def draw(player):
        if player.face_dir == '오른쪽':
            Player.image_run.clip_composite_draw(int(player.frame) * 32, 0, 32, 43, player.x, player.y, 48, 65)
        else:
            Player.image_run.clip_composite_draw(int(player.frame) * 32, 0, 32, 43, 0, 'h',
                                                 player.x, player.y, 48, 65)




class RunLeftDown:
    @staticmethod
    def enter(player, e):
        player.face_dir = '왼쪽'
        player.dir = -1
        # if player.face_dir == '오른쪽' :
        #     player.dir = 1
        # else :


    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12
        player.x -= RUN_SPEED_PPS * game_framework.frame_time * 0.8
        player.y -= RUN_SPEED_PPS * game_framework.frame_time * 0.8

        player.x = clamp(20, player.x, win_w - 10)
        player.y = clamp(50, player.y, win_h / 3)


    @staticmethod
    def draw(player):
        if player.face_dir == '오른쪽':
            Player.image_run.clip_composite_draw(int(player.frame) * 32,0, 32, 43, player.x, player.y, 48, 65)
        else:
            Player.image_run.clip_composite_draw(int(player.frame) * 32, 0, 32, 43, 0, 'h',
                                                 player.x, player.y, 48, 65)



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

        player.x = clamp(20, player.x, win_w - 10)
        player.y = clamp(50, player.y, win_h /3)
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

        player.x = clamp(20, player.x, win_w - 10)
        player.y = clamp(50, player.y, win_h / 3)
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
        player.shadow_y = player.y -35
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
        #player.jump_sound.play()
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 13
        player.y += RUN_SPEED_PPS * game_framework.frame_time * 3
        if get_time() - player.wait_time > 0.2:  # 시간으로 속도 조정
            player.y -= (RUN_SPEED_PPS * game_framework.frame_time) * 6
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
        if player.face_dir == '오른쪽':
            player.dir = 1
        else:
            player.dir = -1


    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 15
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time * 2
        if get_time() - player.wait_time > 0.3:  # 시간으로 속도 조정
            player.state_machine.handle_event(('TIME_OUT', 0))

        player.y = max(0, min(player.y, win_h / 3))
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
        player.shadow_y = player.y -35
        player.action = '스매쉬'
        if player.face_dir == '오른쪽':
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

            player.smash_sound.play()
            player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 13
            player.y += RUN_SPEED_PPS * game_framework.frame_time * 3
            if get_time() - player.wait_time > 0.3:  # 시간으로 속도 조정
                player.y -= (RUN_SPEED_PPS * game_framework.frame_time) * 6
            if get_time() - player.wait_time > 0.6:
                player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        if player.face_dir == '오른쪽':
            Player.image_smash.clip_draw(int(player.frame) * 32, 0, 32, 50, player.x, player.y, 48, 75)
        else:
            Player.image_smash.clip_composite_draw(int(player.frame) * 32, 0, 32, 50,
                                                   0, 'h', player.x, player.y, 48, 75)
# class RandomMove:
#     @staticmethod
#     def enter(player, e):
#         player.target_x = random.randint(int(win_w/2 + 100), int(win_w - 80))
#         player.target_y = random.randint(100, int(win_h/4))
#
#     @staticmethod
#     def do(player):
#         # target_x, target_y로 이동하는 로직 구현
#         pass
#
#     @staticmethod
#     def exit(player, e):
#         pass
#
#     @staticmethod
#     def draw(player):
#         # 필요한 그리기 로직 (있을 경우)
#         pass

class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.state_duration = 2

        self.transitions = {
            Idle: {D_down: RunRight, A_down: RunLeft, A_up: RunRight, D_up: RunLeft, W_down: RunUp,
                   S_down: RunDown, W_up: RunDown, S_up: RunUp,I_down: Slide,
                   space_down: Jump, P_down: Reception, O_down: Smash,U_down: self.player.change_character },
            RunRight: {D_up: Idle, A_down: Idle, A_up: Idle, W_down: RunRightUp, W_up: RunRightDown,
                       S_down: RunRightDown, S_up: RunRightUp,space_down: Jump,
                       P_down: Reception, U_down:self.player.change_character},
            RunDown: {S_up: Idle, A_down: RunLeftDown, W_down: Idle, D_down: RunRightDown,
                      A_up: RunRightDown, D_up: RunLeftDown, space_down: Jump,
                      P_down: Reception, U_down: self.player.change_character},
            RunLeft: {A_up: Idle, W_down: RunLeftUp, D_down: Idle, D_up: Idle, S_down: RunLeftDown,
                      W_up: RunLeftDown, S_up: RunLeftUp,
                      space_down: Jump, P_down: Reception, U_down: self.player.change_character},
            RunUp: {W_up: Idle, A_down: RunLeftUp, D_down: RunRightUp,
                    A_up: RunRightUp, D_up: RunLeftUp},
            RunRightUp: {W_up: RunRight, D_up: RunUp, A_down: RunUp, S_down: RunRight},
            RunLeftUp: {D_down: RunUp, S_down: RunLeft, A_up: RunUp, W_up: RunLeft},
            RunLeftDown: {A_up: RunDown, S_up: RunLeft, W_down: RunLeft, D_down: RunDown,
                          space_down: Jump, P_down: Reception, U_down:self.player.change_character},
            RunRightDown: {D_up: RunDown, S_up: RunRight, A_down: RunDown, W_down: RunRight
                           ,space_down: Jump, P_down: Reception, U_down:self.player.change_character},
            Jump: {time_out: Idle, },
            Reception: {D_down: RunRight, A_down: RunLeft, D_up: Idle, A_up: Idle,
                        W_down: RunUp, S_down: RunDown, W_up: Idle, S_up: Idle,
                        space_down: Jump, time_out: Idle, O_down: Smash},
            Slide: {time_out: Idle, },
            Smash: {time_out: Idle, }
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
            # "Smash" : Smash,
            "Jump" : Jump
        }.get(state_name, Idle)

    def change_state(self):
        # Idle 상태에서 다음 상태를 무작위로 선택
        if self.cur_state == Idle:
            next_state = random.choice([RunUp, RunDown,  Jump])
        # RunUp 상태에서 다음 상태 결정
        elif self.cur_state == RunUp:
            next_state = random.choice([RunDown,  Jump])
        # RunDown 상태에서 다음 상태 결정
        elif self.cur_state == RunDown:
            next_state = random.choice([RunUp,  Jump])
        # 다른 상태에서는 Idle로 전환
        else:
            next_state = Idle

        # 상태 전환 수행
        self.cur_state.exit(self.player, None)
        self.cur_state = next_state
        self.cur_state.enter(self.player, None)

    # def change_state(self):
    #     if self.cur_state == RunUp:
    #         if self.cur_state == RunUp:
    #             if self.cur_state == Idle:
    #                 next_state = random.choice([RunDown, Smash, Jump])
    #         else:
    #             # 그렇지 않은 경우 RunUp과 RunDown을 번갈아 선택
    #             if self.cur_state == Idle:
    #                 next_state = RunDown if self.cur_state == RunDown else RunUp
    #     else:
    #         if self.cur_state == RunDown:
    #             if self.cur_state == Idle:
    #                 next_state = random.choice([RunUp, Smash, Jump])
    #         else:
    #             # 그렇지 않은 경우 RunUp과 RunDown을 번갈아 선택
    #             if self.cur_state == Idle:
    #                 next_state = RunUp if self.cur_state == RunUp else RunDown
    #
    #     self.cur_state.exit(self.player, None)
    #     self.cur_state = next_state
    #     self.cur_state.enter(self.player, None)


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
    smash_sound = None
    image_idle = None
    image_run = None
    image_jump = None
    image_block = None
    image_reception = None
    image_slide = None
    image_smash = None
    image_shadow1 = None
    jump_sound = None


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
            Player.image_run = load_image('./player/playerRun.png')  # 384 x 43
            Player.image_jump = load_image('./player/playerSmash.png')  # 416 x 50
            Player.image_block = load_image('./player/playerBlock.png')  # 416 x 46
            Player.image_reception = load_image('./player/playerReception.png')  # 352 x 43 , 11, 32
            Player.image_slide = load_image('./player/playerSlide.png')  # 645 x 43 , 15, 43
            Player.image_smash = load_image('./player/playerSmash.png')  # 416 x 50 , 13, 32
            Player.image_shadow1 = load_image('./player/shadow1.png')  # 23 x 10
            Player.smash_sound = load_wav('./sound/smashs.wav')  # 동시에 여러 음악 재생시 wav로 진행
            Player.smash_sound.set_volume(24)
            Player.jump_sound = load_wav('./sound/jump.wav')  # 동시에 여러 음악 재생시 wav로 진행
            Player.jump_sound.set_volume(12)


    def update(self):
        if self in play_mode.enemy_team:
            self.state_machine.update()
            self.x = clamp(win_w / 2 + 10, self.x, win_w - 10)
            # self.y = clamp(50, self.y, win_h/3)
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
            self.image_shadow1.clip_draw(0,0,23,10,self.x,  self.shadow_y ,22,10)  # 그림자의 위치를 플레이어 아래로 조정
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

    def change_character(self):
        # 현재 캐릭터를 Idle 상태로 설정
        self.state_machine.cur_state.exit(self, None)
        self.state_machine.cur_state = Idle
        self.state_machine.cur_state.enter(self, None)

        # 다음 캐릭터로 변경
        play_mode.switch_to_next_character()

    # def is_near_net(play_mode.enemy_team):
    #     if enemy_team[0]< enemy_team[1]:
    #         return  player[0]
    #
    #
    # # 행동 트리 노드 정의
    # class BtSmash(Action):
    #     def __init__(self, player):
    #         super().__init__()
    #         self.player = player
    #
    #     def run(self):
    #         # 원래 Smash 클래스의 동작을 수행
    #         result = self.player.perform_smash()  # 가상의 메소드, 실제 구현 필요
    #         return BehaviorTree.SUCCESS if result else BehaviorTree.FAIL
    #
    # class BtSlide(Action):
    #     def __init__(self, player):
    #         super().__init__()
    #         self.player = player
    #
    #     def run(self):
    #         # 원래 Slide 클래스의 동작을 수행
    #         result = self.player.perform_slide()  # 가상의 메소드, 실제 구현 필요
    #         return BehaviorTree.SUCCESS if result else BehaviorTree.FAIL
    # class MoveRandomly(Action):
    #     def run(self):
    #         # 무작위로 이동하는 행동 구현
    #         pass
    #
    # # 조건 노드 정의
    # class NearNet(Condition):
    #     def run(self):
    #         return is_near_net(play_mode.enemy_team, net)
    #
    # # 행동 트리 구성
    # def build_behavior_tree(player):
    #     root = Selector(name="Root")
    #     spike_sequence = Sequence(name="Spike Sequence")
    #     move_sequence = Sequence(name="Move Sequence")
    #
    #     spike_sequence.add_children(NearNet(player), Spike(player))
    #     move_sequence.add_children(Slide(player), MoveRandomly(player))
    #
    #     root.add_children(spike_sequence, move_sequence)
    #     return BehaviorTree(root)
