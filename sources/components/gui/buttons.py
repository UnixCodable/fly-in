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

import pygame as pg

from enum import Enum
from abc import ABC, abstractmethod
from typing import Self
from sources.visualizer import Window
from sources.components.tools.scales import scale_size, scale_pos, scale_text


class Action(Enum):
    FULLSCREEN_BOOL = pg.event.custom_type()
    MINUS_RES = pg.event.custom_type()
    MINUS_SOUND = pg.event.custom_type()
    PLUS_RES = pg.event.custom_type()
    PLUS_SOUND = pg.event.custom_type()


class ViewAction(Enum):
    MENU = pg.event.custom_type()
    MAP_SELECTION = pg.event.custom_type()
    GAME = pg.event.custom_type()
    SETTINGS = pg.event.custom_type()
    EXIT = pg.event.custom_type()


class Button(ABC):
    def __init__(self, pos: tuple[int, int], tag: str,
                 dimensions: tuple[int, int], action: Enum):
        self.pos = pos
        self.tag = tag
        self.action = action
        self.clickable = False
        self.rect = pg.Rect(pos, dimensions)
        self.arrow_cursor = pg.Cursor(pg.SYSTEM_CURSOR_ARROW)
        self.clickable_cursor = pg.Cursor(pg.SYSTEM_CURSOR_HAND)
        self.sound = pg.mixer.Sound("assets/sound/button.mp3")

    @abstractmethod
    def render(self):
        pass


class MenuButton(Button):
    def __init__(self, pos: tuple[int, int], tag: str, action: Enum):
        super().__init__(pos, tag, scale_size(0.15, 0.05), action)
        self.font = pg.Font("assets/fonts/Starjhol.ttf", scale_text(0.025))
        self.color = pg.Color(255, 255, 255)
        self.color_hover = pg.Color(255, 228, 54)

    def render(self):
        self.text = self.font.render(self.tag, True, self.color)
        center_text = ((self.rect.width - self.text.get_width()) / 2,
                       (self.rect.height - self.text.get_height()) / 2 * 0.6)
        pg.draw.rect(Window.surface, self.color, self.rect, 6, 10)
        Window.surface.blit(self.text, (self.pos[0] + center_text[0],
                            self.pos[1] + center_text[1]))
        self._collide()

    def _collide(self):
        mouse = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            if self.clickable is False:
                pg.mixer.Channel(1).play(self.sound)
            self.clickable = True
            pg.mouse.set_cursor(self.clickable_cursor)
            pg.Surface.fill(Window.surface, self.color_hover, self.rect, pg.BLEND_MIN)
            pg.Surface.fill(self.text, self.color_hover, special_flags=pg.BLEND_MIN)

            if pg.MOUSEBUTTONUP in [event.type for event in pg.event.get()]:
                pg.event.post(pg.Event(self.action.value))
                pg.mouse.set_cursor(self.arrow_cursor)

        elif self.clickable is True:
            self.clickable = False
            pg.mouse.set_cursor(self.arrow_cursor)


class SquareButton(Button):
    def __init__(self, pos: tuple[int, int], tag: str, action: Enum):
        super().__init__(pos, tag, scale_size(0.02, 0.02), action)
        self.font = pg.Font("assets/fonts/Oswald.ttf", scale_text(0.015))
        self.color = pg.Color(255, 255, 255)
        self.color_hover = pg.Color(255, 228, 54)

    def render(self):
        self.text = self.font.render(self.tag, True, self.color)
        center_text = ((self.rect.width - self.text.get_width()) / 2,
                       (self.rect.height - self.text.get_height()) / 2 * 0.6)
        pg.draw.rect(Window.surface, self.color, self.rect, 6, 10)
        Window.surface.blit(self.text, (self.pos[0] + center_text[0],
                            self.pos[1] + center_text[1]))
        self._collide()

    def _collide(self):
        mouse = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse):

            if self.clickable is False:
                pg.mixer.Channel(1).play(self.sound)
            self.clickable = True
            pg.mouse.set_cursor(self.clickable_cursor)
            pg.Surface.fill(Window.surface, self.color_hover, self.rect, pg.BLEND_MIN)
            pg.Surface.fill(self.text, self.color_hover, special_flags=pg.BLEND_MIN)

            if pg.MOUSEBUTTONUP in [event.type for event in pg.event.get()]:
                pg.event.post(pg.Event(self.action.value))

        elif self.clickable is True:
            self.clickable = False
            pg.mouse.set_cursor(self.arrow_cursor)


class ButtonList(ABC):

    @abstractmethod
    def update(self):
        pass


class ButtonListMenu(ButtonList):
    def __init__(self):
        self.update()

    def update(self):
        self._menu_button_play = MenuButton(
            scale_pos(0.2, 0.33), "Play", ViewAction.MAP_SELECTION)

        self._menu_button_settings = MenuButton(
            scale_pos(0.2, 0.45), "Settings", ViewAction.SETTINGS)

        self._menu_button_exit = MenuButton(
            scale_pos(0.2, 0.57), "Exit", ViewAction.EXIT)


class ButtonListSettings(ButtonList):
    def __init__(self):
        self.update()

    def update(self):
        self._settings_button_minus_res = SquareButton(
            scale_pos(0.2, 0.41), "<", Action.MINUS_RES)

        self._settings_button_minus_sound = SquareButton(
            scale_pos(0.2, 0.53), "-", Action.MINUS_SOUND)

        self._settings_button_plus_res = SquareButton(
            scale_pos(0.3985, 0.41), ">", Action.PLUS_RES)

        self._settings_button_plus_sound = SquareButton(
            scale_pos(0.3985, 0.53), "+", Action.PLUS_SOUND)

        self._settings_button_back = MenuButton(
            scale_pos(0.2, 0.65), "Back", ViewAction.MENU)


class ButtonListMapSelection(ButtonList):
    def __init__(self):
        self.update()

    def update(self):
        self._mapselection_button_back = MenuButton(
            scale_pos(0.2, 0.57), "Back", ViewAction.MENU)
