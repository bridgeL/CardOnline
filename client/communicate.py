import message as gmsg
import globalval as gv

from socket import *
import threading

tcpCliSock = socket(AF_INET, SOCK_STREAM)


def listen_thread():

    while True:

        global tcpCliSock
        bs = tcpCliSock.recv(1024)

        if bs[0] == 255:
            tcpCliSock.close()
            break

        m = gmsg.GAMEMSG(0, 0, 0, 0, '')
        m.BYTE2MSG(bs)
        gv.msg_list.append(m)


def send(msg):
    global tcpCliSock
    tcpCliSock.send(msg.MSG2BYTE())


def connect():
    HOST = '127.0.0.1'  # or 'localhost'
    PORT = 21567
    ADDR = (HOST, PORT)

    global tcpCliSock
    tcpCliSock.connect(ADDR)

    bs = tcpCliSock.recv(1024)

    gv.dev_num = bs[0]
    print('dev_num = ', gv.dev_num)

    threading.Thread(target=listen_thread, args=()).start()


def close():
    global tcpCliSock
    tcpCliSock.send(bytes([255]))
