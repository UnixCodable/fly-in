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
    model_validator
    )
from typing import List


class LineParser(BaseModel, validate_assignment=True):
    lines: List[List[str]] = Field()

    @model_validator(mode='after')
    def invalid_values(self):
        

    @model_validator(mode='after')
    def number_of_drones(self):
        if self.lines[0][0] == 'nb_drones':
            if 'nb_drones' not in [li[0] for li in self.lines[1:]]:
                return self
        raise ValueError('There must be only one nb_drones value and it must be at the first line of the config file.')

    @model_validator(mode='after')
    def start_parsing(self):
        hub_list = [li for li in self.lines if li[0] == "start_hub"]
        if len(hub_list) != 1:
            raise ValueError('There must be only one starting hub.')
        return self

    @model_validator(mode='after')
    def end_parsing(self):
        hub_list = [li for li in self.lines if li[0] == "end_hub"]
        if len(hub_list) != 1:
            raise ValueError('There must be only one starting hub.')
        return self


def read_map() -> List:
    lines = []
    temp = []
    with open("assets/maps/hard/03_ultimate_challenge.txt") as file:
        for line in file.readlines():
            try:
                line = line[0:line.index("#")]
            except ValueError:
                pass
            if line == '\n' or line == '':
                continue
            temp = line.split(':')
            temp[0] = temp[0].strip()
            temp[1] = temp[1].strip()
            lines.append(temp)
        return lines
