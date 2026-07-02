# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_star.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/30 17:36:20 by lbordana        #+#    #+#               #
#  Updated: 2026/07/02 17:27:58 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from sources.components.map_objects import Connection, Hub
from sources.parser import GlobalParser


class Drone():
    def __init__(self, start_hub: Hub):
        self.current_pos = start_hub


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

    def _calc_distance(self):
        mapper = self.map.connections.copy()
        actual_hub = (0, self.end_hub.name)
        dist_calc = {self.end_hub.name: 0}
        queue = []
        count = 0
        index = 0

        while mapper != []:
            count = actual_hub[0] + 1
            while index < len(mapper):
                if mapper[index].first_zone == actual_hub[1]:
                    if count <= dist_calc.get(mapper[index].second_zone, count):
                        dist_calc.update({mapper[index].second_zone: count})
                    queue.append((count, mapper[index].second_zone))
                    mapper.pop(index)
                elif mapper[index].second_zone == actual_hub[1]:
                    if count <= dist_calc.get(mapper[index].first_zone, count):
                        dist_calc.update({mapper[index].first_zone: count})
                    queue.append((count, mapper[index].first_zone))
                    mapper.pop(index)
                else:
                    index += 1
            index = 0
            actual_hub = queue[0]
            queue.pop(0)

        return dist_calc

    def _calc_path(self):
        mapper = self.map.connections.copy()
        actual_hub = (0, self.start_hub.name)
        path_calc = {self.start_hub.name: 0}
        queue = []
        count = 0
        index = 0

        while mapper != []:
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

    def _update_map(self):
        pass


def start_algorithm(map: GlobalParser):
    path = AStarAlgorithm(map)._calc_path()
    dist = AStarAlgorithm(map)._calc_distance()
    return AStarAlgorithm(map)._calc_heuristic(dist, path)
