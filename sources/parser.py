# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#   config_parser.py                                    :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#   By: lbordana <lbordana@student.42mulhouse.fr>   +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#   Created: 2026/05/31 22:39:31 by lbordana           #+#    #+#             #
#   Updated: 2026/05/31 23:21:40 by lbordana          ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

from pydantic import BaseModel, model_validator, Field, ValidationError, field_validator
from map_objects import Hub, Connection, Drone
from typing import List, Any, Optional
from enum import Enum
import sys


class KeyParam(Enum):
    HUB = 'hub'
    START_HUB = 'start_hub'
    END_HUB = 'end_hub'
    CONNECTION = 'connection'
    NB_DRONE = 'nb_drone'


class MetadataParam(Enum):
    pass


class Parsing(BaseModel, validate_assignment=True):
    line:   tuple[int, str] = Field(default=(0, ''))
    keys:         list[str] = Field(default=[])
    values: list[list[str]] = Field(default=[])

    @model_validator(mode='after')
    def line_check_separator(self):
        if ' ' in self.line[1][0] or '  ' in self.line[1] or '::' in self.line[1]:
            raise ValueError(f"(line {self.line[0]}) : Separators issue")
        return self

    @model_validator(mode='after')
    def line_partition(self):

        key, sep, val = self.line[1].partition(': ')
        if not key or not sep or not val:
            raise ValueError(f"(line {self.line[0]}) : Missing key, value or separator")

        self.keys.append(key)
        if 'nb_drones' in key:
            self.values.append(val.split())
        if 'hub' in key:
            self.values.append(val.split(maxsplit=3))
        if 'connection' in key:
            self.values.append(val.split(maxsplit=2))

        return self

    @model_validator(mode='after')
    def keys_checker(self):
        if self.keys[-1] not in ('hub',
                                 'start_hub',
                                 'end_hub',
                                 'connection',
                                 'nb_drones'):
            raise ValueError(f"(line {self.line[0]}) : Invalid key")
        return self


def read_map():
    parser = Parsing.model_construct()
    hub: list[Hub] = []
    with open("assets/maps/hard/03_ultimate_challenge.txt") as file:
        for nb, line in enumerate(file.readlines()):

            line = line[0:line.index("#") if '#' in line else -1]
            if line == '\n' or line == '':
                continue

            parser.line = (nb + 1, line)
            if 'hub' in parser.keys[-1]:
                hub.append(Hub(
                    name=parser.values[-1][0],
                    coordinates=(parser.values[-1][1], parser.values[-1][2]),
                    line=nb + 1,
                    ))
        print(parser)
    return


def parse_map():
    try:
        read_map()
    except ValidationError as err:
        for e in err.errors():
            print('\033[1;31mERROR - ' + e.get('msg').split(', ', 1)[1])
        print('Please ensure format is "<key>: <value> ... <[metadata]>."\033[0m')
        sys.exit(0)
    return
