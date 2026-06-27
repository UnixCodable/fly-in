# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#   visualizer.py                                       :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#   By: lbordana <lbordana@student.42mulhouse.fr>   +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#   Created: 2026/06/16 23:54:23 by lbordana           #+#    #+#             #
#   Updated: 2026/06/18 23:23:44 by lbordana          ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

import pygame as pg
import sys
from pyvidplayer2 import Video
from sources.components.window import Window
from .components.views import (
        Cinematics,
        MenuView,
        SettingsView,
        MapSelectionView
    )


class Visualizer():

    Window()
    lucas = Cinematics(Video("assets/cinematics/lucasfilm.mp4"), end_frame=200)
    intro = Cinematics(Video("assets/cinematics/intro.mp4"), speed=0.9)
    menu = MenuView()
    settings = SettingsView()
    map_selection = MapSelectionView()

    def _start(self):

        from sources.components.buttons import ViewAction

        self.lucas._launch()
        self.intro._launch()
        self.menu._launch()
        while True:
            for event in pg.event.get():
                if event.type == ViewAction.MENU.value:
                    self.menu._launch()
                if event.type == ViewAction.SETTINGS.value:
                    self.settings._launch()
                if event.type == ViewAction.MAP_SELECTION.value:
                    self.map_selection._launch()
                if event.type == ViewAction.EXIT.value:
                    pg.quit()
                    sys.exit(0)
