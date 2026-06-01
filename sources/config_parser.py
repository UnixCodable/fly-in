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

from pydantic import BaseModel, model_validator, Field, ValidationError


class ConfigParser(BaseModel):
    start_hub: str = Field()
    hub: list[str] = Field()
    end_hub: str = Field()


def setup_config():
    config = dict()
    lines = []
    with open("maps/hard/03_ultimate_challenge.txt") as file:
        for line in file.readlines():
            try:
                line = line[0:line.index("#")]
            except ValueError:
                pass
            if line == '\n' or line == '':
                continue
            line = line.strip().split(':')
            lines.append(line)
    print(lines)
    print(config)


try:
    object = setup_config()
except ValidationError as err:
    print(err)
