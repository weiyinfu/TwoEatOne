import numpy as np
from sklearn import tree
from sklearn.externals import joblib

"""
实践证明，决策树导出之后12M，几乎没有压缩
正确率那肯定是百分之百
"""
a = np.fromfile("res/table.txt", np.int32)
x = a[np.arange(len(a) // 2) * 2]
y = a[np.arange(len(a) // 2) * 2 + 1] % 3
big = np.repeat(x[:, np.newaxis], repeats=16, axis=1)
mask = 3 ** np.repeat(np.arange(16)[np.newaxis, :], repeats=len(x), axis=0)
x = big // mask % 3
print("transform over")
eye = tree.DecisionTreeClassifier()
eye.fit(x, y)
print("train over")
yy = eye.predict(x)
# joblib.dump(eye, "tree.bin", compress=9)
print(eye.tree_.node_count)