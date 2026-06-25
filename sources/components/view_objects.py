# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  view_objects.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/25 09:07:21 by lbordana        #+#    #+#               #
#  Updated: 2026/06/25 13:25:45 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import ABC, abstractmethod
from typing import Optional
from pyvidplayer2 import Video
from sources.visualizer import Window
from sources.components.gui_objects import Action, MenuButton
import sys
import pygame


class View(ABC):
    def __init__(self, window: Window):
        self.window = window

    @abstractmethod
    def _get_events(self):
        pass

    @abstractmethod
    def _launch(self) -> int:
        pass

    def _render_image(self, path: str, coord: tuple[int, int] = (0, 0)):
        img = pygame.image.load("assets/gui/background.png")
        img = pygame.transform.scale(img, self.window.surface.get_size())
        self.window.surface.blit(img, coord)

    def _render_button(self):
        pass


class CinematicsView(View):

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
        self.end_frame = end_frame if end_frame else 0

    def _get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.video.stop()
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.video.set_speed(1)
                    if self.end_frame > 0:
                        self.video.seek_frame(self.end_frame - 2)
                    else:
                        self.video.seek_frame(self.video.frame_count - 2)

    def _launch(self) -> int:
        self.video.resize(self.window.surface.get_size())
        while True:
            if self.video.frame == self.end_frame:
                break
            self._get_events()
            self.video.draw(self.window.surface, (0, 0))
            pygame.display.update()
        self.video.stop()
        return 0


class MenuView(View):
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
        play_button = MenuButton(self.window,
                                 (int(self.window.width * 0.2),
                                  int(self.window.height * 0.33)),
                                 (450, 200),
                                 "Play", Action.MAP_SELECTION, 6, 10)
        settings_button = MenuButton(self.window,
                                     (int(self.window.width * 0.2),
                                      int(self.window.height * 0.45)),
                                     (450, 200), "Settings", Action.SETTINGS, 6, 10)
        exit_button = MenuButton(self.window,
                                 (int(self.window.width * 0.2),
                                  int(self.window.height * 0.57)),
                                 (450, 200), "Exit", Action.EXIT, 6, 10)
        while True:
            self._render_image("assets/gui/background.png")
            play_button._render()
            settings_button._render()
            exit_button._render()
            self._get_events()
            pygame.display.update()