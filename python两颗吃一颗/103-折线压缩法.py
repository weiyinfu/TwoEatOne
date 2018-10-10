import numpy as np
import tqdm

"""
棋盘局面从0开始逐渐递增,每个棋盘局面都有3种状态可供选择.
存储时,如果当前局面的胜负和与上一局面的胜负和相同,那么当前局面无需记录.
查询时,直接二分法查找比当前局面小的那一个局面的状态即可.
折线压缩法压缩数据
"""


def turn(x):
    # 旋转90度
    m = np.empty_like(x)
    l = x.shape[0]
    for i in range(l):
        for j in range(l):
            m[i][j] = x[j][l - i - 1]
    return m


def flip_h(x):
    # 水平翻转
    l = x.shape[0]
    m = np.empty_like(x)
    for i in range(l):
        for j in range(l):
            m[i][j] = x[l - 1 - i][j]
    return m


def tonum(x):
    # 棋盘状态转化为数字
    return np.sum(x.reshape(-1) * 3 ** np.arange(16))


def toarray(x):
    # 数字转换为棋盘状态
    return (x // (3 ** np.arange(16)) % 3).reshape(4, 4)


def hash(x):
    # 求状态x的等价状态
    m = toarray(x)
    ans = x
    for _ in range(3):
        m = turn(m)
        ans = min(tonum(m), ans)
    m = flip_h(toarray(x))
    ans = min(ans, tonum(m))
    for _ in range(3):
        m = turn(m)
        ans = min(ans, tonum(m))
    return ans


def load(file):
    # 加载数据
    a = np.fromfile(file, dtype=np.int32)
    return a // 3, a % 3


def build():
    # 压缩
    x, y = load("2eat1.bin")
    xx, yy = [x[0]], [y[0]]
    for i in range(1, len(y)):
        if y[i] == y[i - 1]:
            continue
        else:
            xx.append(x[i])
            yy.append(y[i])
    return xx, yy


def search(xx, yy, x):
    # 查找下界，二分法
    l = 0
    r = len(xx)
    while l < r:
        m = (l + r) >> 1
        if xx[m] > x:
            r = m
        elif xx[m] < x:
            l = m + 1
        else:
            return yy[m]
    return yy[l - 1]


def test_right(xx, yy):
    # 检验正误
    for x, y in tqdm.tqdm(zip(*load("2eat1.bin"))):
        if y != search(xx, yy, hash(x)):
            print("baga")
            print(toarray(x))
            input()


def export():
    xx, yy = build()
    # test_right(xx, yy)
    print(len(yy) * 4)
    with open("compress.bin", "wb") as f:
        for i in range(len(yy)):
            f.write(xx[i] * 3 + yy[i])


export()
