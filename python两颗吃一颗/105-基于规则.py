from data import get_data
import numpy as np
from collections import Counter

x, y = get_data(shuffle=False, one_hot=False)
feature = np.fromfile("feature.bin", np.int32).reshape(-1, 6)
black_chess_count = feature[:, 0]
white_chess_count = feature[:, 1]
black_space_count = feature[:, 2]
white_space_count = feature[:, 3]
black_dis = feature[:, 4]
white_dis = feature[:, 5]

"""
探究起作用的规则
"""


def count_chess(x, y):
    bad_case_x = []
    bad_case_y = []
    for ind, xx, yy in zip(range(len(x)), x, y):
        if white_chess_count[ind] > black_chess_count[ind] and yy == 2:
            continue
        if white_chess_count[ind] < black_chess_count[ind] and yy == 1:
            continue
        if white_chess_count[ind] == black_chess_count[ind] and yy == 0:
            continue
        bad_case_x.append(xx)
        bad_case_y.append(yy)
    return np.array(bad_case_x), np.array(bad_case_y)


def free_space(x, y):
    bad_x = []
    bad_y = []
    for ind, xx, yy in zip(range(len(x)), x, y):
        """
        虽然白棋多一个子，但是黑棋自由度大，那么和棋
        虽然黑棋多一个子，但是白棋自由度大，那么和棋
        """
        if white_space_count[ind] > black_space_count[ind] and yy == 2:
            continue
        if white_space_count[ind] < black_space_count[ind] and yy == 1:
            continue
        if white_space_count[ind] < black_space_count[ind] and yy == 0 and white_chess_count[ind] - 1 == black_chess_count[ind]:
            continue
        if white_space_count[ind] == black_space_count[ind] and yy == 0:
            continue
        if white_chess_count[ind] + 1 == black_chess_count[ind] and black_space_count[ind] < white_space_count[ind] and yy == 0:
            continue
        bad_x.append(xx)
        bad_y.append(yy)
    return np.array(bad_x), np.array(bad_y)


def chess_distance(x, y):
    """
    按照棋子距离
    :return:
    """

    bad_x = []
    bad_y = []
    for ind, xx, yy in zip(range(len(x)), x, y):
        if black_dis[ind] > white_dis[ind] and yy == 2:
            continue
        if black_dis[ind] < white_dis[ind] and yy == 1:
            continue
        if black_dis[ind] == white_dis[ind] and yy == 0:
            continue
        if white_chess_count[ind] - 1 == black_chess_count[ind] and black_dis[ind] < white_dis[ind] and yy == 0:
            continue
        if white_chess_count[ind] + 1 == black_chess_count[ind] and black_dis[ind] > white_dis[ind] and yy == 0:
            continue
        bad_x.append(xx)
        bad_y.append(yy)
    return np.array(bad_x), np.array(bad_y)


def first_hand_win(x, y):
    bad_index = np.argwhere(y != 1)
    return x[bad_index], y[bad_index]


def main():
    print(x.shape, y.shape)
    bad_x, bad_y = count_chess(x, y)
    print("按照棋子数", bad_x.shape, bad_y.shape, Counter(bad_y))

    bad_x, bad_y = free_space(bad_x, bad_y)
    print("按照自由度", bad_x.shape, bad_y.shape, Counter(bad_y))

    bad_x, bad_y = chess_distance(bad_x, bad_y)
    print("按照棋子距离", bad_x.shape, bad_y.shape, Counter(bad_y))

    bad_x, bad_y = first_hand_win(bad_x, bad_y)
    print("按照先手优势", bad_x.shape, bad_y.shape)
    for xx, yy in zip(bad_x, bad_y):
        print(xx.reshape(4, 4))
        print(yy)
        input()


def debug():
    bad = free_space(np.array([[-1, 1, 1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]), [1])
    print(bad)


if __name__ == '__main__':
    main()
    # debug()
"""
(284885, 16) (284885,)
按照棋子数 (116264, 16) (116264,) Counter({1: 78944, 2: 25238, 0: 12082})
按照自由度 (46213, 16) (46213,) Counter({1: 34241, 0: 6117, 2: 5855})
按照棋子距离 (11732, 16) (11732,) Counter({1: 10398, 2: 778, 0: 556})
按照先手优势 (1334, 1, 16) (1334, 1)
"""
