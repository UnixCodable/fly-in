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
from sources.visualizer import Window
import pygame


class Button(ABC):
    def __init__(self, window: Window,
                 pos: tuple[int, int],
                 dimensions: tuple[int, int],
                 tag: str,
                 action: int,
                 border: int = 0,
                 radius: int = -1):
        self.surface = window.surface
        self.pos = pos
        self.tag = tag
        self.border = border
        self.radius = radius
        self.action = action
        self.clickable = False
        self.rect = pygame.Rect(pos, dimensions)
        self.clickable_cursor = pygame.Cursor(pygame.SYSTEM_CURSOR_HAND)
        self.arrow_cursor = pygame.Cursor(pygame.SYSTEM_CURSOR_ARROW)

    @abstractmethod
    def _render(self):
        pass


class MenuButton(Button):
    def __init__(self,
                 window: Window,
                 pos: tuple[int, int],
                 dimensions: tuple[int, int],
                 tag: str,
                 action: int,
                 border: int = 0,
                 radius: int = -1):
        super().__init__(window, pos, dimensions, tag, action, border, radius)
        self.font = pygame.Font("assets/fonts/Oswald.ttf", 110)
        self.color = pygame.Color(255, 255, 255)
        self.color_hover = pygame.Color(255, 228, 54)
        self.text = self.font.render(self.tag, True, self.color)

    def _render(self) -> int:
        pygame.draw.rect(self.surface,
                         self.color,
                         self.rect,
                         self.border,
                         self.radius)
        center_text = ((self.rect.width - self.text.get_width()) / 2,
                       (self.rect.height - self.text.get_height()) / 2)
        self.text = self.font.render(self.tag, True, self.color)
        self.surface.blit(self.text, (self.pos[0] + center_text[0],
                                      self.pos[1] + center_text[1]))
        return self._collide()

    def _collide(self) -> int:
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            self.clickable = True
            pygame.mouse.set_cursor(self.clickable_cursor)
            pygame.Surface.fill(self.surface, self.color_hover, self.rect, pygame.BLEND_MIN)
            pygame.Surface.fill(self.text, self.color_hover, special_flags=pygame.BLEND_MIN | pygame.BLEND_MULT)
            if pygame.MOUSEBUTTONUP in [event.type for event in pygame.event.get()]:
                print(self.action)

        elif self.clickable is True:
            self.clickable = False
            pygame.mouse.set_cursor(self.arrow_cursor)

        return 0
