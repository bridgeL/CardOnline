import message as gmsg
import globalval as gv
import communicate as cmc


def told_wait_manager(msg):
    t = msg.type
    if t == -1:
        told_name_set(msg)
    elif t == -3:
        told_site_set(msg)
    elif t == -4:
        told_game_start(msg)

    elif t == -2:
        wait_site_set(msg)


def told_name_set(msg):
    str0 = msg.msg
    dev_num_comein = str0[0].encode()
    name_comein = str0[1:]

    # 一些图形操作
    print(name_comein, ' 刚刚加入了游戏')

    name_list = gv.name_list
    if name_list[dev_num_comein].__len__() > 0:
        del gv.name_list[dev_num_comein]

    gv.name_list[dev_num_comein].append(name_comein)


def told_site_set(msg):
    bs = msg.msg
    dev_num = bs[0]
    site_num = bs[1]
    site_act = bs[2]

    # 一些图形操作
    if site_act == 1:
        print(gv.name_list[dev_num], ' 离开了 ', site_num, ' 号座位')
    else:
        print(gv.name_list[dev_num], ' 加入了 ', site_num, ' 号座位')

    if site_act == 1:
        gv.site_list[site_num].append(dev_num)
    else:
        del gv.site_list[site_num]


def told_game_start(msg):
    game_mode = gv.game_mode
    if game_mode == 0:

        # 一些图形操作
        print('本局游戏已经开始了，你可（zhi）以（neng）旁观')
    else:

        # 一些图像操纵
        print('游戏开始')

    gv.game_mode = 2


# 缓存
buf_site_num = -1
buf_site_act = -1


def wait_site_set(msg):
    global buf_site_num
    global buf_site_act

    bs = msg.msg
    able = bs[0]

    if able:

        # 一些图形操作
        if buf_site_act:
            print('你离开了 ', buf_site_num, ' 号座位')
        else:
            print('你加入了 ', buf_site_num, ' 号座位')

        if buf_site_act:
            gv.site_num = -1
        else:
            gv.site_num = buf_site_num

    else:

        # 一些图形操作
        if buf_site_act:
            print('你试图离开 ', buf_site_num, ' 号座位，但失败了')
        else:
            print('你试图加入 ', buf_site_num, ' 号座位，但失败了')


def require_name_set(name):
    len0 = name.__len__()
    m = gmsg.GAMEMSG(gv.dev_num, 0, 1, len0, name)
    cmc.send(m)

    # 一些图形操作
    print('命名成功')


def require_site_set(site_num, site_act):
    global buf_site_num
    global buf_site_act
    game_mode = gv.game_mode

    if game_mode == 0:

        # 一些图形操作
        print('你现在还不能选座，请先起个昵称')

    else:

        m = gmsg.GAMEMSG(gv.dev_num, 0, 2, 2, chr(site_num)+chr(site_act))
        cmc.send(m)

        buf_site_num = site_num
        buf_site_act = site_act


def require_game_start():

    game_mode = gv.game_mode

    if game_mode == 0:

        # 一些图形操作
        print('你不能开始游戏，请先起个昵称，并找个座位坐下')

    else:
        if gv.site_num != 0:

            # 一些图形操作
            print('你不能开始游戏，只有0号位玩家可以宣布开始游戏')

        else:

            m = gmsg.GAMEMSG(gv.dev_num, 0, 4, 1, chr(1))
            cmc.send(m)

            gv.game_mode = 2
