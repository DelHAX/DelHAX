#!python
# -*- coding: utf-8 -*-

import argparse
import filecmp
import os
import sys
import zipfile

parser = argparse.ArgumentParser(description='Скрипт для сравнения двух zip файлов.')
parser.add_argument('etalon_file', help='Эталон для сравнения.')
parser.add_argument('export_file', help='Экспортированный файл".')
args = parser.parse_args()
dir01 = 'etalon'
dir02 = 'export'


def extract(argument, folder):
    unzip = zipfile.ZipFile(argument)
    unzip.extractall(folder)
    unzip.close()


def folder_map(dir):
    folder = ''
    for root, dirs, files in os.walk(dir):
        folder += os.listdir(os.path.join(root)).__str__() + '\n'
    return folder


def file_compare(dir1, dir2):
    i = 0
    for root, dirs, files in os.walk(dir1):
        for name in files:
            f_src = os.path.join(root, name)
            f_dst = f_src.replace(dir1, dir2)
            if not filecmp.cmp(f_src, f_dst) and name not in excludeFiles:
                print('Файлы ' + name + ' не совпали, сравню их построчно!\n')
                file1_dict = dict()
                file2_dict = dict()
                with open(f_src, 'r', encoding='UTF8') as etalon_file:
                    filling_dict(file1_dict, etalon_file)
                with open(f_dst, 'r', encoding='UTF8') as act_file:
                    filling_dict(file2_dict, act_file)
                for key in file1_dict.keys():
                    if key not in file2_dict:
                        sys.stderr.write('В файле ' + name + ' отличаются строки: ' + key + ' .\n')
                        i = i + 1
                    else:
                        continue
                for key1 in file2_dict.keys():
                    if key1 not in file1_dict:
                        sys.stderr.write('Файлы ' + name + ' отличаются строки: ' + key1 + ' .\n')
                        i = i + 1
                    else:
                        continue
    return i


def filling_dict(dict_name, open_file_name):
    for line in open_file_name.readlines():
        if dict_name.keys().__contains__(line):
            dict_name[line] = dict_name[line] + 1
        else:
            dict_name[line] = 1


if __name__ == "__main__":
    extract(args.etalon_file, dir01)
    extract(args.export_file, dir02)
    if folder_map(dir01) == folder_map(dir02):
        if file_compare(dir01, dir02) > 0:
            sys.exit(1)
        else:
            print('Файлы ' + args.etalon_file + ' и ' + args.export_file + ' совпадают.')
            sys.exit(0)
    else:
        sys.stderr.write(
            'Ошибка! Структура каталогов ' + args.etalon_file + ' и ' + args.export_file + ' отличается!\n')
        sys.stderr.write('Структура ' + args.etalon_file + '\n' + folder_map(dir01))
        sys.stderr.write('Структура ' + args.export_file + '\n' + folder_map(dir02))
        sys.exit(1)
