import message as gmsg
import globalval as gv
import keyboard as kb
import communicate as cmc
import gameroom
import gui
import msgdeal


def deal_manager(msg):
    game_mode = gv.game_mode
    if game_mode == 0 or game_mode == 1:
        gameroom.told_wait_manager(msg)
    elif game_mode == 2:
        pass


if __name__ == "__main__":
    print('test start...')

    kb.init()
    cmc.connect()

    while True:

        # 读取并处理键盘事件
        if gui.deal_keyboard():
            break

        # 读取并处理鼠标事件
        if gui.deal_mouse():
            break

        # 读取并处理游戏消息
        msgdeal.deal_msg()

    print('...test end')

# if __name__ == "__main__":
#     print('test start...')

#     kb.init()
#     cmc.connect()

#     while True:
#         word = gv.word_input
#         if word:
#             if word[0] == '$':
#                 if word == '$exit':
#                     cmc.close()
#                     break
#             else:
#                 m = gmsg.GAMEMSG(0, 0, 0, 0, word)
#                 cmc.send(m)
#                 gv.word_input = ''

#         msg_list = gv.msg_list
#         gv.msg_list = []
#         for m in msg_list:
#             print(m.MSG2BYTE())

#     print('...test end')
