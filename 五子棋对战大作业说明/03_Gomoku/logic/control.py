import draw.graphic as gc
import logic.judge as jd
from draw.cmd import IOcontrol
from player.chenna.chenna import ChenNa
from player.easyai.easyai import EasyAi

class PlayerControl():

    def __init__(self, table):
        
        # init PlayerControl attribute
        self.src_table = table
        self.table_row = table.table_row
        self.table_col = table.table_col
        self.grid_size = table.grid_size

        self.ioer = IOcontrol()
        self.playerjudger = jd.Judge(table)
        self.win = table.win
        self.gc_draw = table.gc_draw

        # others
        self.last_pos = [-1,-1]

        # players
        self.channa = ChenNa(table)
        self.easyai = EasyAi(table)

    def player_turn(self, player_name, color, step):
        mess = self.gc_draw(self.grid_size/3, "blue", 3*self.grid_size, 0.5*self.grid_size, \
                                  color+" Turn.    "+"Step: "+str(step))
        gc.update()

        # update table2d of playerjudger
        self.playerjudger.table_2d = self.src_table.table_2d.copy()
        # player move, 
        # players can use "playerjudger.table2d" and "playerjudger.check" to design their algorithm
        pos_x, pos_y = self.player_move(player_name, color, step)
        mess.undraw()

        self.last_pos = [pos_x, pos_y]
        return [pos_x, pos_y]


    def player_move(self, player_name, color, step):
        if player_name in ['pc', 'pc_copy']:
            point = self.win.getMouse()
            pos_x = round((point.getX()) / 40)
            pos_y = round((point.getY()) / 40)
            print(player_name+'\'s decision:','x =',pos_x, 'y =',pos_y)
            return pos_x, pos_y

        elif player_name in ['chenna', 'chenna_copy']:
            pos_x, pos_y = self.channa.xiazi(self.playerjudger, color, step)
            print(player_name+'\'s decision:','x =',pos_x, 'y =',pos_y)
            return pos_y, pos_x

        elif player_name in ['easyai', 'easyai_copy']:
            pos_x, pos_y = self.easyai.xiazi(self.playerjudger, color, step)
            print(player_name+'\'s decision:','x =',pos_x, 'y =',pos_y)
            return pos_y, pos_x

        else:
            raise NotImplementedError
