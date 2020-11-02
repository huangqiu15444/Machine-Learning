import os
import numpy as np
import draw.graphic as gc

class IOcontrol():

    def cmd_clear(self):
        os.system('cls')

    def cmd_print(self, content):
        print(content)

    def platform_info(self, p1, p2):
        os.system('cls')
        self.cmd_print('---------------------------------------------')
        self.cmd_print('                                           ')
        self.cmd_print('            Gomuku vs platform             ')
        self.cmd_print('                                           ')
        self.cmd_print('                                           ')
        self.cmd_print('          player1         '+p1+'           ')
        self.cmd_print('                                           ')
        self.cmd_print('            vs.                            ')
        self.cmd_print('                                           ')
        self.cmd_print('          player2         '+p2+'           ')
        self.cmd_print('                                           ')
        self.cmd_print('---------------------------------------------')

    def save_table(self, table):
        # in txt form
        f = open('chess_log.txt','w')
        f.write(str(table))
        f.close()

        # or you can save it in *.npy form
        # np.save('chess_log.npy', table)

    def config_player(self, player_list):
        self.cmd_print('Player List')
        self.cmd_print('index\tname')
        for i in player_list:
            self.cmd_print((i) + '\t' + player_list[i])

        player1 = player2 = '-1'
        while player1 not in player_list or player2 not in player_list:
            self.cmd_print('Select players')
            player1 = input('Player1 (black):')
            player2 = input('Player2 (white):')

        player1 = player_list[player1]
        player2 = player_list[player2]
        if player1 == player2:
            player2 = player2 + '_copy'

        return player1, player2