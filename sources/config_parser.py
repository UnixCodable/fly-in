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
    field_validator,
    )
from typing import List, Any
import sys


class ConfigParser(BaseModel):
    keys: list[str]
    hub_name: list[str]
    hub_coordinates: list[tuple[int, int]]
    hub_metadata: Any
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
        accredited = {'connection', 'hub', 'start_hub', 'end_hub', 'nb_drones'}

        for key in v:
            if key not in accredited:
                raise ValueError('Key can only contain "hub", "start_hub",'
                                 '"end_hub", "connection", "nb_drones".')
        if v[0] != 'nb_drones':
            raise ValueError('No nb_drones at first line of config.')
        if 'nb_drones' in [k for k in v[1:]]:
            raise ValueError('There must be only one nb_drones value.')
        if len(start_list) != 1:
            raise ValueError('There must be only one starting hub.')
        if len(end_list) != 1:
            raise ValueError('There must be only one ending hub.')

        return v


def read_map() -> list:
    with open("assets/maps/hard/03_ultimate_challenge.txt") as file:
        for nb, line in enumerate(file.readlines()):
            line = line[0:line.index("#") if '#' in line else -1]

            if line == '\n' or line == '':
                continue
            if ' ' in line[0] or '  ' in line or '::' in line:
                raise ValueError(f'Error: separators on line {nb + 1}')

            values = line.split(':', maxsplit=1)[:1] + line.split()[1:]
            
    return values


def parse_map() -> ConfigParser:
    try:
        values = read_map()
        parsed = ConfigParser(
            keys=[k[0] for k in values],
            nb_drones=values[0][1],
            hub_name=[v[1] for v in values if 'hub' in v[0]],
            hub_coordinates=[(v[2], v[3]) for v in values if 'hub' in v[0]],
            hub_metadata=[v[4] for v in values if 'hub' in v[0]]
        )
    except ValidationError as err:
        for e in err.errors():
            print(e.get('msg'))
        print('Please ensure format is "<key>: <value> ... <[metadata]>."')
        sys.exit(0)
    except ValueError as err:
        print(err)
        print('Please ensure format is "<key>: <value> ... <[metadata]>."')
        sys.exit(0)
    return parsed


        #     if ' ' in line[0]:
        #         raise ValueError(f'One or multiple space on line {nb + 1}')
        #     line = line[0:line.index("#") if '#' in line else -1]
        #     if '[' in line:
        #         if ']' not in line[line.index('['):]:
        #             raise ValueError(f'Metadata must be a list: line {nb + 1}')
        #         line = line[0:line.index('[')] + line[line.index('['):line.index(']')].replace(' ', ',') + line[line.index(']'):]
        #     if line == '\n' or line == '':
        #         continue
        #     temp = line.split(':')[:1] + line.split()[1:]

        #     if 'hub' in temp[0]:
        #         if len(temp) > 5:
        #             raise ValueError(f'Too much values on line {nb + 1}')
        #         values.append(
        #             [temp[0],
        #              temp[1] if len(temp) > 1 else None,
        #              temp[2] if len(temp) > 2 else None,
        #              temp[3] if len(temp) > 3 else None,
        #              metadata if len(temp) > 4 else None]
        #              )

        #     elif 'connection' in temp[0]:
        #         if len(temp) > 3:
        #             raise ValueError(f'Too much values on line {nb + 1}')
        #         values.append(
        #             [temp[0],
        #              temp[1] if len(temp) > 1 else None,
        #              metadata if len(temp) > 2 else None]
        #              )
        #     elif 'nb_drone' in temp[0]:
        #         if len(temp) > 2:
        #             raise ValueError(f'Too much values on line {nb + 1}')
        #         values.append(
        #             [temp[0],
        #              temp[1] if len(temp) > 1 else None]
        #              )
        # print(values)