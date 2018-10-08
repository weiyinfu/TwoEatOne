using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Drawing;
using System.Media;
//总是黑棋先走
/*对于只初始化一次的东西，放在构造函数中；
 * 对于初始化多次的东西，放在init函数中
 */
class MyForm : BaseForm {
    //0空着，1为黑棋AI，2为白棋AI
    AI[] ai = { null, null, new SearchAI() };
    int gameState = 0;
    int userChess;//不要在这里赋值
    int whoseTurn;//不要在这里赋值
    string initState = "2222000000001111";
    //string initState = "0121120000000000";
    //string initState = "0000000012211000";
    Timer laterTimer = new Timer();
    Timer thinkTimer = new Timer();
    System.Threading.Thread computerThread;
    public MyForm() {
        laterTimer.Interval = 1000;
        laterTimer.Tick += delegate {
            laterTimer.Stop();
            thinkTimer.Start();
            if (ai[whoseTurn] != null) {
                computerThread = new System.Threading.Thread(() => {
                    computer();
                });
                computerThread.Start();
            }
        };
        thinkTimer.Interval = 105000;
        thinkTimer.Tick += delegate {
            thinkTimer.Stop();
            if (computerThread != null && computerThread.IsAlive) {
                computerThread.Abort();
            }
            timeOver(whoseTurn);
        };
        if (ai[1] == null || ai[2] == null) {
            MouseClick += clk;
            userChess = ai[1] == null ? 1 : 2;
        }
        init();
    }
    override protected void init() {
        isMoving = oldPlace = newPlace = -1;
        map = Util.stringToMap(initState);
        new SoundPlayer("start.wav").Play();
        whoseTurn = 1;
        laterTimer.Start();
    }
    void clk(object o, MouseEventArgs e) {
        if (whoseTurn != userChess) return;
        int x = (int)Math.Round((e.Y - 50.0) / 150), y = (int)Math.Round((e.X - 50.0) / 150);
        if (Util.dis(x * 150 + 50, y * 150 + 50, e.Y, e.X) > 40) return;
        int i = x * 4 + y;
        if (i < 0 || i >= 16) return;
        if (map[i] == 3 - userChess) return;
        if (map[i] == userChess) {
            if (isMoving == -1) {
                isMoving = i;
            } else {
                if (isMoving == i) {
                    isMoving = -1;
                } else {
                    isMoving = i;
                }
            }
            draw();
        } else if (map[i] == 0) {
            if (isMoving != -1) {
                submitMove((isMoving << 4) + i);
            }
        }
    }
    void computer() {
        int[] aiMap = map;
        if (whoseTurn == 2) {
            aiMap = Util.reverse(map);
        }
        int temp = gameState;
        int nextMove = ai[whoseTurn].getMove(aiMap, ref gameState);
        if (whoseTurn == 2) {
            if (gameState != 0)
                gameState = 3 - gameState;
        }
        this.Invoke(new Action(delegate {
            if (gameState == 1 && temp == 0) {
                new SoundPlayer("lose.wav").PlaySync();
            }
            submitMove(nextMove);
        }));
    }
    //这个函数被调用时必须作为函数的最后一句话
    void submitMove(int nextMove) {
        thinkTimer.Stop();
        if (Util.isMoveLegal(nextMove, map, whoseTurn)) {
            move(nextMove / 16, nextMove % 16);
            int nowState = getGameState(map);
            if (nowState != 0) {
                gameOver(nowState);
            } else {
                whoseTurn = 3 - whoseTurn;
                laterTimer.Start();
            }
        } else {
            moveIllegal(whoseTurn);
        }
    }
}