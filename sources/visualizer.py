# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#   visualizer.py                                       :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#   By: lbordana <lbordana@student.42mulhouse.fr>   +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#   Created: 2026/06/16 23:54:23 by lbordana           #+#    #+#             #
#   Updated: 2026/06/17 23:37:45 by lbordana          ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

import pygame
from pyvidplayer2 import Video

pygame.init()
pygame.display.set_caption("Fly-in : Echoes of the galaxy")


class Display():
    size_w = pygame.display.Info().current_w
    size_h = pygame.display.Info().current_h


class Viewport():
    surface = pygame.display.set_mode((Display().size_w, Display().size_h))


class Cinematics(Viewport):
    intro = Video("assets/cinematics/intro.mp4")

    def __init__(self):
        self.intro.resize((Display().size_w, Display().size_h))

    def _cinematics_events(self):
        pass

    def _launch_intro(self):
        while True:
            self.intro.update()
            if self.intro.draw(self.surface, (0, 0)) is True:
                pygame.display.update()
                break
        while True:
            self.intro.update()
            if self.intro.draw(self.surface, (0, 0)) is False:
                break
            pygame.display.update()


def start_vizualizer():
    running = True
    visualizer = Cinematics()
    visualizer._launch_intro()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
