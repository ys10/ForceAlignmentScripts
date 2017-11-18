text_file_name = "text"
text_key_list = list()
with open(text_file_name, 'r', encoding='UTF-8') as text_file:
    while 1:
        text_lines = text_file.readlines(10000)
        if not text_lines:
            break
        for line in text_lines:
            key = line.split("\t")[0]
            text_key_list.append(key)
            pass
        pass
    pass

utt_file_name = "utt2spk"
utt_key_list = list()
with open(utt_file_name, 'r', encoding='UTF-8') as utt_file:
    while 1:
        utt_lines = utt_file.readlines(10000)
        if not utt_lines:
            break
        for line in utt_lines:
            key = line.split(" ")[0]
            utt_key_list.append(key)
            pass
        pass
    pass

residual_list = list(set(text_key_list)^set(utt_key_list))
print(residual_list)