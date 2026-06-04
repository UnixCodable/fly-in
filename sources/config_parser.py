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

from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    model_validator,
    field_validator,
    validate_call_decorator
    )
from typing import List
import sys


class ConfigParser(BaseModel, validate_assignment=True):
    keys: list[str]
    hub_name: list[str]
    hub_coordinates: list[tuple[int, int]]
    hub_metadata: list[str | None]
    nb_drones: int = Field(gt=0)

    @field_validator('hub_name', mode='after')
    @classmethod
    def validate_hub_name(cls, v):
        if len(set(v)) != len(v):
            raise ValueError('Hub names cannot be duplicated')
        return v

    @field_validator('keys', mode='after')
    @classmethod
    def validate_keys(cls, v):

        start_list = [key for key in v if key == "start_hub"]
        end_list = [key for key in v if key == "end_hub"]

        for key in v:
            if key not in ('connection', 'hub', 'start_hub', 'end_hub', 'nb_drones'):
                raise ValueError('Key can only contain "hub", "start_hub",'
                                 '"end_hub", "connection", "nb_drones"')

        if v[0] != 'nb_drones':
            raise ValueError('No nb_drones at first line of config.')

        if 'nb_drones' in [k for k in v[1:]]:
            raise ValueError('There must be only one nb_drones value.')

        if len(start_list) != 1:
            raise ValueError('There must be only one starting hub.')

        if len(end_list) != 1:
            raise ValueError('There must be only one ending hub.')

        return v


def parse_map() -> ConfigParser:
    parsed = ConfigParser.model_construct()
    dot = []
    space = []
    lines: dict[str, List] = {
        'keys': [],
        'hub_name': [],
        'hub_coordinates': [],
        'hub_metadata': [],
        'connections': []
    }
    with open("assets/maps/hard/03_ultimate_challenge.txt") as file:
        for line in file.readlines():
            try:
                line = line[0:line.index("#")]
            except ValueError:
                pass
            if line == '\n' or line == '':
                continue
            dot = line.split(':', maxsplit=1)
            if dot[0] in ('hub', 'start_hub', 'end_hub'):
                space = dot[1].strip().split(maxsplit=3)
                lines['hub_name'].append(space[0] if len(space) >= 3 else None)
                lines['hub_coordinates'].append((space[1], space[2]) if len(space) >= 3 else None)
                lines['hub_metadata'].append(space[3] if len(space) >= 4 else None)
            elif dot[0] == 'connection':
                space = dot[1].strip().split(maxsplit=1)
            else:
                space = [dot[1].strip()]
            lines['keys'].append(dot[0].strip())
    try:
        parsed.keys = lines.get('keys', [])
        parsed.hub_name = lines.get('hub_name', [])
        parsed.hub_coordinates = lines.get('hub_coordinates', [])
        parsed.hub_metadata = lines.get('hub_metadata', [])
    except ValidationError as err:
        for e in err.errors():
            print(e.get('msg'))
        sys.exit(0)
    print(parsed.hub_metadata)
    return parsed
