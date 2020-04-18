import globalvalue as gv

from socket import *
import threading


class GAMEMSG:
    '''游戏消息类'''

    def __init__(self, send, rec, type0, len0, msg):
        ''' 
            int 寄信人设备号
            int 收信人设备号
            int 消息类型
            int 消息长度
            string 消息数组
        '''
        self.send = send
        self.rec = rec
        self.type = type0
        self.len = len0
        self.msg = msg

    # def __init__(self):
    #     __init__(self,0,0,0,0,'')

    def MSG2BYTE(self):
        '''转换消息类为BYTE信息，便于传输'''
        return bytes([self.send, self.rec, self.type+128, self.len]) \
            + str.encode(self.msg)

    def BYTE2MSG(self, bs):
        '''转换BYTE信息为消息类，便于使用'''
        self.send = bs[0]
        self.rec = bs[1]
        self.type = bs[2]-128
        self.len = bs[3]
        self.msg = bytes.decode(bs[4:])


def listen_thread(conn, addr):
    '''为每个客户端都建立一份监听线程'''

    print('...connnecting from:', addr)

    dev_num = gv.dev_list.add(conn)
    conn.send(bytes([dev_num]))

    print('dev_num = ', dev_num)

    while True:
        bs = conn.recv(1024)

        if bs[0] == 255:
            conn.send(bs)
            conn.recv(1024)
            break

        msg = GAMEMSG(0, 0, 0, 0, '')
        msg.BYTE2MSG(bs)
        gv.msg_list.append(msg)
        print(['debug recv:', msg.MSG2BYTE()])

    del gv.dev_list.dev_list[dev_num]
    conn.close()

    print('...connnection close:', addr)


# 连接许可通过，这个关闭connect函数
connect_permission = 1


def init():
    threading.Thread(target=connect, args=()).start()


def connect():
    HOST = ''
    PORT = 21567
    ADDR = (HOST, PORT)

    server = socket(AF_INET, SOCK_STREAM)
    server.bind(ADDR)
    server.listen(10)  # 最大连接数10

    print('waiting for connection...')
    while True:
        conn, addr = server.accept()
        threading.Thread(target=listen_thread, args=(conn, addr)).start()

        global connect_permission
        if not connect_permission:
            break

    server.close()
    print('server connect permission close')


def close():
    global connect_permission
    if connect_permission:
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
        # 广播告知所有设备
        dev_list = gv.dev_list.dev_list
        for k in dev_list.keys():
            conn = dev_list[k][0]
            conn.send(msg.MSG2BYTE())
            print(['debug send:', msg.MSG2BYTE()])
        return 1

    else:
        # 仅发送此设备
        conn = gv.dev_list.dev_list[dev_num]
        if conn.__len__() == 0:
            return 0
        conn = conn[0]
        conn.send(msg.MSG2BYTE())
        print(['debug send:', msg.MSG2BYTE()])
        return 1
