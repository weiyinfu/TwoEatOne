"""
局面特征提取器
"""
import numpy as np
import tqdm


def free_space_count(xx):
    black_space_count = 0
    white_space_count = 0
    for j in np.argwhere(xx != 0):
        for dx in (1, -1, 4, -4):
            if dx == -1 and j % 4 == 0: continue
            if dx == 1 and j % 4 == 3: continue
            if len(xx) > j + dx >= 0 and xx[j + dx] == 0:
                if xx[j] == 1:
                    black_space_count += 1
                else:
                    white_space_count += 1
    return black_space_count, white_space_count


def chess_distance(xx):
    """
    棋子之间的距离
    :param xx:
    :return:
    """

    def nearest_sum(a):
        s = 0
        for i in a:
            min_dis = 16
            for j in a:
                if i == j: continue
                min_dis = min(min_dis, np.abs(i // 4 - j // 4) + np.abs(i % 4 - j % 4))
            s += min_dis
        return s

    black_chess = np.argwhere(xx == 1)
    white_chess = np.argwhere(xx == -1)
    black_dis = nearest_sum(black_chess)
    white_dis = nearest_sum(white_chess)
    return black_dis, white_dis


def get_feature(xx):
    black_chess_count = np.count_nonzero(xx == 1)
    white_chess_count = np.count_nonzero(xx == -1)
    black_space_count, white_space_count = free_space_count(xx)
    black_dis, white_dis = chess_distance(xx)
    return [black_chess_count, white_chess_count, black_space_count, white_space_count, black_dis, white_dis]


def extract(x):
    print("extracting")
    a = []
    for i in tqdm.tqdm(range(len(x))):
        a.append(get_feature(x[i]))
    return np.array(a)


if __name__ == '__main__':
    """
    提取特征并保存
    """
    import data

    x, y = data.get_data(shuffle=False, one_hot=False)
    print(x.shape)
    x = extract(x)
    print(x.shape)
    x = x.astype(np.int32)
    x.tofile("feature.bin")
