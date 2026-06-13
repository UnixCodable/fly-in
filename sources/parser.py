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


class Parsing(BaseModel):
    line:      tuple[int, str] = Field()
    key:                 str = Field(default='')
    values:        list[str] = Field(default=[])
    metadata: dict[str, str] = Field(default={})

    @model_validator(mode='after')
    def line_check_separator(self):
        string = self.line[1]

        if ' ' in string[0] or '  ' in string or '::' in string:
            raise ValueError(f"(line {self.line[0]}) : Separators issue.")
        return self

    @model_validator(mode='after')
    def line_partition(self):
        l_num = self.line[0]

        self.key, sep, val = self.line[1].partition(': ')
        if not self.key or not sep or not val:
            raise ValueError(f"(line {l_num}) : Missing key, value or separator")
        if self.key not in ('hub', 'start_hub', 'end_hub', 'connection', 'nb_drones'):
            raise ValueError(f"(line {l_num}) : Invalid key")

        if 'nb_drones' in self.key:
            self.values = val.split()
            if len(self.values) > 1:
                raise ValueError(f"(line {l_num}) : Too much values")
        if 'hub' in self.key:
            self.values = val.split(maxsplit=3)
            if len(self.values) < 3:
                raise ValueError(f"(line {l_num}) : Not enough values")
        if 'connection' in self.key:
            self.values = val.split(maxsplit=2)

        return self

    @model_validator(mode='after')
    def metadata_partition(self):
        values = self.values
        l_num = self.line[0]

        if 'hub' in self.key and len(values) == 4:
            if values[3].startswith('[') and values[3].endswith(']'):
                metadata = values[3][1:-1].split()
                self.metadata = {}
                for m in metadata:
                    key, sep, val = m.partition('=')
                    if not key or not sep or not val:
                        raise ValueError(f'(line {l_num}) Invalid metadata.')
                    if key not in ('color', 'zone', 'max_drones') or key in self.metadata.keys():
                        raise ValueError(f'(line {l_num}) Invalid metadata.')
                    self.metadata.update({key: val})
            else:
                raise ValueError(f'(line {l_num}) Too much values. Ensure metadata are in list.')
        if 'connection' in self.key and len(values) == 2:
            if values[1].startswith('[') and values[1].endswith(']'):
                metadata = values[1][1:-1].split()
                self.metadata = {}
                for m in metadata:
                    key, sep, val = m.partition('=')
                    if not key or not sep or not val:
                        raise ValueError(f'(line {l_num}) Invalid metadata.')
                    if key not in ('max_link_capacity') or key in self.metadata.keys():
                        raise ValueError(f'(line {l_num}) Invalid metadata.')
                    self.metadata.update({key: val})
            else:
                raise ValueError(f'(line {l_num}) Too much values. Ensure metadata are in list.')
        return self


def read_map():
    hub: list[Hub] = []
    connection: list[Connection] = []
    with open("assets/maps/hard/03_ultimate_challenge.txt") as file:
        for nb, line in enumerate(file.readlines()):

            line = line[0:line.index("#") if '#' in line else -1]
            if line == '\n' or line == '':
                continue

            parser = Parsing(line=(nb + 1, line))
            if 'hub' in parser.key:
                hub.append(Hub(
                    name=parser.values[0],
                    coordinates=(parser.values[1], parser.values[2]),
                    line=nb + 1,
                    color=parser.metadata.get('color', 'black'),
                    zone=parser.metadata.get('zone', 'normal'),
                    max_drones=parser.metadata.get('max_drones', 1),
                    ))
        print(hub)
    return


def parse_map():
    try:
        read_map()
    except ValidationError as err:
        for e in err.errors():
            print(e.get('msg'))
        print('Please ensure format is "<key>: <value> ... <[metadata]>."\033[0m')
        sys.exit(0)
    return
