# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  algorithm.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/14 07:11:09 by lbordana        #+#    #+#               #
#  Updated: 2026/07/15 13:49:31 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from sources.game.map_objects import Connection, Hub, Drone
from sources.tools.parser import GlobalParser


class Algorithm():
    def __init__(self, map: GlobalParser):
        self.map: GlobalParser = map
        self.start_hub: Hub = self.map.get_start_hub()
        self.end_hub: Hub = self.map.get_end_hub()

    def _score(self, hub: Hub, connection: Connection):
        pass

    def _find_adjacent(self, current_hub: Hub) -> list[Hub]:
        available = []
        for connection in self.map.connections:
            if connection.first_zone == current_hub.name:
                available.append(self.map.get_hub(connection.second_zone))
            elif connection.second_zone == current_hub.name:
                available.append(self.map.get_hub(connection.first_zone))
        return available

    def run(self, drone: Drone):
        pass
