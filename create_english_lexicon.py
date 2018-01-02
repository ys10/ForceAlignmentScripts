# coding=utf-8

lexicon_line_list = list()
with open("resource/cmudict-0.7b.symbols") as symbol_file:
    while 1:
        lines = symbol_file.readlines(10000)
        if not lines:
            break
        for line in lines:
            symbol = line.strip()
            lexicon_line_list.append(" ".join([symbol, symbol]) + "\n")
            pass
        pass
    pass

with open("resource/english_lexicon", "w") as english_lexicon_file:
    english_lexicon_file.writelines(lexicon_line_list)
    pass