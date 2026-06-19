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
        self.surface = pygame.display.set_mode((self.size_w, self.size_h))


class View(ABC):
    @abstractmethod
    def _get_events(self):
        pass

    @abstractmethod
    def _launch(self):
        pass


class Cinematics(View):

    def __init__(self, window: WindowManager, video):
        self.window: WindowManager = window
        self.video: Video = video
        self.video.resize((self.window.size_w, self.window.size_h))

    def _get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print(self.video.frame)


    def _launch(self):
        while self.window.running:
            self._get_events()
            if self.video.draw(self.window.surface, (0, 0)) is True:
                pygame.display.update()
                break
        while self.window.running:
            self._get_events()
            if self.video.draw(self.window.surface, (0, 0)) is False:
                break
            pygame.display.update()


class Menu(View):

    def __init__(self, window: WindowManager):
        self.window: WindowManager = window

    def _get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window.running = False

    def _launch(self):
        while self.window.running:
            self._get_events()


class Controller():
    window = WindowManager()
    intro = Cinematics(window, Video("assets/cinematics/intro2.mp4"))
    menu = Menu(window)

    def __init__(self):
        self.intro._launch()
        self.menu._launch()


def start_vizualizer():
    Controller()
    pygame.quit()
