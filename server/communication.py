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
        return bytes([self.send, self.rec, self.type + 30, self.len]) \
            + self.msg

    def BYTE2MSG(self, bs):
        '''转换BYTE信息为消息类，便于使用'''
        self.send = bs[0]
        self.rec = bs[1]
        self.type = bs[2]-30
        self.len = bs[3]
        self.msg = bs[4:]


def listen_thread(conn, addr):
    '''为每个客户端都建立一份监听线程'''

    print('...connnecting from:', addr)

    dev_num = gv.dev_list.add(conn)
    conn.send(bytes([dev_num]))

    print('give dev_num = ', dev_num)

    while True:
        bs = conn.recv(1024)

        if bs[0] == 255:
            conn.send(bs)
            conn.recv(1024)
            break

        # 根据信息尾标254，进行信息分割
        bs_list = bs.split(bytes([254]))
        # print(bs_list)
        for b in bs_list:
            if b.__len__() == 0:
                continue
            msg = GAMEMSG(0, 0, 0, 0, bytes([]))
            msg.BYTE2MSG(b)
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
        for conn in dev_list.values():

            # 添加信息尾标254，用于信息分割
            bs = msg.MSG2BYTE() + bytes([254])
            conn.send(bs)
            print(['debug send:', bs])

    else:
        # 仅发送此设备
        dev_list = gv.dev_list.dev_list
        if dev_num in dev_list.keys():

            conn = dev_list[dev_num]

            # 添加信息尾标254，用于信息分割
            bs = msg.MSG2BYTE() + bytes([254])
            conn.send(bs)
            print(['debug send:', bs])
