import numpy as np

from draw.cmd import IOcontrol
import draw.graphic as gc
import logic.judge as jd

class Table():

    def __init__(self, table_row, table_col, grid_size):

        # init table attribute
        self.table_row = table_row
        self.table_col = table_col
        self.grid_size = grid_size

        self.table_2d = np.zeros([self.table_row+1, self.table_col+1], dtype=int)
        self.piece_dict = {}
        self.color_dict = {'White':1, 'Black':-1, 'Blank':0}

        # close autoflash for updating table by myself
        self.win = gc.GraphWin("Gomoku Game", self.grid_size * self.table_col, self.grid_size * self.table_row, autoflush=False)

        self.ioer = IOcontrol()
        self.Threechose = [[[9, 7], [8, 10]],
                           [[9, 7], [9, 10]],
                           [[9, 7], [7, 10]],
                           [[9, 7], [10, 10]],
                           #[[9, 7], [10, 7]],
                           [[9, 7], [9, 8]],
                           [[9, 7], [10, 8]],
                           [[9, 7], [10, 6]],
                           [[9, 7], [7, 9]],
                           #[[9, 7], [9, 9]],
                           #[[9, 7], [10, 9]],
                           [[9, 7], [8, 9]],
                           #[[9, 7], [6, 10]],
                           #[[8, 7], [10, 10]],
                           [[8, 7], [10, 8]],
                           [[8, 7], [9, 10]],
                           [[8, 7], [8, 6]],
                           [[8, 7], [9, 9]],
                           [[8, 7], [10, 8]],
                           [[8, 7], [9, 8]],
                           [[8, 7], [10, 7]],
                           #[[8, 7], [9, 7]],
                           [[8, 7], [10, 6]],
                           #[[8, 7], [9, 6]],
                           [[8, 7], [10, 9]],
                           [[8, 7], [8, 9]]]

    def init_table(self, player1, player2):

        # set my favourite color
        #win.setBackground(gc.color_rgb(164,211,238))
        self.win.setBackground(gc.color_rgb(227,236,193))

        # draw table
        i1 = 1*self.grid_size
        while i1 < self.grid_size * self.table_col:
            l = gc.Line(gc.Point(i1, 1*self.grid_size), gc.Point(i1, self.grid_size * (self.table_col-1)))
            l.draw(self.win)
            i1 = i1 + self.grid_size
        
        i2 = 1*self.grid_size
        while i2 < self.grid_size * self.table_row:
            l = gc.Line(gc.Point(1*self.grid_size, i2), gc.Point(self.grid_size * (self.table_row-1), i2))
            l.draw(self.win)
            i2 = i2 + self.grid_size

        # display player
        msg = "[Black] "+player1+" , "+"[White] "+player2
        message = gc.Text(gc.Point(12*self.grid_size, 0.5*self.grid_size), msg)
        message.setSize(int(self.grid_size/3))
        message.setTextColor('blue3')
        message.draw(self.win)

    
    def move_chess(self, pos, player, step_count):

        # use pos[0] pos[1] to draw windows
        # ------> x
        # |
        # ↓ y
        # use pos[1] pos[0] to index table
        # ------> y
        # |
        # ↓ x

        # piece == current player chess
        piece = gc.Circle(gc.Point(self.grid_size * pos[0], self.grid_size * pos[1]), self.grid_size/2.5)
        piece.setFill(player)
        piece.draw(self.win)

        # draw step on chess
        message = gc.Text(gc.Point(self.grid_size * pos[0], self.grid_size * pos[1]), str(step_count))
        message.setSize(int(self.grid_size/4))
        message.setTextColor(gc.color_rgb(250,128,114))
        message.draw(self.win)

        # update window
        gc.update()

        # save piece object into dict for unmoving
        self.piece_dict[str(pos)] = [piece, message]    #print(self.piece_dict)    #print(type(piece) == gc.Circle)

        # save table in 2d form
        # note that pos[0] is col index, pos[1] is row index
        self.table_2d[pos[1]][pos[0]] = self.color_dict[player]

        # save to local dir
        self.ioer.save_table(self.table_2d[1:16,1:16])


    def unmove_chess(self, pos):

        # the piece can be obtained from "func move_chess()"
        
        # check existence
        if str(pos) in self.piece_dict.keys():
            piece = self.piece_dict[str(pos)][0]
            mess = self.piece_dict[str(pos)][1]
            self.piece_dict.pop(str(pos))
        else:
            raise Exception('no piece in this pos')

        # undraw the chess
        piece.undraw()
        mess.undraw()

        # undate window
        gc.update()

        # unwrite the table
        self.table_2d[pos[1]][pos[0]] = self.color_dict['Blank']

        # save to local dir
        # self.ioer.save_table(self.table_2d)

    def gc_draw(self, size, color, x, y, msg):
        message = gc.Text(gc.Point(x, y), msg)
        message.setSize(int(size))
        message.setStyle("bold")
        message.setTextColor(color)
        message.draw(self.win)
        return message


        