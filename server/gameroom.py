import message as gmsg
import globalval as gv
import communicate as cmc


def manager(msg):
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
    #
    pass


def answer_game_start(msg):
    gv.game_num = gv.site_list.__len__()
    pass


def answer_game_end():
    pass
