from turtle import *
from random import *

snake = [[0, 0]]  # 蛇的起始位置
aim_x, aim_y = 0, -10  # 蛇的起始方向


def square(x, y, size, sq_color):
    """绘制小正方形, 代表一格"""
    color(sq_color)
    up()
    goto(x, y)
    down()
    begin_fill()
    for i in range(4):
        fd(size)
        left(90)
    end_fill()


def frame():
    """绘制边框"""
    for i in range(-210, 200, 10):
        square(i, -200, 10, 'gray')
        square(i, 200, 10, 'gray')
    for i in range(-200, 200, 10):
        square(-210, i, 10, 'gray')
        square(190, i, 10, 'gray')


def change(x, y):
    """改变蛇的运动方向"""
    global aim_x, aim_y
    if x != -aim_x or y != -aim_y:
        aim_x, aim_y = x, y


def inside(head_x, head_y):
    """判断蛇是否在边框内"""
    if -210 < head_x < 190 and -200 < head_y < 200:
        return True
    else:
        return False


all_food = []  # 所有食物的位置
for x_ in range(-200, 190, 10):
    for y_ in range(-190, 200, 10):
        all_food.append([x_, y_])


def new_food():
    """随机生成食物位置"""
    food = all_food.copy()
    for i in snake:  # 去掉蛇所在的位置
        food.remove(i)
    new_food_x, new_food_y = food.pop(randint(0, len(food) - 1))
    return new_food_x, new_food_y


food_x, food_y = new_food()  # 食物的起始位置


def move():
    global food_x, food_y
    head_move_x = snake[-1][0] + aim_x
    head_move_y = snake[-1][1] + aim_y

    # 判断是否撞到边框或者撞到自己
    if not inside(head_move_x, head_move_y) or [head_move_x, head_move_y] in snake:
        square(head_move_x, head_move_y, 10, 'red')
        update()
        print('得分: ', len(snake))
        return

    snake.append([head_move_x, head_move_y])

    # 判断是否吃到食物以及是否胜利
    if head_move_x == food_x and head_move_y == food_y:
        if len(snake) == len(all_food):
            print('YOU WIN!')
            return
        else:
            food_x, food_y = new_food()
    else:
        snake.pop(0)
    clear()
    # 绘制边框, 蛇和食物
    frame()
    for body in snake:
        square(body[0], body[1], 10, 'black')
    square(food_x, food_y, 10, 'green')
    update()
    # 根据得分调节速度, 每到达一定分数会提高速度
    # if len(snake) < 10:
    #     ontimer(move, 40)
    # elif len(snake) < 20:
    #     ontimer(move, 30)
    # elif len(snake) < 30:
    #     ontimer(move, 20)
    # elif len(snake) < 40:
    #     ontimer(move, 10)
    # else:
    ontimer(move, 0)


setup(420, 420)
title('贪吃蛇')
hideturtle()
tracer(False)
listen()
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, -10), 'Down')
onkey(lambda: change(10, 0), 'Right')
move()
