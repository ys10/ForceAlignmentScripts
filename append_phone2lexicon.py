# coding: UTF-8

original_lexicon_file_name = "results/lexicon.txt"
result_lexicon_file_name = "results/new_lexicon.txt"

result_lines_list = list()
with open(original_lexicon_file_name, 'r', encoding='UTF-8') as original_lexicon_file:
    while 1:
        lines = original_lexicon_file.readlines(10000)
        if not lines:
            break
        for line in lines:
            result_lines_list.append(line)
            if "5" in line:
                new_line = line.replace("5", "6", 1)
                new_line = new_line.replace("5", "2", 1)
                result_lines_list.append(new_line)
                pass
            pass
        pass
    pass

with open(result_lexicon_file_name, 'w', encoding='UTF-8') as result_lexicon_file:
    result_lexicon_file.writelines(result_lines_list)
    pass