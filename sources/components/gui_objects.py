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
        self.font = pygame.Font("assets/fonts/Oswald.ttf", 110)
        self.rect = pygame.Rect(pos, dimensions)
        self.pos = pos
        self.window = window
        self.tag = tag
        self.border = border
        self.radius = radius
        self.color_inactive = pygame.Color(255, 255, 255)
        self.color_hover = pygame.Color(255, 228, 54)
        self.clickable = False
        self.clickable_cursor = pygame.Cursor(pygame.SYSTEM_CURSOR_HAND)
        self.arrow_cursor = pygame.Cursor(pygame.SYSTEM_CURSOR_ARROW)

    def _render(self):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            pygame.mouse.set_cursor(self.clickable_cursor)
            self.clickable = True
            pygame.draw.rect(self.window.surface,
                             self.color_hover,
                             self.rect,
                             self.border,
                             self.radius)
            text = self.font.render(self.tag, True, self.color_hover)
        else:
            if self.clickable is True:
                pygame.mouse.set_cursor(self.arrow_cursor)
                self.clickable = False
            pygame.draw.rect(self.window.surface,
                             self.color_inactive,
                             self.rect,
                             self.border,
                             self.radius)
            text = self.font.render(self.tag, True, self.color_inactive)
        center_text = ((self.rect.width - text.get_width()) / 2,
                       (self.rect.height - text.get_height()) / 2)
        self.window.surface.blit(text, (self.pos[0] + center_text[0],
                                        self.pos[1] + center_text[1]))


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
        play_button = MenuButton(self.window,
                                 (int(self.window.width * 0.2),
                                  int(self.window.height * 0.33)),
                                 (450, 200), "Play", 6, 10)
        settings_button = MenuButton(self.window,
                                     (int(self.window.width * 0.2),
                                      int(self.window.height * 0.45)),
                                     (450, 200), "Settings", 6, 10)
        exit_button = MenuButton(self.window,
                                 (int(self.window.width * 0.2),
                                  int(self.window.height * 0.57)),
                                 (450, 200), "Exit", 6, 10)
        while True:
            self._render_image("assets/gui/background.png")
            play_button._render()
            settings_button._render()
            exit_button._render()
            self._get_events()
            pygame.display.update()
