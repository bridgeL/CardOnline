from collections import defaultdict


# 按键输入
word = ''

# 消息队列
msg_list = []

# 被分配得设备号
dev_num = 0

# 游戏模式
game_mode = 0
'''
    0 游戏注册阶段
    1 游戏大厅阶段
    2 游戏打牌阶段
    3 游戏结算阶段
'''

# 请求消息缓存 -- 一些请求消息需要得到服务器端的回复，这一缓存用于使客户端记住上次发送的请求，以便调用对应的函数
msg_require = []

# 自己的昵称
my_name = ''

# 昵称列表 <dev_num, name>
name_list = defaultdict(list)

# 自己的座位号
my_site_num = -1

# 座位列表 <site_num, dev_num>
site_list = defaultdict(list)

# 有序座位表
site_order_list = []

# 自己在游戏中的阵营
my_group = 0
