import argparse

parser = argparse.ArgumentParser(description='Скрипт делит исходный фаил.')
parser.add_argument('file_name', help='Имя файла')
parser.add_argument('count_strings', help='Колличество строк в выходных файлах.')
args = parser.parse_args()


def count_line(name, count_strings):
    with open(name) as my_file:
        count = sum(1 for _ in my_file)
        n = 0
        while n < count:
            with open(name) as my_file2:
                with open(n.__str__() + name[-4:], 'a') as res_file:
                    res_file.write('VER2\nREM Список элементов\n\n')
                    res_file.writelines(my_file2.readlines()[n:n + int(count_strings)])
            n = n + int(count_strings)


if __name__ == "__main__":
    count_line(args.file_name, args.count_strings)
