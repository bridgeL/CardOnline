import message as gmsg
import keyboard as kb
import globalval as gv
import communicate as cmc
import gameroom


if __name__ == "__main__":
    print('test start...')

    kb.init()
    cmc.init()

    while True:
        word = gv.word_input
        if word:
            if word[0] == '$':
                if word == '$exit':
                    break
                elif word == '$close connect':
                    cmc.close()
                    gv.word_input = ''
            else:
                m = gmsg.GAMEMSG(0, 0, 0, 0, word)
                cmc.send(m)
                gv.word_input = ''

        msg_list = gv.msg_list
        gv.msg_list = []
        for m in msg_list:
            print(m.MSG2BYTE())
            gameroom.manager(m)

    print('...test end')
