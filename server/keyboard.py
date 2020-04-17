import globalval as gv

import threading


def keyborad_thread():
    '''为键盘输入设置一个线程'''
    while True:
        gv.word_input = input('>')
        if gv.word_input == '$exit':
            break


def init():
    threading.Thread(target=keyborad_thread, args=()).start()
