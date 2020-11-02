import draw.graphic as gc
from draw.cmd import IOcontrol
import time

class Movepoint:
    def __init__(self):
        self.x = 0
        self.y = 0

class Pointhelper:
    def __init__(self):
        self.point = Movepoint()
        self.score = 0

class ChenNa():

    def __init__(self, table):
        self.maxdepth = 5
        self.nodenum = 10
        self.number = 0
        self.flag = 0
        self.table_2d = None
        self.playerjudger = None
        self._bestmove = Movepoint()
        self.color_dict = {'White':1, 'Black':-1, 'Blank':0}

        self.color = None
        self.anticolor = None
        self.piece_dict = table.piece_dict

        self.t1 = None

    def xiazi(self, playerjudger, color, step):
        print('Chennas_turn start!')
        if color == 'Black':
            self.color = 'Black'
            self.anticolor = 'White'
        else:
            self.color = 'White'
            self.anticolor = 'Black'

        # first step of black
        if step == 0:
            pos_x = 7
            pos_y = 7
        else:
            print('Chenna GO GO GO 1')
            number = 0
            flag = 0
            self.playerjudger = playerjudger
            print('Chenna GO GO GO 2')
            self.table_2d = playerjudger.table_2d[1:16,1:16]
            print('Chenna GO GO GO 3')
            self.t1 = time.clock()
            self.Maxmin(self.maxdepth, 1, -214748364, 214748364, 0, 0)
            print('Chenna GO GO GO 4')
            pos_x = self._bestmove.x
            pos_y = self._bestmove.y

        # edge adjust
        pos_x, pos_y = pos_x+1, pos_y+1
        print('Chennas_turn {},{}'.format(pos_x, pos_y))
        return pos_x, pos_y

    def Maxmin(self, depth, who, alpha, beta, heng, zong):
        if depth == 0 or self.finished(heng,zong):
            #number++;
            #cout << "此时的层数是" << depth << '\n';
            #cout << "此时的number是" << number << '\n';
            #cout << "此时的分数是" << evaluate(mytable) << '\n';
            #mytable.display();
            #cout << "\n\n";*/
            #print("who",who, self.evaluate(heng, zong))
            
            return who*self.evaluate(heng, zong);
        
        score = 0; index = 0; num = 0

        points = [Pointhelper() for i in range(225)]    #这时候并没有初始化，只是开辟了一个空间
        #points = []

        index,points = self.getpossiblepoint(points)           #是返回的index，也就是有多少个可用点哦

        if index > self.nodenum:
            num = self.nodenum
        else:
            num = index
        #print('num',num,'inedx',index)
        #print(points[0].point.x, points[0].point.y, points[0].score)
        #for xx in points:
        #    print(xx.point.x, xx.point.y, xx.score)
        #for (int i = 1; i <= num; i++) {
        #    cout << "当前的层数是：" << depth << '\n';
        #    cout << "由启发式搜索得到的子节点的分数依次为" << points[index - i].score << '\n';

        if who > 0:
            for i in range(1, num+1):
                self.table_2d[points[index - i].point.x][points[index - i].point.y] = self.color_dict[self.color]
                #print("who>0\n",self.table_2d)
                
                #mytable.set(points[index - i].point.x, points[index - i].point.y, color);
                #mytable.display();
            
                self.switchplayer()
                score = self.Maxmin(depth - 1, -who, alpha, beta, points[index - i].point.x, points[index - i].point.y)
                self.switchplayer()
                
                self.table_2d[points[index - i].point.x][points[index - i].point.y] = self.color_dict['Blank']
                #mytable.set(points[index - i].point.x, points[index - i].point.y, 0);
                #cout << "此时的层数是" << depth << "score是" << score << "\n" << "横坐标" << points[index - i].point.x << "\n" << "纵坐标" << points[index - i].point.y << "\n";
                #cout << "alpha是" << alpha << '\n';
                #mytable.display();

                if score > alpha:   #此层为max层
                    alpha = score   #alpha存放着的是已发现节点的最大值,因为是max层，所以母节点的分数会比alpha要更大
                    if depth == self.maxdepth:
                        self._bestmove.x = points[index - i].point.x
                        #如果发现一个节点的分数大于alpha的话，那么将alpha更新，并且_bestmove也要更新
                        self._bestmove.y = points[index - i].point.y
                        if alpha >= beta:
                            break

                if depth == self.maxdepth:
                    duration = round(time.clock()-self.t1, 2)
                    print('ChenNa已思考...', duration, 's', end='\r')
                    #print("电脑正在计算中......\n"+"_bestmove.x "+str(self._bestmove.x)+"\n_bestmove.y "+str(self._bestmove.y)+"\nalpha"+str(alpha)+"\n\n")

            flag = 1
            return alpha

        else:
            for i in range(1, num+1):
                self.table_2d[points[index - i].point.x][points[index - i].point.y] = self.color_dict[self.color]
                #mytable.set(points[index - i].point.x, points[index - i].point.y, color);
                #mytable.display();

                self.switchplayer()
                score = self.Maxmin(depth - 1, -who, alpha, beta, points[index - i].point.x, points[index - i].point.y)
                self.switchplayer()
                
                self.table_2d[points[index - i].point.x][points[index - i].point.y] = self.color_dict['Blank']
                #mytable.set(points[index - i].point.x, points[index - i].point.y, 0);
                #cout << "此时的层数是" << depth << "score" << score << "\n" << "横坐标" << points[index - i].point.x << "\n" << "纵坐标" << points[index - i].point.y << "\n";
                      
                if score < beta:
                    beta = score#beta存放着已发现节点的最小值
                    if alpha >= beta:
                        break
                             
                #cout << "beta" << beta << '\n';*/
                #mytable.display();

            return beta

    def finished(self, line, index):
        blackScore = self.evaluateWithPieceType(self.color_dict['Black'])  # channa的来判断 15x15
        whiteScore = self.evaluateWithPieceType(self.color_dict['White'])
        #print(blackScore)
        #print(whiteScore)
        #print('----------------')

        # end flag
        if blackScore >= 100000 or whiteScore >= 100000:                      #如果当前的局面形成了五连的话
            return True
        elif self.color == 'Black' and \
             not self.playerjudger.check_forbidden([line,index], self.color, draw=False):    #如果黑子禁手 juedger来判断17x17
            return True
        else:
            return False

    #返回当前局面的分数哦
    def evaluateWithPieceType(self, colornum):
        score = 0

        # 横路
        for i in range(15):
            for j in range(15):
                if self.table_2d[i][j] == colornum:
                    block = 0
                    piece = 1

                    # left
                    if j == 0 or self.table_2d[i][j - 1] != self.color_dict['Blank']:
                        block += 1
                    
                    # pieceNum
                    j += 1
                    while j < 15 and self.table_2d[i][j] == colornum:
                        piece += 1
                        j += 1

                    # right
                    if j == 15 or self.table_2d[i][j] != self.color_dict['Blank']:
                        block += 1

                    score += self.evaluateLu(piece, block)
        #print('score=',score)

        # 竖路
        for i in range(15):
            for j in range(15):
                if self.table_2d[j][i] == colornum:
                    block = 0
                    piece = 1

                    # left
                    if j == 0 or self.table_2d[j - 1][i] != self.color_dict['Blank']:
                        block += 1

                    # pieceNum
                    j += 1
                    while j < 15 and self.table_2d[j][i] == colornum:
                        piece += 1
                        j += 1

                    # right
                    if j == 15 or self.table_2d[j][i] != self.color_dict['Blank']:
                        block += 1
                    
                    score += self.evaluateLu(piece, block)
        #print('score=',score)

        # '\'型的路
        for i in range(21):
            iLength = 15 - self.abs(i - 10);
            if i <= 10:
                for j in range(iLength):
                    if self.table_2d[j][15 - iLength + j] == colornum:
                        block = 0
                        piece = 1

                        # left
                        if j == 0 or self.table_2d[j - 1][15 - iLength + j - 1] != self.color_dict['Blank']:
                            block += 1
                        # pieceNum
                        j += 1
                        while j < iLength and self.table_2d[j][15 - iLength + j] == colornum:
                            piece += 1
                            j += 1
                        # right
                        if j == iLength or self.table_2d[j][15 - iLength + j] != self.color_dict['Blank']:
                            block += 1
                        score += self.evaluateLu(piece, block)


            else:
                for j in range(iLength):
                    if self.table_2d[15 - iLength + j][j] == colornum:
                        block = 0
                        piece = 1

                        # left
                        if j == 0 or self.table_2d[15 - iLength + j - 1][j - 1] != self.color_dict['Blank']:
                            block += 1

                        # pieceNum
                        j += 1
                        while j < iLength and self.table_2d[15 - iLength + j][j] == colornum:
                            piece += 1
                            j += 1

                        # right
                        if j == iLength or self.table_2d[15 - iLength + j][j] != self.color_dict['Blank']:
                            block += 1

                        score += self.evaluateLu(piece, block)
        #print('score=',score)

        #  '/'型的路
        for i in range(21):
            iLength = 15 - self.abs(i - 10);

            if i <= 10:
                for j in range(iLength):
                    if self.table_2d[j][iLength - 1 - j] == colornum:
                        block = 0
                        piece = 1

                        # left
                        if j == 0 or self.table_2d[j - 1][iLength - 1 - (j - 1)] != self.color_dict['Blank']:
                            block += 1

                        # pieceNum
                        j += 1
                        while j < iLength and self.table_2d[j][iLength - 1 - j] == colornum:
                            piece += 1
                            j += 1

                        # right
                        if j == iLength or self.table_2d[j][iLength - 1 - j] != self.color_dict['Blank']:
                            block += 1

                        score += self.evaluateLu(piece, block)
            else:
                for j in range(iLength):
                    if self.table_2d[15 - iLength + j][15 - 1 - j] == colornum:
                        block = 0
                        piece = 1

                        # left
                        if j == 0 or self.table_2d[15 - iLength + j - 1][15 - 1 - (j - 1)] != self.color_dict['Blank']:
                            block += 1

                        # pieceNum
                        j += 1
                        while j < iLength and self.table_2d[15 - iLength + j][15 - 1 - j] == colornum:
                            piece += 1
                            j += 1

                        # right
                        if j == iLength or self.table_2d[15 - iLength + j][15 - 1 - j] != self.color_dict['Blank']:
                            block += 1

                        score += self.evaluateLu(piece, block)
        #print('score=',score)
        return score

    def evaluateLu(self, piece, block):
        if block == 0:
            if piece == 1:
                return 10       #GGTupleTypeLiveOne
            elif piece == 2:
                return 100      #GGTupleTypeLiveTwo
            elif piece == 3:
                return 1000     #GGTupleTypeLiveThree
            elif piece == 4:
                return 10000    #GGTupleTypeLiveFour
            else:
                return 100000   #GGTupleTypeFive

        elif block == 1:
            if piece == 1:
                return 1        #GGTupleTypeDeadOne
            elif piece == 2:
                return 10       #GGTupleTypeDeadTwo
            elif piece == 3:
                return 100      #GGTupleTypeDeadThree
            elif piece == 4:
                return 1000     #GGTupleTypeDeadFour
            else:
                return 100000   #GGTupleTypeFive

        else:
            if piece >= 5:
                return 100000   #GGTupleTypeFive
            else:
                return 0
    
    def evaluate(self, line, index):
        blackScore = self.evaluateWithPieceType(self.color_dict['Black'])     #计算当前局面下黑子的得分
        whiteScore = self.evaluateWithPieceType(self.color_dict['White'])     #计算当前局面下白子的得分
        #print(blackScore)
        #print(whiteScore)

        if self.color == 'White' and not self.playerjudger.longlink_info([line,index],'Black'):
            whiteScore += 200000

        if self.color=='White' and blackScore<100000 and \
          (not self.playerjudger.huosi_info([line,index],'Black') or not self.playerjudger.huosan_info([line,index],'Black')):
            whiteScore += 100000

        #print(blackScore)
        #print(whiteScore)
        
        if self.color == 'Black': # 如果当前的My是黑子的话，那么返回（黑子分数-白子分数）
            return blackScore - whiteScore

        elif self.color == 'White':
            return whiteScore - blackScore
        else:
            raise Exception("什么颜色都不是！/n")
    
    def abs(self, x):
        if x > 0:
            return x
        else:
            return -x  #条件运算符?和：是一对运算符，不能分开单独使用,运算方向从右到左

    def switchplayer(self):
        if self.color == 'White':
            self.color = 'Black' 
            self.anticolor = 'White'
        else:
            self.color = 'White'
            self.anticolor = 'Black'

    def getpossiblepoint(self, points):
        index = 0
        i = 0; j = 0
        #print(self.table_2d)
        
        #print('step', self.piece_dict)
        for i in range(15):
            for j in range(15):
                #if str([j+1,i+1]) not in self.piece_dict.keys():
                if self.table_2d[i][j] == self.color_dict['Blank']:
                    point = Movepoint()  #point为(x,y)的坐标
                    point.x = i
                    point.y = j
                    #tmp = Pointhelper()
                    #tmp.point = point
                    #tmp.score = self.getScoreWithPoint(point)
                    #points.append(tmp)
                    points[index].point = point
                    points[index].score = self.getScoreWithPoint(point)
                    #print(i,j,"points[index].score",points[index].score)
                    index += 1
        #print('---------------------')
        #上面得出了共有index个可行的点
        temp = Pointhelper()
        #排序出十个节点，节点从最后的开始，即最后的最大
        if index > self.nodenum:
            for i in range(1, self.nodenum+1):
                for j in range(0, index-i):
                    if points[j].score > points[j + 1].score:
                        temp = points[j]
                        points[j] = points[j + 1]
                        points[j + 1] = temp
        return index,points # 检查一下point有没有修改


    def getScoreWithPoint(self, point):
        score = 0
        i = point.x
        j = point.y
        S = [[7,35,800,15000,800000], [0,15, 400,1800,100000]]

        # Horizontal
        while i > point.x - 5:
            if i >= 0 and i + 4 < 15:
                m = i
                n = j
                conum = 0
                anticonum = 0
                while m < i+5:
                    if self.table_2d[m][n] == self.color_dict[self.color]:
                        conum += 1
                    if self.table_2d[m][n] == self.color_dict[self.anticolor]:
                        anticonum += 1
                    m += 1
                if conum >= 1 and anticonum >= 1:
                    score += 0
                elif anticonum == 0:
                    score += S[0][conum]
                elif conum == 0:
                    score += S[1][anticonum];
                conum = 0
                anticonum = 0
            i -= 1

        # Vertical
        i = point.x;
        while j > point.y - 5:
            if j >= 0 and j + 4 < 15:
                m = i
                n = j
                conum = 0
                anticonum = 0
                while n < j+5:
                    if self.table_2d[m][n] == self.color_dict[self.color]:
                        conum += 1
                    if self.table_2d[m][n] == self.color_dict[self.anticolor]:
                        anticonum += 1
                    n += 1
                if conum >= 1 and anticonum >= 1:
                    score += 0
                elif anticonum == 0:
                    score += S[0][conum]
                elif conum == 0:
                    score += S[1][anticonum]
                conum = 0
                anticonum = 0
            j -= 1

        # Oblique up
        i = point.x;
        j = point.y;
        while (i > point.x - 5) and (j > point.y - 5):
            if i >= 0 and j >= 0 and i + 4 < 15 and j + 4 < 15:
                m = i
                n = j
                conum = 0
                anticonum = 0
                while (m<i+5) and (n<j+5):
                    if self.table_2d[m][n] == self.color_dict[self.color]:
                        conum += 1
                    if self.table_2d[m][n] == self.color_dict[self.anticolor]:
                        anticonum += 1
                    m += 1
                    n += 1
                if conum >= 1 and anticonum >= 1:
                    score += 0
                elif anticonum == 0:
                    score += S[0][conum]
                elif conum == 0:
                    score += S[1][anticonum]
                conum = 0
                anticonum = 0
            i -= 1
            j -= 1

        # Oblique down
        i = point.x;
        j = point.y;
        while (i > point.x - 5) and (j < point.y + 5):
            if i >= 0 and j < 15 and i + 4 < 15 and j - 4 >= 0:
                m = i
                n = j
                conum = 0
                anticonum = 0
                while (m<i+5) and (n>j-5):
                    if self.table_2d[m][n] == self.color_dict[self.color]:
                        conum +=1
                    if self.table_2d[m][n] == self.color_dict[self.anticolor]:
                        anticonum +=1
                    m += 1
                    n -= 1
                if conum >= 1 and anticonum >= 1:
                    score += 0
                elif anticonum == 0:
                    score += S[0][conum]
                elif conum == 0:
                    score += S[1][anticonum]
                conum = 0
                anticonum = 0
            i -= 1
            j += 1

        #这一段需要修改的
        if self.color == 'Black':
            self.table_2d[point.x][point.y] = self.color_dict['Black']

            if self.playerjudger.check_forbidden([point.x+1,point.y+1], 'Black', False) == False:
                score = 0

            self.table_2d[point.x][point.y] = self.color_dict['Blank']

        elif self.color == 'White':
            '''
            self.table_2d[point.x][point.y] = self.color_dict['Black']
            if not self.playerjudger.check_forbidden([point.x+1,point.y+1], 'Black', False):
                score -= 200000
            self.table_2d[point.x][point.y] = self.color_dict['Blank']
            
            #if not self.playerjudger.huosi_info([i+1,j+1], 'Black'):
            #    score -= 3600
            #if not self.playerjudger.huosan_info([i+1,j+1], 'Black'):
            #    score -= 800
            '''
            self.table_2d[point.x][point.y] = self.color_dict['Black']
            if not self.playerjudger.longlink_info([point.x+1,point.y+1], 'Black'):
                score -= 200000
            if not self.playerjudger.huosi_info([point.x+1,point.y+1], 'Black'):
                score -= 3600
            if not self.playerjudger.huosan_info([point.x+1,point.y+1], 'Black'):
                score -= 800
            self.table_2d[point.x][point.y] = self.color_dict['Blank']
         
        return score