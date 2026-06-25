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

import pygame
from pyvidplayer2 import Video
from .settings import Settings

pygame.init()
pygame.display.set_caption("Fly-in : Echoes of the galaxy")


class Window():
    def __init__(self):
        self.settings = Settings()
        self.data = self.settings._get_settings()
        self.width, self.height = self.data["resolution"]
        if self.data["mode"] == "fullscreen":
            self.surface = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.surface = pygame.display.set_mode((self.width, self.height))
        self.primary_font = pygame.Font("assets/fonts/Starjhol.ttf")

    def _rewrite(self, new_config: dict):
        self.settings._set_settings(new_config)
        self.data = self.settings._get_settings()
        self.width, self.height = self.data["resolution"]
        if self.data["mode"] == "fullscreen":
            self.surface = pygame.display.set_mode(
                (self.width, self.height), pygame.FULLSCREEN)
        else:
            self.surface = pygame.display.set_mode(
                (self.width, self.height))


class Controller():

    from .components.view_objects import CinematicsView, MenuView

    window = Window()
    lucasfilm = CinematicsView(Video("assets/cinematics/lucasfilm.mp4"),
                               window, end_frame=200)
    intro = CinematicsView(Video("assets/cinematics/intro.mp4"),
                           window, speed=0.9)
    menu = MenuView(window)
    # settings = SettingsView
    # map_selection = MapSelectionView

    def __init__(self):
        self.lucasfilm._launch()
        self.intro._launch()
        view = self.menu._launch()
        while True:
            if view == 1:
                self.menu._launch()
            # if view == 2:
                # self.settings._launch()
            # if view == 3:
            #     self.map_selection._launch()


def start_vizualizer():
    Controller()
    pygame.quit()
