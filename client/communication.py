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


conn = socket(AF_INET, SOCK_STREAM)


def connect():
    HOST = '127.0.0.1'  # or 'localhost'
    PORT = 21567
    ADDR = (HOST, PORT)

    global conn
    conn.connect(ADDR)

    bs = conn.recv(1024)

    gv.dev_num = bs[0]
    print('dev_num = ', gv.dev_num)

    threading.Thread(target=listen_thread, args=()).start()


def listen_thread():

    while True:

        global conn
        bs = conn.recv(1024)

        if bs[0] == 255:
            conn.close()
            break

        msg = GAMEMSG(0, 0, 0, 0, '')
        msg.BYTE2MSG(bs)
        gv.msg_list.append(msg)
        print(['debug recv:', msg.MSG2BYTE()])


def send(msg):
    global conn
    conn.send(msg.MSG2BYTE())
    print(['debug send:', msg.MSG2BYTE()])


def close():
    global conn
    conn.send(bytes([255]))
