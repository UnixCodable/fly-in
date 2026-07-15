# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  algorithm.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/14 07:11:09 by lbordana        #+#    #+#               #
#  Updated: 2026/07/15 13:39:37 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from sqlite3 import connect

from sources.game.map_objects import Connection, Hub, Drone
from sources.tools.parser import GlobalParser


class Algorithm():
    def __init__(self, map: GlobalParser):
        self.map: GlobalParser = map
        self.start_hub: Hub = self.map.get_start_hub()
        self.end_hub: Hub = self.map.get_end_hub()

    def _score(self, hub: Hub, connection: Connection):
        score = 1
        if len(hub.occupants) > 0:
            if hub.zone == "restricted":
                score += (len(hub.occupants) + len(hub.waiting)) * 2
            else:
                score += (len(hub.occupants) + len(hub.waiting))
        if connection is not None and connection.get_passages() > 0:
            if hub.zone == "restricted":
                score += (len(connection.waiting) + connection.max_link) * 2
            else:
                score += (len(connection.waiting) + connection.max_link)
        if hub.zone == "restricted":
            score += 1
        if hub.zone == "priority":
            score += -1
        return score

    def _find_adjacent(self, current_hub: Hub) -> list[Hub]:
        available = []
        for connection in self.map.connections:
            if connection.first_zone == current_hub.name:
                available.append(self.map.get_hub(connection.second_zone))
            elif connection.second_zone == current_hub.name:
                available.append(self.map.get_hub(connection.first_zone))
        return available

    def run(self, drone: Drone):
        start = drone.get_current_pos()
        start.score = 0

        opened: list[Hub] = [start]
        closed = []
        while self.end_hub not in opened:

            current = min(opened, key=lambda x: (x.distance + x.score))
            opened.pop(opened.index(current))
            closed.append(current)

            for adj in self._find_adjacent(current):

                if adj.zone == "blocked" or adj in closed:
                    continue
                connection = self.map.get_connection(current, adj)
                if current.score + self._score(adj, connection) < adj.score or adj.score == -1:
                    # print(current.name, current.score)
                    adj.distance += current.distance
                    adj.score = current.score + self._score(adj, connection)
                    adj.parent = current.name
                    opened.append(adj)

        best_hub = self.end_hub
        while best_hub != drone.get_current_pos():
            last_visited = best_hub
            best_hub = self.map.get_hub(best_hub.parent)
        self.map.reset_scores()

        if last_visited == self.end_hub:
            drone.shutdown()
        drone.distance += last_visited.distance
        return last_visited
