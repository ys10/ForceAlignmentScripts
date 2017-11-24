# coding: UTF-8

merged_align_file_name = "results/final_align_zero_initial.txt"
sentence_dict = dict()  # A dictionary of  sentence lists, each list contains some phonemes with their begin & end time.
with open(merged_align_file_name, "r") as merged_align_file:
    while 1:
        lines = merged_align_file.readlines(10000)
        if not lines:
            break
        for line in lines:
            phoneme = line.split("\t\t")
            # print(phoneme)
            if phoneme[0] not in sentence_dict.keys():
                sentence_dict[phoneme[0]] = list()
                pass
            sentence_dict[phoneme[0]].append("\t".join(phoneme[1:]))
            pass
        pass
    pass

labs_dir_name = "labs/ours_zero_initial/"
labs_prefix_name = "ours_zero_initial_"
labs_extension_name = ".lab"
for sentence_file_name in sentence_dict.keys():
    with open(labs_dir_name + labs_prefix_name + sentence_file_name + labs_extension_name, "w") as sentence_file:
        sentence_file.writelines(sentence_dict[sentence_file_name])
        pass
    pass
