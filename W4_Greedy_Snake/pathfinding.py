import snake
import numpy as np

# 定义距离矩阵
distance = np.zeros([500, 500])
# 四个方向
directions = [[0, 10], [0, -10], [10, 0], [-10, 0]]
# 节点排队
queue = []

# bfs算法
def bfs():
    global distance

    while queue:
        # 取出队首元素
        x, y = queue.pop(0)

        # 四个方向
        for direct in directions:
            nx = x + direct[0]
            ny = y + direct[1]

            # 判断是否在边界内或者是否是蛇身
            if not snake.inside(nx, ny) or [nx, ny] in snake.snake[:]:
                continue
            # 判断相邻点是否是最短路径
            if distance[nx, ny] > distance[x, y] + 1:
                distance[nx, ny] = distance[x, y] + 1
                # 将相邻点加入队列
                if [nx, ny] not in queue:
                    queue.append([nx, ny])

# 设置最佳方向
def set_best_direct():
    # 蛇头位置及初始化
    global distance
    best = 1e5
    best_direct = []

    # 遍历四个方向
    for direct in directions:
        nx = snake.snake[-1][0] + direct[0]
        ny = snake.snake[-1][1] + direct[1]
        # 判断是否在边界内或者是否是蛇身
        if not snake.inside(nx, ny) or [nx, ny] in snake.snake[:]:
            pass
        else:
            if distance[nx, ny] == 1e5:
                distance[nx, ny] = 1e4

        # 判断是否是最短路径
        if distance[nx, ny] == best:
            best_direct.append(direct)

        if distance[nx, ny] < best:
            best = distance[nx, ny]
            best_direct = [direct]
    # 打乱方向
    if np.random.uniform(0, 1) < 0.5:
        np.random.shuffle(best_direct)
    # 设置方向
    snake.change(best_direct[0][0], best_direct[0][1])


def pathfinding():
    # 初始化距离矩阵
    distance.fill(1e5)
    # 食物位置
    food_x, food_y = snake.food_x, snake.food_y
    distance[food_x, food_y] = 0
    # 将食物加入队列
    queue.append([food_x, food_y])
    # bfs算法
    bfs()
    # 设置最佳方向
    set_best_direct()
    snake.ontimer(pathfinding, 6)
