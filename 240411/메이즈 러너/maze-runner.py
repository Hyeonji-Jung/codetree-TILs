N, M, K = map(int, input().split())
miro = [list(map(int, input().split())) for _ in range(N)]
men = []
for _ in range(M):
    r, c = map(int, input().split())
    men.append([r - 1, c - 1])
exit = [x - 1 for x in map(int, input().split())]

dxs = [-1, 1, 0, 0]
dys = [0, 0, -1, 1]

escape = [False] * M
escape_cnt = 0
move_cnt = 0


# 거리 척도: 맨해튼 거리
def get_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


# 사각형 내에 아직 탈출하지 못한 참가자가 한 명이라도 포함되는지 확인
def is_contain(sx, sy, d):
    for m in range(M):
        if escape[m]:
            continue
        if sx <= men[m][0] < sx + d and sy <= men[m][1] < sy + d:
            return True
    return False


# 가장 작은 정사각형 찾기
def get_square():
    d = 2
    while d <= N:
        for sx in range(N - d + 1):
            for sy in range(N - d + 1):
                if sx <= exit[0] < sx + d and sy <= exit[1] < sy + d and is_contain(sx, sy, d):
                    return sx, sy, d
        d += 1
    return -1, -1, -1


for _ in range(K):
    # 모든 참가자가 탈출했다면 종료
    if escape_cnt == M:
        break

    # 아직 탈출하지 못한 참가자를 한 칸씩 움직이기
    # 상하좌우로 움직였을 때 출구까지의 최단거리가 가까워지면 이동, 움직일 수 없으면 움직이지 않기
    for m in range(M):
        if escape[m]:
            continue
        curr_dist = get_dist(men[m], exit)
        for i in range(4):
            nx, ny = men[m][0] + dxs[i], men[m][1] + dys[i]
            if 0 <= nx < N and 0 <= ny < N and miro[nx][ny] == 0 and get_dist([nx, ny], exit) < curr_dist:
                men[m][0], men[m][1] = nx, ny
                move_cnt += 1
                if men[m][0] == exit[0] and men[m][1] == exit[1]:
                    escape[m] = True
                    escape_cnt += 1
                break

    # 정사각형 잡기: 한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형
    sx, sy, d = get_square()

    # 시계방향으로 90도 회전시키기, 벽이면 내구도 깎기
    # 출구 회전
    exit[0], exit[1] = sx + exit[1] - sy, sy + d - 1 - (exit[0] - sx)

    # 사각형 내에 존재하는 참가자 회전
    for m in range(M):
        if escape[m]:
            continue
        if sx <= men[m][0] < sx + d and sy <= men[m][1] < sy + d:
            men[m][0], men[m][1] = sx + men[m][1] - sy, sy + d - 1 - (men[m][0] - sx)

    # 사각형 회전
    temp = [[miro[i][j] for j in range(sy, sy + d)] for i in range(sx, sx + d)]
    for i in range(d):
        for j in range(d):
            miro[sx + j][sy + d - 1 - i] = temp[i][j] if temp[i][j] == 0 else temp[i][j] - 1

print(move_cnt)
print(exit[0] + 1, exit[1] + 1)