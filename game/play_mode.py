import random

from pico2d import *
import game_framework

import game_world
from background import Beach
from background import Net
from player import Player
from ball import Ball

win_w ,win_h = 1000, 600
# boy = None
def switch_to_next_character():
    global player_slect
    current_index = players.index(player_slect)
    next_index = (current_index + 1) % len(players)
    player_slect = players[next_index]

def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN and event.key == SDLK_u:
            switch_to_next_character()

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

    players = [Player(win_w/2- 80,  win_h/2 ), Player(80, 100)]
    for player in players:
        game_world.add_object(player, 1)
    player_slect = players[0]

    enemy_team = [Player(win_w/2 + 100, win_h/2, "RunUp"),
                  Player(win_w - 80, 100, "RunDown")]
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
