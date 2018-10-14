import numpy as np
from sklearn.tree import DecisionTreeClassifier

import data

x, y = data.get_data(shuffle=False, one_hot=False)
feature = np.fromfile("feature.bin", np.int32).reshape(len(x), -1)
black_chess_count = feature[:, 0]
white_chess_count = feature[:, 1]
black_space_count = feature[:, 2]
white_space_count = feature[:, 3]
black_dis = feature[:, 4]
white_dis = feature[:, 5]

rules = np.array([
    black_chess_count - white_chess_count,
    black_space_count - white_space_count,
    black_dis - white_dis
]).T
print(x.shape, feature.shape, rules.shape)
x = np.hstack((x, feature, rules))
print(x.shape)
his = DecisionTreeClassifier()
his.fit(rules, y)
print("his", his.tree_.node_count)
yy = his.predict(rules)
print(np.count_nonzero(yy == y))
"""
决策树需要1185条规则才能够建立起64885的黑名单
(284885, 16) (284885, 6) (284885, 3)
(284885, 25)
his 1185
220815
"""
