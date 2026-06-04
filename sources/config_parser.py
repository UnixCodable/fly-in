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
    validate_call_decorator,
    mypy
    )
from typing import List, Any
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
    keys_values = []
    with open("assets/maps/hard/03_ultimate_challenge.txt") as file:
        for line in file.readlines():
            line = line[0:line.index("#") if '#' in line else -1]
            if line == '\n' or line == '':
                continue
            line = line.replace(':', ' ')
            keys_values.append(line.split())
        print(keys_values)
    try:
        parsed.keys = [k[0] for k in keys_values]
        parsed.nb_drones = keys_values[0][1]
        parsed.hub_name = [k[1] for k in keys_values if 'hub' in k[0]]
        parsed.hub_coordinates = [(int(k[2]), int(k[3])) for k in keys_values if 'hub' in k[0]]
    except ValidationError as err:
        for e in err.errors():
            print(e.get('msg'))
        sys.exit(0)
    print(parsed.keys)
    print(parsed.nb_drones)
    print(parsed.hub_name)
    return parsed
