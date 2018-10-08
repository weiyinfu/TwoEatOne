using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

class Util {
    public static int[] stringToMap(string s) {
        int[] map = new int[16];
        for (int i = 0; i < 16; i++) {
            map[i] = s[i] - '0';
        }
        return map;
    }
    public static int stringToInt(string s) {
        return mapToInt(stringToMap(s));
    }

    public static int[] reverse(int[] map) {
        int[] ans = new int[16];
        for (int i = 0; i < 16; i++) if (map[i] != 0) ans[i] = 3 - map[i];
        return ans;
    }
    public static int reverse(int x) {
        int ans = x;
        for (int i = 0; i < 16; i++) {
            if (x % 3 == 1) ans += (int)Math.Pow(3, i);
            if (x % 3 == 2) ans -= (int)Math.Pow(3, i);
        }
        return ans;
    }
    public static int mapToInt(int[] map) {
        int ans = 0;
        for (int i = 0; i < 16; i++) ans += (int)Math.Pow(3, i) * map[i];
        return ans;
    }
    public static int[] intToMap(int x) {
        int[] map = new int[16];
        for (int i = 0; i < 16; i++) map[i] = (x % (int)Math.Pow(3, i + 1)) / (int)Math.Pow(3, i);
        return map;
    }
    public static string tos(int[] map) {
        StringBuilder ans = new StringBuilder();
        for (int i = 0; i < 16; i++) {
            ans.Append(map[i]);
            if (i % 4 == 3) {
                ans.Append("\n");
            }
        }
        ans.Append("===========");
        return ans.ToString();
    }
    public static string tos(int state) {
        return tos(intToMap(state));
    }
    public static bool legal(int x, int y) {
        return x >= 0 && y >= 0 && x < 4 && y < 4;
    }
    public static double dis(double fx, double fy, double tx, double ty) {
        return Math.Sqrt(Math.Pow(fx - tx, 2) + Math.Pow(fy - ty, 2));
    }
    public static int getMove(int[] oldMap, int[] newMap) {
        int oldPlace = -1, newPlace = -1;
        for (int i = 0; i < 16; i++)
            if (newMap[i] == 0 && oldMap[i] == 1) oldPlace = i;
            else if (newMap[i] == 1 && oldMap[i] == 0) newPlace = i;
        return oldPlace * 16 + newPlace;
    }
    public static bool isMoveLegal(int move, int[] map, int chess) {
        int oldPlace = move / 16, newPlace = move % 16;
        if (oldPlace < 0 || newPlace < 0 || oldPlace > 15 || newPlace > 15) return false;
        if (dis(oldPlace / 4, oldPlace % 4, newPlace / 4, newPlace % 4) > 1) return false;
        if (map[oldPlace] != chess || map[newPlace] != 0) return false;
        return true;
    }
}