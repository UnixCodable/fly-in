# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  gui_objects.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/20 13:20:13 by lbordana        #+#    #+#               #
#  Updated: 2026/06/22 01:09:06 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import ABC, abstractmethod
from typing import Optional
from pyvidplayer2 import Video
from ..visualizer import WindowManager
import pygame


class View(ABC):
    @abstractmethod
    def _get_events(self):
        pass

    @abstractmethod
    def _launch(self):
        pass


class Cinematics(View):

    def __init__(self,
                 window: WindowManager,
                 video: Video,
                 speed: float = 1,
                 begin_frame: int = 1,
                 end_frame: Optional[int] = None):
        self.window: WindowManager = window
        self.video: Video = video
        self.video.set_speed(speed)
        self.video.seek_frame(begin_frame)
        self.end_frame = end_frame if end_frame else self.video.frame_count

    def _get_events(self):
        self.video.resize((int(pygame.display.get_window_size()[1] * (16/9)), pygame.display.get_window_size()[1]))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.video.set_speed(1)
                    self.video.seek_frame(self.end_frame - 2)

    def _launch(self):
        draw_pos = (0, 0)
        while self.window.running:
            self._get_events()
            draw_pos = (int((pygame.display.get_window_size()[0] - int(pygame.display.get_window_size()[1] * (16/9))) / 2), 0)
            self.video.draw(self.window.surface, draw_pos)
            if self.video.frame >= self.end_frame:
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
