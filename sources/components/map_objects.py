# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#   map_objects.py                                      :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#   By: lbordana <lbordana@student.42mulhouse.fr>   +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#   Created: 2026/06/10 17:43:11 by lbordana           #+#    #+#             #
#   Updated: 2026/06/16 11:26:15 by lbordana          ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

from pydantic import BaseModel, Field


class Connection(BaseModel):
    first_zone:  str = Field(max_length=30, pattern=r"^([a-zA-Z0-9_]+)$")
    second_zone: str = Field(max_length=30, pattern=r"^([a-zA-Z0-9_]+)$")
    max_link:    int = Field(gt=0)
    line:        int = Field(ge=0)


class Hub(BaseModel):
    hub_type:    str
    name:        str = Field(max_length=30, pattern=r"^([a-zA-Z0-9_]+)$")
    coordinates: tuple[int, int]
    color:       str = Field(pattern=r"^([a-zA-Z]+)$")
    zone:        str = Field(pattern=r"(restricted|priority|normal|blocked)")
    max_drones:  int = Field(gt=0)
    line:        int = Field(ge=0)
    status:      str = Field(default="free")
    queue: list[str] = Field(default=[])
