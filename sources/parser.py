# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#   parser.py                                           :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#   By: lbordana <lbordana@student.42mulhouse.fr>   +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#   Created: 2026/05/31 22:39:31 by lbordana           #+#    #+#             #
#   Updated: 2026/06/15 19:19:23 by lbordana          ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

from pydantic import BaseModel, model_validator, Field, ValidationError
from enum import Enum
from map_objects import Hub, Connection, Drone
from typing import Optional
import sys


class Error(Enum):
    E1000 = "Duplicated name"
    E1001 = "No start_hub found. Please define one."
    E1002 = "Too many start_hub."
    E1003 = "Duplicated coordinates"

    @classmethod
    def get_err(cls, code: str, line: Optional[int] = None):
        if line is None:
            return Error[code].value
        return f"(line {line}), {Error[code].value}"


class GlobalParser(BaseModel):
    hubs: list[Hub]
    connections: list[Connection]
    drone: list[Drone]

    @model_validator(mode='after')
    def check_double_name(self):
        hub_line = [h.line for h in self.hubs]
        hub_name = [h.name for h in self.hubs]
        for index, h in enumerate(hub_name):
            if h in hub_name[:index]:
                raise ValueError(Error.get_err('E1000', hub_line[index]))
        return self

    @model_validator(mode='after')
    def check_double_coord(self):
        hub_line = [h.line for h in self.hubs]
        hub_coord = [h.coordinates for h in self.hubs]
        for index, h in enumerate(hub_coord):
            if h in hub_coord[:index]:
                raise ValueError(Error.get_err('E1003', hub_line[index]))
        return self

    @model_validator(mode='after')
    def check_start(self):
        hub_line = [h.line for h in self.hubs if h.hub_type == 'start_hub']
        if len(hub_line) == 0:
            raise ValueError(Error.get_err('E1001'))
        if len(hub_line) > 1:
            raise ValueError(Error['E1002'].value)
        return self

    @model_validator(mode='after')
    def check_end(self):
        hub_line = [h.line for h in self.hubs if h.hub_type == 'end_hub']
        if len(hub_line) == 0:
            raise ValueError("No end_hub found. Please define one.")
        if len(hub_line) > 1:
            raise ValueError(f"(line {hub_line[1:]}) Too many end_hub.")
        return self

    @model_validator(mode='after')
    def check_double_link(self):

        hub_name = [h.name for h in self.hubs]

        for c in self.connections:

            if c.first_zone == c.second_zone:
                raise ValueError(f'(line {c.line}) : Link between same hub')

            if c.first_zone not in hub_name:
                raise ValueError(f'(line {c.line}) : Unknown first zone')

            if c.second_zone not in hub_name:
                raise ValueError(f'(line {c.line}) : Unknown second zone')

        return self

    @model_validator(mode='after')
    def check_drone_alone(self):

        drone_line = [d.line for d in self.drone]

        if len(self.drone) == 0:
            raise ValueError('No nb_drones found. Please define it.')

        if len(self.drone) > 1:
            raise ValueError(f"(line {drone_line[1:]}) : Too many nb_drones.")

        return self

    @model_validator(mode='after')
    def check_drone_first(self):
        lines = sorted([h.line for h in self.hubs]
                       + [c.line for c in self.connections]
                       + [self.drone[0].line])
        if self.drone[0].line != lines[0]:
            raise ValueError(f'(line {self.drone[0].line}) : nb_drones must be at first line of the file')
        return self


class LineParser(BaseModel):
    line:    tuple[int, str] = Field()
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
        l_num = f'(line {self.line[0]}) : '

        self.key, sep, val = self.line[1].partition(': ')
        if not self.key or not sep or not val:
            raise ValueError(l_num + "Missing key, value or separator.")
        if self.key not in ('hub', 'start_hub', 'end_hub', 'connection', 'nb_drones'):
            raise ValueError(l_num + "Invalid key")

        if 'nb_drones' in self.key:
            self.values = val.strip().split()
            if len(self.values) > 1:
                raise ValueError(l_num + "Too much values for nb_drones.")

        if 'hub' in self.key:
            self.values = val.strip().split(maxsplit=3)
            if len(self.values) < 3:
                raise ValueError(l_num + "Not enough values")

        if 'connection' in self.key:
            self.values = val.strip().split(maxsplit=1)
            self.values[:1] = self.values[0].split('-', maxsplit=1)
            if len(self.values) < 2:
                raise ValueError(l_num + "Not enough values, check connection format.")

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
        if 'connection' in self.key and len(values) == 3:
            if values[2].startswith('[') and values[2].endswith(']'):
                metadata = values[2][1:-1].split()
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


def read_map() -> GlobalParser:
    hub_list: list[Hub] = []
    connection_list: list[Connection] = []
    drone_list: list[Drone] = []
    try:
        with open("assets/maps/hard/03_ultimate_challenge.txt") as file:
            for nb, line in enumerate(file.readlines()):

                line = line[0:line.index("#") if '#' in line else -1]
                if line == '\n' or line == '':
                    continue

                parser = LineParser(line=(nb + 1, line))
                if 'hub' in parser.key:
                    hub_list.append(Hub(
                        hub_type=parser.key,
                        name=parser.values[0],
                        coordinates=(parser.values[1], parser.values[2]),
                        line=nb + 1,
                        color=parser.metadata.get('color', 'black'),
                        zone=parser.metadata.get('zone', 'normal'),
                        max_drones=parser.metadata.get('max_drones', 1),
                        ))
                if 'connection' in parser.key:
                    connection_list.append(Connection(
                        first_zone=parser.values[0],
                        second_zone=parser.values[1],
                        max_link=parser.metadata.get('max_link_capacity', 1),
                        line=nb + 1
                    ))
                if 'nb_drone' in parser.key:
                    drone_list.append(Drone(number=parser.values[0], line=nb + 1))

        return GlobalParser(hubs=hub_list,
                            connections=connection_list,
                            drone=drone_list)
    except ValidationError as err:
        for e in err.errors():
            if e.get('type') != 'value_error':
                print(f"(line {nb + 1}), {e.get('msg')}")
            else:
                print(e.get('msg').split(', ', maxsplit=1)[1])
        print('Please ensure format is "<key>: <value> ... <[metadata]>."\033[0m')
        sys.exit(0)
