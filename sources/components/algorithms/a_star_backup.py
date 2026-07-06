# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#   a_star.py                                           :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#   By: lbordana <lbordana@student.42mulhouse.fr>   +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#   Created: 2026/06/30 17:36:20 by lbordana           #+#    #+#             #
#   Updated: 2026/07/06 13:22:11 by lbordana          ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

import sys

from sources.components.map_objects import Connection, Drone, Hub
from sources.parser import GlobalParser


class AStarAlgorithm():
    def __init__(self, map: GlobalParser):
        self.map: GlobalParser = map
        self.start_hub: Hub = self.map.get_start_hub()
        self.end_hub: Hub = self.map.get_end_hub()

    def _calc_heuristic(self, dist_calc: dict[str, int], path_calc: dict[str, int]):

        heur_calc = {}
        for d in dist_calc.keys():
            heur_calc.update({d: dist_calc.get(d, 0) + path_calc.get(d, 0)})

        return heur_calc

    # @lru_cache()
    def _calc_path(self, start_hub: Hub):
        mapper = self.map.connections.copy()
        actual_hub = (0, start_hub.name)
        path_calc = {start_hub.name: 0}
        queue = []
        count = 0
        index = 0

        while mapper != []:

            hub = self.map.get_hub(actual_hub[1])

            if hub != self.start_hub and hub.zone == "restricted":
                count = actual_hub[0] + 2
            elif hub != self.start_hub and len(hub.occupant) >= hub.max_drones:
                count = actual_hub[0] + 2 + len(hub.queued)
            else:
                count = actual_hub[0] + 1

            while index < len(mapper):

                if mapper[index].first_zone == actual_hub[1]:
                    if count <= path_calc.get(mapper[index].second_zone, count):
                        path_calc.update({mapper[index].second_zone: count})
                    queue.append((count, mapper[index].second_zone))
                    mapper.pop(index)

                elif mapper[index].second_zone == actual_hub[1]:
                    if count <= path_calc.get(mapper[index].first_zone, count):
                        path_calc.update({mapper[index].first_zone: count})
                    queue.append((count, mapper[index].first_zone))
                    mapper.pop(index)

                else:
                    index += 1

            index = 0
            actual_hub = queue[0]
            queue.pop(0)

        return path_calc

    def _find_best_node(self, drone: Drone, heuristic: dict):
        possible_zones = []

        for connection in self.map.connections:
            if connection.first_zone == drone.pos:
                possible_zones.append(connection.second_zone)
            elif connection.second_zone == drone.pos:
                possible_zones.append(connection.first_zone)

        best_hub = sorted([nb for nb in heuristic.items() if nb[0] in possible_zones],
                          key=lambda item: item[1])[0][0]
        return best_hub

    def update_map(self, pos: Hub):
        dist = self._calc_path(pos)
        path = self._calc_path(self.end_hub)
        return self._calc_heuristic(dist, path)

    def move_drone(self, drone: Drone):

        if drone.pos == self.end_hub.name:
            return

        map_heuristic = self.update_map(self.map.get_hub(drone.pos))
        pos: Hub | Connection = self.map.get_hub(self._find_best_node(drone, map_heuristic))

        with open("output.txt", "a") as file:
            if type(pos) is Hub:
                if len(pos.occupant) >= pos.max_drones:
                    pos.queued.append(drone)
                    return
                self.map.get_hub(drone.pos).occupant.pop(0)
                file.write(f"{drone.id}-{pos.name} ")
                pos.occupant.append(drone)
                drone.pos = pos.name
            elif type(pos) is Connection:
                file.write(f"{drone.id}-{pos.first_zone}-{pos.second_zone} ")


def start_algorithm(map: GlobalParser):
    algorithm = AStarAlgorithm(map)
    drones: list[Drone] = []
    for id in range(map.total_drone):
        drones.append(Drone(f"D{id}", algorithm.start_hub.name))
        algorithm.start_hub.occupant.append(drones[-1])
        with open("output.txt", "a") as file:
            file.write(f"D{id}-{algorithm.start_hub.name} ")

    with open("output.txt", "a") as file:
        file.write('\n')

    while len(drones) != len([d for d in drones if map.get_hub(d.pos).hub_type == 'end_hub']):
        for d in drones:
            algorithm.move_drone(d)
        with open("output.txt", "a") as file:
            file.write('\n')

    return
