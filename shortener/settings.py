# -*- coding: utf-8 -*-

import logging
import pathlib

import yaml


def load_config(filename):
    with open(filename) as f:
        data = yaml.load(f)

    return data


BASE_DIR = pathlib.Path(__file__).parent.parent

config = load_config(BASE_DIR / 'config' / 'config.yml')

logging.basicConfig(
    level=logging.getLevelName(config['logging']['level'].upper()),
    format=config['logging']['format'])
