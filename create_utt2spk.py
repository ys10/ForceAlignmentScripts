# coding: UTF-8


def get_utt2spk_list(wav_scp_file_name):
    result_lines_list = list()
    with open(wav_scp_file_name) as wav_scp_file:
        while 1:
            lines = wav_scp_file.readlines(10000)
            if not lines:
                break
            for line in lines:
                file_id, _ = line.strip().split("\t")
                spk_id = "0000001"
                result_line = "\t".join([file_id, spk_id])+"\n"
                result_lines_list.append(result_line)
                pass
            pass
        pass
    return result_lines_list


def write_utt2spk_file(utt2spk_file_name, result_lines_list):
    with open(utt2spk_file_name, 'w', encoding='UTF-8') as utt2spk_file:
        utt2spk_file.writelines(result_lines_list)
        pass
    pass


if __name__ == "__main__":
    results_list = get_utt2spk_list("resource/wav.scp")
    write_utt2spk_file("resource/utt2spk", results_list)
