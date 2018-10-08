using System;
using System.Windows.Forms;
using System.Drawing;
using System.IO;
using System.Media;
using System.Collections;
using System.Collections.Generic;
abstract class BaseForm : Form {
    protected int[] map = new int[16];
    protected int newPlace = -1;//去往的地方
    protected int oldPlace = -1;//移动之前的位置
    protected int isMoving = -1;

    int animationTicks = 0;
    Timer animationTimer = new Timer();
    protected BaseForm() {
        animationTimer.Interval = 100;
        animationTimer.Tick += delegate { animationDraw(); };
        MaximizeBox = MinimizeBox = false;
        ClientSize = new Size(550, 550);
        Text = "两颗吃一颗";
        Paint += delegate { draw(); };
        FormClosed += delegate {
            Application.Exit();
        };
    }
    protected abstract void init();

    protected void gameOver(int gameResult) {
        new SoundPlayer("over.wav").Play();
        DialogResult res = MessageBox.Show((gameResult == 1 ? "黑棋" : "白棋") + "赢了", "对局结果", MessageBoxButtons.RetryCancel);
        if (res == DialogResult.Cancel) {
            Application.Exit();
        } else {
            init();
            draw();
        }
    }
    protected void moveIllegal(int who) {
        new SoundPlayer("over.wav").Play();
        DialogResult res = MessageBox.Show((who == 1 ? "黑棋" : "白棋") + "走了不合法的棋，重开一局？", "对局结果", MessageBoxButtons.RetryCancel);
        if (res == DialogResult.Cancel) {
            Application.Exit();
        } else {
            init();
            draw();
        }
    }
    protected void timeOver(int who) {
        new SoundPlayer("over.wav").Play();
        DialogResult res = MessageBox.Show((who == 1 ? "黑棋" : "白棋") + "超时，重开一局？", "对局结果", MessageBoxButtons.RetryCancel);
        if (res == DialogResult.Cancel) {
            Application.Exit();
        } else {
            init();
            draw();
        }
    }
    protected int getGameState(int[] map) {
        int black = 0, white = 0;
        for (int i = 0; i < 16; i++) {
            if (map[i] == 1) black++;
            if (map[i] == 2) white++;
        }
        if (black == 1) return 2;
        else if (white == 1) return 1;
        else return 0;
    }
    protected void move(int oldPos, int newPos) {
        newPlace = newPos;
        oldPlace = oldPos;
        isMoving = -1;
        map[newPlace] = map[oldPlace];
        map[oldPlace] = 0;
        this.Invoke(new Action(delegate {
            animationTimer.Start();
        }));
        new SoundPlayer("move.wav").PlaySync();
        checkDie(newPos / 4, newPos % 4);
    }
    void checkDie(int x, int y) {
        int[] tempMap = map;
        if (map[x * 4 + y] == 2) {
            tempMap = Util.reverse(map);
        }
        int xx = tempMap[x * 4] * 27 + tempMap[x * 4 + 1] * 9 + tempMap[x * 4 + 2] * 3 + tempMap[x * 4 + 3];
        int yy = tempMap[y] * 27 + tempMap[y + 4] * 9 + tempMap[y + 8] * 3 + tempMap[y + 12];
        bool hasDie = false;
        switch (xx) {
            case 66: map[x * 4] = 0; hasDie = true; break;
            case 22: map[x * 4 + 1] = 0; hasDie = true; break;
            case 42: map[x * 4 + 2] = 0; hasDie = true; break;
            case 14: map[x * 4 + 3] = 0; hasDie = true; break;
        }
        switch (yy) {
            case 66: map[y] = 0; hasDie = true; break;
            case 22: map[y + 4] = 0; hasDie = true; break;
            case 42: map[y + 8] = 0; hasDie = true; break;
            case 14: map[y + 12] = 0; hasDie = true; break;
        }
        if (hasDie) new SoundPlayer("die.wav").Play();
    }
    void animationDraw() {
        animationTicks++;
        if (animationTicks == 5) {
            animationTicks = 0;
            animationTimer.Stop();
            draw();
            return;
        }
        Bitmap bit = new Bitmap(Spirite.board);
        for (int i = 0; i < 4; i++)
            for (int j = 0; j < 4; j++) {
                if (newPlace == i * 4 + j) continue;
                if (map[i * 4 + j] != 0)
                    Graphics.FromImage(bit).DrawImage(Spirite.chess[map[i * 4 + j]], new Rectangle(50 + j * 150 - 25, 50 + i * 150 - 25, 50, 50));
            }
        int oldx = 50 + (oldPlace % 4) * 150;
        int oldy = 50 + (oldPlace / 4) * 150;
        int newx = 50 + (newPlace % 4) * 150;
        int newy = 50 + (newPlace / 4) * 150;
        int nowx = oldx + (newx - oldx) / 5 * animationTicks;
        int nowy = oldy + (newy - oldy) / 5 * animationTicks;
        Graphics.FromImage(bit).DrawImage(Spirite.chess[map[newPlace]], new Rectangle(nowx - 25, nowy - 25, 50, 50));
        CreateGraphics().DrawImage(bit, 0, 0);
    }
    protected void draw() {
        Bitmap bit = new Bitmap(Spirite.board);
        for (int i = 0; i < 4; i++)
            for (int j = 0; j < 4; j++) {
                if (isMoving == i * 4 + j) {
                    Graphics.FromImage(bit).DrawImage(Spirite.chess[map[isMoving]], new Rectangle(50 + j * 150 - 35, 50 + i * 150 - 35, 70, 70));
                    continue;
                }
                if (newPlace == i * 4 + j) {
                    Graphics.FromImage(bit).DrawRectangle(new Pen(Color.Red, 5), new Rectangle(50 + j * 150 - 30, 50 + i * 150 - 30, 60, 60));
                }
                if (oldPlace == i * 4 + j) {
                    Graphics.FromImage(bit).DrawEllipse(new Pen(Color.CadetBlue, 4), new Rectangle(50 + j * 150 - 25, 50 + i * 150 - 25, 50, 50));
                }
                if (map[i * 4 + j] != 0)
                    Graphics.FromImage(bit).DrawImage(Spirite.chess[map[i * 4 + j]], new Rectangle(50 + j * 150 - 25, 50 + i * 150 - 25, 50, 50));
            }
        CreateGraphics().DrawImage(bit, 0, 0);
    }
}