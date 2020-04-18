import message as gmsg
import globalval as gv
import communicate as cmc


def told_wait_manager(msg):
    pass


def told_name_set(msg):
    str0 = msg.msg
    dev_num_comein = ord(str0[0])
    name_comein = str0[1:]

    # 一些图形操作
    print(name_comein, ' 刚刚加入了游戏')

    name_list = gv.name_list
    if name_list[dev_num_comein].__len__() > 0:
        del gv.name_list[dev_num_comein]

    gv.name_list[dev_num_comein].append(name_comein)


def told_site_set(msg):
    str0 = msg.msg
    dev_num = ord(str0[0])
    site_num = ord(str0[1])
    site_act = ord(str0[2])

    # 一些图形操作
    name = gv.name_list[dev_num][0]

    if site_act == 1:
        print(name, ' 离开了 ', site_num, ' 号座位')
    else:
        print(name, ' 加入了 ', site_num, ' 号座位')

    if site_act == 1:
        del gv.site_list[site_num]
    else:
        gv.site_list[site_num].append(dev_num)


def told_game_start(msg):

    str0 = msg.msg
    able = ord(str0[0])

    if able == 0:
        game_mode = gv.game_mode
        if game_mode == 0:

            # 一些图形操作
            print('本局游戏已经开始了，你可（zhi）以（neng）旁观')
        else:

            # 一些图像操纵
            print('游戏开始')

            site_list = gv.site_list
            site_order_list = []
            for k in site_list.keys():
                site_order_list.append(k)
            site_order_list.sort()
            gv.site_order_list = site_order_list

            gv.game_mode = 2

    elif able == 1:

        # 一些图形操作
        print('不能开始游戏，游戏人数少于4人')

    # elif able == 2:

    #     # 一些图形操作
    #     print('你不能开始游戏，只有0号位玩家可以宣布开始游戏')


# 缓存
buf_site_num = -1
buf_site_act = -1


def wait_site_set(msg):
    global buf_site_num
    global buf_site_act

    str0 = msg.msg
    able = ord(str0[0])

    if able == 1:

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

    gv.game_mode = 1

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
            print('不能开始游戏，只有0号位玩家可以宣布开始游戏')

        else:

            m = gmsg.GAMEMSG(gv.dev_num, 0, 4, 1, chr(1))
            cmc.send(m)
