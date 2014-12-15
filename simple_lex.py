# coding=utf-8



#在这部分中，你将使用图转移算法手工实现一个小型的词法分析器。
#* 分析器的输入：存储在文本文件中的字符序列，字符取自ASCII字符集。文件中可能包括四种记号：关键字if、符合C语言标准的标识符、空格符、回车符\n。
#* 分析器的输出：打印出所识别的标识符的种类、及行号、列号信息。
#【示例】对于下面的文本文件：
#ifx if iif       if
#iff     if
#你的输出应该是：
#ID(ifx) (1, 1)
#IF        (1, 4)
#ID(iif)  (1, 8)
#IF       (1, 13)
#ID(iff) (2, 1)
#IF       (2, 8)

import string

key_words = {"if"}
identifier_head_chars = set(list(string.ascii_letters + "_"))
digits = set(list(string.digits))
identifier_chars = identifier_head_chars | digits


def get_text_data(file_name):
    return open(file_name).readlines()


def analyse(text_data):
    token_info = {}
    counter = 0
    for data in text_data:
        counter += 1
        index = 0
        while index < len(data):
            if data[index] in identifier_head_chars:
                start = end = index
                if index < len(data) - 1:
                    index += 1
                    while data[index] in identifier_chars:
                        end = index
                        if index < len(data) - 1:
                            index += 1
                        else:
                            break
                else:
                    break
                token = data[start:end + 1]
                position = (counter, start + 1)
                if token in key_words:
                    token_info[position] = token.upper()
                else:
                    token_info[position] = "ID({token})".format(token=token)
            else:
                index += 1
                start = end = index
    return token_info

if __name__ == "__main__":
    print "please input file name: \n"
    file_name = raw_input()
    print "TOKEN INFO:\n"
    text_data = get_text_data(file_name)
    token_info = analyse(text_data)
    for key, value in token_info.iteritems():
        print value, key
