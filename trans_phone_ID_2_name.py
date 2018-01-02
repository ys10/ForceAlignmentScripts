# coding: UTF-8

# construct phone dict.
phone_file_name = "results/phones.txt"
phone_dict = dict()
with open(phone_file_name) as phone_file:
    while 1:
        phone_lines = phone_file.readlines(100000)
        if not phone_lines:
            break
        for phone_line in phone_lines:
            phone_list = phone_line.split(' ')
            phone_name = phone_list[0]
            phone_ID = phone_list[1]
            phone_dict[phone_ID] = phone_name
            pass
        pass
#
result_file_name = "results/mono_final_align.txt"
with open(result_file_name, 'w') as result_file:
    #
    original_file_name = "results/mono_merged_alignment.txt"
    with open(original_file_name) as f:
        while 1:
            result_lines = list()
            lines = f.readlines(100000)
            if not lines:
                break
            for line in lines:
                # print(line)
                original_list = line.split(' ')
                # replace duration with end time
                start_time = float(original_list[2])
                duration = float(original_list[3])
                end_time = round(start_time + duration, 3)
                original_list[3] = str(end_time)
                # replace phone ID with phone name
                phone_ID = original_list[4]
                phone_name = phone_dict[phone_ID]
                original_list[4] = phone_name
                # remove channel info
                original_list.pop(1)
                # join & append to result lines
                result_line = "\t\t".join(original_list) + "\n"
                result_lines.append(result_line)
                pass
            result_file.writelines(result_lines)
            pass
        pass
    pass
