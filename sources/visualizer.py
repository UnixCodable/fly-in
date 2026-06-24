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
        self.surface = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.font = pygame.Font()

    def _rewrite(self, new_config: dict):
        self.settings._set_settings(new_config)
        self.data = self.settings._get_settings()
        self.width, self.height = self.data["resolution"]
        if self.data["mode"] == "fullscreen":
            self.surface = pygame.display.set_mode(
                (self.width, self.height),
                pygame.RESIZABLE | pygame.NOFRAME)
        else:
            self.surface = pygame.display.set_mode(
                (self.width, self.height),
                pygame.RESIZABLE)


class Controller():

    from .components.gui_objects import Cinematics, Menu

    window = Window()
    intro = Cinematics(Video("assets/cinematics/intro.mp4"), window)
    menu = Menu(window)

    def __init__(self):
        self.intro._launch()
        self.menu._launch()


def start_vizualizer():
    Controller()
    pygame.quit()
