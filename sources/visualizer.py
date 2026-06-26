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
import threading
from pyvidplayer2 import Video
from .settings import Settings

pg.init()
pg.display.set_caption("Fly-in : Echoes of the galaxy")


class Window():
    settings = Settings()
    data = settings._get_settings()
    width, height = data["resolution"]
    if data["mode"] == "fullscreen":
        surface = pg.display.set_mode((width, height), pg.FULLSCREEN)
    else:
        surface = pg.display.set_mode((width, height))

    @classmethod
    def _rewrite(cls, new_config: dict):
        cls.settings._set_settings(new_config)
        cls.data = cls.settings._get_settings()
        cls.width, cls.height = cls.data["resolution"]
        if cls.data["mode"] == "fullscreen":
            cls.surface = pg.display.set_mode((cls.width, cls.height),
                                              pg.FULLSCREEN)
        else:
            cls.surface = pg.display.set_mode((cls.width, cls.height))


# Window constants
SURFACE = Window.surface
WIN_WIDTH = Window.width
WIN_HEIGHT = Window.height


class Controller():

    from sources.components.gui_objects import Action
    from .components.view_objects import (
        Cinematics,
        MenuView,
        SettingsView,
        MapSelectionView)

    window = Window()
    lucas = Cinematics(Video("assets/cinematics/lucasfilm.mp4"), end_frame=200)
    intro = Cinematics(Video("assets/cinematics/intro.mp4"), speed=0.9)
    menu = MenuView()
    settings = SettingsView()
    map_selection = MapSelectionView()
    selector = 0

    def __init__(self):
        self.lucas._launch()
        self.intro._launch()
        self.menu._launch()
        while True:
            for event in pg.event.get():
                if event.type == self.Action.MENU.value:
                    self.menu._launch()
                if event.type == self.Action.SETTINGS.value:
                    self.settings._launch()
                if event.type == self.Action.MAP_SELECTION.value:
                    self.map_selection._launch()
                if event.type == self.Action.EXIT.value:
                    pg.quit()
                    sys.exit(0)


def start_vizualizer():
    Controller()
    pg.quit()
