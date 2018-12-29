import numpy as np
import tqdm

a = np.fromfile("../table.bin", dtype=np.int32)
x, y = a[np.arange(0, len(a) >> 1) * 2], a[np.arange(0, len(a) >> 1) * 2 + 1] % 3
# 把x转换成4*4的数组
mask = 3 ** np.tile(np.arange(16), (len(x), 1))
xx = np.tile(x, (16, 1)).transpose() // mask % 3
xx = xx.reshape(-1, 4, 4)
ind = dict((x[i], i) for i in range(len(x)))
father = np.arange(len(x))  # 每个人的父亲都是自己
sons_count = [0] * len(x)  # 每个人的儿子书
tonum = lambda x: np.sum(x.reshape(-1) * 3 ** np.arange(16))  # 把局面转成数字
print("原来的局面总数", len(x))


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


def test(x, i):
    """
    x表示棋盘局面,i表示当前是第几个
    :param x:
    :param i:
    :return:
    """
    last = x
    cnt = 0  # 儿子的个数
    for _ in range(4):
        last = turn(last)
        # 旋转
        h = ind[tonum(last)]
        if father[h] == h and h != i:
            father[h] = i
            # 这两者的胜负和状态必然相同,否则不正常
            assert y[h] == y[i]
            sons_count[i] += 1
            cnt += 1
    return cnt


def main():
    # 从小到大一次遍历
    a = []
    for i in tqdm.tqdm(range(len(xx))):
        if i != father[i]:
            # 如果已经被前面的状态包含了,不处理此状态
            continue
        test(xx[i], i)  # 旋转4次并更新状态
        test(flip_h(xx[i]), i)  # 先水平翻转在旋转4次
        a.append(x[i] * 3 + y[i])
    a = np.array(a, dtype=np.int32)
    a.tofile("2eat1.bin")
    # 压缩之后的状态个数
    print(np.count_nonzero(father == np.arange(len(x))))


if __name__ == '__main__':
    main()
