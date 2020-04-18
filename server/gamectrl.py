import globalvalue as gv
import communication as com


def answer_name_set(msg):
    '''
        1号消息
        客户端设备号，0，消息号，名字长度，名字

        -1号消息
        0，0，消息号，1 + 名字长度，[设备号 名字] 
    '''
    dev_num = msg.send
    name = msg.msg
    len0 = msg.len

    m_all = com.GAMEMSG(0, 0, -1, len0 + 1, chr(dev_num) + name)

    name_list = gv.name_list

    # 同一设备号的重命名将顶掉之前的昵称，但为了方便，目前在require函数中禁止重命名
    if name_list[dev_num].__len__() > 0:
        del gv.name_list[dev_num]

    gv.name_list[dev_num].append(name)

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
    str0 = msg.msg
    site_num = ord(str0[0])
    site_act = ord(str0[1])

    m_ok = com.GAMEMSG(0, dev_num, -2, 1, chr(0))
    m_no = com.GAMEMSG(0, dev_num, -2, 1, chr(1))

    m_all = com.GAMEMSG(0, 0, -3, 3, chr(dev_num)+chr(site_num)+chr(site_act))

    site_list = gv.site_list
    if site_act:
        if site_list[site_num].__len__() > 0:
            if site_list[site_num][0] == dev_num:
                com.send(m_ok)
                com.send(m_all)
                del gv.site_list[site_num]

            else:
                com.send(m_no)
        else:
            com.send(m_no)
    else:
        if site_list[site_num].__len__() > 0:
            com.send(m_no)
        else:
            gv.site_list[site_num].append(dev_num)
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

    m_ok = com.GAMEMSG(0, dev_num, -4, 1, chr(0))
    m_not_enough = com.GAMEMSG(0, dev_num, -4, 1, chr(1))
    m_no_power = com.GAMEMSG(0, dev_num, -4, 1, chr(2))

    m_all = com.GAMEMSG(0, 0, -5, 0, '')

    site_list = gv.site_list

    if site_list[0].__len__() > 0:

        if site_list[0][0] == dev_num:

            player_num = site_list.__len__()

            if player_num >= 4:

                com.send(m_ok)
                com.send(m_all)

                # 游戏开始
                gv.game_mode = 2

                # 生成有序座位表
                site_order_list = []
                for k in site_list.keys():
                    site_order_list.append(k)
                site_order_list.sort()
                gv.site_order_list = site_order_list

                # 生成牌库

                # 洗牌，发牌

                # 告知
                answer_init_cards()

                # 查找第一发现人

            else:
                com.send(m_not_enough)
        else:
            com.send(m_no_power)
    else:
        com.send(m_no_power)


def answer_init_cards():
    '''
        -12号消息
        0，客户端设备号，消息号，卡牌个数，[卡牌id,...]
    '''
    pass


def answer_game_end():
    pass
