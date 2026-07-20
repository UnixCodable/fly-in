# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#   map_objects.py                                      :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#   By: lbordana <lbordana@student.42mulhouse.fr>   +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#   Created: 2026/06/10 17:43:11 by lbordana           #+#    #+#             #
#   Updated: 2026/07/07 02:36:59 by lbordana          ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

from pydantic import BaseModel, Field
from typing import Optional


class Connection(BaseModel):
    first_zone:  str = Field(max_length=60, pattern=r"^([a-zA-Z0-9_]+)$")
    second_zone: str = Field(max_length=60, pattern=r"^([a-zA-Z0-9_]+)$")
    max_link:    int = Field(gt=0)
    line:        int = Field(ge=0)
    passages:    int = Field(default=0)
    waiting: list[str] = Field(default=[])
    restricted: bool = Field(default=False)

    def reset_passages(self):
        self.passages = 0

    def set_passages(self, value):
        self.passages += value

    def get_passages(self):
        return self.passages

    def is_restricted(self):
        return self.restricted

    def set_restriction(self, boolean: bool):
        self.restricted = boolean

    def is_full(self) -> bool:
        if self.passages == self.max_link:
            return True
        return False


class Hub(BaseModel, arbitrary_types_allowed=True):
    hub_type:    str
    name:        str = Field(max_length=60, pattern=r"^([a-zA-Z0-9_]+)$")
    coordinates: tuple[int, int]
    color:       str = Field(pattern=r"^([a-zA-Z]+)$")
    zone:        str = Field(pattern=r"(restricted|priority|normal|blocked)")
    max_drones:  int = Field(gt=0)
    line:        int = Field(ge=0)
    occupants:   int = Field(default=0)
    locked:     bool = Field(default=False)
    waiting: list[str] = Field(default=[])
    score:       int = Field(default=0)
    distance:   int = Field(default=0)
    remaining:   int = Field(default=0)

    def add_occupant(self):
        self.occupants += 1

    def remove_occupant(self):
        self.occupants -= 1

    def is_full(self) -> bool:
        if self.occupants == self.max_drones:
            return True
        return False


class Drone():
    def __init__(self, id: str, current_pos: Hub) -> None:
        self.id = id
        self._current_pos: Hub = current_pos
        self._last_pos: Hub = current_pos
        self._restricted: bool = False
        self._running = True

    def set_current_pos(self, current_pos: Hub) -> None:
        self._current_pos = current_pos

    def get_current_pos(self) -> Hub:
        return self._current_pos

    def set_last_pos(self, last_pos: Hub) -> None:
        self._last_pos = last_pos

    def get_last_pos(self) -> Hub:
        return self._last_pos

    def set_restriction(self, boolean: bool) -> None:
        self._restricted = boolean

    def is_restricted(self) -> bool:
        return self._restricted

    def is_running(self) -> bool:
        return self._running

    def shutdown(self):
        self._running = False
