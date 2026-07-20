# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  algorithm.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/14 07:11:09 by lbordana        #+#    #+#               #
#  Updated: 2026/07/20 03:35:47 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from sources.game.map_objects import Connection, Hub, Drone
from sources.tools.parser import GlobalParser


class Algorithm():
    def __init__(self, map: GlobalParser):
        self.map: GlobalParser = map
        self.start_hub: Hub = self.map.get_start_hub()
        self.end_hub: Hub = self.map.get_end_hub()
        self._create_remaining()

    def _update_score(self, hub: Hub, connection: Connection):
        hub.score = 0
        if hub.zone == "priority":
            hub.score -= 1
        if hub.is_full():
            if hub.zone == "restricted":
                hub.score += ((len(hub.waiting) + hub.max_drones) * 2)
            else:
                hub.score += (len(hub.waiting) + hub.max_drones)
        if connection.is_full():
            hub.score += (len(connection.waiting) + connection.max_link)

    def _create_remaining(self):
        opened = [self.end_hub]
        opened[0].remaining += 1

        while opened != []:
            current = opened.pop(0)
            adjacent = self._find_adjacent(current)

            if len(adjacent) == 1 and current != self.end_hub:
                # print(adjacent[0].name)
                while len(adjacent) == 1 and current != self.end_hub:
                    current.locked = True
                    current = adjacent[0]
                    adjacent = [adj for adj in self._find_adjacent(current) if adj.locked is False]

            for adj in adjacent:
                if adj.locked is True:
                    continue
                if adj.zone == "blocked":
                    adj.locked = True
                    continue
                if adj.remaining > current.remaining or adj.remaining == 0:
                    if adj.zone == "restricted":
                        adj.remaining = current.remaining + 2
                    else:
                        adj.remaining = current.remaining + 1
                    opened.append(adj)

            opened = sorted(opened, key=lambda x: x.remaining)

    def _find_adjacent(self, current_hub: Hub) -> list[Hub]:
        available = []
        for connection in self.map.connections:
            if connection.first_zone == current_hub.name:
                available.append(self.map.get_hub(connection.second_zone))
            elif connection.second_zone == current_hub.name:
                available.append(self.map.get_hub(connection.first_zone))
        return available

    def check_hub(self, drone: Drone) -> Hub:
        current = drone.get_current_pos()
        adjacent = [adj for adj in self._find_adjacent(current)
                    if adj != drone.get_last_pos()]
        for adj in adjacent:
            if adj.locked is True:
                adjacent.pop(adjacent.index(adj))
                continue
            connection = self.map.get_connection(current, adj)
            if connection is not None:
                if drone.id in connection.waiting or drone.id in adj.waiting:
                    adjacent = [adj]
                    break
                self._update_score(adj, connection)

        best_node = min(adjacent, key=lambda x: (x.remaining + x.score, x.remaining))
        if best_node == self.end_hub:
            drone.shutdown()

        return best_node
