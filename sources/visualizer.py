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

pygame.init()
pygame.display.set_caption("Fly-in : Echoes of the galaxy")


class WindowManager():
    size_w = pygame.display.Info().current_w
    size_h = pygame.display.Info().current_h
    running = True

    def __init__(self):
        self.surface = pygame.display.set_mode((self.size_w, self.size_h))


class Controller():

    from .components.gui_objects import Cinematics, Menu

    window = WindowManager()
    intro = Cinematics(window, Video("assets/cinematics/intro.mp4"), 1.2, 130, 5600)
    menu = Menu(window)

    def __init__(self):
        self.intro._launch()
        self.menu._launch()


def start_vizualizer():
    Controller()
    pygame.quit()
