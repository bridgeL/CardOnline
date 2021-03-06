class GAMEDEVICELIST:
    '''管理设备的设备列表, 专门写成一个类是为了便于实现自动分配设备号'''

    def __init__(self):
        self.dev_list = dict()
        self.cnt = 1

    def add(self, conn):
        num = self.cnt
        self.dev_list[num] = conn

        self.cnt = self.cnt + 1
        return num


# 键盘输入
word = ''

# 消息队列
msg_list = []

# 设备列表 <dev_num, conn>
dev_list = GAMEDEVICELIST()

# 昵称列表 <dev_num, name>
name_dict = dict()

# 座位列表 <site_num, dev_num>
site_dict = dict()

# 有序座位表
site_order_list = []

# 当前玩家的座位号
current_site_num = 0

# 玩家手牌列表 <site_num, card_dict>
player_card_dict = dict()

# 阵营列表 <site_num, group_num>
group_dict = dict()

# 游戏模式
game_mode = 0
