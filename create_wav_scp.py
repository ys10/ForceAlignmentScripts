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

result_lines_list = list()
for file_name in file_name_list:
    result_line = "\t".join([file_name, wave_dir_path + file_name + wave_extension])+"\n"
    result_lines_list.append(result_line)
    pass

wave_scp_file_name = "wav.scp"
with open(wave_scp_file_name, 'w', encoding='UTF-8') as wave_scp_file:
    wave_scp_file.writelines(result_lines_list)
    pass
