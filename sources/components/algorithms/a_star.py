# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_star.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/07 00:54:06 by lbordana        #+#    #+#               #
#  Updated: 2026/07/07 02:16:21 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from sources.components.map_objects import Connection, Drone, Hub
from sources.parser import GlobalParser


class Algorithm():
    def __init__(self, map: GlobalParser):
        self.map: GlobalParser = map
        self.start_hub: Hub = self.map.get_start_hub()
        self.end_hub: Hub = self.map.get_end_hub()

    def _h_path(self, next_hub: Hub):
        h_diff = (self.end_hub.coordinates[0] - next_hub.coordinates[0],
                  self.end_hub.coordinates[1] - next_hub.coordinates[1])
        next_hub.h_pos = (h_diff[0] ** h_diff[0]) + (h_diff[1] ** h_diff[1])

    def _g_path(self, current_hub: Hub, next_hub: Hub):
        next_hub.g_pos = int(((current_hub.g_pos / 10) + 1) * 10)

    def _f_path(self, next_hub: Hub):
        next_hub.f_pos = next_hub.h_pos + next_hub.g_pos

    def _find_connections(self, current_hub: Hub) -> list[Hub]:
        available = []
        for connection in self.map.connections:
            if connection.first_zone == current_hub.name:
                available.append(self.map.get_hub(connection.second_zone))
            elif connection.second_zone == current_hub.name:
                available.append(self.map.get_hub(connection.first_zone))
        return available

    def run(self):
        opened = []
        opened.append(self.start_hub)
        while self.end_hub not in self.closed:
            current = sorted(self.open, key=lambda item: item.f_pos)[0]
            self.closed.append(current)
            self.open.pop(self.closed.index(current))
            connected = self._find_connections(current)
            for c in connected:
                if c not in self.open:
                    self._g_path(current, c)
                    self._h_path(c)
                    self._f_path(c)
                    self.open.append(c)
                elif c in self.open:
                    self._g_path(current, c)
                    self._h_path(c)
                    self._f_path(c)
                    