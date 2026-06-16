# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#   parser.py                                           :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#   By: lbordana <lbordana@student.42mulhouse.fr>   +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#   Created: 2026/05/31 22:39:31 by lbordana           #+#    #+#             #
#   Updated: 2026/06/16 23:53:04 by lbordana          ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

from pydantic import BaseModel, model_validator, Field, ValidationError
from enum import Enum
from map_objects import Hub, Connection, Drone
from typing import Optional
import sys


class Error(Enum):
    E1000 = "Duplicated name. Please define an other one."
    E1001 = "No start_hub found. Please define it."
    E1002 = "There must be only one start_hub. Please remove others."
    E1003 = "Duplicated coordinates. Please define other ones."
    E1004 = "No end_hub found. Please define one."
    E1005 = "There must be only one end_hub. Please remove others."
    E1006 = "You cannot link between two same hub."
    E1007 = "Unknown first zone. Please ensure it is part of the hub name."
    E1008 = "Unknown second zone. Please ensure it is part of the hub name."
    E1009 = "These zones are already linked."
    E1010 = "No nb_drones found. Please define it."
    E1011 = "There must be only one nb_drones. Please remove others."
    E1012 = "Expected nb_drones at first line of the config file."
    E1013 = "Separators issue. Can be duplicated ones or at line beginning."
    E1014 = "Missing key, value or separator."
    E1015 = "Invalid key. Ensure it is part of the authorized keys."
    E1016 = "Too much values for nb_drones. It can only take number of drones."
    E1017 = "Not enough values, please check hub format."
    E1018 = "Not enough values, please check connection format."
    E1019 = "Invalid metadata. Can be separators or format."
    E1020 = "Too much values. Ensure metadata are in list : [<metadata>]."

    @classmethod
    def get_err(cls, code: str, line: Optional[int] = None):
        if line is None:
            return f"[ERROR] : {Error[code].value}"
        return f"[ERROR] - (line {line}) : {Error[code].value}"


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
            raise ValueError(Error.get_err('E1002', hub_line[1:]))
        return self

    @model_validator(mode='after')
    def check_end(self):
        hub_line = [h.line for h in self.hubs if h.hub_type == 'end_hub']
        if len(hub_line) == 0:
            raise ValueError(Error.get_err('E1004'))
        if len(hub_line) > 1:
            raise ValueError(Error.get_err('E1005', hub_line[1:]))
        return self

    @model_validator(mode='after')
    def check_double_link(self):

        hub_name = [h.name for h in self.hubs]

        for c in self.connections:

            if c.first_zone == c.second_zone:
                raise ValueError(Error.get_err('E1006', c.line))

            if c.first_zone not in hub_name:
                raise ValueError(Error.get_err('E1007', c.line))

            if c.second_zone not in hub_name:
                raise ValueError(Error.get_err('E1008', c.line))

        return self

    @model_validator(mode='after')
    def check_linked(self):
        zone_list = [(c.first_zone, c.second_zone) for c in self.connections]
        for index, co in enumerate(self.connections):
            if (co.first_zone, co.second_zone) in zone_list[:index]:
                raise ValueError(Error.get_err('E1009', co.line))
            if (co.second_zone, co.first_zone) in zone_list[:index]:
                raise ValueError(Error.get_err('E1009', co.line))
        return self

    @model_validator(mode='after')
    def check_drone_alone(self):

        drone_line = [d.line for d in self.drone]

        if len(self.drone) == 0:
            raise ValueError(Error.get_err('E1010'))

        if len(self.drone) > 1:
            raise ValueError(Error.get_err('E1011', drone_line[1:]))

        return self

    @model_validator(mode='after')
    def check_drone_first(self):
        lines = sorted([h.line for h in self.hubs]
                       + [c.line for c in self.connections]
                       + [self.drone[0].line])
        if self.drone[0].line != lines[0]:
            raise ValueError(Error.get_err('E1012', self.drone[0].line))
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
            raise ValueError(Error.get_err('E1013', self.line[0]))
        return self

    @model_validator(mode='after')
    def line_partition(self):
        accepted = ('hub', 'start_hub', 'end_hub', 'connection', 'nb_drones')

        self.key, sep, val = self.line[1].partition(': ')
        if not self.key or not sep or not val:
            raise ValueError(Error.get_err('E1014', self.line[0]))
        if self.key not in accepted:
            raise ValueError(Error.get_err('E1015', self.line[0]))

        if 'nb_drones' in self.key:
            self.values = val.strip().split()
            if len(self.values) > 1:
                raise ValueError(Error.get_err('E1016', self.line[0]))

        if 'hub' in self.key:
            self.values = val.strip().split(maxsplit=3)
            if len(self.values) < 3:
                raise ValueError(Error.get_err('E1017', self.line[0]))

        if 'connection' in self.key:
            self.values = val.strip().split(maxsplit=1)
            length = len(self.values)
            self.values[:1] = self.values[0].split('-', maxsplit=1)
            if len(self.values) < length + 1:
                raise ValueError(Error.get_err('E1018', self.line[0]))
        return self

    @model_validator(mode='after')
    def metadata_partition(self):
        values = self.values

        if 'hub' in self.key and len(values) == 4:
            pos = 3
            val_meta = ('color', 'zone', 'max_drones')
        elif 'connection' in self.key and len(values) == 3:
            pos = 2
            val_meta = ('max_link_capacity')
        else:
            return self
        if values[pos].startswith('[') and values[pos].endswith(']'):
            metadata = values[pos][1:-1].split()
            self.metadata = {}
            for m in metadata:
                key, sep, val = m.partition('=')
                if not key or not sep or not val:
                    raise ValueError(Error.get_err('E1019', self.line[0]))
                if key not in val_meta or key in self.metadata.keys():
                    raise ValueError(Error.get_err('E1019', self.line[0]))
                self.metadata.update({key: val})
        else:
            raise ValueError(Error.get_err('E1020', self.line[0]))
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
                    drone_list.append(Drone(number=parser.values[0],
                                            line=nb + 1))

        return GlobalParser(hubs=hub_list,
                            connections=connection_list,
                            drone=drone_list)
    except ValidationError as err:
        for e in err.errors():
            print(ANSII_RED)
            if e.get('type') != 'value_error':
                print(f"[ERROR] - (line {nb + 1}) : {e.get('msg')}")
            else:
                print(e.get('msg').split(', ', maxsplit=1)[1])
        print('Please ensure format is "<key>: <value> ... <[metadata]>."')
        print(ANSII_NORMAL)
        sys.exit(0)


# Constants
ANSII_RED = "\033[1;31m"
ANSII_NORMAL = "\033[0m"
