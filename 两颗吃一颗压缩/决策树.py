import math
import numpy as np
import pydot

"""
自己实现决策树：无剪枝
"""


class Node:
    def __init__(self, data):
        self.attr = -1  # 当前节点上的划分属性
        self.sons = {}  # 该结点的儿子结点
        self.ans = None  # 该结点的答案，只有叶子节点才有，通过此属性判断是否是叶子节点
        self.data = data  # 数据的下标列表

    def is_leaf(self):
        return self.ans is not None

    def __str__(self):
        return "node_cnt:{} {}".format(len(self.data), "ans:%d" % self.ans if self.ans else "")


class DicisionTree:
    def __init__(self, x, y, creteria="id3"):
        self.x = np.array(x)
        self.y = np.array(y)
        if self.x.dtype not in (np.int, np.int64) or self.y.dtype not in (np.int, np.int64):
            raise Exception("这里的决策树只能处理整数类型")
        self.num_class = len(set(y))
        self.num_attr = len(x[0])
        self.creteria = creteria
        self.root = self._build(list(range(len(self.y))), list(range(self.num_attr)))

    def _split(self, x, attr):
        # 将数据集x按照属性attr的取值分开
        xset = {}
        for i in x:
            v = self.x[i][attr]
            if v not in xset:
                xset[v] = []
            xset[v].append(i)
        return xset

    def _buildTable(self, x, attrs):
        # 按照属性、属性取值、类别三个维度统计元素个数
        table = [{} for _ in range(self.num_attr)]
        for i in x:
            for attr in range(self.num_attr):
                v, c = self.x[i][attr], self.y[i]
                if v not in table[attr]:
                    table[attr][v] = {}
                if c not in table[attr][v]:
                    table[attr][v][c] = 0
                table[attr][v][c] += 1
        return table

    def _id3(self, table):
        # 根据表求id3的值
        aloga = 0
        rlogr = 0
        for v in table:
            r = 0
            for c in table[v]:
                aloga += table[v][c] * math.log(table[v][c])
                r += table[v][c]
            rlogr += r * math.log(r)
        return aloga - rlogr

    def _c45(self, table, tlogt, slogs):
        aloga = 0
        rlogr = 0
        for v in table:
            r = 0
            for c in table[v]:
                aloga += table[v][c] * math.log(table[v][c])
                r += table[v][c]
            rlogr += r * math.log(r)
        return (tlogt - aloga) / (1 if len(table) == 1 else  rlogr - slogs)

    def _gini(self, table):
        gain = 0
        for v in table:
            a2 = 0
            r = 0
            for c in table[v]:
                a2 += table[v][c] ** 2
                r += table[v][c]
            gain += a2 / r
        return gain

    # 只有C45用到了slogs和tlogt，id3和gini都没有用到
    def _c45_tlogt(self, data):
        slogs = len(data) * math.log(len(data))
        cnt = {}
        for i in data:
            y = self.y[i]
            if y not in cnt:
                cnt[y] = 0
            cnt[y] += 1
        tlogt = 0
        for i in cnt:
            tlogt += cnt[i] * math.log(cnt[i])
        return tlogt, slogs

    def _selectAttr(self, x, attrs):
        # 选择属性
        t = self._buildTable(x, attrs)
        ans_attr, ans_gain = None, -0xfffff
        for attr in attrs:
            if self.creteria == "id3":
                gain = self._id3(t[attr])
            elif self.creteria == "gini":
                gain = self._gini(t[attr])
            elif self.creteria == "c45":
                tlogt, slogs = self._c45_tlogt(x)
                gain = self._c45(t[attr], tlogt=tlogt, slogs=slogs)
            else:
                raise Exception("unkown creterial{},the 3 suported creteria are id3,c45,gini".format(self.creteria))
            if ans_gain is None or gain > ans_gain:
                ans_gain = gain
                ans_attr = attr
        return ans_attr

    def _allsame(self, array):
        x = array[0]
        for i in array:
            if x != i: return False
        return True

    def _build(self, data, attrs):
        node = Node(data)
        if self._allsame(self.y[data]) or not attrs:
            node.ans = self.y[data[0]]
            return node
        node.attr = self._selectAttr(data, attrs)
        # print(node.attr, "selected attr")
        attrs.remove(node.attr)
        xset = self._split(data, node.attr)
        for v in xset.keys():
            node.sons[v] = self._build(xset[v], attrs)
        attrs.append(node.attr)  # 将属性复原还给父结点
        return node

    def predict(self, data_x):
        def _predict_one(x):
            node = self.root
            while not node.is_leaf():
                value = x[node.attr]
                if value in node.sons:
                    node = node.sons[value]
                else:
                    break
            if node.is_leaf():
                print(node.ans, node)
                return node.ans
            return None  # 无答案

        return np.array(list(map(_predict_one, data_x)))

    def get_node_count(self):
        def dfs(node):
            cnt = 1
            for i in node.sons:
                cnt += dfs(node.sons[i])
            return cnt

        return dfs(self.root)

    def export_graphviz(self):
        g = pydot.Dot(graph_type="digraph")

        def dfs(node, parent, label):
            if hasattr(dfs, "nodeid"):
                dfs.nodeid += 1
            else:
                dfs.nodeid = 0
            me = pydot.Node(str(dfs.nodeid), label=str(node))
            g.add_node(me)
            if parent is not None:
                g.add_edge(pydot.Edge(parent, me, label=label))
            for k, v in node.sons.items():
                dfs(v, me, "attr{}={}".format(node.attr, k))

        dfs(self.root, None, "")
        g.write("haha.jpg", prog='dot', format="jpg")


if __name__ == '__main__':
    # 增益函数的选取:id3,gini,c45
    gain_f = "id3"
    x = np.array([[0, 3, 0], [0, 2, 1], [1, 1, 2], [1, 2, 2], [2, 3, 0], [2, 1, 1]])
    y = np.array([0, 0, 1, 2, 0, 1])
    tree = DicisionTree(x, y, gain_f)
    ans = tree.predict(x)
    print(ans)
    cnt = np.count_nonzero(y == ans)
    print(cnt)
    print(ans)
    print('正确的个数,正确率', cnt, cnt / len(x))
    print('不确定的个数', len([1 for i in range(len(ans)) if ans[i] == 'not found']))
    print('结点总数', tree.get_node_count())
