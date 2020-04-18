from collections import defaultdict


# 消息队列
msg_list = []

# 被分配得设备号
dev_num = 0

# 输入单词
word_input = ''

# 自己的昵称
my_name = ''

# 昵称列表 <dev_num, name>
name_list = defaultdict(list)

# 自己的座位号
my_site_num = -1

# 消息应答状态
waiting = 0

# 座位列表 <site_num, dev_num>
site_list = defaultdict(list)

# 座位顺序
site_order_list = []

# 在游戏中的阵营
group = 0

# 游戏模式
game_mode = 0
# 0 游戏大厅 只允许进行注册昵称操作
# 1 游戏大厅 可以重新注册昵称，或者在座位上坐下/站起
# 2 游戏     游戏开始
