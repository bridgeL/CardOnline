from collections import defaultdict


class GAMEDEVICELIST:
    '''管理设备的设备列表, 专门写成一个类是为了便于实现自动分配设备号'''

    def __init__(self):
        self.dev_list = defaultdict(list)
        self.cnt = 1

    def add(self, conn):
        num = self.cnt
        self.dev_list[num].append(conn)

        self.cnt = self.cnt + 1
        return num

    def remove(self, dev_num):
        del self.dev_list[dev_num]

    def find_dev(self, dev_num):
        '''返回值为key=dev_num的元素的列表，如果没有查到，返回空列表'''
        return self.dev_list[dev_num]


# 消息队列
msg_list = []

# 设备列表 <dev_num, conn>
dev_list = GAMEDEVICELIST()

# 输入单词
word_input = ''

# 昵称列表 <dev_num, name>
name_list = defaultdict(list)

# 座位列表 <site_num, dev_num>
site_list = defaultdict(list)

# 参与游戏的人数
game_num = 0

# 阵营列表 <site_num, group_num>
group_list = defaultdict(list)

# 当前玩家的座位号
current_site_num = 0
