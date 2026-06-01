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
    def start_parsing(self):
        hub_list = [line for line in self.lines if line[0] == "start_hub"]
        if len(hub_list) != 1:
            raise ValueError('There must be only one starting hub.')


def read_map() -> List:
    lines = []
    temp = []
    with open("maps/hard/03_ultimate_challenge.txt") as file:
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
            print(temp)
            lines.append(temp)
        return lines


try:
    object = LineParser(lines=read_map())
except ValidationError as err:
    print(err)
