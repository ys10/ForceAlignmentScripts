# coding: UTF-8
import wave
import sys, getopt


def get_wav_end_time(wav_file_path):
    with wave.open(wav_file_path, "rb") as wave_file:
        params = wave_file.getparams()
        _, _, sampling_rate, num_sampling_points = params[:4]
        end_time = str(round(num_sampling_points / sampling_rate, 3))
        pass
    return end_time


def get_segment_list(wav_scp_file_name):
    result_lines_list = list()
    with open(wav_scp_file_name) as wav_scp_file:
        while 1:
            lines = wav_scp_file.readlines(10000)
            if not lines:
                break
            for line in lines:
                file_id, file_path = line.strip().split("\t")
                start_time = str(0.000)
                end_time = get_wav_end_time(file_path)
                result_line = "\t".join([file_id, file_id, start_time, end_time]) + "\n"
                result_lines_list.append(result_line)
                pass
            pass
        pass
    return result_lines_list


def write_segment_file(segment_file_name, result_lines_list):
    with open(segment_file_name, 'w', encoding='UTF-8') as segment_file:
        segment_file.writelines(result_lines_list)
        pass
    pass


def usage():
    print("Usage: python create_segments.py [-i wav.scp_path] [-o output_file_path] ")


if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
    input_file = ""
    output_file = ""
    for op, value in opts:
        if op == "-i":
            input_file = value
        elif op == "-o":
            output_file = value
        elif op == "-h":
            usage()
            sys.exit()
    results_list = get_segment_list(input_file)
    write_segment_file(output_file, results_list)
