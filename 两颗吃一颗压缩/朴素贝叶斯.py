import numpy as np
from sklearn import naive_bayes
from sklearn.externals import joblib
import collections

"""
实践证明，朴素贝叶斯导出之后非常小，但是正确率却很低
"""
a = np.fromfile("2eat1.bin", np.int32)
print(len(a))
x = a // 3
y = a % 3
big = np.repeat(x[:, np.newaxis], 16, axis=1)
mask = np.repeat(3 ** np.arange(16)[np.newaxis, :], len(x), axis=0)
x = big // mask % 3
print("transform over")
eye = naive_bayes.BernoulliNB()
eye.fit(x, y)
yy = eye.predict(x)
print(np.count_nonzero(yy == y), len(y))
# joblib.dump(eye, "tree.bin", compress=9)
