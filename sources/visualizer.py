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
from .settings import get_settings

pygame.init()
pygame.display.set_caption("Fly-in : Echoes of the galaxy")


class Window():
    def __init__(self):
        self.settings = get_settings()
        self.width, self.height = self.settings["resolution"]
        self.surface = pygame.display.set_mode((0, 0), pygame.RESIZABLE)

    def _resize(self, dimensions: tuple[int, int]):
        self.settings = get_settings()
        self.width, self.height = self.settings["resolution"]
        self.surface = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)


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
