from collections import deque

N, M, K = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]

dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]
dxs = [0, 1, 0, -1, 1, -1, 1, -1]
dys = [1, 0, -1, 0, 1, -1, -1, 1]

attack = [[0] * M for _ in range(N)]
turret = []
broken = 0
for i in range(N):
    for j in range(M):
        if grid[i][j] == 0:
            broken += 1
        else:
            turret.append((i, j))
no_repair = []


def get_attacker():
    attackers = []
    min_power = 10000
    for t in turret:
        if grid[t[0]][t[1]] < min_power:
            attackers = [t]
            min_power = grid[t[0]][t[1]]
        elif grid[t[0]][t[1]] == min_power:
            attackers.append(t)
    attackers.sort(key=lambda x: (-attack[x[0]][x[1]], -(x[0] + x[1]), -x[1]))
    return attackers[0]


def get_defender():
    defenders = []
    max_power = -1
    for t in turret:
        if grid[t[0]][t[1]] > max_power:
            defenders = [t]
            max_power = grid[t[0]][t[1]]
        elif grid[t[0]][t[1]] == max_power:
            defenders.append(t)
    defenders.sort(key=lambda x: (attack[x[0]][x[1]], x[0] + x[1], x[1]))
    return defenders[0]


def laser(attacker, defender):
    global grid, no_repair

    q = deque([])
    visited = [[False] * M for _ in range(N)]
    q.append((attacker[0], attacker[1], []))
    visited[attacker[0]][attacker[1]] = True

    while q:
        x, y, path = q.popleft()
        if x == defender[0] and y == defender[1]:
            for p in path:
                grid[p[0]][p[1]] -= grid[attacker[0]][attacker[1]] // 2
                no_repair.append(p)
            grid[defender[0]][defender[1]] -= grid[attacker[0]][attacker[1]] - grid[attacker[0]][attacker[1]] // 2
            return True

        for i in range(4):
            nx = (x + dx[i]) % N
            ny = (y + dy[i]) % M
            if grid[nx][ny] > 0 and not visited[nx][ny]:
                q.append((nx, ny, path + [(nx, ny)]))
                visited[nx][ny] = True
    return False


def bomb(attacker, defender):
    global grid, no_repair

    grid[defender[0]][defender[1]] -= grid[attacker[0]][attacker[1]]
    for i in range(8):
        nx = (defender[0] + dxs[i]) % N
        ny = (defender[1] + dys[i]) % M
        if nx != attacker[0] and ny != attacker[1] and grid[nx][ny] > 0:
            grid[nx][ny] -= grid[attacker[0]][attacker[1]] // 2
            no_repair.append((nx, ny))


for k in range(1, K + 1):
    # 1. 공격자 선정
    attacker = get_attacker()
    grid[attacker[0]][attacker[1]] += N + M
    attack[attacker[0]][attacker[1]] = k
    no_repair.append(attacker)

    # 2. 공격
    # 2-1. 공격받을 포탑 선정
    defender = get_defender()
    no_repair.append(defender)

    # 2-3. 레이저 공격, 레이저 공격 실패 시 포탄 공격
    if not laser(attacker, defender):
        bomb(attacker, defender)

    # 3. 포탑 부서짐
    broken = 0
    remains = []
    for i in range(N):
        for j in range(M):
            if grid[i][j] <= 0:
                grid[i][j] = 0
                broken += 1
            else:
                remains.append((i, j))
    turret = remains

    # 포탑 하나 남으면 즉시 종료
    if N * M - broken == 1:
        break

    # 4. 포탑 정비
    for t in turret:
        if t not in no_repair:
            grid[t[0]][t[1]] += 1
    no_repair = []

turret.sort(key=lambda x: grid[x[0]][x[1]])
print(grid[turret[-1][0]][turret[-1][1]])