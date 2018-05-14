# coding: UTF-8
import os, sys, getopt
from collections import deque


def get_wav_scp_results(dir_path, wave_extension, wav_prefix=None):
    result_lines_list = list()
    dir_queue = deque()
    dir_queue.append(dir_path)
    while 1:
        if not dir_queue:  # No more iterated directories.
            break
        current_path = dir_queue.popleft()
        items = os.listdir(current_path)
        for names in items:
            if os.path.isdir(current_path + "/" + names):  # A directory.
                dir_queue.append(current_path + "/" + names)  # Append directory to the queue.
                continue
            if names.endswith(wave_extension):
                if wav_prefix == 'zh' and names.startswith('2'):
                    continue
                if wav_prefix == 'en' and not names.startswith('2'):
                    continue
                file_name = names.split(".")[0]
                result_line = "\t".join([file_name, current_path + "/" + file_name + wave_extension]) + "\n"
                result_lines_list.append(result_line)
                pass
            pass
        pass
    result_lines_list.sort(key=lambda line: line.split("\t")[0])
    return result_lines_list


def write_wav_scp(wave_scp_file_name, result_lines_list):
    with open(wave_scp_file_name, 'w', encoding='UTF-8') as wave_scp_file:
        wave_scp_file.writelines(result_lines_list)
        pass
    pass


def usage():
    print("Usage: python create_wav_scp.py [-i wave_directory_path] [-o output_file_path] [-l language: zh | en]")


if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:l:")
    input_dir = ""
    output_file = ""
    lang = None
    for op, value in opts:
        if op == "-i":
            input_dir = value
        elif op == "-o":
            output_file = value
        elif op == "-l":
            lang = value
        elif op == "-h":
            usage()
            sys.exit()
    results_list = get_wav_scp_results(input_dir, ".wav", lang)
    write_wav_scp(output_file, results_list)
