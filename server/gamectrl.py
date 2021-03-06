import globalvalue as gv
import communication as com

from collections import defaultdict


def answer_name_set(msg):
    '''
        1号消息
        客户端设备号，0，消息号，名字长度，名字

        -1号消息
        0，0，消息号，1 + 名字长度，[设备号 名字]
    '''
    dev_num = msg.send
    name = msg.msg.decode()
    len0 = msg.len

    m_all = com.GAMEMSG(0, 0, -1, len0 + 1, bytes([dev_num]) + name.encode())

    name_dict = gv.name_dict

    # 同一设备号的重命名将顶掉之前的昵称，但为了方便，目前在require函数中禁止重命名
    if dev_num in name_dict.keys():
        del gv.name_dict[dev_num]

    gv.name_dict[dev_num] = name

    com.send(m_all)


def answer_site_set(msg):
    '''
        2号消息 需要批复
        客户端设备号，0，消息号，2，[座位号 动作]
                                        1 离开
                                        0 坐下

        -2号消息
        0，客户端设备号，消息号，1，答复
                                    0 可以
                                    1 不可以

        -3号消息
        0，0，消息号，3，[设备号 座位号 动作]
    '''
    dev_num = msg.send
    bs = msg.msg
    site_num = bs[0]
    site_act = bs[1]

    m_ok = com.GAMEMSG(0, dev_num, -2, 1, bytes([0]))
    m_no = com.GAMEMSG(0, dev_num, -2, 1, bytes([1]))

    m_all = com.GAMEMSG(0, 0, -3, 3, bytes([dev_num, site_num, site_act]))

    site_dict = gv.site_dict
    if site_act:
        if site_num in site_dict.keys():
            if site_dict[site_num] == dev_num:
                com.send(m_ok)
                com.send(m_all)
                del gv.site_dict[site_num]

            else:
                com.send(m_no)
        else:
            com.send(m_no)
    else:
        if site_num in site_dict.keys():
            com.send(m_no)
        else:
            gv.site_dict[site_num] = dev_num
            com.send(m_ok)
            com.send(m_all)


def answer_game_start(msg):
    '''
        4号消息
        客户端设备号，0，消息号，0，''

        -4号消息
        0，客户端设备号，消息号，1，答复
                                0 可以开始
                                1 人数不足
                                2 没有权限

        -5号消息
        0，0，消息号，0，''
    '''
    dev_num = msg.send

    m_ok = com.GAMEMSG(0, dev_num, -4, 1, bytes([0]))
    m_not_enough = com.GAMEMSG(0, dev_num, -4, 1, bytes([1]))
    m_no_power = com.GAMEMSG(0, dev_num, -4, 1, bytes([2]))

    m_all = com.GAMEMSG(0, 0, -5, 0, bytes([]))

    site_dict = gv.site_dict

    if 0 in site_dict.keys():

        if site_dict[0] == dev_num:

            player_num = site_dict.__len__()

            if player_num >= 4:

                com.send(m_ok)
                com.send(m_all)

                # 游戏开始
                gv.game_mode = 2

                # 生成有序座位表
                site_order_list = []
                for k in site_dict.keys():
                    site_order_list.append(k)
                site_order_list.sort()
                gv.site_order_list = site_order_list

                # 生成牌库，洗牌，发牌
                build_deck()

                # 查找第一发现人

            else:
                com.send(m_not_enough)
        else:
            com.send(m_no_power)
    else:
        com.send(m_no_power)


def answer_game_end():
    pass


def build_deck():
    '''
        创建牌组，洗牌，并分配初始手牌

        普通人 0
        不在场证明 1
        第一发现人 2
        共犯 3
        目击者 4
        谣言 5
        情报交换 6
        交易 7
        犯人 8
        侦探 9
        神犬 10

        -12号消息
        0，客户端设备号，消息号，1 + 2*卡牌个数，[自己/其他人设备号,[卡牌id,卡牌type],...]

    '''
    player_num = gv.site_dict.__len__()
    card_num = player_num * 4

    # <card_id, card_type>
    deck = dict()

    # 全部是普通人
    for i in range(card_num):
        deck[i] = 0

    # 洗牌

    # 发牌

    site_order_list = gv.site_order_list
    for site_num in site_order_list:
        gv.player_card_dict[site_num] = dict()

    for i in range(card_num):
        site_num = site_order_list[i % player_num]
        gv.player_card_dict[site_num][i] = deck[i]

    site_dict = gv.site_dict
    for site_num in site_order_list:
        card_list = gv.player_card_dict[site_num]
        dev_num = site_dict[site_num]
        bs = bytes([])
        for card_id in card_list.keys():
            card_type = card_list[card_id]
            bs = bs + bytes([card_id, card_type])
        msg = com.GAMEMSG(0, dev_num, -12, 2*4+1,
                          bytes([dev_num]) + bs)
        com.send(msg)
