# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  algorithm.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/14 07:11:09 by lbordana        #+#    #+#               #
#  Updated: 2026/07/18 22:59:17 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from sources.game.map_objects import Connection, Hub, Drone
from sources.tools.parser import GlobalParser


class Algorithm():
    def __init__(self, map: GlobalParser):
        self.map: GlobalParser = map
        self.start_hub: Hub = self.map.get_start_hub()
        self.end_hub: Hub = self.map.get_end_hub()
        self._create_distance()
        self._create_remaining()

    def _update_score(self, hub: Hub, connection: Connection):
        hub.score = 0
        if hub.zone == "restricted":
            hub.score += 6
        elif hub.zone == "normal":
            hub.score += 4
        elif hub.zone == "priority":
            hub.score += 2
        if hub.occupants > hub.max_drones:
            hub.score += (hub.occupants - hub.max_drones) * 2

    def _create_remaining(self):
        opened = [self.end_hub]
        opened[0].remaining += 1

        while opened != []:
            current = opened.pop(0)
            adjacent = self._find_adjacent(current)

            for adj in adjacent:
                if adj.remaining > current.remaining or adj.remaining == 0:
                    adj.remaining = current.remaining + 1
                    opened.append(adj)

            opened = sorted(opened, key=lambda x: x.distance)

    def _create_distance(self):
        opened = [self.start_hub]
        opened[0].distance += 1

        while opened != []:
            current = opened.pop(0)
            adjacent = self._find_adjacent(current)

            for adj in adjacent:
                if adj.distance > current.distance or adj.distance == 0:
                    adj.distance = current.distance + 1
                    opened.append(adj)

            opened = sorted(opened, key=lambda x: x.distance)

    def _find_adjacent(self, current_hub: Hub) -> list[Hub]:
        available = []
        for connection in self.map.connections:
            if connection.first_zone == current_hub.name:
                available.append(self.map.get_hub(connection.second_zone))
            elif connection.second_zone == current_hub.name:
                available.append(self.map.get_hub(connection.first_zone))
        return available

    def run(self):
        pass