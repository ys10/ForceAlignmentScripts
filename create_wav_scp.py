# coding: UTF-8
import os
from collections import deque


def get_wav_scp_results(dir_path, wave_extension):
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


if __name__ == "__main__":
    results_list = get_wav_scp_results("wave", ".wav")
    write_wav_scp("resource/wav.scp", results_list)
