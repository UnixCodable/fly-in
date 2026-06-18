# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#   visualizer.py                                       :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#   By: lbordana <lbordana@student.42mulhouse.fr>   +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#   Created: 2026/06/16 23:54:23 by lbordana           #+#    #+#             #
#   Updated: 2026/06/18 19:50:13 by lbordana          ###   ########.fr       #
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
        self.__surface = pygame.display.set_mode((self.size_w, self.size_h))


class Events(WindowManager):
    def _get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


class Cinematics(Events):

    def __init__(self, video):
        self.video = video
        self.intro.resize((self.size_w, self.size_h))

    def _get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _launch_intro(self):
        while True:
            self._get_events()
            self.intro.update()
            if self.intro.draw(self.surface, (0, 0)) is True:
                pygame.display.update()
                break
        while True:
            self._get_events()
            self.intro.update()
            if self.intro.draw(self.surface, (0, 0)) is False:
                break
            pygame.display.update()


class Menu(Events):
    def _launch_menu(self):
        while True:
            self._get_events()
            self.intro.update()
            if self.intro.draw(self.surface, (0, 0)) is True:
                pygame.display.update()
                break
        while True:
            self._get_events()
            self.intro.update()
            if self.intro.draw(self.surface, (0, 0)) is False:
                break
            pygame.display.update()


class Controller(WindowManager):
    intro = Cinematics(Video("assets/cinematics/intro.mp4"))

    def __init__(self):
        self.intro._launch_intro()


def start_vizualizer():
    Controller()
    pygame.quit()
