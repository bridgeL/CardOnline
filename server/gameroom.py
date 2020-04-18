import message as gmsg
import globalval as gv
import communicate as cmc


def answer_manager(msg):
    t = msg.type
    if t == 1:
        answer_name_set(msg)
    elif t == 2:
        answer_site_set(msg)
    elif t == 4:
        answer_game_start(msg)


def answer_name_set(msg):
    dev_num = msg.send
    name = msg.msg
    len0 = msg.len
    if (gv.name_list[dev_num]).__len__() > 0:
        del gv.name_list[dev_num]

    gv.name_list[dev_num].append(name)
    m = gmsg.GAMEMSG(0, 0, -1, len0+1, chr(dev_num) + name)
    cmc.send(m)


def answer_site_set(msg):
    dev_num = msg.send
    bs = msg.msg.encode()
    site_num = bs[0]
    site_act = bs[1]

    m_all = gmsg.GAMEMSG(0, 0, -3, 3, chr(dev_num)+chr(site_num)+chr(site_act))

    m_no = gmsg.GAMEMSG(0, dev_num, -2, 1, chr(0))
    m_ok = gmsg.GAMEMSG(0, dev_num, -2, 1, chr(1))

    site_list = gv.site_list
    for k in site_list.keys():
        if site_list[k] == dev_num:
            if site_act:
                del gv.site_list[k]
                cmc.send(m_ok)
                cmc.send(m_all)
                return 1
            else:
                cmc.send(m_no)
                return 0

    if site_list[site_num].__len__() != 0:
        cmc.send(m_no)
        return 0

    gv.site_list[site_num].append(dev_num)
    cmc.send(m_ok)
    cmc.send(m_all)
    return 1


def answer_game_start(msg):
    dev_num = msg.send

    m_ok = gmsg.GAMEMSG(0, 0, -4, 1, chr(0))
    m_not_enough = gmsg.GAMEMSG(0, 0, -4, 1, chr(1))
    m_no_power = gmsg.GAMEMSG(0, 0, -4, 1, chr(2))

    site_list = gv.site_list

    if site_list[0].__len__() != 0:
        if site_list[0] == dev_num:
            game_num = site_list.__len__()
            if game_num >= 4:
                gv.game_num = game_num
                gv.game_mode = 2

                site_order_list = []
                for k in site_list.keys():
                    site_order_list.append(k)
                site_order_list.sort()
                gv.site_order_list = site_order_list

                cmc.send(m_ok)

                # 生成牌库

                # 洗牌，发牌

                # 告知

            else:
                cmc.send(m_not_enough)
        else:
            cmc.send(m_no_power)
    else:
        cmc.send(m_no_power)


def answer_game_end():
    pass
