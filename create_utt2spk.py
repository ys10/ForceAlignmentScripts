import os

wave_dir_path = "wave/"
wave_extension = ".wav"

items = os.listdir(wave_dir_path)
file_name_list = []
for names in items:
    if names.endswith(wave_extension):
        file_name_list.append(names.split(".")[0])
        pass
    pass

file_name_list = list(set(file_name_list))
file_name_list.sort()

result_lines_list = list()
for file_name in file_name_list:
    result_line = "\t".join([file_name, "0000001"])+"\n"
    result_lines_list.append(result_line)
    pass

utt2spk_file_name = "utt2spk.txt"
with open(utt2spk_file_name, 'w', encoding='UTF-8') as utt2spk_file:
    utt2spk_file.writelines(result_lines_list)
    pass
