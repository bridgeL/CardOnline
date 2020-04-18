import message as gmsg
import globalval as gv
import keyboard as kb
import communicate as cmc


if __name__ == "__main__":
    print('test start...')

    kb.init()
    cmc.connect()

    while True:
        word = gv.word_input
        if word:
            if word[0] == '$':
                if word == '$exit':
                    cmc.close()
                    break
                elif word == '$submit name':
                    name = 'tom'
                    gv.my_name = name
                    m = gmsg.GAMEMSG(gv.dev_num, 0, 1, name.__len__(), name)
                    cmc.send(m)
                    gv.word_input = ''
            else:
                m = gmsg.GAMEMSG(0, 0, 0, 0, word)
                cmc.send(m)
                gv.word_input = ''

        msg_list = gv.msg_list
        gv.msg_list = []
        for m in msg_list:
            print(m.MSG2BYTE())

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
