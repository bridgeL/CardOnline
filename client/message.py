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
        self.type = bs[2] - 128
        self.len = bs[3]
        self.msg = bytes.decode(bs[4:])


if __name__ == "__main__":
    msg1 = GAMEMSG(0, 1, 2, 3, 'you')
    bs = msg1.MSG2BYTE()
    print(bs)

    msg2 = GAMEMSG(0, 0, 0, 0, '')
    msg2.BYTE2MSG(bs)
    print(msg2.send, msg2.rec, msg2.type, msg2.len, msg2.msg)
