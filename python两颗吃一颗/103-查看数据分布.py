from matplotlib import pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

a = np.fromfile("2eat1.bin", np.int)
x = a // 3
y = a % 3


def 一维显示():
    global x, y
    x = x[:100]
    y = y[:100]
    z = y
    plt.scatter(x[z == 2], y[z == 2], c="r")
    plt.scatter(x[z == 1], y[z == 1], c='y')
    plt.scatter(x[z == 0], y[z == 0], c='b')
    plt.ylim(0, 3)
    plt.show()


def pca_2d():
    global x, y
    mask = 3 ** np.tile(np.arange(16), (len(x), 1))
    x = np.tile(x, (16, 1)).transpose() // mask % 3
    # PCA降维到二维空间进行显示
    pca = PCA(2, whiten=True)
    x = x[:100]
    y = y[:100]
    x = pca.fit_transform(x, y)
    fig, axes = plt.subplots(2, 2)
    axes = axes.ravel()
    axes[2].scatter(x[y == 2, 0], x[y == 2, 1], c='r', s=50)
    axes[1].scatter(x[y == 1, 0], x[y == 1, 1], c="y", s=50)
    axes[0].scatter(x[y == 0, 0], x[y == 0, 1], c="b", s=50)
    axes[3].scatter(x[y == 2, 0], x[y == 2, 1], c='r', s=50)
    axes[3].scatter(x[y == 1, 0], x[y == 1, 1], c="y", s=50)
    axes[3].scatter(x[y == 0, 0], x[y == 0, 1], c="b", s=50)
    plt.show()


pca_2d()
print(np.count_nonzero(y == 1))
print(np.count_nonzero(y == 2))
print(np.count_nonzero(y == 0))
