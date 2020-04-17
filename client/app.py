import message as gmsg
import globalval as gv
import keyboard as kb
import communicate as cmc
import gameroom


def deal_cmd(word):
    if word == '$exit':
        cmc.close()
        return 1
    else:
        cmd_list = word.split()
        gv.word_input = ''

        if cmd_list[0] == '$rename':
            gameroom.require_name_set(cmd_list[1])

        elif cmd_list[0] == '$site':

            if cmd_list[1] == 'sit':
                sit_act = 0
            elif cmd_list[1] == 'leave':
                sit_act = 1

            gameroom.require_site_set(int(cmd_list[2]), sit_act)

        elif cmd_list[0] == '$start':
            gameroom.require_game_start()

    return 0


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
        word = gv.word_input
        if word:
            if word[0] == '$':
                if deal_cmd(word):
                    break
            # else:
            #     m = gmsg.GAMEMSG(0, 0, 0, 0, word)
            #     cmc.send(m)
            #     gv.word_input = ''

        msg_list = gv.msg_list
        gv.msg_list = []
        for m in msg_list:
            print(m.MSG2BYTE())
            deal_manager(m)

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
