import globalval as gv
import gameroom


def deal_msg():
    msg_list = gv.msg_list
    gv.msg_list = []
    for m in msg_list:
        print('recv:', m.MSG2BYTE())
        deal_manager(m)


def deal_manager(msg):
    t = msg.type
    if t == -1:
        gameroom.told_name_set(msg)
    elif t == -3:
        gameroom.told_site_set(msg)
    elif t == -4:
        gameroom.told_game_start(msg)
    elif t == -2:
        wait_site_set(msg)
