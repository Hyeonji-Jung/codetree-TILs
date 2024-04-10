from collections import deque

N, M = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]
conv = [list(map(int, input().split())) for _ in range(M)]
dxs = [-1, 0, 0, 1]
dys = [0, -1, 1, 0]
men = []
arrived = [False] * M
arrived_cnt = 0
t = 0


# bfs로 편의점까지의 최단거리를 찾되, 맨 처음 출발 시 방향 플래그를 가지고 움직이기
def move(idx, man):
    global men, arrived, arrived_cnt
    q = deque([])
    visited = [[False] * N for _ in range(N)]
    visited[man[0]][man[1]] = True
    for i in range(4):
        nx = man[0] + dxs[i]
        ny = man[1] + dys[i]
        if 0 <= nx < N and 0 <= ny < N and grid[nx][ny] >= 0:
            if nx == conv[idx][0] - 1 and ny == conv[idx][1] - 1:
                arrived[idx] = True
                arrived_cnt += 1
                return nx, ny
            else:
                q.append((nx, ny, i))
                visited[nx][ny] = True

    while q:
        x, y, dir = q.popleft()
        if x == conv[idx][0] - 1 and y == conv[idx][1] - 1:
            men[idx][0], men[idx][1] = man[0] + dxs[dir], man[1] + dys[dir]
            break

        for i in range(4):
            nx = x + dxs[i]
            ny = y + dys[i]
            if 0 <= nx < N and 0 <= ny < N and grid[nx][ny] >= 0:
                q.append((nx, ny, dir))
                visited[nx][ny] = True
    return -1, -1


# bfs로 해당 편의점에서 가장 가까운 베이스캠프 찾은 후 해당 베이스캠프 좌표 반환
def find_near_conv(con):
    q = deque([])
    visited = [[False] * N for _ in range(N)]
    q.append((con[0] - 1, con[1] - 1))
    visited[con[0] - 1][con[1] - 1] = True

    while q:
        x, y = q.popleft()
        if grid[x][y] == 1:
            return [x, y]

        for i in range(4):
            nx = x + dxs[i]
            ny = y + dys[i]
            if 0 <= nx < N and 0 <= ny < N and grid[nx][ny] >= 0:
                q.append((nx, ny))
                visited[nx][ny] = True
    return [0, 0]


while True:
    if arrived_cnt == M:
        break
    t += 1

    # print("------------------")
    # for i in range(N):
    #     print(*grid[i])
    # for m in men:
    #     print(*m)
    # print("------------------")

    # 1. 편의점을 향해 1칸 이동
    # 2. 편의점에 도착했는지 확인, 도착했다면 이후 단계부터는 해당 칸을 지나갈 수 없음
    for idx, m in enumerate(men):
        cantmove = []
        if not arrived[idx]:
            x, y = move(idx, m)
            if x != -1 and y != -1:
                cantmove.append((x, y))
        for c in cantmove:
            grid[c[0]][c[1]] = -1

    # 3. t <= m일 때 t번 사람이 베이스캠프로 이동, 이후 단계부터는 해당 베이스캠프 칸을 지나갈 수 없음
    if t <= M:
        base = find_near_conv(conv[t - 1])
        men.append(base)
        grid[base[0]][base[1]] = -1

print(t)