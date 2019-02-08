# -*- coding: utf-8 -*-

import string

import yaml


alphabet = ''.join((string.ascii_lowercase,
                    string.ascii_uppercase,
                    string.digits))


def load_config(filename):
    with open(filename) as f:
        data = yaml.load(f)

    return data


def encode(num):
    if num == 0:
        return alphabet[0]

    result = ''
    while num > 0:
        num, rem = divmod(num, len(alphabet))
        result = alphabet[rem] + result

    return result


def decode(short_id):
    num = 0
    for i, ch in enumerate(short_id):
        index = alphabet.index(ch)
        num += index * len(alphabet) ** (len(short_id) - i - 1)
    return num
