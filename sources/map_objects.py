# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#   map_objects.py                                      :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#   By: lbordana <lbordana@student.42mulhouse.fr>   +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#   Created: 2026/06/10 17:43:11 by lbordana           #+#    #+#             #
#   Updated: 2026/06/15 23:17:49 by lbordana          ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

from pydantic import BaseModel, Field, model_validator


class Drone(BaseModel):
    number: int = Field(gt=0)
    line:   int = Field(ge=0)


class Connection(BaseModel):
    first_zone:  str = Field(max_length=30)
    second_zone: str = Field(max_length=30)
    max_link:    int = Field(ge=0)
    line:        int = Field(ge=0)

    @model_validator(mode='after')
    def validate_zone(self):
        if "".join(self.first_zone.split('_')).isalnum() is False:
            raise ValueError(f"(line {self.line}) Zone {self.first_zone} must only contain alphanumeric or"
                             " underscore characters")
        if "".join(self.second_zone.split('_')).isalnum() is False:
            raise ValueError(f"(line {self.line}) Zone {self.second_zone} must only contain alphanumeric or"
                             " underscore characters")
        return self


class Hub(BaseModel):
    hub_type:    str
    name:        str = Field(max_length=30)
    coordinates: tuple[int, int]
    color:       str = Field(pattern=r"^([a-zA-Z]+)$")
    zone:        str
    max_drones:  int = Field(ge=0)
    line: int = Field(ge=0)

    @model_validator(mode='after')
    def validate_name(self):
        if "".join(self.name.split('_')).isalnum() is False:
            raise ValueError(f"(line {self.line}) Name {self.name} must only contain alphanumeric or"
                             " underscore characters")
        return self
