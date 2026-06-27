# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  scale_calculations.py                             :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/27 02:15:46 by lbordana        #+#    #+#               #
#  Updated: 2026/06/27 02:16:27 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from sources.visualizer import Window


class Scale():
    def __init__(self):
        self._menu_button = (Window.width * 0.15, Window.width * 0.05)
        self._menu_button_square = (Window.width * 0.02, Window.width * 0.02)

    @property
    def menu_button(self):
        return self._menu_button

    @property
    def menu_button_square(self):
        return self._menu_button_square
