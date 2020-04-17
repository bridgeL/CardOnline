import message as gmsg
import keyboard as kb
import globalval as gv
import communicate as cmc
import gameroom


def deal_cmd(word):
    if word == '$exit':
        return 1
    elif word == '$close connect':
        cmc.close()

    gv.word_input = ''
    return 0


def deal_manager(msg):
    game_mode = gv.game_mode
    if game_mode == 0:
        gameroom.answer_manager(msg)
    elif game_mode == 2:
        pass


if __name__ == "__main__":
    print('test start...')

    kb.init()
    cmc.init()

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
