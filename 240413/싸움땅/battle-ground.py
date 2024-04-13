N, M, K = map(int, input().split())
grid = [[[] for _ in range(N)] for _ in range(N)]
for i in range(N):
    row = list(map(int, input().split()))
    for j in range(N):
        if row[j] > 0:
            grid[i][j].append(row[j])
players = []
for i in range(M):
    x, y, d, s = map(int, input().split())
    players.append({"x": x - 1, "y": y - 1, "d": d, "s": s})

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

guns = [0] * M
points = [0] * M


def is_player(player, x, y):
    flag = False
    for i in range(M):
        if player != i and x == players[i]["x"] and y == players[i]["y"]:
            flag = True
            break
    return flag


def player_move(player):
    nx = players[player]["x"] + dx[players[player]["d"]]
    ny = players[player]["y"] + dy[players[player]["d"]]

    # 격자 벗어나면 정반대 방향으로 이동
    if nx < 0 or nx >= N or ny < 0 or ny >= N:
        players[player]["d"] = (players[player]["d"] + 2) % 4
        nx = players[player]["x"] + dx[players[player]["d"]]
        ny = players[player]["y"] + dy[players[player]["d"]]

    players[player]["x"], players[player]["y"] = nx, ny


def loser_move(loser):
    nx = players[loser]["x"] + dx[players[loser]["d"]]
    ny = players[loser]["y"] + dy[players[loser]["d"]]

    # 격자 벗어나거나 플레이어 있으면 오른쪽으로 90도씩 회전
    while nx < 0 or nx >= N or ny < 0 or ny >= N or is_player(players[loser], nx, ny):
        players[loser]["d"] = (players[loser]["d"] + 1) % 4
        nx = players[loser]["x"] + dx[players[loser]["d"]]
        ny = players[loser]["y"] + dy[players[loser]["d"]]

    players[loser]["x"], players[loser]["y"] = nx, ny


for k in range(K):
    # 플레이어 순차 이동
    for i in range(M):
        player_move(i)

        fought = False
        # 이동 방향에 플레이어가 있으면 싸우기
        for j in range(M):
            if (
                i != j
                and players[i]["x"] == players[j]["x"]
                and players[i]["y"] == players[j]["y"]
            ):
                fought = True
                power_i = players[i]["s"] + guns[i]
                power_j = players[j]["s"] + guns[j]
                winner, loser = (
                    (i, j)
                    if (
                        power_i > power_j
                        or (power_i == power_j and players[i]["s"] > players[j]["s"])
                    )
                    else (j, i)
                )

                points[winner] += abs(power_i - power_j)

                # 진 플레이어 총 내려놓고 이동 후 총 획득
                if guns[loser] > 0:
                    grid[players[loser]["x"]][players[loser]["y"]].append(guns[loser])
                    guns[loser] = 0
                loser_move(loser)
                if len(grid[players[loser]["x"]][players[loser]["y"]]) > 0:
                    grid[players[loser]["x"]][players[loser]["y"]].sort()
                    guns[loser] = grid[players[loser]["x"]][players[loser]["y"]].pop()

                # 이긴 플레이어 총 획득
                if guns[winner] > 0:
                    grid[players[winner]["x"]][players[winner]["y"]].append(
                        guns[winner]
                    )
                    guns[winner] = 0
                if len(grid[players[winner]["x"]][players[winner]["y"]]) > 0:
                    grid[players[winner]["x"]][players[winner]["y"]].sort()
                    guns[winner] = grid[players[winner]["x"]][
                        players[winner]["y"]
                    ].pop()

                break

        if not fought:
            if guns[i] > 0:
                grid[players[i]["x"]][players[i]["y"]].append(guns[i])
                guns[i] = 0
            if len(grid[players[i]["x"]][players[i]["y"]]) > 0:
                grid[players[i]["x"]][players[i]["y"]].sort()
                guns[i] = grid[players[i]["x"]][players[i]["y"]].pop()


print(*points)