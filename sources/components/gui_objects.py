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
from ..visualizer import SURFACE, DIFFERENCE_H, DIFFERENCE_W
import sys
import pygame


class MenuButton():
    def __init__(self,
                 pos_x: int,
                 pos_y: int,
                 width: int,
                 height: int,
                 border: int = 0,
                 radius: int = -1):
        self.shape = pygame.Rect(pos_x, pos_y, width, height)
        color = pygame.Color(255, 255, 255)
        pygame.draw.rect(SURFACE, color, self.shape, border, radius)


class View(ABC):
    @abstractmethod
    def _get_events(self):
        pass

    @abstractmethod
    def _launch(self):
        pass


class Cinematics(View):

    def __init__(self,
                 video: Video,
                 speed: float = 1,
                 begin_frame: int = 1,
                 end_frame: Optional[int] = None):
        self.video: Video = video
        self.video.set_speed(speed)
        self.video.seek_frame(begin_frame)
        self.end_frame = end_frame if end_frame else self.video.frame_count

    def _get_events(self):
        self.video.resize((int(SURFACE.get_height() * (16/9)),
                           pygame.display.get_window_size()[1]))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.video.set_speed(1)
                    self.video.seek_frame(self.end_frame - 2)
                if event.key == pygame.K_a:
                    pygame.transform.scale(SURFACE, (1920, 1080))

    def _launch(self):
        draw_pos = (0, 0)
        while True:
            SURFACE.fill("#000000")
            self._get_events()
            draw_pos = (int((pygame.display.get_window_size()[0] -
                        int(pygame.display.get_window_size()[1] * (16/9))) / 2), 0)
            self.video.draw(SURFACE, draw_pos)
            pygame.display.update()
            if self.video.frame == (self.end_frame - 1):
                break


class Menu(View):
    def _get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    pygame.transform.scale(SURFACE, (1920, 1080))

    def _launch(self):
        MenuButton(100, 100, 200, 100, 6, 10)
        while True:
            self._get_events()
            pygame.display.update()
