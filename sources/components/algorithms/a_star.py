# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_star.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/30 17:36:20 by lbordana        #+#    #+#               #
#  Updated: 2026/07/01 12:37:46 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from sources.components.map_objects import Connection, Hub
from sources.parser import GlobalParser


class StarA():
    def _hub_order(self):
        pass

    def _get_next_cost(self):
        pass

    def _get_next_heuristic(self):
        pass


def start_algorithm(map: GlobalParser):
    start_hub = map.get_start_hub()
    # end_hub = map.get_end_hub()
    actual_hub = (0, start_hub.name)
    count = 0
    mapper = map.connections.copy()
    final = []
    queue = []

    while mapper != []:
        count = actual_hub[0] + 1
        for c in mapper:
            if c.first_zone == actual_hub[1]:
                final.append((count, c.second_zone))
                queue.append((count, c.second_zone))
                mapper.pop(mapper.index(c))
            elif c.second_zone == actual_hub[1]:
                final.append((count, c.first_zone))
                queue.append((count, c.first_zone))
                mapper.pop(mapper.index(c))
        try:
            actual_hub = queue[0]
            print(queue)
            queue.pop(0)
        except IndexError:
            pass

    return final
