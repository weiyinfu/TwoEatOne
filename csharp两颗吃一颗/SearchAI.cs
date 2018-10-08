using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
/*记录搜索过的结点，这样就能够避免重复扩展，提高效率
 * 每个Node有Value和Depth两个属性
 * Depth越浅说明评估地越准确
 */
class NodeValueDepth {
    public int value;
    public int depth;
}
class SearchAI : AI {
    const int MAX_DEPTH = 10;//搜索的深度
    const int MIN_VALUE = -100, MAX_VALUE = 100;//局面的最大值和最小值
    static int[] dir = { 1, 0, -1, 0, 0, 1, 0, -1 };//四个方向
    static Random random = new Random();//随机数
    const int HashSize = 42777721;
    //每次不清空字典，随着搜索次数的增多，搜索速度会越来越快，因为命中率越来越高
    NodeValueDepth[] dic = new NodeValueDepth[HashSize];
    List<int> bestMoves = new List<int>();
    int go(int[] map, int fatherValue, int depth) {
        //if (depth == 1)
        //    Console.WriteLine(Util.tos(map) + depth);
        int black = 0, white = 0;
        int id = 0;
        int pow = 1;
        for (int i = 0; i < 16; i++) {
            if (map[i] == 1) { black++; id += pow; }
            if (map[i] == 2) { white++; id += (pow << 1); }
            pow = (pow << 1) + pow;
        }
        if (black < 2) {
            return MIN_VALUE + depth;
        }
        if (white < 2) {
            return MAX_VALUE + depth;
        }

        if (depth == MAX_DEPTH) { //这个地方不能返回0，否则会影响搜索的质量
            return black - white;
        }
        /*因为NodeValueDepth字典中没有存储着法
         *所以在根结点处必须展开而不能直接返回*/
        if (depth > 0 && dic[id] != null && dic[id].depth <= depth) {
            return dic[id].value;
        }

        int minSonValue = MAX_VALUE + MAX_DEPTH;//取最大值，慢慢变小
        for (int i = 0; i < 16; i++) {
            if (map[i] != 1) continue;
            int m = i / 4, n = i % 4;
            for (int j = 0; j < 4; j++) {
                int x = m + dir[j << 1], y = n + dir[j << 1 | 1];
                if (!Util.legal(x, y) || map[x * 4 + y] != 0) continue;
                map[x * 4 + y] = 1;
                map[i] = 0;
                int xx = map[x * 4] * 27 + map[x * 4 + 1] * 9 + map[x * 4 + 2] * 3 + map[x * 4 + 3];
                int yy = map[y] * 27 + map[y + 4] * 9 + map[y + 8] * 3 + map[y + 12];
                int[] son = Util.reverse(map);
                map[i] = 1;
                map[x * 4 + y] = 0;
                switch (xx) {
                    case 66: son[x * 4] = 0; break;
                    case 22: son[x * 4 + 1] = 0; break;
                    case 42: son[x * 4 + 2] = 0; break;
                    case 14: son[x * 4 + 3] = 0; break;
                }
                switch (yy) {
                    case 66: son[y] = 0; break;
                    case 22: son[y + 4] = 0; break;
                    case 42: son[y + 8] = 0; break;
                    case 14: son[y + 12] = 0; break;
                }
                int sonValue = go(son, -minSonValue, depth + 1);
                if (sonValue <= minSonValue) {
                    if (depth == 0) {
                        if (sonValue < minSonValue) {
                            bestMoves.Clear();
                        }
                        bestMoves.Add(i * 16 + x * 4 + y);
                    }
                    minSonValue = sonValue;
                }
                /*如果minSonValue等于fatherValue，那么当前结点一定不会改良父结点，
                 * 但是如果这时返回minSonValue，有可能
                 * 父结点把当前结点当做最优解之一，而实际上当前结点可能还有更小的minsonValue，
                 * 这就使得父结点走了一步错棋。
                 * 如果这时不返回，则剪枝少，影响效率
                 * 
                 * 如果minSonValue等于fatherValue，求之无益,
                 * 此时一定不能返回minSonValue，
                 * 否则这个结点会被加入到父结点的最优着法列表中去。
                 * 而实际上，这个结点有可能对父结点非常不利，因为已经不利到剪枝了！
                 * 将本结点当做必胜态（也就是MaxValue），从而让父结点一定不选这个剪枝了的结点
                 * 
                 * 如果等于的时候返回max_value，父结点必然会忽略这个结点，而实际上，这个结点完全有可能也是最优着法，
                 * 但是它没有加入到父结点的最优着法列表中去。
                 * 但是，父结点不差优秀的儿子，这个儿子再吊炸天也只能并列第一
                 */
                if (minSonValue < fatherValue || (minSonValue == fatherValue && depth > 1))
                    return MAX_VALUE + MAX_DEPTH;
            }
        }
        if (dic[id] == null) {
            dic[id] = new NodeValueDepth();
        }
        dic[id].depth = depth;
        dic[id].value = -minSonValue;
        return -minSonValue;
    }
    public int getMove(int[] map, ref int result) {
        bestMoves.Clear();
        int res = go(map, MIN_VALUE, 0);
        if (res <= MIN_VALUE + MAX_DEPTH) result = 2;
        else if (res >= MAX_VALUE) result = 1;
        else result = 0;
        if (bestMoves.Count == 0) {
            return -1;
        } else {
            return bestMoves[random.Next(bestMoves.Count)];
        }
    }
}