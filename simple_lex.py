# coding=utf-8

import string

key_word = {"if"}
identifier_head_chars = set(list(string.ascii_letters + "_"))
digits = set(list(string.digits))
identifier_chars = identifier_head_chars | digits


def analyse(text_data):
    for data in text_data:
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
                print data[start:end + 1]
                print start + 1, end + 1
            else:
                index += 1
                start = end = index


if __name__ == "__main__":
    text_data = ["ifx if iif       if"]
    analyse(text_data)
