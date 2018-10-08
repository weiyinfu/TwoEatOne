如果着法是通过ajax请求来的，那么这个项目就不是一个静态的项目。
而如果要弄成静态的，打表得到的文件太大。
这部分代码所要解决的问题就是压缩表。

最原始的table.bin是一个int数组，这个数组每两个数字是一对。第一个数字表示当前状态，第二个数字表示下一状态和当前状态的类别（胜负和）。
之所以存下来下一状态，是为了让计算机显得招式更加凌厉，尽快解决战斗。
否则的话，计算机虽然是必胜状态，它却不肯向着必胜状态前进。

数据文件2eat1.bin，这是一个32为的int数组。把每个int转换成17位3进制形式，最末位表示该局面的胜负和状态，前面16位表示棋局状态。相当于table.bin中的元素去掉了等价元素，相当于压缩。此文件变为原来的1/8*1/2。

数据文件compress.bin，这是一个使用折线压缩法进行压缩的int数组，把2eat1.bin压缩为了原来的2/5。


给定一个int数组x，将其转化为len(x)行16列的矩阵a。
a\[i]\[j]表示第i个数字转化为3进制之后第j位的值。

如果用python中的列表推导式，会非常缓慢：
```python
# 下面这种写法效率非常低
# x = np.array(list(map(lambda n: [n // (3 ** i) % 3 for i in range(16)], x)))
```
使用Numpy则非常快速
```python
big = np.repeat(x[:, np.newaxis], repeats=16, axis=1)
mask = 3 ** np.repeat(np.arange(16)[np.newaxis, :], repeats=len(x), axis=0)
x = big // mask % 3
```
使用np.tile函数也是可以的
```python
big=np.tile(x,(16,1)).T
mask=3**np.tile(np.arange(16),(len(x),1))
```

获取决策树的结构：
http://scikit-learn.org/stable/auto_examples/tree/plot_unveil_tree_structure.html

sklearn中的决策树有两种：entropy和gini。其中entropy是C4.5算法。
sklearn的决策树一定是二叉树，因为它把全部属性当成一样的。


虽然状态+分类可以使计算机处于不败地位，但是也不一定能让计算机走向胜利。
因为计算机在胜利的状态上来回踱步，却并不肯向着胜利多走一步。导致看上
去像和棋一样。也就是说，计算机虽然能够胜利，却不够犀利。
