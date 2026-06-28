# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  scales.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/27 02:15:46 by lbordana        #+#    #+#               #
#  Updated: 2026/06/28 01:52:17 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from sources.visualizer import Window


def scale_size(scale_x, scale_y) -> tuple[int, int]:
    return (int(Window.width * scale_x), int(Window.width * scale_y))


def scale_pos(scale_x, scale_y) -> tuple[int, int]:
    return (int(Window.width * scale_x), int(Window.height * scale_y))


def scale_text(scale: float) -> int:
    return int(Window.width * scale)
