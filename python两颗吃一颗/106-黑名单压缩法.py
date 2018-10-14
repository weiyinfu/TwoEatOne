"""
基于规则的压缩
每一条规则都能够干掉一批数据，最后没有被规则覆盖到的情况使用硬编码保存下来，这种压缩方式缺点在于需要人来参与，优点在于压缩率极高
"""
from collections import Counter

import numpy as np

import data

x, y = data.get_data(shuffle=False, one_hot=False)
feature = np.fromfile("feature.bin", np.int32).reshape(len(x), -1)
black_chess_count = feature[:, 0]
white_chess_count = feature[:, 1]
black_space_count = feature[:, 2]
white_space_count = feature[:, 3]
black_dis = feature[:, 4]
white_dis = feature[:, 5]

print("未压缩前", len(x))
bad_x = []
bad_y = []

ungot_x = []
ungot_y = []

rules = [
    (lambda ind: black_chess_count[ind] > white_chess_count[ind], 1),
    (lambda ind: black_chess_count[ind] < white_chess_count[ind], 2),
    (lambda ind: white_space_count[ind] < black_space_count[ind], 1),
    (lambda ind: black_chess_count[ind] == white_chess_count[ind] and white_dis[ind] > black_dis[ind], 1),
    (lambda ind:  white_chess_count[ind] == black_chess_count[ind] and white_space_count[ind] == black_space_count[ind], 1),
    (lambda ind: True, 2),
]
error = [0] * len(rules)
right = [0] * len(rules)
got_command = 0  # 命中规则的个数
for ind, xx, yy in zip(range(len(x)), x, y):
    handled = False  # 规则是否处理掉了这个样本
    got = False  # 是否命中规则
    for rule_id, (r, res) in enumerate(rules):
        if r(ind):
            got = True
            if res == yy:
                handled = True
                right[rule_id] += 1
            else:
                error[rule_id] += 1
            break
    if got:
        got_command += 1
    else:
        ungot_x.append(xx)
        ungot_y.append(yy)
    if not handled:
        bad_x.append(xx)
        bad_y.append(yy)
bad_x = np.array(bad_x)
bad_y = np.array(bad_y)
print("压缩之后", bad_x.shape)
print("误伤", Counter(bad_y))
print("未命中", Counter(ungot_y))
print("误伤分析", error)
print("正确分析", right)
print("未命中规则", len(x) - got_command)
bad_x[bad_x == -1] = 2
bad = np.sum(bad_x * 3 ** np.arange(0, 16), axis=1) * 3 + bad_y
bad = bad.astype(np.int32)
bad.tofile("black_list.bin")


def watch(x, y):
    for xx, yy in zip(x, y):
        print(xx.reshape(4, 4))
        print(yy)
        input()


watch(ungot_x, ungot_y)
watch(bad_x, bad_y)
