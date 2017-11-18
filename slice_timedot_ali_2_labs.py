# coding: UTF-8

timepot_align_file_name = "test/timepot_dnn_2_test.txt"
sentence_dict = dict()  # A dictionary of  sentence lists, each list contains some phonemes with their begin & end time.
with open(timepot_align_file_name, "r") as timepot_align_file:
    current_sentence_name = ""
    while 1:
        lines = timepot_align_file.readlines(10000)
        if not lines:
            break
        for line in lines:
            temp_list = line.strip().split("\t")
            print(temp_list)
            if len(temp_list) == 1:  # New sentence(sentence name) or sentence end(a char ".").
                current_sentence_name = temp_list[0]
                continue
            if current_sentence_name not in sentence_dict.keys():# First phoneme of a sentence.
                sentence_dict[current_sentence_name] = list()
                pass
            phoneme_list = temp_list[1].strip("[]").split(",")
            phoneme_list.append(temp_list[0]+"\n")
            phoneme = "\t".join(phoneme_list)
            sentence_dict[current_sentence_name].append(phoneme)
            pass
        pass
    pass

labs_dir_name = "labs/dnn2/"
for sentence_file_name in sentence_dict.keys():
    with open(labs_dir_name + sentence_file_name, "w") as sentence_file:
        sentence_file.writelines(sentence_dict[sentence_file_name])
        pass
    pass