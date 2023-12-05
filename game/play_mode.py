import random

from pico2d import *
import game_framework
import finish_mode
import game_world
from background import Beach
from background import Net
from player import Player
from ball import Ball

win_w ,win_h = 1000, 600
global enemy_score, ally_score
enemy_score = 0
ally_score = 0
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

        elif event.type == SDL_KEYDOWN and event.key == SDLK_r:
            restart_game()
        else:
            player_slect.handle_event(event)
def restart_game():
    global players, enemy_team, ball, player_slect, beach, net

    # 게임 객체들을 제거합니다.
    game_world.clear()

    # 게임 환경을 다시 초기화합니다.
    beach = Beach()
    game_world.add_object(beach, 0)

    net = Net()
    game_world.add_object(net, 0)

    players = [Player(80, 100), Player(win_w/2 - 80, win_h/4)]
    for player in players:
        game_world.add_object(player, 1)
    player_slect = players[0]

    enemy_team = [Player(win_w/2 + 100, win_h/4, "RunUp"),
                  Player(win_w - 80, 100, "RunDown")]
    for player in enemy_team:
        player.face_dir = '왼쪽'
        game_world.add_object(player, 1)

    ball = Ball()
    game_world.add_object(ball, 1)

    # 콜리전 페어를 다시 추가합니다.
    game_world.add_collision_pair('player:net', None, net)
    for player in players:
        game_world.add_collision_pair('player:net', player, None)

    game_world.add_collision_pair('player:ball', None, ball)
    for player in players:
        game_world.add_collision_pair('player:ball', player, None)

    game_world.add_collision_pair('enemy:ball', None, ball)
    for player in enemy_team:
        game_world.add_collision_pair('enemy:ball', player, None)

def init():

    global beach
    global players
    global enemy_team
    global net
    global ball
    global player_slect
    global enemy_score, ally_score
    global n1,n2,n3,n4,n5,n6,n7,n8,n9,n0
    global diamond

    n1 = load_image('./number/1.png')
    n2 = load_image('./number/2.png')
    n3 = load_image('./number/3.png')
    n4 = load_image('./number/4.png')
    n5 = load_image('./number/5.png')
    n6 = load_image('./number/6.png')
    n7 = load_image('./number/7.png')
    n8 = load_image('./number/8.png')
    n9 = load_image('./number/9.png')
    n0 = load_image('./number/0.png')
    diamond = load_image('./player/diamond.png')

    enemy_score = 0
    ally_score = 0

    beach = Beach()
    game_world.add_object(beach, 0)

    net = Net()
    game_world.add_object(net, 0)

    players = [Player(win_w/2- 80,  win_h/4), Player(80, 100)]
    for player in players:
        game_world.add_object(player, 1)
    player_slect = players[0]


    enemy_team = [Player(win_w/2 + 100, win_h/4, "RunUp"),
                  Player(win_w - 150, 100, "RunDown")]
    for player in enemy_team:
        player.face_dir = '왼쪽'  # 모든 적 팀 플레이어를 왼쪽을 바라보도록 설정
        game_world.add_object(player, 1)

    ball = Ball()
    game_world.add_object(ball, 1)

    game_world.add_collision_pair('player:net', None, net)
    for player in players:
        game_world.add_collision_pair('player:net', player, None)
    game_world.add_collision_pair('ball:net', None, net)
    game_world.add_collision_pair('ball:net', ball, None)

    game_world.add_collision_pair('player:ball', None, ball)
    for player in players:
        game_world.add_collision_pair('player:ball', player, None)

    game_world.add_collision_pair('enemy:ball', None, ball)
    for player in enemy_team:
        game_world.add_collision_pair('enemy:ball', player, None)

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

    global enemy_score, ally_score
    #print(ball.y)
    if ball.y <= 100:  # 예: 바닥에 닿는 y값
        if ball.x < win_w / 2:
            enemy_score += 1
        else:
            ally_score += 1
        ball.reset_position()

    if ally_score >= 5 or enemy_score >= 5:
        game_framework.change_mode(finish_mode)

        # fill here
    # for ball in balls.copy():
    #     if game_world.collide(boy, ball):
    #         print('COLLISION boy:Ball')
    #         boy.ball_count += 1     # 소년 관점의 충돌처리
    #         balls.remove(ball)
    #         game_world.remove_object(ball)  # 볼을 제거

def draw_number(x, y, number, scale=0.1):
    global n0, n1, n2, n3, n4, n5, n6, n7, n8, n9
    number_images = [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9]

    digits = [int(i) for i in str(number)]  # 숫자를 각 자리수로 분리
    digit_width = 10 * scale  # 각 숫자 이미지의 조정된 너비
    digit_height = 20 * scale  # 각 숫자 이미지의 조정된 높이

    for i, digit in enumerate(digits):
        number_images[digit].draw(x + i * digit_width, y, digit_width, digit_height)


def draw():
    clear_canvas()
    game_world.render()
    diamond.draw(player_slect.x + 5, player_slect.y + 40, 10, 10)
    draw_number(100, win_h - 50, ally_score, scale=5 )  # 적 점수
    draw_number(win_w - 100, win_h - 50, enemy_score, scale=5)  # 아군 점수
    update_canvas()


def pause():
    pass


def resume():
    pass
