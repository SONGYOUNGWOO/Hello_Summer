import random

from pico2d import *
import game_framework

import game_world
from background import Beach
from background import Net
from player import Player
from ball import Ball

win_w ,win_h = 1000, 700
# boy = None

def handle_events():
    global player_slect
    
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN and event.key == SDLK_u:
            player_slect = players[0] if player_slect == players[1] else players[1]

        else:
            player_slect.handle_event(event)


def init():
    global beach
    global players
    global enemy_team
    global net
    global ball
    global player_slect

    running = True

    beach = Beach()
    game_world.add_object(beach, 0)

    net = Net()
    game_world.add_object(net, 0)

    players = [Player(random.randint(20, win_w/2 - 20), random.randint(100,300)) for _ in range(2)]
    for player in players:
        game_world.add_object(player, 1)
    player_slect = players[0]

    enemy_team = [Player(win_w/2 + 50, win_h/2), Player(win_w - 80, 100)]
    for player in enemy_team:
        player.face_dir = '왼쪽'  # 모든 적 팀 플레이어를 왼쪽을 바라보도록 설정
        game_world.add_object(player, 1)

    ball = Ball()
    game_world.add_object(ball, 1)

    game_world.add_collision_pair('player:net', None, net)
    for player in players:
        game_world.add_collision_pair('player:net', player, None)

    game_world.add_collision_pair('player:ball', None, ball)
    for player in players:
        game_world.add_collision_pair('player:ball', player, None)

    # global balls
    # balls = [Ball(random.randint(0,1600),60,0) for _ in range(50)]
    # game_world.add_objects(balls,1)
    #
    #
    # # 충돌 검사 필요 상황을 등록
    # game_world.add_collision_pair('boy:ball', boy, None)   # 소년을 등록
    # for ball in balls:
    #     game_world.add_collision_pair('boy:ball', None, ball)


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()
    # fill here
    # for ball in balls.copy():
    #     if game_world.collide(boy, ball):
    #         print('COLLISION boy:Ball')
    #         boy.ball_count += 1     # 소년 관점의 충돌처리
    #         balls.remove(ball)
    #         game_world.remove_object(ball)  # 볼을 제거


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass
