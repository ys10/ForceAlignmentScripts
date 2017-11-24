from collections import deque

def transform_phoneme(phoneme): # Transform phoneme format
    """
    transform_phoneme(phoneme) -> str

    :param phoneme: a list storing a phoneme as [sentence_ID, begin_time, end_time, phoneme_name].
    :return:  a string in new format as "phoneme_name [begin_time,end_time]".
    """
    new_phoneme = "{2}\t[{0},{1}]\n".format(*phoneme[1:])
    return new_phoneme

def transform_phoneme_name(phoneme_name):
    """
    transform_phoneme_name(phoneme_name) -> str

    :param phoneme_name: a string as "ang4_B".
    :return: a string as "ang4".
    """
    new_phoneme_name = phoneme_name.split("_")[0]
    return new_phoneme_name

sentence_dict = dict()
final_align_file_name = "test/results/final_align_zero_initial.txt"
with open(final_align_file_name, "r") as final_align_file:
    while 1:
        lines = final_align_file.readlines(10000)
        if not lines:
            break
        for line in lines:
            phoneme = line.strip().split("\t\t")
            # print(phoneme)
            if phoneme[0] not in sentence_dict.keys(): # A new sentence.
                sentence_dict[phoneme[0]] = list() # Add a new list to store phonemes of the sentence.
                pass
            phoneme[3] = transform_phoneme_name(phoneme[3]) # Transform phoneme name.
            transformed_phoneme = transform_phoneme(phoneme) # Transform phoneme format.
            sentence_dict[phoneme[0]].append(transformed_phoneme)
            pass
        pass
    pass

transformed_alignment_file_name = "test/results/transformed_align_zero_initial.txt"
with open(transformed_alignment_file_name, "w") as transformed_alignment_file:
    for key in sentence_dict.keys():
        phoneme_queue = deque(sentence_dict[key])
        phoneme_queue.appendleft(key + "\n")
        phoneme_queue.append(".\n")
        transformed_alignment_file.writelines(phoneme_queue)
        pass
    pass