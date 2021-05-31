import argparse
import filecmp
import os
import sys


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
            if not filecmp.cmp(f_src, f_dst):
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
    parser = argparse.ArgumentParser(description='Скрипт для сравнения двух zip файлов.')
    parser.add_argument('etalon_folder', help='папка c эталоном')
    parser.add_argument('actual_folder', help='папка для сравнения')
    args = parser.parse_args()

    if folder_map(args.etalon_folder) == folder_map(args.actual_folder):
        if file_compare(args.etalon_folder, args.actual_folder) > 0:
            sys.exit(1)
        else:
            print('Каталоги ' + args.etalon_folder + ' и ' + args.actual_folder + ' совпадают.')
            sys.exit(0)
    else:
        sys.stderr.write(
            'Ошибка! Структура каталогов ' + args.etalon_folder + ' и ' + args.actual_folder + ' отличается!\n')
        sys.stderr.write('Структура ' + args.etalon_file + '\n' + folder_map(args.etalon_folder))
        sys.stderr.write('Структура ' + args.export_file + '\n' + folder_map(args.actual_folder))
        sys.exit(1)
