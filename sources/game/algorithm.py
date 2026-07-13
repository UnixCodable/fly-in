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

from sources.game.map_objects import Connection, Hub
from sources.tools.parser import GlobalParser


class Algorithm():
    def __init__(self, map: GlobalParser):
        self.map: GlobalParser = map
        self.start_hub: Hub = self.map.get_start_hub()
        self.end_hub: Hub = self.map.get_end_hub()
        self.paths: list[list[Hub]] = []

    def _score(self, connection: Connection, current_hub: Hub, next_hub: Hub):
        weight = 0.0

        pos = int((current_hub.pos) + 1)
        check_same_turn = len([p for p in self.paths
                               if len(p) >= pos and p[pos - 1] == next_hub])
        check_connection_link = len([p for p in self.paths if len(p) >= pos
                                    and self.map.get_connection(p[pos - 1], p[pos - 2]) == connection])

        if check_same_turn < next_hub.max_drones:
            if next_hub.zone == "restricted":
                weight += 1
            if next_hub.zone == "priority":
                weight -= 1
        elif 0 < check_same_turn < next_hub.max_drones:
            weight -= next_hub.max_drones - check_same_turn
        elif next_hub.max_drones < check_same_turn:
            weight += check_same_turn - next_hub.max_drones
            if next_hub.zone == "restricted":
                weight += (check_same_turn - next_hub.max_drones) * 2

        if 0 < check_connection_link < connection.max_link:
            weight -= connection.max_link - check_connection_link
        elif connection.max_link < check_connection_link:
            weight += (check_connection_link - connection.max_link)

        if weight < next_hub.weight and current_hub.pos < next_hub.pos or next_hub.pos == 0:
            next_hub.pos = pos
            next_hub.weight = weight

    def _find_adjacent(self, current_hub: Hub) -> list[Hub]:
        available = []
        for connection in self.map.connections:
            if connection.first_zone == current_hub.name:
                available.append(self.map.get_hub(connection.second_zone))
            elif connection.second_zone == current_hub.name:
                available.append(self.map.get_hub(connection.first_zone))
        return available

    def run(self):
        path = []
        closed = []
        opened = [self.start_hub]

        while len(opened) != 0:

            current = opened.pop(0)
            closed.append(current)
            adjacent = self._find_adjacent(current)

            for adj_hub in adjacent:
                if adj_hub in closed:
                    continue
                connection = self.map.get_connection(current, adj_hub)
                self._score(connection, current, adj_hub)
                if adj_hub not in opened:
                    opened.append(adj_hub)

                opened = sorted(opened, key=lambda x: (x.weight, x.pos))

        current = self.start_hub
        # closed = []
        issues = []
        while current != self.end_hub:
            closed.append(current)
            adjacent = filter(lambda item: (current, item) not in issues and item.pos > current.pos, self._find_adjacent(current))
            try:
                current = min([f for f in adjacent], key=lambda item: (item.weight, item.pos))
                path.append(current)
            except ValueError:
                issues.append((closed[-2], current))
                # print([(i[0].name, i[1].name) for i in issues])
                # print([current.name])
                closed = []
                current = self.start_hub
                path = []

        for h in self.map.hubs:
            h.pos = 0
            # h.weight = 0

        self.paths.append(path)
        return path
