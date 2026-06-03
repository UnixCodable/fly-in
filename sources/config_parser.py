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


class ConfigParser(BaseModel, validate_assignment=True):
    keys: list[str]
    hub_name: list[str]

    @field_validator('hub_name', mode='after')
    @classmethod
    def validate_hub_name(cls, v):
        if len(set(v)) != len(v):
            raise ValueError('Hub names cannot be duplicated')
        return v

    @field_validator('keys', mode='after')
    @classmethod
    def validate_keys(cls, v):
        start_list = [k for k in v if k == "start_hub"]
        end_list = [k for k in v if k == "end_hub"]
        for k in v:
            if k not in ('connection', 'hub', 'start_hub', 'end_hub', 'nb_drones'):
                raise ValueError('Key can only contain "hub", "start_hub", "end_hub", "connection", "nb_drones"')
        if v[0] != 'nb_drones':
            raise ValueError('No nb_drones at first line of config.')
        if 'nb_drones' in [k for k in v[1:]]:
            raise ValueError('There must be only one nb_drones value.')
        if len(start_list) != 1:
            raise ValueError('There must be only one starting hub.')
        if len(end_list) != 1:
            raise ValueError('There must be only one ending hub.')
        return v


def parse_map() -> List:
    parsed = ConfigParser.model_construct()
    temp = []
    lines = {
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
            lines['keys'].append(line.split(':')[0].strip())
        parsed.keys = lines.get('keys', [])
    return parsed
