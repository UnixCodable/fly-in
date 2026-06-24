# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#   gui_objects.py                                      :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#   By: lbordana <lbordana@student.42mulhouse.fr>   +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#   Created: 2026/06/20 13:20:13 by lbordana           #+#    #+#             #
#   Updated: 2026/06/24 01:28:49 by lbordana          ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

from abc import ABC, abstractmethod
from typing import Optional
from pyvidplayer2 import Video
from sources.visualizer import Window
import sys
import pygame


class MenuButton():
    def __init__(self,
                 window: Window,
                 pos: tuple[int, int],
                 dimensions: tuple[int, int],
                 tag: str,
                 border: int = 0,
                 radius: int = -1):
        menu_font = pygame.Font("assets/fonts/Oswald.ttf", 70)
        self.shape = pygame.Rect(pos, dimensions)
        color = pygame.Color(255, 255, 255)
        pygame.draw.rect(window.surface, color, self.shape, border, radius)
        text = pygame.Font.render(menu_font, tag, True, (255, 255, 255))
        window.surface.blit(text, ((pos[0], pos[1]), (dimensions[0], dimensions[1])))


class View(ABC):
    def __init__(self, window: Window):
        self.window = window

    @abstractmethod
    def _get_events(self):
        pass

    @abstractmethod
    def _launch(self):
        pass


class Cinematics(View):

    def __init__(self,
                 video: Video,
                 window: Window,
                 speed: float = 1,
                 begin_frame: int = 1,
                 end_frame: Optional[int] = None):
        super().__init__(window)
        self.video: Video = video
        self.video.set_speed(speed)
        self.video.seek_frame(begin_frame)
        self.end_frame = end_frame if end_frame else self.video.frame_count

    def _get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.video.stop()
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.video.set_speed(1)
                    self.video.seek_frame(self.end_frame - 2)

    def _launch(self):
        while True:
            if self.video.frame == 0:
                break
            self.window.surface.fill("#000000")
            self._get_events()
            self.video.draw(self.window.surface, (0, 0))
            pygame.display.update()


class Menu(View):
    def __init__(self, window: Window):
        super().__init__(window)

    def _get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    if self.window.data["mode"] == "fullscreen":
                        self.window._rewrite({"mode": "windowed"})
                    elif self.window.data["mode"] == "windowed":
                        self.window._rewrite({"mode": "fullscreen"})

    def _launch(self):
        while True:
            image = pygame.image.load("assets/gui/background.png")
            self.window.surface.blit(image)
            MenuButton(self.window, (100, 100), (200, 100), "Play", 6, 10)
            self._get_events()
            pygame.display.update()
