import math
import tkinter
import tkinter.messagebox as box
import winsound
import numpy as np


def load():
    f = open("../table.bin", 'rb')
    dic = {}
    while 1:
        k, v = f.read(4), f.read(4)
        if not k:
            break
        k, v = int.from_bytes(k, 'little'), int.from_bytes(v, 'little')
        dic[k] = v
    return dic


table = load()
board = []
chess = []
window = tkinter.Tk()
window.resizable(0, 0)
window.title("两颗吃一颗")
canvas = tkinter.Canvas(window, width=550, height=550, bg='orange')
canvas.pack()

isMoving = None
chess_size = 30
win_lose = 0
init_board_state = '2112212100000000'


def grid_pos(x, y):
    return 50 + 150 * x, 50 + y * 150


def init():
    global isMoving, win_lose, board, chess
    for i in chess: canvas.delete(i)
    board = list(map(lambda x: int(x), init_board_state))
    isMoving = None
    win_lose = 0
    chess = []
    """
    画四条线组成棋盘
    """
    for i in range(4):
        canvas.create_line(50, 50 + i * 150, 500, 50 + i * 150, width=4)
        canvas.create_line(50 + i * 150, 50, 50 + i * 150, 500, width=4)

    # 画棋子
    for i in range(16):
        if board[i] == 0: continue
        x, y = grid_pos(i % 4, i // 4)
        c = canvas.create_oval(x - chess_size, y - chess_size, x + chess_size, y + chess_size, fill='white' if board[i] == 2 else 'black')
        chess.append(c)
    play_sound('start')


def play_sound(file):
    if file == 'lose':
        winsound.PlaySound("res/%s.wav" % file, winsound.SND_FILENAME)
    else:
        winsound.PlaySound("res/%s.wav" % file, winsound.SND_FILENAME | winsound.SND_ASYNC)


def get_chess(x, y):
    xx, yy = y * 150 + 50, x * 150 + 50
    for i in chess:
        rec = canvas.coords(i)
        if rec[0] < xx < rec[2] and rec[1] < yy < rec[3]:
            return i


def remove_chess(x, y):
    c = get_chess(x, y)
    chess.remove(c)
    canvas.delete(c)
    board[x * 4 + y] = 0


def config_chess(id, x, y, sz):
    xx, yy = 150 * y + 50, 150 * x + 50
    canvas.coords(id, (xx - sz, yy - sz, xx + sz, yy + sz))


def move(oldx, oldy, newx, newy):
    play_sound('move')
    new = newx * 4 + newy
    old = oldx * 4 + oldy
    board[new] = board[old]
    board[old] = 0
    config_chess(get_chess(oldx, oldy), newx, newy, chess_size)
    after_move(newx, newy)


def after_move(x, y):
    b = reverse(board) if board[x * 4 + y] == 2 else board
    xx = b[x * 4] * 27 + b[x * 4 + 1] * 9 + b[x * 4 + 2] * 3 + b[x * 4 + 3]
    yy = b[y] * 27 + b[y + 4] * 9 + b[y + 8] * 3 + b[y + 12]
    state_diedChess = [66, 22, 42, 14]
    if xx in state_diedChess: remove_chess(x, state_diedChess.index(xx))
    if yy in state_diedChess: remove_chess(state_diedChess.index(yy), y)


def toint(m):
    s = 0
    p = 1
    for i in m:
        s += i * p
        p *= 3
    return s


def fromint(x):
    m = [0] * 16
    for i in range(16):
        m[i] = x % 3
        x //= 3
    return m


def reverse(m):
    return [3 - i if i > 0 else 0 for i in m]


def computer(newmap):
    global win_lose
    ans = table[toint(newmap)]
    oldmap = newmap
    newmap = reverse(fromint(ans // 3))
    if win_lose == 0 and ans % 3 == 1:
        win_lose = ans % 3
        play_sound('lose')
    oldx, oldy, newx, newy = 0, 0, 0, 0
    for i in range(16):
        if oldmap[i] == 1 and newmap[i] == 0:
            oldx, oldy = i // 4, i % 4
        if oldmap[i] == 0 and newmap[i] == 1:
            newx, newy = i // 4, i % 4
    move(oldx, oldy, newx, newy)


def over(board):
    return board.count(1) < 2


def lose():
    retry = box.askretrycancel("对局结果", 'You lose !')
    if retry:
        init()
    else:
        exit(0)


def clk(e):
    global isMoving
    y, x = round((e.x - 50) / 150), round((e.y - 50) / 150)
    id = x * 4 + y
    if id < 0 or id > 15: return
    if board[id] == 2: return
    if board[id] == 1:
        if isMoving:
            config_chess(get_chess(isMoving // 4, isMoving % 4), isMoving // 4, isMoving % 4, chess_size)
            if isMoving == id:
                isMoving = None
            else:
                isMoving = id
                config_chess(get_chess(x, y), x, y, chess_size + 10)
        else:
            isMoving = id
            config_chess(get_chess(x, y), x, y, chess_size + 10)
    if board[id] == 0:
        oldx, oldy = isMoving // 4, isMoving % 4
        if isMoving and math.hypot(oldx - x, oldy - y) <= 1:
            move(oldx, oldy, x, y)
            isMoving = None
            computer(reverse(board))
            if over(board):
                lose()


init()
window.bind('<Button-1>', clk)
window.mainloop()
