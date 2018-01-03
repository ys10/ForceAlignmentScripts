# coding: UTF-8

import os, sys, getopt


def make_text(first_line, second_line):
    first_line = first_line.encode('utf-8').decode('utf-8-sig')
    second_line = second_line.encode('utf-8').decode('utf-8-sig')
    if "/" not in second_line and "." not in second_line:  # Chinese phonemes.
        return "\t".join([first_line.split("\t")[0], second_line.strip()]) + "\n"
    if "/" in first_line or "%" in first_line:  # English phonemes need insert silence phonemes.
        id_str, word_str = first_line.strip().split("\t")
        phoneme_str = second_line.strip()
        """replace char in str"""
        word_str = word_str.replace(",", "")
        word_str = word_str.replace(".", "")
        word_str = word_str.replace("?", "")
        word_str = word_str.replace("!", "")
        phoneme_str = phoneme_str.replace(". ", "")
        """insert silence phonemes"""
        word_list = word_str.split(" ")
        phoneme_list = phoneme_str.split(" / ")
        index = 0  # Current index.
        insert = 0  # Insert silence number.
        concat = 0  # Concatenated word number.
        for word in word_list:
            if "%" in word:
                if word.endswith("%"):
                    phoneme_list.insert(index + 1 + insert + concat, "sil")
                    pass
                else:  # Two concatenated words
                    phoneme_list.insert(index + 1 + insert + concat, "sil")
                    concat += 1
                insert += 1
            if "/" in word:
                if word.endswith("/"):
                    phoneme_list.insert(index + 1 + insert + concat, "sil")
                    pass
                else:  # Two concatenated words
                    phoneme_list.insert(index + 1 + insert + concat, "sil")
                    concat += 1
                insert += 1
            index += 1
            pass
        return "\t".join([id_str, " ".join(phoneme_list)]) + "\n"
    else:  # English phonemes needn't insert silence phonemes.
        id_str, _ = first_line.strip().split("\t")
        phoneme_str = second_line.strip()
        """replace char in str"""
        phoneme_str = phoneme_str.replace(". ", "")
        phoneme_str = phoneme_str.replace(" / ", " ")
        return "\t".join([id_str, phoneme_str]) + "\n"


def get_text_from_transcription_file(transcription_file_name):
    result_line_list = list()
    with open(transcription_file_name, 'r', encoding='UTF-8') as original_text_file:
        while 1:
            lines = original_text_file.readlines(10000)
            if not lines:
                break
            for i in range(0, len(lines), 2):
                if i + 1 >= len(lines):
                    text_line = make_text(lines[i], original_text_file.readlines(1)[0])
                else:
                    text_line = make_text(lines[i], lines[i+1])
                result_line_list.append(text_line)
                pass
            pass
        pass
    return result_line_list


def get_text_list(transcription_dir):
    result_line_list = list()
    items = os.listdir(transcription_dir)
    for item in items:
        result_line_list.extend(get_text_from_transcription_file(transcription_dir + "/" + item))
        pass
    result_line_list.sort()
    return result_line_list


def write_text_file(text_file_name, result_lines_list):
    with open(text_file_name, 'w', encoding='UTF-8') as result_text_file:
        result_text_file.writelines(result_lines_list)
        pass
    pass


def usage():
    print("Usage: python create_text.py [-i transcription_directory_path] [-o output_file_path] ")


if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
    input_dir = ""
    output_file = ""
    for op, value in opts:
        if op == "-i":
            input_dir = value
        elif op == "-o":
            output_file = value
        elif op == "-h":
            usage()
            sys.exit()
    results_list = get_text_list(input_dir)
    write_text_file(output_file, results_list)
