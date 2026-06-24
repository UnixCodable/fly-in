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

    from .components.gui_objects import Cinematics, Menu

    window = Window()
    lucasfilm = Cinematics(Video("assets/cinematics/lucasfilm.mp4"),
                           window, end_frame=200)
    intro = Cinematics(Video("assets/cinematics/intro.mp4"),
                       window, speed=0.9)
    menu = Menu(window)

    def __init__(self):
        self.lucasfilm._launch()
        self.intro._launch()
        while True:
            self.menu._launch()


def start_vizualizer():
    Controller()
    pygame.quit()
