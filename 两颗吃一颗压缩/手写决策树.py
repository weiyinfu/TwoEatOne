from 决策树 import DicisionTree
import numpy as np
from sklearn.tree import DecisionTreeClassifier

# 如果用table.bin,1865463,2200000,压缩了40万的数据
#如果用去掉等效结点之后的
a = np.fromfile("2eat1.bin", np.int32)
x = a // 3
y = a % 3
big = np.tile(x, (16, 1)).T
mask = 3 ** np.tile(np.arange(16), (len(x), 1))
x = big // mask % 3
black_cnt = np.count_nonzero(x == 1, axis=1).reshape(-1, 1)
white_cnt = np.count_nonzero(x == 2, axis=1).reshape(-1, 1)
x = np.hstack((x, black_cnt, white_cnt))
# x = x[:20000]
# y = y[:20000]
print("data load over")
tree = DicisionTree(x, y, "c45")
his = DecisionTreeClassifier()
his.fit(x, y)
print("mine", tree.get_node_count())
print("his", his.tree_.node_count)
