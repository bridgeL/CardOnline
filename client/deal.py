import communication as com
import globalvalue as gv
import gamectrl

import threading


def init():
    threading.Thread(target=keyboard_thread, args=()).start()
    com.connect()


def keyboard_thread():
    '''为键盘输入设置一个线程'''
    while True:
        gv.word = input('>')
        if gv.word == '$exit':
            break


def deal():
    '''处理各类事件'''
    # 处理鼠标事件
    if deal_mouse():
        return 1

    # 处理键盘事件
    if deal_keyboard():
        return 1

    # 处理消息事件
    deal_msg()

    return 0


def deal_mouse():
    '''处理点击卡片/座位等操作，以及关闭窗口等操作'''

    return 0


def deal_keyboard():
    '''处理键盘输入的各种命令'''
    word = gv.word
    if word:
        if word[0] == '$':
            if word == '$exit':

                # 关闭通讯模块
                com.close()
                return 1

            else:
                # 命令分解
                cmd_list = word.split()
                gv.word = ''

                # 修改昵称
                if cmd_list[0] == '$name':
                    gamectrl.require_name_set(cmd_list[1])

                # 修改座位
                elif cmd_list[0] == '$sit':
                    gamectrl.require_site_set(int(cmd_list[1]), 0)

                elif cmd_list[0] == '$leave':
                    gamectrl.require_site_set(int(cmd_list[1]), 1)

                # 开始游戏
                elif cmd_list[0] == '$start':
                    gamectrl.require_game_start()

                # 打牌
                elif cmd_list[0] == '$play':
                    gamectrl.require_play_card(int(cmd_list[1]))

                # 测试
                elif cmd_list[0] == '$test':

                    # 测试 多信息密集发送 是否能做到 接收端 自动 分割
                    if cmd_list[1] == 'msgs':
                        msg = com.GAMEMSG(gv.dev_num, 0, 0, 1, bytes([99]))
                        com.send(msg)
                        com.send(msg)
                        com.send(msg)

                    # 方便测试，自动输入加入房间后的各类指令
                    elif cmd_list[1] == '0':
                        gamectrl.require_name_set('a')
                        gamectrl.require_site_set(0, 0)
                    elif cmd_list[1] == '1':
                        gamectrl.require_name_set('b')
                        gamectrl.require_site_set(1, 0)
                    elif cmd_list[1] == '2':
                        gamectrl.require_name_set('c')
                        gamectrl.require_site_set(2, 0)
                    elif cmd_list[1] == '3':
                        gamectrl.require_name_set('d')
                        gamectrl.require_site_set(3, 0)

    return 0


def deal_msg():
    '''处理消息队列中的消息'''
    msg_list = gv.msg_list
    gv.msg_list = []

    for m in msg_list:
        manager_msg(m)


def manager_msg(msg):
    '''管理各类消息，丢给不同的模块的函数处理'''
    t = msg.type
    if t == -1:
        gamectrl.told_name_set(msg)
    elif t == -3:
        gamectrl.told_site_set(msg)
    elif t == -5:
        gamectrl.told_game_start()
    elif t == -12:
        gamectrl.told_card_dict(msg)

    elif t == -2:
        gamectrl.wait_site_set(msg)
    elif t == -4:
        gamectrl.wait_game_start(msg)
