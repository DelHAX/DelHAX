#!python
# -*- coding: utf-8 -*-

import argparse

parser = argparse.ArgumentParser(description='Скрипт для сравнения Oracle артефактов.')
parser.add_argument('actual', help='Префикс файла для сравнения.')
parser.add_argument('etalon', help='Префикс файла для сравнения.')
args = parser.parse_args()


def read(file1, file2):
    file1_dict = dict()
    file2_dict = dict()
    with open(file1, 'r') as act_file:
        filling_dict(file1_dict, act_file)
    with open(file2, 'r') as etalon_file:
        filling_dict(file2_dict, etalon_file)
    with open('file1_1.txt', 'a') as resfile1, open('file2_1.txt', 'a') as resfile2, open('not_in_file2.txt',
                                                                                          'a') as resfile3, open(
            'not_in_file1.txt', 'a') as resfile4:
        for key in file1_dict.keys():
            if key in file2_dict:
                if file1_dict[key] - file2_dict[key] > 0:
                    resfile1.write(key * int(file1_dict[key] - file2_dict[key]))
                elif file1_dict[key] - file2_dict[key] < 0:
                    resfile2.write(key * int(file2_dict[key] - file1_dict[key]))
                elif file1_dict[key] - file2_dict[key] == 0:
                    continue
                else:
                    print('что то не так')
            else:
                resfile3.write(key)
        for key1 in file2_dict.keys():
            if key1 not in file1_dict:
                resfile4.write(key1)


def filling_dict(dict_name, open_file_name):
    for line in open_file_name.readlines():
        if dict_name.keys().__contains__(line):
            dict_name[line] = dict_name[line] + 1
        else:
            dict_name[line] = 1


read(args.actual, args.etalon)
