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
        if 0 <= nx < N and 0 <= ny < N:
            if nx == conv[idx][0] - 1 and ny == conv[idx][1] - 1:
                # 편의점에 도착한 경우 처리, 해당 편의점 좌표 반환
                arrived[idx] = True
                arrived_cnt += 1
                return nx, ny
            elif grid[nx][ny] >= 0:
                q.append((nx, ny, i, 1))
                visited[nx][ny] = True

    min_dirs = []
    min_dist = 10000
    while q:
        x, y, dir, dist = q.popleft()
        if x == conv[idx][0] - 1 and y == conv[idx][1] - 1:
            # 상좌우하 중 가장 우선순위가 높은 방향을 찾기 위해 최단거리가 같은 경우를 모두 저장
            if dist < min_dist:
                min_dist = dist
                min_dirs = [dir]
            elif dist == min_dirs:
                min_dirs.append(dir)
            else:
                break

        for i in range(4):
            nx = x + dxs[i]
            ny = y + dys[i]
            if (
                0 <= nx < N
                and 0 <= ny < N
                and not visited[nx][ny]
                and grid[nx][ny] >= 0
            ):
                q.append((nx, ny, dir, dist + 1))
                visited[nx][ny] = True

    # 가장 우선순위가 높은 방향 찾기
    min_dirs.sort()
    men[idx][0], men[idx][1] = man[0] + dxs[min_dirs[0]], man[1] + dys[min_dirs[0]]
    return -1, -1


# bfs로 해당 편의점에서 가장 가까운 베이스캠프 찾은 후 해당 베이스캠프 좌표 반환
def find_near_conv(con):
    q = deque([])
    visited = [[False] * N for _ in range(N)]
    q.append((con[0] - 1, con[1] - 1, 0))
    visited[con[0] - 1][con[1] - 1] = True

    bases = [[-1, -1]]
    min_dist = 10000

    while q:
        x, y, d = q.popleft()
        if grid[x][y] == 1:
            # 가장 우선순위가 높은 베이스캠프를 찾기 위해 최단거리가 같은 경우를 모두 저장
            if d < min_dist:
                min_dist = d
                bases = [[x, y]]
            elif d == min_dist:
                bases.append([x, y])
            else:
                break

        for i in range(4):
            nx = x + dxs[i]
            ny = y + dys[i]
            if (
                0 <= nx < N
                and 0 <= ny < N
                and not visited[nx][ny]
                and grid[nx][ny] >= 0
            ):
                q.append((nx, ny, d + 1))
                visited[nx][ny] = True

    # 가장 우선순위가 높은 베이스캠프 찾기 (행이 가장 작거나, 행이 같으면 열이 가장 작은 베이스캠프)
    bases.sort(key=lambda x: (x[0], x[1]))
    return bases[0]


while True:
    if arrived_cnt == M:
        break
    t += 1

    # 1. 편의점을 향해 1칸 이동
    # 2. 편의점에 도착했는지 확인, 도착했다면 이후 단계부터는 해당 칸을 지나갈 수 없음
    arrived_conv = []
    for idx, m in enumerate(men):
        if not arrived[idx]:
            x, y = move(idx, m)
            if x != -1 and y != -1:
                arrived_conv.append((x, y))

    # 도착한 편의점은 더이상 지나갈 수 없음
    for c in arrived_conv:
        grid[c[0]][c[1]] = -1

    # 3. t <= m일 때 t번 사람이 베이스캠프로 이동, 이후 단계부터는 해당 베이스캠프 칸을 지나갈 수 없음
    if t <= M:
        base = find_near_conv(conv[t - 1])
        men.append(base)
        grid[base[0]][base[1]] = -1

print(t)