# layer 0 : Background Object
# layer 1 : Foreground Object
# 게임 월드에 담겨있는 모든 객체들을 담고 있는 리스트, Drawing Layer에 따라서 분류.
# 필요에 따라 Layer를 추가하면 됨. 현재는 두개의 Layer만
objects = [[] for _ in range(4)]    # 보이는 세계
collision_pairs = {}

def add_collision_pair(group, a = None, b = None):    # a 와 b 사이에 충돌 검사가 필요하다는 점을 등록
    if group not in collision_pairs:
        print(f'New group {group} added....')
        collision_pairs[group] = [ [], [] ]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def add_object(o, depth=0):
    objects[depth].append(o)


def add_objects(ol, depth = 0):
    objects[depth] += ol

def update():
    for layer in objects:
        for o in layer:
            o.update()


def render():
    for layer in objects:
        for o in layer:
            o.draw()
def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True
def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)
def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            return
    raise ValueError('Cannot delete non existing object, 존재하지 않는 객체는 못지운다구 !!!')

def clear():
    for layer in objects:
        layer.clear()

def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
