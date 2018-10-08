using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;
/*精灵类：提供棋子图片和棋盘图片
 */
public static class Spirite {
    public static Bitmap[] chess = new Bitmap[3] { null, new Bitmap(Image.FromFile("black.bmp")), new Bitmap(Image.FromFile("white.bmp")) };
    public static Bitmap board = new Bitmap(550, 550);
    static Spirite() {
        chess[1].MakeTransparent(Color.White);
        chess[2].MakeTransparent(Color.White);
        Graphics.FromImage(board).Clear(Color.Chocolate);
        for (int i = 0; i < 4; i++) {
            Graphics.FromImage(board).DrawLine(new Pen(Color.Black, 10), new Point(50, 50 + i * 150), new Point(500, 50 + i * 150));
            Graphics.FromImage(board).DrawLine(new Pen(Color.Black, 10), new Point(50 + i * 150, 50), new Point(50 + i * 150, 500));
        }
    }
}