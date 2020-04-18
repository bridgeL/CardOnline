import globalval as gv
import communicate as cmc
import gameroom
import threading


def keyborad_thread():
    '''为键盘输入设置一个线程'''
    while True:
        gv.word_input = input('>')
        if gv.word_input == '$exit':
            break


def init():
    threading.Thread(target=keyborad_thread, args=()).start()


def deal_keyboard():
    word = gv.word_input
    if word:
        if word[0] == '$':

            # 退出游戏
            if word == '$exit':
                cmc.close()
                return 1

            # 拆解命令
            cmd_list = word.split()
            gv.word_input = ''

            # 修改昵称
            if cmd_list[0] == '$rename':
                gameroom.require_name_set(cmd_list[1])

            # 修改座位
            elif cmd_list[0] == '$site':

                if cmd_list[1] == 'sit':
                    sit_act = 0
                elif cmd_list[1] == 'leave':
                    sit_act = 1

                gameroom.require_site_set(int(cmd_list[2]), sit_act)

            # 开始游戏
            elif cmd_list[0] == '$start':
                gameroom.require_game_start()

        # 自定义消息，调试用
        # else:
        #     m = gmsg.GAMEMSG(0, 0, 0, 0, word)
        #     cmc.send(m)
        #     gv.word_input = ''

    return 0


def deal_mouse():
    pass
