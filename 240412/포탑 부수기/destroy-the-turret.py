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
        if grid[i][j] > 0:
            turret.append((i, j))
        else:
            broken += 1
no_repair = []


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
        if nx == attacker[0] and ny == attacker[1]:
            continue
        grid[nx][ny] -= grid[attacker[0]][attacker[1]] // 2
        no_repair.append((nx, ny))


for k in range(1, K + 1):
    # 공격할 포탑, 공격받을 포탑 선정
    turret.sort(key=lambda x: (grid[x[0]][x[1]], -attack[x[0]][x[1]], -(x[0] + x[1]), -x[1]))
    attacker = turret[0]
    defender = turret[-1]
    attack[attacker[0]][attacker[1]] = k
    grid[attacker[0]][attacker[1]] += N + M
    no_repair.append(attacker)
    no_repair.append(defender)

    # 레이저 공격, 레이저 공격 실패 시 포탄 공격
    if not laser(attacker, defender):
        bomb(attacker, defender)

    # 포탑 부서짐
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