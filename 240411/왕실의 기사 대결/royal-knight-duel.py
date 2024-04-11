L, N, Q = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(L)]
knights = []
for _ in range(N):
    knight = dict()
    r, c, h, w, k = map(int, input().split())
    knight["r"] = r - 1
    knight["c"] = c - 1
    knight["h"] = h
    knight["w"] = w
    knight["k"] = k
    knights.append(knight)
commands = []
for _ in range(Q):
    i, d = map(int, input().split())
    commands.append([i - 1, d])

dxs = [-1, 0, 1, 0]
dys = [0, 1, 0, -1]

alive = [True] * N
damages = [0] * N
pushed = []


def is_overlap(k1, k2):
    return not (k1['c'] + k1['w'] <= k2['c'] or k2['c'] + k2['w'] <= k1['c'] or k1['r'] + k1['h'] <= k2['r']
                or k2['r'] + k2['h'] <= k1['r'])


def is_wall(k):
    wall = False
    for i in range(k['r'], k['r'] + k['h']):
        if wall:
            break
        for j in range(k['c'], k['c'] + k['w']):
            if i < 0 or i >= L or j < 0 or j >= L or board[i][j] == 2:
                wall = True
                break
    return wall


def push(idx, dir):
    global pushed

    # 기사 이동 가정
    nr, nc = knights[idx]['r'] + dxs[dir], knights[idx]['c'] + dys[dir]
    moved = {'r': nr, 'c': nc, 'h': knights[idx]['h'], 'w': knights[idx]['w'], 'k': knights[idx]['k']}

    # 벽이랑 겹치는지 확인
    if is_wall(moved):
        return False

    # 이동시켰을 때 밀려나는 기사 있는지 찾기
    flag = True
    for i in range(N):
        if i != idx and alive[i] and is_overlap(moved, knights[i]):
            if flag:
                flag = push(i, dir)
            else:
                break

    if flag:
        pushed.append(idx)
    return flag


def move(idx, dir):
    global knights, alive, damages

    # 기사 이동
    knights[idx]['r'], knights[idx]['c'] = knights[idx]['r'] + dxs[dir], knights[idx]['c'] + dys[dir]

    # 기사가 입는 데미지 계산
    damage = 0
    for i in range(knights[idx]['r'], knights[idx]['r'] + knights[idx]['h']):
        for j in range(knights[idx]['c'], knights[idx]['c'] + knights[idx]['w']):
            if board[i][j] == 1:
                damage += 1

    # 데미지 입기
    if damage >= knights[idx]['k']:
        alive[idx] = False
    else:
        knights[idx]['k'] -= damage
        damages[idx] += damage


# 명령을 하나씩 진행
for idx, dir in commands:
    # 이미 사라진 기사라면 넘어가기
    if not alive[idx]:
        continue

    # 기사 이동
    tr, tc = knights[idx]['r'], knights[idx]['c']
    knights[idx]['r'], knights[idx]['c'] = knights[idx]['r'] + dxs[dir], knights[idx]['c'] + dys[dir]

    # 이동했을 때 혹시 벽이랑 겹치는지 확인, 벽이랑 겹치면 이동 못하므로 좌표 복원하고 다음 명령으로 넘어감
    if is_wall(knights[idx]):
        knights[idx]['r'], knights[idx]['c'] = tr, tc
        continue

    # 기사가 명령을 받고 이동했을 때 밀려나는 기사 찾기
    flag = True
    pushed = []
    for i in range(N):
        if i != idx and alive[i] and is_overlap(knights[idx], knights[i]):
            if flag:
                flag = push(i, dir)
            else:
                break

    # 움직이는 게 가능한 상황이라면 기사들이 이동하고 데미지 입기, 움직일 수 없다면 움직이지 않기
    if flag:
        for i in pushed:
            move(i, dir)
    else:
        knights[idx]['r'], knights[idx]['c'] = tr, tc

total_damage = 0
for i in range(N):
    if alive[i]:
        total_damage += damages[i]
print(total_damage)