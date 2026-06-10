# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  map_objects.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/10 17:43:11 by lbordana        #+#    #+#               #
#  Updated: 2026/06/10 17:43:56 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pydantic import BaseModel, Field, model_validator


class Drone(BaseModel):
    number:      int = Field(gt=0)
    config_line: int = Field(ge=0)


class Connection(BaseModel):
    first_zone:        str = Field(max_length=30)
    second_zone:       str = Field(max_length=30)
    max_link_capacity: int = Field(default=1, gt=0)
    line:              int = Field(ge=0)


class Hub(BaseModel):
    name:        str = Field(max_length=30)
    coordinates: tuple[int, int]
    color:       str = Field(default='black')
    zone:        str = Field(default='normal')
    max_drones:  int = Field(default=1, gt=0)
    line: int = Field(ge=0)

    @model_validator(mode='after')
    def validate_name(self):
        if "".join(self.name.split('_')).isalnum() is False:
            raise ValueError(f"(line {self.line}) Name {self.name} must only contain alphanumeric or"
                             " underscore characters")
        return self