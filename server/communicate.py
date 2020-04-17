import message as gmsg
import globalval as gv

from socket import *
import threading

connect_permission = 1


def listen_thread(tcpCliSock, addr):
    '''为每个客户端都建立一份监听线程'''

    print('...connnecting from:', addr)

    dev_num = gv.dev_list.add(tcpCliSock)
    tcpCliSock.send(bytes([dev_num]))

    print('dev_num = ', dev_num)

    while True:
        bs = tcpCliSock.recv(1024)

        if bs[0] == 255:
            tcpCliSock.send(bs)
            tcpCliSock.recv(1024)
            break

        m = gmsg.GAMEMSG(0, 0, 0, 0, '')
        m.BYTE2MSG(bs)
        gv.msg_list.append(m)

    gv.dev_list.remove(dev_num)
    tcpCliSock.close()

    print('...connnection close:', addr)


def connect():
    HOST = ''
    PORT = 21567
    ADDR = (HOST, PORT)

    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(10)  # 最大连接数10

    print('waiting for connection...')
    while True:
        tcpCliSock, addr = tcpSerSock.accept()
        threading.Thread(target=listen_thread, args=(tcpCliSock, addr)).start()

        global connect_permission
        if not connect_permission:
            break

    tcpSerSock.close()
    print('server connect permission close')


def close():
    global connect_permission
    connect_permission = 0
    # 新建一个虚拟客户端连接
    HOST = '127.0.0.1'  # or 'localhost'
    PORT = 21567
    ADDR = (HOST, PORT)

    fakeCliSock = socket(AF_INET, SOCK_STREAM)
    fakeCliSock.connect(ADDR)
    fakeCliSock.recv(1024)
    fakeCliSock.send(bytes([255]))
    fakeCliSock.recv(1024)
    fakeCliSock.close()


def send(msg):
    dev_num = msg.rec
    if dev_num == 0:
        dev_list = gv.dev_list
        for i in gv.dev_list.dev_list.keys():
            conn = gv.dev_list.find_dev(i)
            if not conn:
                continue
            conn = conn[0]
            conn.send(msg.MSG2BYTE())
            print('send:', msg.MSG2BYTE())
        return 1
    else:
        conn = gv.dev_list.find_dev(dev_num)
        if not conn:
            return 0
        conn = conn[0]
        conn.send(msg.MSG2BYTE())
        print('send:', msg.MSG2BYTE())
        return 1


def init():
    threading.Thread(target=connect, args=()).start()
