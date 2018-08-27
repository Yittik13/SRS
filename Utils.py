# coding=utf-8
import random
# import pinyin
from subprocess import call
from datetime import date
# from Sentences import sentences_chinese
from Sentences import sentences


def combine(dictionaries):
    """
    Combine a list of dictionaries into one
    :param dictionaries: List of dictionaries to combine
    :return: Combined dictionary
    """
    res = {}
    for d in dictionaries:
        res.update(d)

    return res


def reverse(dictionary):
    """
    Reverse the keys and values in a dictionary
    :param dictionary: Dictionary to reverse
    :return: The reversed dictionary
    """
    return {v: k for k, v in dictionary.iteritems()}


def compare_file_length(f1, f2):
    f1 = open(f1, 'r')
    f2 = open(f2, 'r')
    return sum(1 for line in f1) == sum(1 for line in f2)


def days_apart(date1, date2):
    """
    Determine how many days there are between date1 and date2
    :param date1: Date object
    :param date2: Date object
    :return: Number of days
    """
    delta = date2 - date1
    return delta.days


def extract_date(date_str):
    """
    Extract date from string
    :param date_str: Date in string form: 'YYYY-MM-DD'
    :return: Date object of provided date
    """
    split = date_str.split('-')
    year = int(split[0])
    month = int(split[1])
    day = int(split[2])
    return date(year, month, day)


def find_example_sentence(word):
    # for k in sentences_chinese.keys():
    res = []
    count = 0
    max_sentences = 5
    for k in sentences.keys():
        if word[0] in k and count < max_sentences:
            spl = k.split('/')
            nk = spl[1] + '\n' + spl[0]
            res.append(nk + '\n' + sentences[k])
            count += 1
            # return res

    f = open('Cards/2000Phrases.txt', 'r')
    f.readline()  # Skip header
    line = f.readline()

    while line and count < max_sentences:
        split = line.split('\t')
        if word[0] in split[0]:
            res.append(split[0] + '\n' + split[1] + '\n' + split[2].strip('\n'))
            count += 1
        line = f.readline()
    f.close()

    f = open('/home/joel/PycharmProjects/Chinese/Cards/hsk3_sentences.txt', 'r')
    line = f.readline()

    while line and count < max_sentences:
        split = line.split('\t')
        if word[0] in split[0]:
            res.append(split[0] + '\n' + split[1] + '\n' + split[2].strip('\n'))
            count += 1
        line = f.readline()
    f.close()

    return res


def shuffle_file(fname):
    f = open(fname, 'r')
    lines = f.readlines()
    f.close()

    random.shuffle(lines)

    f = open('shuffle.txt', 'w')
    f.writelines(lines)
    f.close()
    if compare_file_length(fname, 'shuffle.txt'):
        print('files same length')
        call(['rm', fname])
        call(['mv', 'shuffle.txt', fname])


#def chinese_to_pinyin(char):
#    return pinyin.get(char)


if __name__ == '__main__':
    shuffle_file('srs_char.csv')
