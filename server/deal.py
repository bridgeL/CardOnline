import communication as com
import globalvalue as gv
import gamectrl

import threading


def init():
    threading.Thread(target=keyboard_thread, args=()).start()
    com.init()


def keyboard_thread():
    '''为键盘输入设置一个线程'''
    while True:
        gv.word = input('>')
        if gv.word == '$exit':
            break


def deal():
    '''处理各类事件'''
    # 处理键盘事件
    if deal_keyboard():
        return 1

    # 处理消息事件
    deal_msg()

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

            elif word == '$close connect':
                gv.word = ''
                com.close()

            # elif word == '$build deck':
            #     gv.word = ''
            #     gamectrl.build_deck()

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
    if t == 1:
        gamectrl.answer_name_set(msg)
    elif t == 2:
        gamectrl.answer_site_set(msg)
    elif t == 4:
        gamectrl.answer_game_start(msg)
