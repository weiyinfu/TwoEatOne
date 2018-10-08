#include<iostream>
#include<time.h>
#include<fstream> 
#include<stdlib.h>
using namespace std;
/*
众子皆胜我必败,破罐破摔可乱走
一子为败我必胜，取此败子
否则必为和棋，取一非胜子

胜利1黑子1
失败2白子2
平局0空白0
*/
int power[16];//3的幂
const int qsz = 3e6;//自定义队列
struct Queue{
	int a[qsz];
	int head, rear;
	void init(){
		head = 0;
		rear = 0;
	}
	void enq(int x){
		a[rear] = x;
		rear++;//用rear=(rear+1)%qsz效率更低，因为每次入队都要做除法
		if (rear == qsz)rear = 0;
	}
	int deq(){
		int temp = a[head];
		head++;
		if (head == qsz)head = 0;
		return temp;
	}
	bool empty(){
		return head == rear;
	}
};
//自定义链表
struct ancestor{
	int name;
	ancestor*next;
};
//状态结点
struct node{
	int winSons;//胜利儿子的个数
	int sonSize;//儿子的个数
	ancestor *father;//谁能到达这个结点
	int how;//本结点是胜1是负2还是平0
	int nextState;//若可胜利，下一状态为何？若不能胜利，就得瞎走一步；若为和棋，如何走才能继续保持和棋
	void init(){
		winSons = 0;
		sonSize = 0;
		father = new ancestor();
		how = 0;//和态
		nextState = 0;
	}
	void addfather(int f){
		ancestor *temp = new ancestor();
		temp->name = f;
		temp->next = father->next;
		father->next = temp;
	}
};
//一次性开辟空间，避免使用指针
node nodes[2300000];
int nodesIndex = 0;
node*newNode(){
	return &nodes[nodesIndex++];
}
//定义哈希表
const int HashSize = 42777721;
node* a[HashSize] = { 0 };
int table[HashSize];
Queue q;//用于存储已经确定状态的结点
Queue Q;//用于广度优先搜索
const int dir[4][2] = { 0, 1, 1, 0, -1, 0, 0, -1 };

