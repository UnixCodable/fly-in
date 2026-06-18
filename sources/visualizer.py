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
from abc import ABC, abstractmethod

pygame.init()
pygame.display.set_caption("Fly-in : Echoes of the galaxy")


class WindowManager():
    size_w = pygame.display.Info().current_w
    size_h = pygame.display.Info().current_h
    running = True

    def __init__(self):
        self.__surface = pygame.display.set_mode((self.size_w, self.size_h))

    @classmethod
    def _set_running(cls, boolean):
        cls.running = boolean


class View(ABC):
    @abstractmethod
    def _get_events(self):
        pass

    @abstractmethod
    def _launch(self):
        pass


class Cinematics(View):

    def __init__(self, video):
        self.video = video
        self.intro.resize((self.size_w, self.size_h))

    def _get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _launch(self):
        while self.running:
            self._get_events()
            self.intro.update()
            if self.intro.draw(self.surface, (0, 0)) is True:
                pygame.display.update()
                break
        while self.running:
            self._get_events()
            self.intro.update()
            if self.intro.draw(self.surface, (0, 0)) is False:
                break
            pygame.display.update()


class Menu(View):
    def _get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _launch(self):
        while self.running:
            self._get_events()


class Controller():
    intro = Cinematics(Video("assets/cinematics/intro.mp4"))

    def __init__(self, window: WindowManager):
        self.window = window
        self.intro._launch_intro()


def start_vizualizer():
    window = WindowManager()
    Controller(window)
    pygame.quit()
