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


class Connection(BaseModel):
    first_zone:  str = Field(max_length=30, pattern=r"^([a-zA-Z0-9_]+)$")
    second_zone: str = Field(max_length=30, pattern=r"^([a-zA-Z0-9_]+)$")
    max_link:    int = Field(gt=0)
    line:        int = Field(ge=0)
    passages:    int = Field(default=0)

    def reset_passages(self):
        self.passages = 0

    def set_passages(self):
        self.passages += 1

    def get_passages(self):
        return self.passages


class Hub(BaseModel, arbitrary_types_allowed=True):
    hub_type:    str
    name:        str = Field(max_length=30, pattern=r"^([a-zA-Z0-9_]+)$")
    coordinates: tuple[int, int]
    color:       str = Field(pattern=r"^([a-zA-Z]+)$")
    zone:        str = Field(pattern=r"(restricted|priority|normal|blocked)")
    max_drones:  int = Field(gt=0)
    line:        int = Field(ge=0)
    g_pos:       int = Field(default=0)
    h_pos:       int = Field(default=0)
    f_pos:       int = Field(default=0)
    parent:      str = Field(default="")


class Drone():
    def __init__(self, id: str, current_pos: Hub, path: list[Hub]) -> None:
        self.id = id
        self._last_pos = current_pos
        self._current_pos = current_pos
        self._path: list[Hub] = path

    def set_current_pos(self, current_pos: Hub) -> None:
        self._current_pos = current_pos

    def get_current_pos(self) -> Hub:
        return self._current_pos

    def set_last_pos(self, current_pos: Hub) -> None:
        self._last_pos = current_pos
    
    def get_last_pos(self) -> Hub:
        return self._last_pos

    def set_path(self, path: list[Hub]) -> None:
        self._path = path

    def get_path(self) -> list[Hub]:
        return self._path
