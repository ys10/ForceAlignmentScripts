original_text_file_name = "han_ad_decl.txt"
result_text_file_name = "transcription.txt"

result_line_list = list()
with open(original_text_file_name, 'r', encoding='UTF-8') as original_text_file:
    while 1:
        lines = original_text_file.readlines(10000)
        if not lines:
            break
        # print(len(lines))
        for i in range(0, len(lines), 2):
            original_list = lines[i].split("\t")
            # print(i)
            # print(original_list[0])
            # print(original_list[1])
            if(i+1 >= len(lines)):
                text = original_text_file.readlines(1)[0].split("\t")
            else:
                text = lines[i + 1].split("\t")
            # print(text)
            # print(text[1])
            original_list[1] = text[1]
            result_line_list.append("\t".join(original_list) + "\n")
            pass
        pass
pass

# result_line_list = list(set(result_line_list))
result_line_list.sort()

with open(result_text_file_name, 'w', encoding='UTF-8') as result_text_file:
    result_text_file.writelines(result_line_list)
    pass