void calpower(){//计算3的幂
	int  j = 1;
	for (int i = 0; i < 16; i++){
		power[i] = j;
		j *= 3;
	}
}
/*打印状态，用于调试结点
*/
void print(int state){
	cout << "===========" << endl;
	int array[16];
	for (int i = 0; i < 16; i++){
		array[i] = state % 3;
		state /= 3;
	}
	for (int i = 0; i < 16; i++)
	{
		if (array[i] == 2)cout << " @";
		else if (array[i] == 1)cout << " *";
		else cout << " -";
		if (i % 4 == 3)cout << endl;
	}
}
/*
函数名称：void init（）
函数功能：对全部结点进行初始化
1.看结点是否合格
2.看结点是否为必胜或者必败，若是，进队
3.构造图形，建立结点之间的联系
*/
void init(){
	cout << "init() " << time(0) << endl;
	//用map直接记录棋盘状态，不用把int转换成棋盘状态，每次更改时直接更改棋盘状态,避免了将int值映射成map[16]的过程。这个过程模拟的是3进制数字串递增的过程
	int map[16] = { 0 };
	int black = 0, white = 0;
	int blackPos[4];
	for (int i = 1; i <= 42777720; i++){
		int j;
		for (j = 0; map[j] == 2; j++){
			map[j] = 0;
			white--;
		}
		map[j]++;
		if (map[j] == 2){
			black--;
			white++;
		}
		else if (map[j] == 1)black++;

		//如果黑白双方皆只剩1子，这是不可能出现的
		if (black < 2 && white < 2)continue;
		//或者有一方大于4那就continue,这也是不可能出现的
		if (black>4 || white>4)continue;

		if (a[i] == 0){//如果未曾访问a[i]结点，那就创建这个节点
			a[i] = new node();
			a[i]->init();
		}
		/*判断有没有输，如果有棋子变成1，说明输了，那就加入到队列中去
		游戏终止条件在这里设置：如果全部杀光算赢,那么剩余0子时可以判定
		如果丧失战斗力算输，那么剩余1子时可以判定
		*/
		if (black == 1){//黑子丧失战斗力，输了
			a[i]->how = 2;
			q.enq(i);
			continue;
		}
		if (white == 1){//白子输了
			a[i]->how = 1;
			q.enq(i);
			continue;
		}
		int state = i;
		bool canMove = 0;//黑子无法移动，憋死也算一种死法
		int t = 0;
		//根据map构建儿子的state，需要进行颜色翻转，颜色反转的过程如下
		for (j = 0; j < 16; j++){
			if (map[j] == 2)state -= power[j];
			else if (map[j] == 1){ state += power[j]; blackPos[t++] = j; }
		}
		int temp = state;
		/*对于棋盘上的全部黑子，考虑上下左右四种走法
		如果考虑夹死，憋死等规则需要在下面修改
		*/
		for (t = 0; t < black; t++){
			j = blackPos[t];
			if (map[j] != 1)continue;//只考虑移动黑子
			int m = j / 4, n = j % 4;//白子的行和列
			for (int k = 0; k < 4; k++){//考虑这个棋子的四个方向
				int x = m + dir[k][0], y = n + dir[k][1];
				if (x < 0 || y < 0 || x >= 4 || y >= 4)continue;
				if (map[x * 4 + y] != 0)continue;
				canMove = true;
				state = temp - power[j] * 2 + power[x * 4 + y] * 2;//移动之后状态值改变
				map[j] = 0, map[x * 4 + y] = 1;//移动之后，棋盘改变
				/**为了描述当前黑子所在的行和列，可以将当前行和列的状态映射为一个4位3进制数字。这些全部状态中只有一部分是需要研究的（也就是发生吃子的）
				*/
				int xx = map[x * 4 + 0] * 27 + map[x * 4 + 1] * 9 + map[x * 4 + 2] * 3 + map[x * 4 + 3];//当前行值
				int yy = map[y] * 27 + map[y + 4] * 9 + map[y + 8] * 3 + map[y + 12];//当前列值
				/*四种吃子的状态：@**_,_@**,_**@,**@_
				*/
				switch (xx){
				case 66:state -= power[x * 4 + 0]; break;
				case 22:state -= power[x * 4 + 1]; break;
				case 42:state -= power[x * 4 + 2]; break;
				case 14:state -= power[x * 4 + 3]; break;
				}
				switch (yy){
				case 66:state -= power[y + 0]; break;
				case 22:state -= power[y + 4]; break;
				case 42:state -= power[y + 8]; break;
				case 14:state -= power[y + 12]; break;
				}
				a[i]->sonSize++;
				if (a[state] == 0){//如果未曾访问这个节点，那就初始化它
					a[state] = newNode();
					a[state]->init();
				}

				a[state]->addfather(i);
				//复位，准备下次循环
				map[j] = 1; map[x * 4 + y] = 0;
			}
		}
		//如果各个棋子都无法移动，那就只能认输
		if (canMove == 0){
			q.enq(i);
			a[i]->how = 2;
		}
	}
	cout << " init() over " << time(0) << endl;
}
/*初始化图有两种方法：从初始状态进行广度优先搜索；按照哈希值逐个访问
*/
void init2(){
	cout << "init2() " << time(0) << endl;
	int initNodeName = 21257720;
	Q.enq(initNodeName);
	a[initNodeName] = newNode();
	a[initNodeName]->init();
	int blackPos[4], black, white;
	int map[16];
	while (Q.empty() == false){
		int id = Q.deq();
		node*now = a[id];
		int state = id;
		black = white = 0;
		int temp = id;
		for (int i = 0; i < 16; i++){
			map[i] = temp % 3;
			temp /= 3;
			if (map[i] == 1){
				blackPos[black] = i;
				black++;
				state += power[i];
			}
			else if (map[i] == 2){
				white++;
				state -= power[i];
			}
		}
		if (black == 1){
			q.enq(id);
			now->how = 2;
			continue;
		}
		if (white == 1){
			q.enq(id);
			now->how = 1;
			continue;
		}
		bool canMove = false;
		temp = state;
		for (int t = 0; t < black; t++){
			int j = blackPos[t];
			if (map[j] != 1)continue;//只考虑移动黑子
			int m = j / 4, n = j % 4;//白子的行和列
			for (int k = 0; k < 4; k++){//考虑这个棋子的四个方向
				int x = m + dir[k][0], y = n + dir[k][1];
				if (x < 0 || y < 0 || x >= 4 || y >= 4)continue;
				if (map[x * 4 + y] != 0)continue;
				canMove = true;
				state = temp - power[j] * 2 + power[x * 4 + y] * 2;//移动之后状态值改变
				map[j] = 0, map[x * 4 + y] = 1;//移动之后，棋盘改变
				int xx = map[x * 4 + 0] * 27 + map[x * 4 + 1] * 9 + map[x * 4 + 2] * 3 + map[x * 4 + 3];//当前行值
				int yy = map[y] * 27 + map[y + 4] * 9 + map[y + 8] * 3 + map[y + 12];//当前列值
				/*四种吃子的状态：@**_,_@**,_**@,**@_
				*/
				switch (xx){
				case 66:state -= power[x * 4 + 0]; break;
				case 22:state -= power[x * 4 + 1]; break;
				case 42:state -= power[x * 4 + 2]; break;
				case 14:state -= power[x * 4 + 3]; break;
				}
				switch (yy){
				case 66:state -= power[y + 0]; break;
				case 22:state -= power[y + 4]; break;
				case 42:state -= power[y + 8]; break;
				case 14:state -= power[y + 12]; break;
				}
				a[id]->sonSize++;
				if (a[state] == 0){//如果未曾访问这个节点，那就初始化它
					a[state] = newNode();
					a[state]->init();
					Q.enq(state);
				}

				a[state]->addfather(id);
				//复位，准备下次循环
				map[j] = 1; map[x * 4 + y] = 0;
			}
		}
		//如果各个棋子都无法移动，那就只能认输
		if (canMove == 0){
			q.enq(id);
			a[id]->how = 2;
		}
	}
	cout << "init2() over " << time(0) << endl;
}
/*处理已经确定状态的结点，更新它们的父节点，一旦父节点也变成确定状态，则将之入队
对于我的状态：
2：如果我父为1，则罢；否则我父=1
1：如果我父为-1（不确定状态），则更新我父胜子数；否则罢
因为队列里面要么为1态要么为2态，不可能含有0态，也就是和棋状态是无法判断的，此队列中只能存放必胜态和必败态
这个函数里讨论结点为0状态没有意义，因为0态儿子不可能使父节点确定化，也就不可能使父节点进栈。而最开始栈里面没有0态，只有0态才能产生0态。
*/
void go(){
	while (q.empty() == false){
		int temp = q.deq();
		if (a[temp]->how == 2){
			for (ancestor *anc = a[temp]->father->next; anc != 0; anc = anc->next){
				//如果父节点已经遇见了一个败子，那么父节点必胜，不必再访问
				if (a[anc->name]->how == 1)continue;
				a[anc->name]->how = 1;//我为败子，父节点必胜，以后不再更新之
				q.enq(anc->name);
				a[anc->name]->nextState = temp;
			}
		}
		else if (a[temp]->how == 1){
			for (ancestor*anc = a[temp]->father->next; anc != 0; anc = anc->next){
				if (a[anc->name]->how != 0)continue;
				a[anc->name]->winSons++;//胜子数
				if (a[anc->name]->winSons == a[anc->name]->sonSize){
					//众子皆胜我必败
					a[anc->name]->how = 2;
					q.enq(anc->name);
					a[anc->name]->nextState = temp;
				}
			}
		}
	}
}
int reverse(int x){ 
	int ans = x;
	for (int i = 0; i < 16; i++){
		if (x % 3 == 1)ans += power[i];
		if (x % 3 == 2)ans -= power[i]; 
	}
	return ans;
}
//如果结点为胜利状态，至多需要多少步才能胜利
void getMaxDepthIfWin(){
	int maxDepth = 0;
	for (int i = 0; i < HashSize; i++){
		if (a[i] == 0)continue;
		if (a[i]->how != 1)continue;
		int j = i;
		int cnt = 0;
		while (1){
			cnt++;
			j = a[j]->nextState;
			j = reverse(j);
			if (j<0 || j >= HashSize)break;
			if (a[j] == 0)break;
		}
		if (cnt > maxDepth){
			maxDepth = cnt;
			print(i);
			printf("need %d steps to win\n", maxDepth);
		}
	}
} 
/*统计个数*/
void checkResult(){
	int r[3] = { 0 };
	for (int i = 0; i < HashSize; i++){
		if (a[i]){
			r[a[i]->how]++;
		}
	}
	printf("win:%d lose:%d peace:%d sum:%d\n", r[1], r[2], r[0], r[0] + r[1] + r[2]);
}
/*计算和态的下一步应该怎么走
*/
int peaceNext(int i){
	int state = i;
	int map[16];
	int j, k;
	for (j = 0; j < 16; j++){
		map[j] = i % 3;
		i /= 3;
	}
	int dir[4][2] = { 0, 1, 1, 0, -1, 0, 0, -1 };
	int x, y, m, n;
	for (j = 0; j < 16; j++){
		if (map[j] == 2)state -= power[j];
		else if (map[j] == 1)state += power[j];
	}
	int temp = state;
	for (j = 0; j < 16; j++){
		if (map[j] != 1)continue;
		m = j / 4; n = j % 4;
		for (k = 0; k < 4; k++){
			x = m + dir[k][0]; y = n + dir[k][1];
			if (x < 0 || y < 0 || x >= 4 || y >= 4)continue;
			if (map[x * 4 + y] != 0)continue;
			state = temp - power[j] * 2 + power[x * 4 + y] * 2;
			map[j] = 0; map[x * 4 + y] = 1;
			int xx = map[x * 4 + 0] * 27 + map[x * 4 + 1] * 9 + map[x * 4 + 2] * 3 + map[x * 4 + 3];
			int yy = map[y] * 27 + map[y + 4] * 9 + map[y + 8] * 3 + map[y + 12];
			switch (xx){
			case 66:state -= power[x * 4 + 0]; break;
			case 22:state -= power[x * 4 + 1]; break;
			case 42:state -= power[x * 4 + 2]; break;
			case 14:state -= power[x * 4 + 3]; break;
			}
			switch (yy){
			case 66:state -= power[y + 0]; break;
			case 22:state -= power[y + 4]; break;
			case 42:state -= power[y + 8]; break;
			case 14:state -= power[y + 12]; break;
			}
			map[j] = 1; map[x * 4 + y] = 0;
			if (a[state]->how == 0)return state;
		}
	}
	return -1;
}
//确定和棋状态的下一步该走什么
void peace(){
	int i;
	for (i = 0; i < HashSize; i++)
	if (a[i] != 0 && a[i]->how == 0)
		a[i]->nextState = peaceNext(i);
}
//只保存那些有实际意义的结点
void save(){
	fstream file("table.bin", ios::binary | ios::out);
	int j = 0;
	for (int i = 0; i < 42777721; i++){
		if (a[i] == 0)
			continue;
		table[j++] = i;
		table[j++] = a[i]->nextState * 3 + a[i]->how;
	}
	int sz = sizeof(int)*j;
	file.write((char*)table, sz);
	file.close();
	cout << "生成table.bin大小：" << sz / 1024 / 1024 << "M" << endl;
}

int main(){
	cout << "main start  " << time(0) << endl;
	calpower();
	//init2();//使用广度优先搜索的方式初始化
	init();//使用遍历的方式进行初始化
	go();
	peace();
	getMaxDepthIfWin();
	checkResult();//统计结点个数
	save();
	cout << "main end " << time(0) << endl;;
	return 0;
}
