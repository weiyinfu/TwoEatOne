import numpy as np


def get_data(shuffle=True, one_hot=True):
    a = np.fromfile("2eat1.bin", np.int)
    x = a // 3
    y = a % 3
    # onehot
    if one_hot:
        yy = np.zeros((len(y), 3))
        yy[y == 0, 0] = 1
        yy[y == 1, 1] = 1
        yy[y == 2, 2] = 1
    else:
        yy = y
    # 扩展x
    mask = np.tile(3 ** np.arange(16), (len(x), 1))
    xx = np.tile(x, (16, 1)).T // mask % 3
    # 打乱顺序
    if shuffle:
        arg = np.arange(len(x))
        np.random.shuffle(arg)
        xx = xx[arg]
        yy = yy[arg]
    xx = xx.astype(np.float32)
    """
    如果知道数据中的特点，尽量应用数据的特点
    空白是0，黑棋是1，白棋如果是2就不太好，白棋应该是-1
    """
    t = xx.reshape(-1)
    t[t == 2] = -1
    return xx, yy


if __name__ == '__main__':
    x, y = get_data(False)
    print(x.shape, y.shape)
    for i in x[:10]:
        print(i)
