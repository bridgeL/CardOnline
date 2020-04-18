import globalvalue as gv
import communication as com


def require_name_set(name):
    '''
        1号消息
        自己设备号，0，消息号，名字长度，名字 
    '''
    game_mode = gv.game_mode
    if game_mode == 0:
        len0 = name.__len__()
        m = com.GAMEMSG(gv.dev_num, 0, 1, len0, name)
        com.send(m)

        # 一些图形操作
        print('命名成功')

        gv.game_mode = 1
        gv.my_name = name

    else:
        # 一些图形操作
        print('你已经起过名字了')


def require_site_set(site_num, site_act):
    '''
        2号消息 需要批复
        自己设备号，0，消息号，2，[座位号 动作]
                                        1 离开
                                        0 坐下
    '''
    m = com.GAMEMSG(gv.dev_num, 0, 2, 2, chr(site_num)+chr(site_act))

    game_mode = gv.game_mode

    if game_mode == 0:

        # 一些图形操作
        print('你现在还不能选座，请先起个昵称')

    elif game_mode == 1:

        if site_act:

            if gv.my_site_num != site_num:

                # 一些图形操作
                print('你不能离开此座位，因为坐的人不是你')

            else:
                com.send(m)

                # 放入请求消息缓存
                gv.msg_require.append(m)

        else:

            if gv.my_site_num != -1:

                # 一些图形操作
                print('你已经坐下了，请先离开原座位再换座')

            else:
                com.send(m)

                # 放入请求消息缓存
                gv.msg_require.append(m)

    else:

        # 一些图形操作
        print('当前不能选座')


def require_game_start():
    '''
        4号消息
        自己设备号，0，消息号，0，''
    '''
    game_mode = gv.game_mode

    if game_mode == 0:

        # 一些图形操作
        print('你不能开始游戏，请先起个昵称，并找个座位坐下')

    elif game_mode == 1:
        site_num = gv.my_site_num

        if site_num == -1:

            # 一些图形操作
            print('你不能开始游戏，请找个座位坐下')

        elif site_num != 0:

            # 一些图形操作
            print('你不能开始游戏，只有0号位玩家可以宣布开始游戏')

        else:

            m = com.GAMEMSG(gv.dev_num, 0, 4, 0, '')
            com.send(m)

    else:

        # 一些图形操作
        print('不能重复开始游戏')


def told_name_set(msg):
    '''
        -1号消息
        0，0，消息号，1 + 名字长度，[设备号 名字]
    '''
    str0 = msg.msg
    dev_num = ord(str0[0])
    name = str0[1:]

    # 一些图形操作
    print(name, '刚刚加入了游戏')

    name_list = gv.name_list

    # 同一设备号的重命名将顶掉之前的昵称，但为了方便，目前在require函数中禁止重命名
    if name_list[dev_num].__len__() > 0:
        del gv.name_list[dev_num]

    gv.name_list[dev_num].append(name)


def told_site_set(msg):
    '''
        -3号消息
        0，0，消息号，3，[设备号 座位号 动作]
    '''
    str0 = msg.msg
    dev_num = ord(str0[0])
    site_num = ord(str0[1])
    site_act = ord(str0[2])

    # 一些图形操作
    if site_act == 1:
        print(gv.name_list[dev_num], ' 离开了 ', site_num, ' 号座位')
    else:
        print(gv.name_list[dev_num], ' 加入了 ', site_num, ' 号座位')

    if site_act == 1:
        del gv.site_list[site_num]
        gv.my_site_num = -1
    else:
        gv.site_list[site_num].append(dev_num)
        gv.my_site_num = site_num


def told_game_start(msg):
    '''
        -5号消息
        0，0，消息号，0，''
    '''
    game_mode = gv.game_mode
    if game_mode == 1 and gv.my_site_num != -1:

        # 一些图像操纵
        print('游戏开始')

        gv.game_mode = 2

    # else:
    # 旁观模式仍在开发中
    #     # 一些图形操作
    #     print('本局游戏已经开始了，你可（zhi）以（neng）旁观')


def wait_site_set(msg):
    '''
        -2号消息
        0，自己的设备号，消息号，1，答复
                                    0 可以
                                    1 不可以
    '''
    str0 = msg.msg
    disable = ord(str0[0])

    # 取出请求消息缓存
    m_r = gv.msg_require[0]
    gv.msg_require.clear()

    str0 = m_r.msg
    site_num = ord(str0[0])
    site_act = ord(str0[1])

    if disable:

        # 一些图形操作
        if site_act:
            print('你试图离开 ', site_num, ' 号座位，但失败了')
        else:
            print('你试图加入 ', site_num, ' 号座位，但失败了')

    else:

        # 一些图形操作
        if site_act:
            print('你离开了 ', site_num, ' 号座位')
        else:
            print('你加入了 ', site_num, ' 号座位')

        if site_act:
            gv.site_num = -1
        else:
            gv.site_num = site_num


def wait_game_start(msg):
    '''
        -4号消息
        0，自己设备号，消息号，1，答复
                                0 可以开始
                                1 人数不足
                                2 没有权限
    '''
    str0 = msg.msg
    disable = ord(str0[0])

    if disable == 0:

        # 一些图形操作
        print('游戏开始')

    elif disable == 1:

        # 一些图形操作
        print('人数不足，不能开始游戏')

    else:

        # 一些图形操作
        print('不是0号位玩家，没有权限开始游戏')
