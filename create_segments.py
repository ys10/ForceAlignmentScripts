# coding: UTF-8

import os
import wave

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
    with wave.open(wave_dir_path + file_name + wave_extension, "rb") as waveFile:
        params = waveFile.getparams()
        nChannels, sampleWidth, samplingRate, nSamplingPoints = params[:4]
        start_time = str(0.000)
        end_time = str(round(nSamplingPoints/samplingRate, 3))
        result_line = "\t".join([file_name, file_name, start_time, end_time]) + "\n"
        result_lines_list.append(result_line)
        pass
    pass

segment_file_name = "segments.txt"
with open(segment_file_name, 'w', encoding='UTF-8') as segment_file:
    segment_file.writelines(result_lines_list)
    pass
