using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

class TableAI : AI {
    static Dictionary<int, int> table = new Dictionary<int, int>();
    static TableAI() {
        BinaryReader reader = new BinaryReader(File.Open("table.bin", FileMode.Open));
        long sz = reader.BaseStream.Length / 8;
        while (sz > 0) {
            sz--;
            int k = reader.ReadInt32(), v = reader.ReadInt32();
            table.Add(k, v);
        }
    }
    public int getMove(int[] map, ref int winLosePeace) {
        int state = Util.mapToInt(map);
        int ans = table[state];
        winLosePeace = ans % 3;
        int[] newMap = Util.intToMap(ans / 3);
        return Util.getMove(map, Util.reverse(newMap));
    }
    //查看SearchAI失算的那些棋局
    static public void debug() {
        SearchAI search = new SearchAI();
        foreach (int i in table.Keys) {
            Console.WriteLine(i);
            int ans = table[i] % 3;
            int mine = 0;
            search.getMove(Util.intToMap(i), ref  mine);
            // if ((ans != 2 && mine ==2)||(ans==2&&mine!=2)) {
            if (ans != mine) {
                Console.WriteLine(Util.tos(i) + " " + i + " mine=" + mine + " ans=" + ans);
                Console.ReadKey();
            }
        }
    }
    //测试一个状态需要多少步才能变正确
    static public void debug2() {
        SearchAI search = new SearchAI();
        int state = 2773;
        int[] map = Util.intToMap(state);
        int mine = 0;
        search.getMove(map, ref mine);
        Console.WriteLine(Util.tos(state) + " " + state + " mine=" + mine + " ans=" + table[state] % 3);
    }
}
