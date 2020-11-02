import os
import sys
import time
import random

import draw.cmd as cmd
import draw.table as tb
import logic.judge as jd
import logic.control as cl
#import logic.crash_on_ipy

def Gomoku():
    ########################################
    # Platform config and CMD preprint
    ########################################

    # config and initialization
    table_row = 16  # 1 ~ 15 is valid
    table_col = 16  # 0 , 16 is invalid
    grid_size = 40

    table   = tb.Table(table_row=table_row, table_col=table_col, grid_size=grid_size)
    ioer    = cmd.IOcontrol()
    judger  = jd.Judge(table)
    cler    = cl.PlayerControl(table)

    # config player
    player_list = {'0':'pc',         #E.g. yourself control the pc
                   '1':'chenna',
                   '2':'easyai'}
    player1, player2 = ioer.config_player(player_list)

    # show table
    ioer.platform_info(player1, player2)
    table.init_table(player1, player2)


    ########################################
    # Game start
    ########################################
    select_bigin = table.Threechose
    #print(len(select_bigin))
    random.shuffle(select_bigin)
    #print(select_bigin[0][0],select_bigin[0][1])
    player_turn = player2
    color_dict = {player1:'Black', player2:'White'}
    table.move_chess([8,8], color_dict[player1], 0)
    table.move_chess(select_bigin[0][0], color_dict[player2], 1)
    table.move_chess(select_bigin[0][1], color_dict[player1], 2)

    end_flag = None
    end_player = None
    step_count = 3

    while(1):
        if player_turn == player1:      # black
            # make decision
            pos = cler.player_turn(player1, "Black", step_count)

            # move
            table.move_chess(pos, color_dict[player1], step_count)

            # check validation
            end_flag = judger.check(pos, color_dict[player1], True)
            end_player = player1
            end_color = color_dict[player1]

            # switch player
            player_turn = player2
            
            if end_flag != 'continue':
                break

        elif player_turn == player2:    # white
            # make decision
            pos = cler.player_turn(player2, "White", step_count)

            # move
            table.move_chess(pos, color_dict[player2], step_count)

            # check validation
            end_flag = judger.check(pos, color_dict[player2], True)
            end_player = player2
            end_color = color_dict[player2]

            # switch player
            player_turn = player1
            
            if end_flag != 'continue':
                break

        else:
            print('err turn')

        step_count = step_count + 1
        if step_count == (table_row-1)*(table_col-1):
            break

    ########################################
    # Game end
    ########################################
    if step_count == (table_row-1)*(table_col-1) and end_flag == 'continue':
        ioer.cmd_print('No winner!')
        table.gc_draw(grid_size/2, "red", 8*grid_size, 10*grid_size, "No winner!")

    if end_flag == 'pos_confict':
        ioer.cmd_print('player ' + end_player  +'('+end_color+')' +' made a confict decision, Lose!')
        ioer.cmd_print('player ' + player_turn +'('+color_dict[player_turn]+')' + ' win this game.')
        table.gc_draw(grid_size/2, "red", 8*grid_size, 10*grid_size, "Position Conflicted!\n"+player_turn+"("+color_dict[player_turn]+") win!")

    if end_flag.find('forbidden') >= 0:
        ioer.cmd_print('player ' + end_player  +'('+end_color+')' +' made a forbidden decision, Lose!')
        ioer.cmd_print('player ' + player_turn +'('+color_dict[player_turn]+')' + ' win this game.')
        table.gc_draw(grid_size/2, "red", 8*grid_size, 10*grid_size, end_flag+"\n"+player_turn+"("+color_dict[player_turn]+") win!")

    if end_flag == 'winner':
        ioer.cmd_print('player ' + end_player  +'('+end_color+')' +' finished five link, Win!')
        ioer.cmd_print('player ' + player_turn +'('+color_dict[player_turn]+')' + ' lose.')
        table.gc_draw(grid_size/2, "red", 8*grid_size, 10*grid_size, "Five Link!\n"+end_player+"("+end_color+") win!")


    # pause and observe the result
    table.win.getMouse()
    table.win.close()


    # restart the game
    print('\nplay again? just input ' + 'r')
    return input()


if __name__ == '__main__':
    while Gomoku() == 'r':
        pass
    