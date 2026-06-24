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

# Constants
SETTINGS = get_settings()
SCREEN_W = SETTINGS["resolution"][0]
SCREEN_H = SETTINGS["resolution"][1]
SURFACE = pygame.display.set_mode((SCREEN_W, SCREEN_H))


class Controller():

    from .components.gui_objects import Cinematics, Menu

    intro = Cinematics(Video("assets/cinematics/intro.mp4"))
    menu = Menu()

    def __init__(self):
        self.intro._launch()
        self.menu._launch()


def start_vizualizer():
    Controller()
    pygame.quit()
