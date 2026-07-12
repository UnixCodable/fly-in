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

    def _g_path(self, connection: Connection, current_hub: Hub, next_hub: Hub):
        weight = 1

        g_pos = int((current_hub.g_pos) + 1)
        check_same_turn = len([p for p in self.paths if len(p) >= g_pos
                               and p[g_pos - 1] == next_hub])

        if check_same_turn > 0:
            if next_hub.zone == "restricted":
                weight += (check_same_turn) * 2
            else:
                weight += check_same_turn
        if next_hub.zone == "restricted":
            weight += 1

        if next_hub.zone == "priority":
            weight -= 1

        check_connection_link = len([p for p in self.paths if len(p) >= g_pos
                                     and p[g_pos - 1] == next_hub
                                     and p[g_pos - 2] == current_hub])
        if check_connection_link > 0:
            if next_hub.zone == "restricted":
                weight += (check_connection_link) * 2
            else:
                weight += check_connection_link

        if weight <= next_hub.f_pos and current_hub.g_pos < next_hub.g_pos or next_hub.g_pos == 0:
            next_hub.g_pos = g_pos
            next_hub.f_pos = weight

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
                self._g_path(connection, current, adj_hub)
                if adj_hub not in opened:
                    opened.append(adj_hub)

        current = self.start_hub
        # closed = []
        opened = []
        issues = []
        while current != self.end_hub:
            closed.append(current)
            adjacent = filter(lambda item: (current, item) not in issues and item.g_pos > current.g_pos, self._find_adjacent(current))
            try:
                current = min([f for f in adjacent], key=lambda item: item.f_pos)
                path.append(current)
            except ValueError:
                issues.append((closed[-2], current))
                print([(i[0].name, i[1].name) for i in issues])
                print([current.name])
                closed = []
                current = self.start_hub
                path = []

        for h in self.map.hubs:
            h.g_pos = 0
            # h.f_pos = 0

        self.paths.append(path)
        return path
