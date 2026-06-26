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
from sources.visualizer import SURFACE, WIN_WIDTH
from enum import Enum
import pygame as pg


class Action(Enum):
    MENU = pg.event.custom_type()
    MAP_SELECTION = pg.event.custom_type()
    GAME = pg.event.custom_type()
    SETTINGS = pg.event.custom_type()
    EXIT = pg.event.custom_type()


class Button(ABC):
    def __init__(self,
                 pos: tuple[int, int],
                 dimensions: tuple[int, int],
                 tag: str,
                 action: Enum,
                 border: int = 0,
                 radius: int = -1):
        self.pos = pos
        self.tag = tag
        self.border = border
        self.radius = radius
        self.action = action
        self.clickable = False
        self.rect = pg.Rect(pos, dimensions)
        self.clickable_cursor = pg.Cursor(pg.SYSTEM_CURSOR_HAND)
        self.arrow_cursor = pg.Cursor(pg.SYSTEM_CURSOR_ARROW)
        self.sound = pg.mixer.Sound("assets/sound/button.mp3")

    @abstractmethod
    def _render(self):
        pass


class MenuButton(Button):
    def __init__(self,
                 pos: tuple[int, int],
                 dimensions: tuple[int, int],
                 tag: str,
                 action: Enum,
                 border: int = 0,
                 radius: int = -1):
        super().__init__(pos, dimensions, tag, action, border, radius)
        self.font = pg.Font("assets/fonts/Oswald.ttf", int(WIN_WIDTH * 0.025))
        self.color = pg.Color(255, 255, 255)
        self.color_hover = pg.Color(255, 228, 54)
        self.text = self.font.render(self.tag, True, self.color)

    def _render(self) -> int:
        pg.draw.rect(SURFACE,
                     self.color,
                     self.rect,
                     self.border,
                     self.radius)
        center_text = ((self.rect.width - self.text.get_width()) / 2,
                       (self.rect.height - self.text.get_height()) / 2)
        self.text = self.font.render(self.tag, True, self.color)
        SURFACE.blit(self.text, (self.pos[0] + center_text[0],
                                 self.pos[1] + center_text[1]))
        return self._collide()

    def _collide(self) -> int:
        mouse = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            if self.clickable is False:
                pg.mixer.Channel(1).play(self.sound)
            self.clickable = True
            pg.mouse.set_cursor(self.clickable_cursor)
            pg.Surface.fill(SURFACE, self.color_hover, self.rect, pg.BLEND_MIN)
            pg.Surface.fill(self.text, self.color_hover, special_flags=pg.BLEND_MIN)
            if pg.MOUSEBUTTONUP in [event.type for event in pg.event.get()]:
                pg.event.post(pg.Event(self.action.value))

        elif self.clickable is True:
            self.clickable = False
            pg.mouse.set_cursor(self.arrow_cursor)

        return 0
