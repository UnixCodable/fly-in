# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#   a_star.py                                           :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#   By: lbordana <lbordana@student.42mulhouse.fr>   +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#   Created: 2026/07/07 00:54:06 by lbordana           #+#    #+#             #
#   Updated: 2026/07/08 11:17:18 by lbordana          ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

from typing import Optional, Union
from sources.components.map_objects import Connection, Hub
from sources.parser import GlobalParser


class Algorithm():
    def __init__(self, map: GlobalParser):
        self.map: GlobalParser = map
        self.start_hub: Hub = self.map.get_start_hub()
        self.end_hub: Hub = self.map.get_end_hub()
        self.paths: list[list[Hub]] = []

    def _h_path(self, connection: Connection, next_hub: Hub):
        weight = 0
        pos = int(next_hub.g_pos / 10)
        overflow = len([p for p in self.paths if len(p) >= pos and p[pos - 1] == next_hub])
        if overflow > next_hub.max_drones:
            if next_hub.zone == "restricted":
                weight += (overflow - next_hub.max_drones) * 2
            else:
                weight += overflow - next_hub.max_drones
        elif next_hub.zone == "restricted":
            weight += 1
        if next_hub.zone == "priority":
            weight -= 1
        overflow = connection.get_passages()
        if overflow > connection.max_link:
            weight += overflow - connection.max_link
        h_diff = (self.end_hub.coordinates[0] - next_hub.coordinates[0],
                  self.end_hub.coordinates[1] - next_hub.coordinates[1])
        next_hub.h_pos = (h_diff[0] * 10) + (h_diff[1] * 10) + (weight * 10)

    def _g_path(self, current_hub: Hub, next_hub: Hub):
        g_pos = int((current_hub.g_pos / 10) + 1)
        next_hub.g_pos = int((g_pos) * 10)

    def _f_path(self, next_hub: Hub):
        next_hub.f_pos = next_hub.h_pos + next_hub.g_pos

    def _find_adjacent(self, current_hub: Hub) -> list[Hub]:
        available = []
        for connection in self.map.connections:
            if connection.first_zone == current_hub.name:
                available.append(self.map.get_hub(connection.second_zone))
            elif connection.second_zone == current_hub.name:
                available.append(self.map.get_hub(connection.first_zone))
        return available

    def run(self):
        opened = []
        closed = []
        path = []
        opened.append(self.start_hub)
        while self.end_hub not in closed:
            current = sorted(opened, key=lambda item: item.f_pos)[0]
            closed.append(current)
            opened.pop(opened.index(current))
            adjacent = self._find_adjacent(current)
            for c in adjacent:
                connection = self.map.get_connection(current, c)
                if c in closed or c.zone == "blocked":
                    continue
                if c not in opened:
                    self._g_path(current, c)
                    self._h_path(connection, c)
                    self._f_path(c)
                    c.parent = current.name
                    opened.append(c)
                elif c in opened:
                    self._g_path(current, c)
                    self._h_path(connection, c)
                    self._f_path(c)
        current = self.end_hub
        while current != self.start_hub:
            path.append(current)
            current = self.map.get_hub(current.parent)
        self.paths.append(path[::-1])
        return path[::-1]
