# layer 0 : Background Object
# layer 1 : Foreground Object
# 게임 월드에 담겨있는 모든 객체들을 담고 있는 리스트, Drawing Layer에 따라서 분류.
# 필요에 따라 Layer를 추가하면 됨. 현재는 두개의 Layer만
objects = [[], []]


def add_objects(o, depth=0):
    objects[depth].append(o)


# def add_objects(ol, depth = 0):
#     objects[depth] += ol

def update():
    for layer in objects:
        for o in layer:
            o.update()


def render():
    for layer in objects:
        for o in layer:
            o.draw()


def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            return
    raise ValueError('Cannot delete non existing object, 존재하지 않는 객체는 못지운다구 !!!')
