import numpy as np

from draw.cmd import IOcontrol
import draw.graphic as gc


class Judge():

    def __init__ (self, table):
        
        # init Judge attribute
        self.table_row = table.table_row
        self.table_col = table.table_col
        self.grid_size = table.grid_size

        self.ioer = IOcontrol()

        self.table_2d = table.table_2d
        self.unmove = table.unmove_chess
        self.win = table.win
        self.gc_draw = table.gc_draw

        self.color_dict = {'White':1, 'Black':-1, 'Blank':0}
        self.forbidden_flag = None

        self.pos_has_occupied = []

    def check(self, pos, color, draw):
        if color == 'Black':
            if self.check_pos_conflic(pos, color, draw) == False:
                return 'pos_confict'
            elif self.check_forbidden(pos, color, draw) == False:
                return self.forbidden_flag+'_forbidden'
            elif self.check_win(pos, color, draw) == True:
                return 'winner'
            else:
                return 'continue'

        elif color == 'White':
            if self.check_pos_conflic(pos, color, draw) == False:
                return 'pos_confict'
            elif self.check_win(pos, color, draw) == True:
                return 'winner'
            else:
                return 'continue'

        else:
            raise Exception('err color')

    def check_pos_conflic(self, pos, color, draw):

        if pos[0] == 0 or pos[0] == self.table_col or pos[1] == 0 or pos[1] == self.table_row:
            if draw == True:
                # cmd output
                self.ioer.cmd_print('out of range!')

            # undraw the object
                self.unmove(pos)

                # put error sign
                self.gc_draw(self.grid_size/2, "red", self.grid_size * pos[0], self.grid_size * pos[1], "×")

                # update drawing window
                gc.update()

            return False

        elif pos in self.pos_has_occupied:
            if draw == True:
                # cmd output
                self.ioer.cmd_print('confict position!')

                # undraw the object
                self.unmove(pos)

                # put error sign
                self.gc_draw(self.grid_size/2, "red", self.grid_size * pos[0], self.grid_size * pos[1], "×")

                # update drawing window
                gc.update()

            return False
        else:
            # add position history
            self.pos_has_occupied.append(pos)

            # save table in 2d form
            # note that pos[0] is col index, pos[1] is row index
            #self.table_2d[pos[1]][pos[0]] = self.color_dict[color]

            # save to local dir
            #self.ioer.save_table(self.table_2d)

            # update chessboard information
            # self.chessboard_info(pos, color)

            return True

    def check_forbidden(self, pos, color, draw):
        if self.longlink_info(pos, color) == False:
            if draw == True:
                self.gc_draw(self.grid_size/1.5, "red", self.grid_size * pos[0], self.grid_size * pos[1], "×")
                gc.update()
            return False
        elif self.huosi_info(pos, color) == False:
            if draw == True:
                self.gc_draw(self.grid_size/1.5, "red", self.grid_size * pos[0], self.grid_size * pos[1], "×")
                gc.update()
            return False
        elif self.huosan_info(pos, color) == False:
            if draw == True:
                self.gc_draw(self.grid_size/1.5, "red", self.grid_size * pos[0], self.grid_size * pos[1], "×")
                gc.update()
            return False
        else:
            return True

    def check_win(self, pos, color, draw):
        color_num = self.color_dict[color]
        #pos[1] table de hang, gc de lie
        #pos[0] table de lie, gc de hang

        # check row '---'
        for i in range(5):
            if  self.outbound_equal(self.table_2d, pos[1], pos[0]-4+i+0, color_num) and \
                self.outbound_equal(self.table_2d, pos[1], pos[0]-4+i+1, color_num) and \
                self.outbound_equal(self.table_2d, pos[1], pos[0]-4+i+2, color_num) and \
                self.outbound_equal(self.table_2d, pos[1], pos[0]-4+i+3, color_num) and \
                self.outbound_equal(self.table_2d, pos[1], pos[0]-4+i+4, color_num) :
                    if draw == True:
                        self.gc_draw(self.grid_size/1.5, gc.color_rgb(0,255,0), \
                                          self.grid_size * pos[0], self.grid_size * pos[1], "☆")
                        gc.update()
                    return True

        # check col '|'
        for i in range(5):
            if  self.outbound_equal(self.table_2d, pos[1]-4+i+0, pos[0], color_num) and \
                self.outbound_equal(self.table_2d, pos[1]-4+i+1, pos[0], color_num) and \
                self.outbound_equal(self.table_2d, pos[1]-4+i+2, pos[0], color_num) and \
                self.outbound_equal(self.table_2d, pos[1]-4+i+3, pos[0], color_num) and \
                self.outbound_equal(self.table_2d, pos[1]-4+i+4, pos[0], color_num) :
                    if draw == True:
                        self.gc_draw(self.grid_size/1.5, gc.color_rgb(0,255,0), \
                                          self.grid_size * pos[0], self.grid_size * pos[1], "☆")
                        gc.update()
                    return True

        # check diagonal '\' 
        for i in range(5):
            if  self.outbound_equal(self.table_2d, pos[1]-4+i+0, pos[0]-4+i+0, color_num) and \
                self.outbound_equal(self.table_2d, pos[1]-4+i+1, pos[0]-4+i+1, color_num) and \
                self.outbound_equal(self.table_2d, pos[1]-4+i+2, pos[0]-4+i+2, color_num) and \
                self.outbound_equal(self.table_2d, pos[1]-4+i+3, pos[0]-4+i+3, color_num) and \
                self.outbound_equal(self.table_2d, pos[1]-4+i+4, pos[0]-4+i+4, color_num) :
                    if draw == True:
                        self.gc_draw(self.grid_size/1.5, gc.color_rgb(0,255,0), \
                                          self.grid_size * pos[0], self.grid_size * pos[1], "☆")
                        gc.update()
                    return True

        # check anti-diagonal '/'
        for i in range(5):
            if  self.outbound_equal(self.table_2d, pos[1]+4-i-0, pos[0]-4+i+0, color_num) and \
                self.outbound_equal(self.table_2d, pos[1]+4-i-1, pos[0]-4+i+1, color_num) and \
                self.outbound_equal(self.table_2d, pos[1]+4-i-2, pos[0]-4+i+2, color_num) and \
                self.outbound_equal(self.table_2d, pos[1]+4-i-3, pos[0]-4+i+3, color_num) and \
                self.outbound_equal(self.table_2d, pos[1]+4-i-4, pos[0]-4+i+4, color_num) :
                    if draw == True:
                        self.gc_draw(self.grid_size/1.5, gc.color_rgb(0,255,0), \
                                          self.grid_size * pos[0], self.grid_size * pos[1], "☆")
                        gc.update()
                    return True
    
        
    def chessboard_info(self, pos, color):
        self.huosan_info(pos, color)
        self.longlink_info(pos, color)
        self.huosi_info(pos, color)

    def huosan_info(self, pos, color):
        '''
        huo_san
        --xxx--
        --x-xx-
        --xx-x-
        '''
        color_num = self.color_dict[color]
        color_bnk = self.color_dict['Blank']
        huosan_row = []
        huosi_col = []
        huosi_dig = []
        huosi_adig = []
        huosan_all = []

        # check row
        for i in range(6):
            if  (not self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+0) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+1) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+2) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+3) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+4) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+5) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+6) == color_bnk ) \
                or \
                (    self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+0) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+1) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+2) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+3) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+4) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+5) == color_bnk and \
                 not self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+6) == color_num ) \
                or \
                (not self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+0) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+1) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+2) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+3) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+4) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+5) == color_bnk and \
                 not self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+6) == color_num ) :
                    chess = [[pos[1], pos[0]-5+i+x] for x in range(7) if self.outbound_value(self.table_2d, pos[1], pos[0]-5+i+x) == color_num]
                    if chess not in huosan_row: 
                        huosan_row.append(chess)
                        huosan_all.append(chess)
                        #print('huosan_row', huosan_row)

        # check col
        for i in range(6):
            if  (not self.outbound_value(self.table_2d, pos[1]-5+i+0, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+1, pos[0]) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+2, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+3, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+4, pos[0]) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+5, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+6, pos[0]) == color_bnk ) \
                or \
                (    self.outbound_value(self.table_2d, pos[1]-5+i+0, pos[0]) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+1, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+2, pos[0]) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+3, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+4, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+5, pos[0]) == color_bnk and \
                 not self.outbound_value(self.table_2d, pos[1]-5+i+6, pos[0]) == color_num ) \
                or \
                (not self.outbound_value(self.table_2d, pos[1]-5+i+0, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+1, pos[0]) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+2, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+3, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+4, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+5, pos[0]) == color_bnk and \
                 not self.outbound_value(self.table_2d, pos[1]-5+i+6, pos[0]) == color_num ) :
                    chess = [[pos[1]-5+i+x, pos[0]] for x in range(7) if self.outbound_value(self.table_2d, pos[1]-5+i+x, pos[0]) == color_num]
                    if chess not in huosi_col:   
                        huosi_col.append(chess)
                        huosan_all.append(chess)
                        #print('huosi_col', huosi_col)

        # check dig
        for i in range(6):
            if  (not self.outbound_value(self.table_2d, pos[1]-5+i+0, pos[0]-5+i+0) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+1, pos[0]-5+i+1) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+2, pos[0]-5+i+2) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+3, pos[0]-5+i+3) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+4, pos[0]-5+i+4) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+5, pos[0]-5+i+5) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+6, pos[0]-5+i+6) == color_bnk ) \
                or \
                (    self.outbound_value(self.table_2d, pos[1]-5+i+0, pos[0]-5+i+0) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+1, pos[0]-5+i+1) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+2, pos[0]-5+i+2) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+3, pos[0]-5+i+3) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+4, pos[0]-5+i+4) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+5, pos[0]-5+i+5) == color_bnk and \
                 not self.outbound_value(self.table_2d, pos[1]-5+i+6, pos[0]-5+i+6) == color_num ) \
                or \
                (not self.outbound_value(self.table_2d, pos[1]-5+i+0, pos[0]-5+i+0) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+1, pos[0]-5+i+1) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+2, pos[0]-5+i+2) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+3, pos[0]-5+i+3) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+4, pos[0]-5+i+4) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-5+i+5, pos[0]-5+i+5) == color_bnk and \
                 not self.outbound_value(self.table_2d, pos[1]-5+i+6, pos[0]-5+i+6) == color_num ) :
                    chess = [[pos[1]-5+i+x, pos[0]-5+i+x] for x in range(7) if self.outbound_value(self.table_2d, pos[1]-5+i+x, pos[0]-5+i+x) == color_num]
                    if chess not in huosi_dig:   
                        huosi_dig.append(chess)
                        huosan_all.append(chess)
                        #print('huosi_dig', huosi_dig)

        # check anti-dig
        for i in range(6):
            if  (not self.outbound_value(self.table_2d, pos[1]+5-i-0, pos[0]-5+i+0) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+5-i-1, pos[0]-5+i+1) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]+5-i-2, pos[0]-5+i+2) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+5-i-3, pos[0]-5+i+3) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+5-i-4, pos[0]-5+i+4) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]+5-i-5, pos[0]-5+i+5) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+5-i-6, pos[0]-5+i+6) == color_bnk ) \
                or \
                (    self.outbound_value(self.table_2d, pos[1]+5-i-0, pos[0]-5+i+0) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]+5-i-1, pos[0]-5+i+1) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+5-i-2, pos[0]-5+i+2) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]+5-i-3, pos[0]-5+i+3) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+5-i-4, pos[0]-5+i+4) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+5-i-5, pos[0]-5+i+5) == color_bnk and \
                 not self.outbound_value(self.table_2d, pos[1]+5-i-6, pos[0]-5+i+6) == color_num ) \
                or \
                (not self.outbound_value(self.table_2d, pos[1]+5-i-0, pos[0]-5+i+0) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+5-i-1, pos[0]-5+i+1) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]+5-i-2, pos[0]-5+i+2) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+5-i-3, pos[0]-5+i+3) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+5-i-4, pos[0]-5+i+4) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+5-i-5, pos[0]-5+i+5) == color_bnk and \
                 not self.outbound_value(self.table_2d, pos[1]+5-i-6, pos[0]-5+i+6) == color_num ) :
                    chess = [[pos[1]+5-i-x, pos[0]-5+i+x] for x in range(7) if self.outbound_value(self.table_2d, pos[1]+5-i-x, pos[0]-5+i+x) == color_num]
                    if chess not in huosi_adig:  
                        huosi_adig.append(chess)
                        huosan_all.append(chess)
                        #print('huosi_adig', huosi_adig)
        #print(huosan_all)
        if len(huosan_all) >= 2:
            self.forbidden_flag = 'sansan'
            return False

    def huosi_info(self, pos, color):
        '''
        chong_si
        oxxxx-
        -xxxxo
        oxxx-x
        x-xxxo
        oxx-xx
        xx-xxo
        ox-xxx
        xxx-xo 
        huo_si
        -xxxx-

        class1
        xxxx-? 
        class2
        -xxxx?
        class3
        xxx-x?
        class4
        xx-xx?
        class5
        x-xxx?
        '''
        color_num = self.color_dict[color]
        color_bnk = self.color_dict['Blank']
        huosi_row = []
        huosi_col = []
        huosi_dig = []
        huosi_adig = []
        huosi_all = []
 
        # check row
        for i in range(5):
            if  (    self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+0) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+1) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+2) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+3) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+4) == color_bnk and \
                 not self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+5) == color_num) \
            or \
                (    self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+0) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+1) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+2) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+3) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+4) == color_num and \
                 not self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+5) == color_num) \
            or \
                (    self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+0) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+1) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+2) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+3) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+4) == color_num and \
                 not self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+5) == color_num) \
            or \
                (    self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+0) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+1) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+2) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+3) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+4) == color_num and \
                 not self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+5) == color_num) \
            or \
                (    self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+0) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+1) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+2) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+3) == color_num and \
                     self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+4) == color_num and \
                 not self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+5) == color_num) :
                    chess = [[pos[1], pos[0]-4+i+x] for x in range(6) if self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+x) == color_num]
                    if chess not in huosi_row:
                        huosi_row.append(chess)
                        huosi_all.append(chess)
                        #print('huosi_row', huosi_row)

        # check col
        for i in range(5):
            if  (    self.outbound_value(self.table_2d, pos[1]-4+i+0, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+1, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+2, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+3, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+4, pos[0]) == color_bnk and \
                 not self.outbound_value(self.table_2d, pos[1]-4+i+5, pos[0]) == color_num) \
            or \
                (    self.outbound_value(self.table_2d, pos[1]-4+i+0, pos[0]) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+1, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+2, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+3, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+4, pos[0]) == color_num and \
                 not self.outbound_value(self.table_2d, pos[1]-4+i+5, pos[0]) == color_num) \
            or \
                (not self.outbound_value(self.table_2d, pos[1]-4+i+0, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+1, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+2, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+3, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+4, pos[0]) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+5, pos[0]) == color_num) \
            or \
                (not self.outbound_value(self.table_2d, pos[1]-4+i+0, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+1, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+2, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+3, pos[0]) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+4, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+5, pos[0]) == color_num) \
            or \
                (not self.outbound_value(self.table_2d, pos[1]-4+i+0, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+1, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+2, pos[0]) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+3, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+4, pos[0]) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+5, pos[0]) == color_num) :
                    chess = [[pos[1]-4+i+x, pos[0]] for x in range(6) if self.outbound_value(self.table_2d, pos[1]-4+i+x, pos[0]) == color_num]
                    if chess not in huosi_col:
                        huosi_col.append(chess)
                        huosi_all.append(chess)
                        #print('huosi_col', huosi_col)

        # check dig
        for i in range(5):
            if  (    self.outbound_value(self.table_2d, pos[1]-4+i+0, pos[0]-4+i+0) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+1, pos[0]-4+i+1) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+2, pos[0]-4+i+2) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+3, pos[0]-4+i+3) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+4, pos[0]-4+i+4) == color_bnk and \
                 not self.outbound_value(self.table_2d, pos[1]-4+i+5, pos[0]-4+i+5) == color_num) \
            or \
                (    self.outbound_value(self.table_2d, pos[1]-4+i+0, pos[0]-4+i+0) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+1, pos[0]-4+i+1) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+2, pos[0]-4+i+2) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+3, pos[0]-4+i+3) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+4, pos[0]-4+i+4) == color_num and \
                 not self.outbound_value(self.table_2d, pos[1]-4+i+5, pos[0]-4+i+5) == color_num) \
            or \
                (not self.outbound_value(self.table_2d, pos[1]-4+i+0, pos[0]-4+i+0) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+1, pos[0]-4+i+1) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+2, pos[0]-4+i+2) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+3, pos[0]-4+i+3) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+4, pos[0]-4+i+4) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+5, pos[0]-4+i+5) == color_num) \
            or \
                (not self.outbound_value(self.table_2d, pos[1]-4+i+0, pos[0]-4+i+0) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+1, pos[0]-4+i+1) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+2, pos[0]-4+i+2) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+3, pos[0]-4+i+3) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+4, pos[0]-4+i+4) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+5, pos[0]-4+i+5) == color_num) \
            or \
                (not self.outbound_value(self.table_2d, pos[1]-4+i+0, pos[0]-4+i+0) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+1, pos[0]-4+i+1) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+2, pos[0]-4+i+2) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+3, pos[0]-4+i+3) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+4, pos[0]-4+i+4) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]-4+i+5, pos[0]-4+i+5) == color_num) :
                    chess = [[pos[1]-4+i+x, pos[0]-4+i+x] for x in range(6) if self.outbound_value(self.table_2d, pos[1]-4+i+x, pos[0]-4+i+x) == color_num]
                    if chess not in huosi_dig:
                        huosi_dig.append(chess)
                        huosi_all.append(chess)
                        #print('huosi_dig', huosi_dig)

        # check anti-dig
        for i in range(5):
            if  (    self.outbound_value(self.table_2d, pos[1]+4-i-0, pos[0]-4+i+0) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-1, pos[0]-4+i+1) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-2, pos[0]-4+i+2) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-3, pos[0]-4+i+3) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-4, pos[0]-4+i+4) == color_bnk and \
                 not self.outbound_value(self.table_2d, pos[1]+4-i-5, pos[0]-4+i+5) == color_num) \
            or \
                (    self.outbound_value(self.table_2d, pos[1]+4-i-0, pos[0]-4+i+0) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-1, pos[0]-4+i+1) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-2, pos[0]-4+i+2) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-3, pos[0]-4+i+3) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-4, pos[0]-4+i+4) == color_num and \
                 not self.outbound_value(self.table_2d, pos[1]+4-i-5, pos[0]-4+i+5) == color_num) \
            or \
                (not self.outbound_value(self.table_2d, pos[1]+4-i-0, pos[0]-4+i+0) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-1, pos[0]-4+i+1) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-2, pos[0]-4+i+2) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-3, pos[0]-4+i+3) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-4, pos[0]-4+i+4) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-5, pos[0]-4+i+5) == color_num) \
            or \
                (not self.outbound_value(self.table_2d, pos[1]+4-i-0, pos[0]-4+i+0) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-1, pos[0]-4+i+1) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-2, pos[0]-4+i+2) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-3, pos[0]-4+i+3) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-4, pos[0]-4+i+4) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-5, pos[0]-4+i+5) == color_num) \
            or \
                (not self.outbound_value(self.table_2d, pos[1]+4-i-0, pos[0]-4+i+0) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-1, pos[0]-4+i+1) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-2, pos[0]-4+i+2) == color_bnk and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-3, pos[0]-4+i+3) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-4, pos[0]-4+i+4) == color_num and \
                     self.outbound_value(self.table_2d, pos[1]+4-i-5, pos[0]-4+i+5) == color_num) :
                    chess = [[pos[1]+4-i-x, pos[0]-4+i+x] for x in range(6) if self.outbound_value(self.table_2d, pos[1]+4-i-x, pos[0]-4+i+x) == color_num]
                    if chess not in huosi_adig:    
                        huosi_adig.append(chess)
                        huosi_all.append(chess)
                        #print('huosi_adig', huosi_adig)

        #print(huosi_all)
        if len(huosi_all) >= 2:
            self.forbidden_flag = 'sisi'
            return False

    def longlink_info(self, pos, color):
        '''
        six link
        xxxxxx
        '''
        color_num = self.color_dict[color]
 
        # check row
        for i in range(5):
            if  self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+0) + \
                self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+1) + \
                self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+2) + \
                self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+3) + \
                self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+4) + \
                self.outbound_value(self.table_2d, pos[1], pos[0]-4+i+5) == 6*color_num:
                    self.forbidden_flag = 'longlink'
                    return False

        # check col
        for i in range(5):
            if  self.outbound_value(self.table_2d, pos[1]-4+i+0, pos[0]) + \
                self.outbound_value(self.table_2d, pos[1]-4+i+1, pos[0]) + \
                self.outbound_value(self.table_2d, pos[1]-4+i+2, pos[0]) + \
                self.outbound_value(self.table_2d, pos[1]-4+i+3, pos[0]) + \
                self.outbound_value(self.table_2d, pos[1]-4+i+4, pos[0]) + \
                self.outbound_value(self.table_2d, pos[1]-4+i+5, pos[0]) == 6*color_num:
                    self.forbidden_flag = 'longlink'
                    return False

        # check dig
        for i in range(5):
            if  self.outbound_value(self.table_2d, pos[1]-4+i+0, pos[0]-4+i+0) + \
                self.outbound_value(self.table_2d, pos[1]-4+i+1, pos[0]-4+i+1) + \
                self.outbound_value(self.table_2d, pos[1]-4+i+2, pos[0]-4+i+2) + \
                self.outbound_value(self.table_2d, pos[1]-4+i+3, pos[0]-4+i+3) + \
                self.outbound_value(self.table_2d, pos[1]-4+i+4, pos[0]-4+i+4) + \
                self.outbound_value(self.table_2d, pos[1]-4+i+5, pos[0]-4+i+5) == 6*color_num:
                    self.forbidden_flag = 'longlink'
                    return False

        # check anti-dig
        for i in range(5):
            if  self.outbound_value(self.table_2d, pos[1]+4-i-0, pos[0]-4+i+0) + \
                self.outbound_value(self.table_2d, pos[1]+4-i-1, pos[0]-4+i+1) + \
                self.outbound_value(self.table_2d, pos[1]+4-i-2, pos[0]-4+i+2) + \
                self.outbound_value(self.table_2d, pos[1]+4-i-3, pos[0]-4+i+3) + \
                self.outbound_value(self.table_2d, pos[1]+4-i-4, pos[0]-4+i+4) + \
                self.outbound_value(self.table_2d, pos[1]+4-i-5, pos[0]-4+i+5) == 6*color_num:
                    self.forbidden_flag = 'longlink'
                    return False


    def outbound_equal(self, table, x, y, pt):
        try:
            return (table[x][y] == pt)
        except:
            return False


    def outbound_value(self, table, x, y):
        if x == 0 or x == 1 or x == self.table_row or \
           y == 0 or y == 1 or y == self.table_col :
            return 999
        else:
            try:
                return table[x][y]
            except:
                return 999

    
    


