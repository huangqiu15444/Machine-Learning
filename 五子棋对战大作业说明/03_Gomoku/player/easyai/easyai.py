import draw.graphic as gc
from draw.cmd import IOcontrol
import time

class EasyAi():

    def __init__(self, table):
        
        self.playerjudger = None
        self.table_2d = None
        self.color = None
        self.anticolor = None
        
        self.color_dict = {'White':1, 'Black':-1, 'Blank':0}
        self.t1 = None

    def xiazi(self, playerjudger, color, step):
        if color == 'Black':
            self.color = 'Black'
            self.anticolor = 'White'
        else:
            self.color = 'White'
            self.anticolor = 'Black'

        # first step of black
        if step == 0:
            best_i = 7
            best_j = 7
        else:
            self.playerjudger = playerjudger
            self.table_2d = playerjudger.table_2d[1:16,1:16]
            self.t1 = time.clock()
            max_score = 0; best_i = 0; best_j = 0
            for i in range(15):
                for j in range(15):
                    if (self.table_2d[i][j] == self.color_dict['Blank']):
                        new_score = self.score(i,j)
                        if new_score > max_score:
                            max_score = new_score
                            best_i = i
                            best_j = j
                duration = round(time.clock()-self.t1, 2)
                print('EasyAi已思考...', duration, 's', end='\r')

        # edge adjust
        pos_x, pos_y = best_i+1, best_j+1
        return pos_x, pos_y

    def score(self, i, j):
        F = [[ 0, 2, 8, 65, 160000 ], [ 0, 10, 34, 750, 160000 ]]
        L = [[ 0, 1, 6, 45, 5000   ], [ 0, 9, 29, 140, 5000    ]]
        num = 0
        i1 = 0; j1 = 0; i2 = 0; j2 = 0
        pcscore = 0; humscore = 0

        self.table_2d[i][j] = self.color_dict['Black']
        colornum = self.color_dict[self.color]
        anticolornum = self.color_dict[self.anticolor]

        #
        #   电脑落子打分   
        #

        # 横向打分
        num = 1 
        i1 = i2 = i
        j1 = j2 = j

        j1-=1
        while j1 >= 0 and self.table_2d[i][j1] == colornum:
            j1-=1
            num+=1
        j2+=1
        while j2 <= 14 and self.table_2d[i][j2] == colornum:
            j2+=1
            num+=1

        if self.color == 'White':
            if num >= 5:
                return F[1][4]       # 成五连
        if self.color == 'Black':
            if num > 5:
                return 0             # 成长连
            if num == 5:
                return F[1][4]       # 成五连
            
        if num == 4:
            if j1 >= 0 and j2 <= 14 and self.table_2d[i][j1] == 0 and self.table_2d[i][j2] == 0:
                pcscore += F[1][3]        #  活四
            elif (j1 >= 0 and self.table_2d[i][j1] == 0) or (j2 <= 14 and self.table_2d[i][j2] == 0):
                pcscore += F[0][3]        #  冲四
            
        if num == 3:
            if j1 >= 0 and j2 <= 14 and self.table_2d[i][j1] == 0 and self.table_2d[i][j2] == 0:
                if (j1-1 >= 0 and self.table_2d[i][j1-1] == colornum) or (j2+1 <= 14 and self.table_2d[i][j2+1] == colornum):
                    pcscore += F[0][3]-2       #  跳四（冲四的一种特殊情况）
                    if (j1-1 >= 0 and self.table_2d[i][j1-1] == colornum) and (j2+1 <= 14 and self.table_2d[i][j2+1] == colornum): 
                        pcscore += F[0][3]-2   #  双跳四
                else:
                    if (j1-1 >= 0 and self.table_2d[i][j1-1] == 0) or (j2+1 <= 14 and self.table_2d[i][j2+1] == 0):
                        pcscore += F[1][2]     #   活三
                    else :
                        pcscore += F[0][2]    #   冲三
            else:
                if j1 >= 0 and self.table_2d[i][j1] == 0:
                    if j1-1 >= 0 and self.table_2d[i][j1-1] == colornum:
                        pcscore += F[0][3]-2      #  跳四
                    if j1-1 >= 0 and self.table_2d[i][j1-1] == 0:
                        pcscore += F[0][2]      #  冲三
                if j2 <= 14 and self.table_2d[i][j2] == 0:
                    if j2+1 <= 14 and self.table_2d[i][j2+1] == colornum:
                        pcscore += F[0][3]-2      #  跳四                  
                    if j2+1 <= 14 and self.table_2d[i][j2+1] == 0:
                        pcscore += F[0][2]        #  冲三

        if num == 2 :
            if j1 >= 0 and self.table_2d[i][j1] == 0:
                if j1-2 >= 0 and self.table_2d[i][j1-1] == colornum and self.table_2d[i][j1-2] == colornum:
                    pcscore += F[0][3]-2      #  跳四
            if j2 <= 14 and self.table_2d[i][j2] == 0:
                if j2+2 <= 14 and self.table_2d[i][j2+1] == colornum and self.table_2d[i][j2+2] == colornum:  
                    pcscore += F[0][3]-2      #  跳四
            
            if j1 >= 0 and j2 <= 14 and self.table_2d[i][j1] == 0 and self.table_2d[i][j2] == 0:
                if j1-2 >= 0 and self.table_2d[i][j1-1] == colornum and  self.table_2d[i][j1-2] == 0:
                    pcscore += F[1][2]-2      #  活三
                if j2+2 <= 14 and self.table_2d[i][j2+1] == colornum and  self.table_2d[i][j2+2] == 0:
                    pcscore += F[1][2]-2      #  活三
                if (j1-1 >= 0 and self.table_2d[i][j1-1] == 0) or (j2+1 <= 14 and self.table_2d[i][j2+1] == 0):
                    pcscore += F[1][1]      #  活二

        if num == 1:
            if j1 >= 0 and self.table_2d[i][j1] == 0:
                if j1-3 >= 0 and self.table_2d[i][j1-1] == colornum and self.table_2d[i][j1-2] == colornum and self.table_2d[i][j1-3] == colornum:
                    pcscore += F[0][3]-2      #  跳四
            if j2 <= 14 and self.table_2d[i][j2] == 0:
                if j2+3 <= 14 and self.table_2d[i][j2+1] == colornum and self.table_2d[i][j2+2] == colornum and self.table_2d[i][j2+3] == colornum:
                    pcscore += F[0][3]-2      #  跳四
            if j1 >= 0 and j2 <= 14 and self.table_2d[i][j1] == 0 and self.table_2d[i][j2] == 0:
                if j1-3 >= 0 and self.table_2d[i][j1-1] == colornum and self.table_2d[i][j1-2] == colornum and self.table_2d[i][j1-3] == 0:
                    pcscore += F[1][2]-2      #  活三
                if j2+3 <= 14 and self.table_2d[i][j2+1] == colornum and self.table_2d[i][j2+2] == colornum and self.table_2d[i][j2+3] == 0:
                    pcscore += F[1][2]-2      #  活三

        # 纵向打分
        num = 1
        i1 = i2 = i
        j1 = j2 = j 
        i1-=1
        while i1 >= 0 and self.table_2d[i1][j1] == colornum:
            i1-=1
            num+=1
        i2+=1
        while i2 <= 14 and self.table_2d[i2][j2] == colornum:
            i2+=1
            num+=1

        if self.color == 'White':
            if num >= 5:
                return F[1][4]        # 成五连
        if self.color == 'Black':
            if num > 5:
                return 0         # 成长连
            if num == 5:
                return F[1][4]        # 成五连
            
        if num == 4:
            if i1 >= 0 and i2 <= 14 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                pcscore += F[1][3]        #  活四
            elif (i1 >= 0 and self.table_2d[i1][j1] == 0) or (i2 <= 14 and self.table_2d[i2][j2] == 0):
                pcscore += F[0][3]        #   冲四
            
        if num == 3:
            if i1 >= 0 and i2 <= 14 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                if (i1-1 >= 0 and self.table_2d[i1-1][j1] == colornum) or (i2+1 <= 14 and self.table_2d[i2+1][j2] == colornum):
                    pcscore += F[0][3]-2      #  跳四（冲四的一种特殊情况）
                    if (i1-1 >= 0 and self.table_2d[i1-1][j1] == colornum) and (i2+1 <= 14 and self.table_2d[i2+1][j2] == colornum):
                        pcscore += F[0][3]-2      #  双跳四
                else:
                    if(i1-1 >= 0 and self.table_2d[i1-1][j1] == 0) or (i2+1 <= 14 and self.table_2d[i2+1][j2] == 0):
                        pcscore += F[1][2]     #   活三
                    else:
                        pcscore += F[0][2]     #  冲三
            else:
                if i1 >= 0 and self.table_2d[i1][j1] == 0:
                    if i1-1 >= 0 and self.table_2d[i1-1][j1] == colornum:
                        pcscore += F[0][3]-2      #  跳四
                    if i1-1 >= 0 and self.table_2d[i1-1][j1] == 0:
                        pcscore += F[0][2]      #  冲三
                
                if i2 <= 14 and self.table_2d[i2][j2] == 0:
                    if i2+1 <= 14 and self.table_2d[i2+1][j2] == colornum:
                        pcscore += F[0][3]-2      #  跳四                 
                    if i2+1 <= 14 and self.table_2d[i2+1][j2] == 0:
                        pcscore += F[0][2]      #  冲三

        if num == 2:
            if i1 >= 0 and self.table_2d[i1][j1] == 0:
                if i1-2 >= 0 and self.table_2d[i1-1][j1] == colornum and self.table_2d[i1-2][j1] == colornum:
                    pcscore += F[0][3]-2      #  跳四
            
            if i2 <= 14 and self.table_2d[i2][j2] == 0:
                if i2+2 <= 14 and self.table_2d[i2+1][j2] == colornum and self.table_2d[i2+2][j2] == colornum:
                    pcscore += F[0][3]-2      #  跳四
            
            if i1 >= 0 and i2 <= 14 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                if i1-2 >= 0 and self.table_2d[i1-1][j1] == colornum and  self.table_2d[i1-2][j1] == 0:
                    pcscore += F[1][2]-2      #  活三
                if i2+2 <= 14 and self.table_2d[i2+1][j2] == colornum and  self.table_2d[i2+2][j2] == 0:
                    pcscore += F[1][2]-2      #  活三
                if (i1-1 >= 0 and self.table_2d[i1-1][j1] == 0) or (i2+1 <= 14 and self.table_2d[i2+1][j2] == 0):
                    pcscore += F[1][1]      #  活二

        if num == 1:
            if i1 >= 0 and self.table_2d[i1][j1] == 0:
                if i1-3 >= 0 and self.table_2d[i1-1][j1] == colornum and self.table_2d[i1-2][j1] == colornum and self.table_2d[i1-3][j1] == colornum: 
                    pcscore += F[0][3]-2      #  跳四
            if i2 <= 14 and self.table_2d[i2][j2] == 0:
                if i2+3 <= 14 and self.table_2d[i2+1][j2] == colornum and self.table_2d[i2+2][j2] == colornum and self.table_2d[i2+3][j2] == colornum:
                    pcscore += F[0][3]-2      #  跳四
            
            if i1 >= 0 and i2 <= 14 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                if i1-3 >= 0 and self.table_2d[i1-1][j1] == colornum and self.table_2d[i1-2][j1] == colornum and self.table_2d[i1-3][j1] == 0:
                    pcscore += F[1][2]-2      #  活三
                if i2+3 <= 14 and self.table_2d[i2+1][j2] == colornum and self.table_2d[i2+2][j2] == colornum and self.table_2d[i2+3][j2] == 0:
                    pcscore += F[1][2]-2      #  活三
            
        # "\"向打分

        num = 1
        i1 = i2 = i
        j1 = j2 = j
        i1-=1
        j1-=1
        while i1 >= 0 and j1 >= 0 and self.table_2d[i1][j1] == colornum:
            i1-=1
            j1-=1
            num+=1
        i2+=1
        j2+=1
        while i2 <= 14 and j2 <= 14 and self.table_2d[i2][j2] == colornum:
            i2+=1
            j2+=1
            num+=1

        if self.color == 'White':
            if num >= 5:
                return F[1][4]       # 成五连
        if self.color == 'Black':
            if num > 5:
                return 0                 # 成长连
            if num == 5:
                return F[1][4]       # 成五连
            
        if num == 4:
            if i1 >= 0 and i2 <= 14 and j1 >=0 and j2 <= 14 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                pcscore += F[1][3]        #  活四
            elif (i1 >= 0 and j1 >= 0 and self.table_2d[i1][j1] == 0) or (i2 <= 14 and j2 <= 14 and self.table_2d[i2][j2] == 0):
                pcscore += F[0][3]        #   冲四
            
        if num == 3:
            if i1 >= 0 and i2 <= 14 and j1 >=0 and j2 <= 14 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                if (i1-1 >= 0 and j1-1 >= 0 and self.table_2d[i1-1][j1-1] == colornum) or (i2+1 <= 14 and j2+1 <= 14 and self.table_2d[i2+1][j2+1] == colornum):
                    pcscore += F[0][3]-2     #  跳四（冲四的一种特殊情况）
                    if (i1-1 >= 0 and j1-1 >= 0 and self.table_2d[i1-1][j1-1] == colornum) and (i2+1 <= 14 and j2+1 <= 14 and self.table_2d[i2+1][j2+1] == colornum):
                        pcscore += F[0][3]-2      #  双跳四
                else:
                    if (i1-1 >= 0 and j1-1 >= 0 and self.table_2d[i1-1][j1-1] == 0) or (i2+1 <= 14 and j2+1 <= 14 and self.table_2d[i2+1][j2+1] == 0):
                        pcscore += F[1][2]     #   活三
                    else:
                        pcscore += F[0][2]     #  冲三
            else:
                if i1 >= 0 and j1 >= 0 and self.table_2d[i1][j1] == 0:
                    if i1-1 >= 0 and j1-1 >= 0 and self.table_2d[i1-1][j1-1] == colornum:
                        pcscore += F[0][3]-2      #  跳四
                    if i1-1 >= 0 and j1-1 >= 0 and self.table_2d[i1-1][j1-1] == 0: 
                        pcscore += F[0][2]      #  冲三
                
                if i2 <= 14 and j2 <= 14 and self.table_2d[i2][j2] == 0:
                    if i2+1 <= 14 and j2+1 <= 14 and self.table_2d[i2+1][j2+1] == colornum:
                        pcscore += F[0][3]-2      #  跳四                 
                    if i2+1 <= 14 and j2+1 <= 14 and self.table_2d[i2+1][j2+1] == 0:
                        pcscore += F[0][2]      #  冲三

        if num == 2:
            if i1 >= 0 and j1 >= 0 and self.table_2d[i1][j1] == 0:
                if i1-2 >= 0 and j1-2 >= 0 and self.table_2d[i1-1][j1-1] == colornum and self.table_2d[i1-2][j1-2] == colornum:
                    pcscore += F[0][3]-2      #  跳四
            
            if i2 <= 14 and j2 <= 14 and self.table_2d[i2][j2] == 0:
                if i2+2 <= 14 and j2+2 <= 14 and self.table_2d[i2+1][j2+1] == colornum and self.table_2d[i2+2][j2+2] == colornum:
                    pcscore += F[0][3]-2      #  跳四
            
            if i1 >= 0 and i2 <= 14 and j1 >=0 and j2 <= 14 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                if i1-2 >= 0 and j1-2 >= 0 and self.table_2d[i1-1][j1-1] == colornum and  self.table_2d[i1-2][j1-2] == 0:
                    pcscore += F[1][2]-2      #  活三
                if i2+2 <= 14 and j2+2 <= 14 and self.table_2d[i2+1][j2+1] == colornum and  self.table_2d[i2+2][j2+2] == 0:
                    pcscore += F[1][2]-2      #  活三
                if (i1-1 >=0 and j1-1 >= 0 and self.table_2d[i1-1][j1-1] == 0) or (i2+1 <= 14 and j2+1 <= 14 and self.table_2d[i2+1][j2+1] == 0):
                    pcscore += F[1][1]      #  活二     

        if num == 1:
            if i1 >= 0 and j1 >= 0 and self.table_2d[i1][j1] == 0:
                if i1-3 >= 0 and j1-3 >= 0 and self.table_2d[i1-1][j1-1] == colornum and self.table_2d[i1-2][j1-2] == colornum and self.table_2d[i1-3][j1-3] == colornum:
                    pcscore += F[0][3]-2      #  跳四
            
            if i2 <= 14 and j2 <= 14 and self.table_2d[i2][j2] == 0:
                if i2+3 <= 14 and j2+3 <= 14 and self.table_2d[i2+1][j2+1] == colornum and self.table_2d[i2+2][j2+2] == colornum and self.table_2d[i2+3][j2+3] == colornum:
                    pcscore += F[0][3]-2      #  跳四
            
            if i1 >= 0 and i2 <= 14 and j1 >=0 and j2 <= 14 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                if i1-3 >= 0 and j1-3 >= 0 and self.table_2d[i1-1][j1-1] == colornum and self.table_2d[i1-2][j1-2] == colornum and self.table_2d[i1-3][j1-3] == 0:
                    pcscore += F[1][2]-2      #  活三
                if i2+3 <= 14 and j2+3 <= 14 and self.table_2d[i2+1][j2+1] == colornum and self.table_2d[i2+2][j2+2] == colornum and self.table_2d[i2+3][j2+3] == 0:
                    pcscore += F[1][2]-2      #  活三

        ###"/"向打分###

        num = 1
        i1 = i2 = i ; j1 = j2 = j
        i1-=1
        j1+=1
        while i1 >= 0 and j1 <= 14 and self.table_2d[i1][j1] == colornum:
            i1-=1
            j1+=1
            num+=1
        i2+=1
        j2-=1
        while i2 <= 14 and j2 >= 0 and self.table_2d[i2][j2] == colornum:
            i2+=1
            j2-=1
            num+=1

        if self.color == 'White':
            if num >= 5:
                return F[1][4]        # 成五连
        if self.color == 'Black':
            if num > 5:
                return 0         # 成长连
            if num == 5: 
                return F[1][4]        # 成五连
            
        if num == 4:
            if i1 >= 0 and i2 <= 14 and j1 <=14 and j2 >= 0 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                pcscore += F[1][3]       #  活四
            elif (i1 >= 0 and j1 <= 14 and self.table_2d[i1][j1] == 0) or (i2 <= 14 and j2 >= 0 and self.table_2d[i2][j2] == 0):
                pcscore += F[0][3]       #   冲四
            
        if num == 3:
            if i1 >= 0 and i2 <= 14 and j1 <= 14 and j2 >= 0 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                if (i1-1 >= 0 and j1+1 <= 14 and self.table_2d[i1-1][j1+1] == colornum) or (i2+1 <= 14 and j2-1 >= 0 and self.table_2d[i2+1][j2-1] == colornum):
                    pcscore += F[0][3]-2      #  跳四（冲四的一种特殊情况）
                    if (i1-1 >= 0 and j1+1 <= 14 and self.table_2d[i1-1][j1+1] == colornum) and (i2+1 <= 14 and j2-1 >= 0 and self.table_2d[i2+1][j2-1] == colornum):
                        pcscore += F[0][3]-2      #  双跳四
                else:
                    if (i1-1 >= 0 and j1+1 <= 14 and self.table_2d[i1-1][j1+1] == 0) or (i2+1 <= 14 and j2-1 >= 0 and self.table_2d[i2+1][j2-1] == 0):
                        pcscore += F[1][2]     #   活三
                    else:
                        pcscore += F[0][2]     #  冲三
   
            else:
                if i1 >= 0 and j1 <= 14 and self.table_2d[i1][j1] == 0:
                    if i1-1 >= 0 and j1+1 <= 14 and self.table_2d[i1-1][j1+1] == colornum:
                        pcscore += F[0][3]-2      #  跳四
                    if i1-1 >= 0 and j1+1 <= 14 and self.table_2d[i1-1][j1+1] == 0:
                        pcscore += F[0][2]      #  冲三

                if i2 <= 14 and j2 >= 0 and self.table_2d[i2][j2] == 0:
                    if i2+1 <= 14 and j2-1 >= 0 and self.table_2d[i2+1][j2-1] == colornum:
                        pcscore += F[0][3]-2      #  跳四                  
                    if i2+1 <= 14 and j2-1 >= 0 and self.table_2d[i2+1][j2-1] == 0:
                        pcscore += F[0][2]      #  冲三

        if num == 2:
            if i1 >= 0 and j1 <= 14 and self.table_2d[i1][j1] == 0:
                if i1-2 >= 0 and j1+2 <= 14 and self.table_2d[i1-1][j1+1] == colornum and self.table_2d[i1-2][j1+2] == colornum:
                    pcscore += F[0][3]-2      #  跳四
            if i2 <= 14 and j2 >= 0 and self.table_2d[i2][j2] == 0:
                if i2+2 <= 14 and j2-2 >= 0 and self.table_2d[i2+1][j2-1] == colornum and self.table_2d[i2+2][j2-2] == colornum:  
                    pcscore += F[0][3]-2      #  跳四
            if i1 >= 0 and i2 <= 14 and j1 <=14 and j2 >= 0 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                if i1-2 >= 0 and j1+2 <= 14 and self.table_2d[i1-1][j1+1] == colornum and  self.table_2d[i1-2][j1+2] == 0:
                    pcscore += F[1][2]-2      #  活三
                if i2+2 <= 14 and j2-2 >= 0 and self.table_2d[i2+1][j2-1] == colornum and  self.table_2d[i2+2][j2-2] == 0:
                    pcscore += F[1][2]-2      #  活三
                if (i1-1 >= 0 and j1+1 <= 14 and self.table_2d[i1-1][j1+1] == 0) or (i2+1 <=14 and j2-1 >= 0 and self.table_2d[i2+1][j2-1] == 0):
                    pcscore += F[1][1]      #  活二

        if num == 1:
            if i1 >= 0 and j1 <= 14 and self.table_2d[i1][j1] == 0:
                if i1-3 >= 0 and j1+3 <= 14 and self.table_2d[i1-1][j1+1] == colornum and self.table_2d[i1-2][j1+2] == colornum and self.table_2d[i1-3][j1+3] == colornum:
                    pcscore += F[0][3]-2      #  跳四
            
            if i2 <= 14 and j2 >= 0 and self.table_2d[i2][j2] == 0:
                if i2+3 <= 14 and j2-3 >= 0 and self.table_2d[i2+1][j2-1] == colornum and self.table_2d[i2+2][j2-2] == colornum and self.table_2d[i2+3][j2-3] == colornum:
                    pcscore += F[0][3]-2      #  跳四
            
            if i1 >= 0 and i2 <= 14 and j1 <=14 and j2 >= 0 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                if i1-3 >= 0 and j1+3 <= 14 and self.table_2d[i1-1][j1+1] == colornum and self.table_2d[i1-2][j1+2] == colornum and self.table_2d[i1-3][j1+3] == 0:
                    pcscore += F[1][2]-2      #  活三
                if i2+3 <= 14 and j2-3 >= 0 and self.table_2d[i2+1][j2-1] == colornum and self.table_2d[i2+2][j2-2] == colornum and self.table_2d[i2+3][j2-3] == 0:
                    pcscore += F[1][2]-2      #  活三

        
        if pcscore > 125:
            pcscore += 500      #   四四 修正
        else:
            if pcscore > 94:
                pcscore += 80   #   四三 修正

        #
        #   玩家落子打分   
        #

        #横向打分
        num = 1
        i1 = i2 = i ; j1 = j2 = j
        j1-=1
        while j1 >= 0 and self.table_2d[i][j1] == anticolornum:
            j1-=1
            num+=1
        j2+=1
        while j2 <= 14 and self.table_2d[i][j2] == anticolornum:
            j2+=1
            num+=1

        if self.anticolor == 'White':
            if num >= 5:
                return L[1][4]        # 成五连

        if self.anticolor == 'Black':
            if num > 5:
                humscore = 0          # 成长连
            if num == 5:
                return L[1][4]        # 成五连
            
        if num == 4:
            if j1 >= 0 and j2 <= 14 and self.table_2d[i][j1] == 0 and self.table_2d[i][j2] == 0:
                humscore += L[1][3]        #  活四
            elif (j1 >= 0 and self.table_2d[i][j1] == 0) or (j2 <= 14 and self.table_2d[i][j2] == 0) :
                humscore += L[0][3]        #   冲四
        
     
        if num == 3:
            if j1 >= 0 and j2 <= 14 and self.table_2d[i][j1] == 0 and self.table_2d[i][j2] == 0:
                if (j1-1 >= 0 and self.table_2d[i][j1-1] == anticolornum) or (j2+1 <= 14 and self.table_2d[i][j2+1] == anticolornum):
                    humscore += L[0][3]      #  跳四（冲四的一种特殊情况）
                    if (j1-1 >= 0 and self.table_2d[i][j1-1] == anticolornum) and (j2+1 <= 14 and self.table_2d[i][j2+1] == anticolornum):
                        humscore += L[0][3]      #  双跳四
                
                else:
                    if (j1-1 >= 0 and self.table_2d[i][j1-1] == 0) or (j2+1 <= 14 and self.table_2d[i][j2+1] == 0):
                        humscore += L[1][2]     #   活三
                    else:
                        humscore += L[0][2]     #  冲三
            else:
                if j1 >= 0 and self.table_2d[i][j1] == 0:
                    if j1-1 >= 0 and self.table_2d[i][j1-1] == anticolornum:
                        humscore += L[0][3]      #  跳四
                    if j1-1 >= 0 and self.table_2d[i][j1-1] == 0:
                        humscore += L[0][2]      #  冲三
                
                if j2 <= 14 and self.table_2d[i][j2] == 0:
                    if j2+1 <= 14 and self.table_2d[i][j2+1] == anticolornum:
                        humscore += L[0][3]      #  跳四                   
                    if j2+1 <= 14 and self.table_2d[i][j2+1] == 0:
                        humscore += L[0][2]      #  冲三


        if num == 2:
            if j1 >= 0 and self.table_2d[i][j1] == 0:
                if j1-2 >= 0 and self.table_2d[i][j1-1] == anticolornum and self.table_2d[i][j1-2] == anticolornum:
                    humscore += L[0][3]      #  跳四
            
            if j2 <= 14 and self.table_2d[i][j2] == 0:
                if j2+2 <= 14 and self.table_2d[i][j2+1] == anticolornum and self.table_2d[i][j2+2] == anticolornum:
                    humscore += L[0][3]      #  跳四
            
            if j1 >= 0 and j2 <= 14 and self.table_2d[i][j1] == 0 and self.table_2d[i][j2] == 0:
                if j1-2 >= 0 and self.table_2d[i][j1-1] == anticolornum and  self.table_2d[i][j1-2] == 0:
                    humscore += L[1][2]-2      #  活三
                if j2+2 <= 14 and self.table_2d[i][j2+1] == anticolornum and  self.table_2d[i][j2+2] == 0:
                    humscore += L[1][2]-2      #  活三
                if (j1-1 >= 0 and self.table_2d[i][j1-1] == 0) or (j2+1 <= 14 and self.table_2d[i][j2+1] == 0):
                    humscore += L[1][1]      #  活二

        if num == 1:
            if j1 >= 0 and self.table_2d[i][j1] == 0:
                if j1-3 >= 0 and self.table_2d[i][j1-1] == anticolornum and self.table_2d[i][j1-2] == anticolornum and self.table_2d[i][j1-3] == anticolornum:
                    humscore += L[0][3]      #  跳四
            
            if j2 <= 14 and self.table_2d[i][j2] == 0:
                if j2+3 <= 14 and self.table_2d[i][j2+1] == anticolornum and self.table_2d[i][j2+2] == anticolornum and self.table_2d[i][j2+3] == anticolornum:
                    humscore += L[0][3]      #  跳四
            
            if j1 >= 0 and j2 <= 14 and self.table_2d[i][j1] == 0 and self.table_2d[i][j2] == 0:
                if j1-3 >= 0 and self.table_2d[i][j1-1] == anticolornum and self.table_2d[i][j1-2] == anticolornum and self.table_2d[i][j1-3] == 0:
                    humscore += L[1][2]-2      #  活三
                if j2+3 <= 14 and self.table_2d[i][j2+1] == anticolornum and self.table_2d[i][j2+2] == anticolornum and self.table_2d[i][j2+3] == 0:
                    humscore += L[1][2]-2      #  活三


        ###纵向打分###
        num = 1
        i1 = i2 = i ; j1 = j2 = j
        i1-=1
        while i1 >= 0 and self.table_2d[i1][j1] == anticolornum:
            i1-=1
            num+=1 
        i2+=1
        while i2 <= 14 and self.table_2d[i2][j2] == anticolornum:
            i2+=1
            num+=1 

        if self.anticolor == 'White':
            if num >= 5:
                return L[1][4]        # 成五连
        
        if self.anticolor == 'Black':
            if num > 5: 
                humscore = 0          # 成长连
            if num == 5:
                return L[1][4]        # 成五连
            
        if num == 4:
            if i1 >= 0 and i2 <= 14 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                humscore += L[1][3]       #  活四
            elif (i1 >= 0 and self.table_2d[i1][j1] == 0) or (i2 <= 14 and self.table_2d[i2][j2] == 0):
                humscore += L[0][3]       #   冲四
        
            
        if num == 3:
            if i1 >= 0 and i2 <= 14 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                if (i1-1 >= 0 and self.table_2d[i1-1][j1] == anticolornum) or (i2+1 <= 14 and self.table_2d[i2+1][j2] == anticolornum):
                    humscore += L[0][3]      #  跳四（冲四的一种特殊情况）
                    if (i1-1 >= 0 and self.table_2d[i1-1][j1] == anticolornum) and (i2+1 <= 14 and self.table_2d[i2+1][j2] == anticolornum):
                        humscore += L[0][3]      #  双跳四
                else:
                    if (i1-1 >= 0 and self.table_2d[i1-1][j1] == 0) or (i2+1 <= 14 and self.table_2d[i2+1][j2] == 0):
                        humscore += L[1][2]     #   活三
                    else:
                        humscore += L[0][2]     #  冲三
            else:
                if i1 >= 0 and self.table_2d[i1][j1] == 0:
                    if i1-1 >= 0 and self.table_2d[i1-1][j1] == anticolornum:
                        humscore += L[0][3]      #  跳四
                    if i1-1 >= 0 and self.table_2d[i1-1][j1] == 0:
                        humscore += L[0][2]      #  冲三
                
                if i2 <= 14 and self.table_2d[i2][j2] == 0:
                    if i2+1 <= 14 and self.table_2d[i2+1][j2] == anticolornum:
                        humscore += L[0][3]      #  跳四                  
                    if i2+1 <= 14 and self.table_2d[i2+1][j2] == 0:
                        humscore += L[0][2]      #  冲三

        if num == 2:
            if i1 >= 0 and self.table_2d[i1][j1] == 0:
                if i1-2 >= 0 and self.table_2d[i1-1][j1] == anticolornum and self.table_2d[i1-2][j1] == anticolornum:
                    humscore += L[0][3]      #  跳四
            
            if i2 <= 14 and self.table_2d[i2][j2] == 0:
                if i2+2 <= 14 and self.table_2d[i2+1][j2] == anticolornum and self.table_2d[i2+2][j2] == anticolornum:
                    humscore += L[0][3]      #  跳四

            if i1 >= 0 and i2 <= 14 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                if i1-2 >= 0 and self.table_2d[i1-1][j1] == anticolornum and  self.table_2d[i1-2][j1] == 0:
                    humscore += L[1][2]-2      #  活三
                if i2+2 <= 14 and self.table_2d[i2+1][j2] == anticolornum and  self.table_2d[i2+2][j2] == 0:
                    humscore += L[1][2]-2      #  活三
                if (i1-1 >= 0 and self.table_2d[i1-1][j1] == 0) or (i2+1 <= 14 and self.table_2d[i2+1][j2] == 0):
                    humscore += L[1][1]      #  活二

        if num == 1:
            if i1 >= 0 and self.table_2d[i1][j1] == 0:
                if i1-3 >= 0 and self.table_2d[i1-1][j1] == anticolornum and self.table_2d[i1-2][j1] == anticolornum and self.table_2d[i1-3][j1] == anticolornum:
                    humscore += L[0][3]      #  跳四

            if i2 <= 14 and self.table_2d[i2][j2] == 0:
                if i2+3 <= 14 and self.table_2d[i2+1][j2] == anticolornum and self.table_2d[i2+2][j2] == anticolornum and self.table_2d[i2+3][j2] == anticolornum:
                    humscore += L[0][3]      #  跳四
            
            if i1 >= 0 and i2 <= 14 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                if i1-3 >= 0 and self.table_2d[i1-1][j1] == anticolornum and self.table_2d[i1-2][j1] == anticolornum and self.table_2d[i1-3][j1] == 0:
                    humscore += L[1][2]-2      #  活三
                if i2+3 <= 14 and self.table_2d[i2+1][j2] == anticolornum and self.table_2d[i2+2][j2] == anticolornum and self.table_2d[i2+3][j2] == 0:
                    humscore += L[1][2]-2      #  活三


        #"\"向打分 
        num = 1
        i1 = i2 = i ; j1 = j2 = j
        i1-=1
        j1-=1
        while i1 >= 0 and j1 >= 0 and self.table_2d[i1][j1] == anticolornum:
            i1-=1
            j1-=1
            num+=1
        i2+=1
        j2+=1
        while i2 <= 14 and j2 <= 14 and self.table_2d[i2][j2] == anticolornum:
            i2+=1
            j2+=1
            num+=1

        if self.anticolor == 'White':
            if num >= 5:
                return L[1][4]        # 成五连
        if self.anticolor == 'Black':
            if num > 5: 
                humscore = 0          # 成长连
            if num == 5:
                return L[1][4]        # 成五连
            
        if num == 4:
            if i1 >= 0 and i2 <= 14 and j1 >=0 and j2 <= 14 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                humscore += L[1][3]        #  活四
            elif (i1 >= 0 and j1 >= 0 and self.table_2d[i1][j1] == 0) or (i2 <= 14 and j2 <= 14 and self.table_2d[i2][j2] == 0):
                humscore += L[0][3]        #   冲四
            
        if num == 3:
            if i1 >= 0 and i2 <= 14 and j1 >=0 and j2 <= 14 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                if (i1-1 >= 0 and j1-1 >= 0 and self.table_2d[i1-1][j1-1] == anticolornum) or (i2+1 <= 14 and j2+1 <= 14 and self.table_2d[i2+1][j2+1] == anticolornum):
                    humscore += L[0][3]      #  跳四（冲四的一种特殊情况）
                    if (i1-1 >= 0 and j1-1 >= 0 and self.table_2d[i1-1][j1-1] == anticolornum) and (i2+1 <= 14 and j2+1 <= 14 and self.table_2d[i2+1][j2+1] == anticolornum):
                        humscore += L[0][3]      #  双跳四
                
                else:
                    if (i1-1 >= 0 and j1-1 >= 0 and self.table_2d[i1-1][j1-1] == 0) or (i2+1 <= 14 and j2+1 <= 14 and self.table_2d[i2+1][j2+1] == 0):
                        humscore += L[1][2]     #   活三
                    else:
                        humscore += L[0][2]     #  冲三
                
            else:
                if i1 >= 0 and j1 >= 0 and self.table_2d[i1][j1] == 0:
                    if i1-1 >= 0 and j1-1 >= 0 and self.table_2d[i1-1][j1-1] == anticolornum:
                        humscore += L[0][3]      #  跳四
                    if i1-1 >= 0 and j1-1 >= 0 and self.table_2d[i1-1][j1-1] == 0:
                        humscore += L[0][2]      #  冲三
                
                if i2 <= 14 and j2 <= 14 and self.table_2d[i2][j2] == 0:
                    if i2+1 <= 14 and j2+1 <= 14 and self.table_2d[i2+1][j2+1] == anticolornum:
                        humscore += L[0][3]      #  跳四                  
                    if i2+1 <= 14 and j2+1 <= 14 and self.table_2d[i2+1][j2+1] == 0:
                        humscore += L[0][2]      #  冲三

        if num == 2:
            if i1 >= 0 and j1 >= 0 and self.table_2d[i1][j1] == 0:
                if i1-2 >= 0 and j1-2 >= 0 and self.table_2d[i1-1][j1-1] == anticolornum and self.table_2d[i1-2][j1-2] == anticolornum:
                    humscore += L[0][3]      #  跳四
            
            if i2 <= 14 and j2 <= 14 and self.table_2d[i2][j2] == 0:
                if i2+2 <= 14 and j2+2 <= 14 and self.table_2d[i2+1][j2+1] == anticolornum and self.table_2d[i2+2][j2+2] == anticolornum:
                    humscore += L[0][3]      #  跳四
            
            if i1 >= 0 and i2 <= 14 and j1 >=0 and j2 <= 14 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                if i1-2 >= 0 and j1-2 >= 0 and self.table_2d[i1-1][j1-1] == anticolornum and  self.table_2d[i1-2][j1-2] == 0:
                    humscore += L[1][2]-2      #  活三
                if i2+2 <= 14 and j2+2 <= 14 and self.table_2d[i2+1][j2+1] == anticolornum and  self.table_2d[i2+2][j2+2] == 0:
                    humscore += L[1][2]-2      #  活三
                if (i1-1 >=0 and j1-1 >= 0 and self.table_2d[i1-1][j1-1] == 0) or (i2+1 <= 14 and j2+1 <= 14 and self.table_2d[i2+1][j2+1] == 0):
                    humscore += L[1][1]      #  活二

        if num == 1:
            if i1 >= 0 and j1 >= 0 and self.table_2d[i1][j1] == 0:
                if i1-3 >= 0 and j1-3 >= 0 and self.table_2d[i1-1][j1-1] == anticolornum and self.table_2d[i1-2][j1-2] == anticolornum and self.table_2d[i1-3][j1-3] == anticolornum:
                    humscore += L[0][3]      #  跳四
            
            if i2 <= 14 and j2 <= 14 and self.table_2d[i2][j2] == 0:
                if i2+3 <= 14 and j2+3 <= 14 and self.table_2d[i2+1][j2+1] == anticolornum and self.table_2d[i2+2][j2+2] == anticolornum and self.table_2d[i2+3][j2+3] == anticolornum:
                    humscore += L[0][3]      #  跳四
            
            if i1 >= 0 and i2 <= 14 and j1 >=0 and j2 <= 14 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                if i1-3 >= 0 and j1-3 >= 0 and self.table_2d[i1-1][j1-1] == anticolornum and self.table_2d[i1-2][j1-2] == anticolornum and self.table_2d[i1-3][j1-3] == 0:
                    humscore += L[1][2]-2      #  活三
                if i2+3 <= 14 and j2+3 <= 14 and self.table_2d[i2+1][j2+1] == anticolornum and self.table_2d[i2+2][j2+2] == anticolornum and self.table_2d[i2+3][j2+3] == 0:
                    humscore += L[1][2]-2      #  活三

        ###"/"向打分###
        num = 1
        i1 = i2 = i ; j1 = j2 = j
        i1-=1
        j1+=1
        while i1 >= 0 and j1 <= 14 and self.table_2d[i1][j1] == anticolornum:
            i1-=1
            j1+=1
            num+=1
        i2+=1
        j2-=1
        while i2 <= 14 and j2 >= 0 and self.table_2d[i2][j2] == anticolornum:
            i2+=1
            j2-=1
            num+=1

        if self.anticolor == 'White':
            if num >= 5:
                return L[1][4]       # 成五连
        
        if self.anticolor == 'Black':
            if num > 5:
                humscore = 0         # 成长连
            if num == 5:
                return L[1][4]        # 成五连
            
        if num == 4:
            if i1 >= 0 and i2 <= 14 and j1 <=14 and j2 >= 0 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                humscore += L[1][3]        #  活四
            elif (i1 >= 0 and j1 <= 14 and self.table_2d[i1][j1] == 0) or (i2 <= 14 and j2 >= 0 and self.table_2d[i2][j2] == 0):
                humscore += L[0][3]        #   冲四
        
            
        if num == 3:
            if i1 >= 0 and i2 <= 14 and j1 <= 14 and j2 >= 0 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                if (i1-1 >= 0 and j1+1 <= 14 and self.table_2d[i1-1][j1+1] == anticolornum) or (i2+1 <= 14 and j2-1 >= 0 and self.table_2d[i2+1][j2-1] == anticolornum):
                    humscore += L[0][3]      #  跳四（冲四的一种特殊情况）
                    if (i1-1 >= 0 and j1+1 <= 14 and self.table_2d[i1-1][j1+1] == anticolornum) and (i2+1 <= 14 and j2-1 >= 0 and self.table_2d[i2+1][j2-1] == anticolornum):
                        humscore += L[0][3]      #  双跳四
                else:
                    if (i1-1 >= 0 and j1+1 <= 14 and self.table_2d[i1-1][j1+1] == 0) or (i2+1 <= 14 and j2-1 >= 0 and self.table_2d[i2+1][j2-1] == 0):
                        humscore += L[1][2]      #   活三
                    else:
                        humscore += L[0][2]     #  冲三
            else:
                if i1 >= 0 and j1 <= 14 and self.table_2d[i1][j1] == 0:
                    if i1-1 >= 0 and j1+1 <= 14 and self.table_2d[i1-1][j1+1] == anticolornum:
                        humscore += L[0][3]      #  跳四
                    if i1-1 >= 0 and j1+1 <= 14 and self.table_2d[i1-1][j1+1] == 0:
                        humscore += L[0][2]      #  冲三
                if i2 <= 14 and j2 >= 0 and self.table_2d[i2][j2] == 0:
                    if i2+1 <= 14 and j2-1 >= 0 and self.table_2d[i2+1][j2-1] == anticolornum:
                        humscore += L[0][3]      #  跳四                   
                    if i2+1 <= 14 and j2-1 >= 0 and self.table_2d[i2+1][j2-1] == 0:
                        humscore += L[0][2]      #  冲三


        if num == 2:
            if i1 >= 0 and j1 <= 14 and self.table_2d[i1][j1] == 0:
                if i1-2 >= 0 and j1+2 <= 14 and self.table_2d[i1-1][j1+1] == anticolornum and self.table_2d[i1-2][j1+2] == anticolornum:
                    humscore += L[0][3]      #  跳四
            
            if i2 <= 14 and j2 >= 0 and self.table_2d[i2][j2] == 0:
                if i2+2 <= 14 and j2-2 >= 0 and self.table_2d[i2+1][j2-1] == anticolornum and self.table_2d[i2+2][j2-2] == anticolornum:
                    humscore += L[0][3]      #  跳四
            
            if i1 >= 0 and i2 <= 14 and j1 <=14 and j2 >= 0 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                if i1-2 >= 0 and j1+2 <= 14 and self.table_2d[i1-1][j1+1] == anticolornum and  self.table_2d[i1-2][j1+2] == 0:
                    humscore += L[1][2]-2      #  活三
                if i2+2 <= 14 and j2-2 >= 0 and self.table_2d[i2+1][j2-1] == anticolornum and  self.table_2d[i2+2][j2-2] == 0:
                    humscore += L[1][2]-2      #  活三
                if (i1-1 >= 0 and j1+1 <= 14 and self.table_2d[i1-1][j1+1] == 0) or (i2+1 <=14 and j2-1 >= 0 and self.table_2d[i2+1][j2-1] == 0):
                    humscore += L[1][1]        #  活二

        if num == 1:
            if i1 >= 0 and j1 <= 14 and self.table_2d[i1][j1] == 0:
                if i1-3 >= 0 and j1+3 <= 14 and self.table_2d[i1-1][j1+1] == anticolornum and self.table_2d[i1-2][j1+2] == anticolornum and self.table_2d[i1-3][j1+3] == anticolornum:
                    humscore += L[0][3]      #  跳四
            
            if i2 <= 14 and j2 >= 0 and self.table_2d[i2][j2] == 0:
                if i2+3 <= 14 and j2-3 >= 0 and self.table_2d[i2+1][j2-1] == anticolornum and self.table_2d[i2+2][j2-2] == anticolornum and self.table_2d[i2+3][j2-3] == anticolornum:
                    humscore += L[0][3]      #  跳四
            
            if i1 >= 0 and i2 <= 14 and j1 <=14 and j2 >= 0 and self.table_2d[i1][j1] == 0 and self.table_2d[i2][j2] == 0:
                if i1-3 >= 0 and j1+3 <= 14 and self.table_2d[i1-1][j1+1] == anticolornum and self.table_2d[i1-2][j1+2] == anticolornum and self.table_2d[i1-3][j1+3] == 0:
                    humscore += L[1][2]-2     #  活三
                if i2+3 <= 14 and j2-3 >= 0 and self.table_2d[i2+1][j2-1] == anticolornum and self.table_2d[i2+2][j2-2] == anticolornum and self.table_2d[i2+3][j2-3] == 0:
                    humscore += L[1][2]-2      #  活三

        if humscore < 139:
            if humscore > 89:
                humscore += 50        #   四四 修正
            else:
                if humscore > 73:
                    humscore += 60    #   四三 修正


        #     黑棋禁手判断     
        if self.color == 'Black':
            self.table_2d[i][j] = self.color_dict['Black']

            if self.playerjudger.check_forbidden([i+1,j+1], 'Black', False) == False:
                pcscore = 0

            self.table_2d[i][j] = self.color_dict['Blank']

            return pcscore + humscore 
        else:
            self.table_2d[i][j] = self.color_dict['Black']

            if self.playerjudger.check_forbidden([i+1,j+1], 'Black', False) == False:
                humscore = 0

            self.table_2d[i][j] = self.color_dict['Blank']

            return pcscore + humscore 
