using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
//AI接口，便于扩展，便于添加其它AI
interface AI {
     int getMove(int[] map, ref int result);
}