# coding: UTF-8

import sys
import getopt


def usage():
    print("Usage: python slice_merged_ali_2_labs.py [-i original_file_path] [-o output_dir_path] [-p prefix_name]")


opts, args = getopt.getopt(sys.argv[1:], "hi:o:p:")
original_file_path = ""
output_dir_path = ""
labs_prefix_name = ""
for op, value in opts:
    if op == "-i":
        original_file_path = value
    elif op == "-o":
        output_dir_path = value
    elif op == "-p":
        labs_prefix_name = value
    elif op == "-h":
        usage()
        sys.exit()

sentence_dict = dict()  # A dictionary of  sentence lists, each list contains some phonemes with their begin & end time.
with open(original_file_path, "r") as merged_align_file:
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

labs_extension_name = ".lab"
for sentence_file_name in sentence_dict.keys():
    with open(output_dir_path + labs_prefix_name + sentence_file_name + labs_extension_name, "w") as sentence_file:
        sentence_file.writelines(sentence_dict[sentence_file_name])
        pass
    pass
