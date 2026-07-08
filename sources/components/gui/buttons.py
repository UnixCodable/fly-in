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
import os

from enum import Enum
from abc import ABC, abstractmethod
from sources.visualizer import Window
from sources.components.tools.scales import scale_size, scale_pos, scale_text


class Action(Enum):
    SCROLL_VIS_RESET = pg.event.custom_type()
    SCROLL_VIS_RIGHT = pg.event.custom_type()
    SCROLL_VIS_LEFT = pg.event.custom_type()
    FULLSCREEN_BOOL = pg.event.custom_type()
    SCROLL_DOWN = pg.event.custom_type()
    MINUS_SOUND = pg.event.custom_type()
    PLUS_SOUND = pg.event.custom_type()
    SCROLL_UP = pg.event.custom_type()
    MINUS_RES = pg.event.custom_type()
    PLUS_RES = pg.event.custom_type()


class ViewAction(Enum):
    MAP_SELECTION = pg.event.custom_type()
    PREVIEW_GAME = pg.event.custom_type()
    SETTINGS = pg.event.custom_type()
    MENU = pg.event.custom_type()
    GAME = pg.event.custom_type()
    EXIT = pg.event.custom_type()


class Button(ABC):
    def __init__(self,
                 pos: tuple[int, int],
                 tag: str,
                 dimensions: tuple[int, int],
                 action: Enum) -> None:

        self.pos = pos
        self.tag = tag
        self.action = action
        self.clickable = False

        self.rect = pg.Rect(pos, dimensions)
        self.arrow_cursor = pg.Cursor(pg.SYSTEM_CURSOR_ARROW)
        self.clickable_cursor = pg.Cursor(pg.SYSTEM_CURSOR_HAND)
        self.sound = pg.mixer.Sound("assets/sound/button.mp3")

    @abstractmethod
    def render(self) -> None:
        pass


class MenuButton(Button):
    def __init__(self,
                 pos: tuple[int, int],
                 tag: str,
                 action: Enum) -> None:

        super().__init__(pos, tag, scale_size(0.15, 0.05), action)

        self.color = pg.Color(255, 255, 255)
        self.color_hover = pg.Color(255, 228, 54)
        self.font = pg.font.Font("assets/fonts/Starjhol.ttf", scale_text(0.025))

    def render(self) -> None:

        self.text = self.font.render(self.tag, True, self.color)
        center_text = ((self.rect.width - self.text.get_width()) / 2,
                       (self.rect.height - self.text.get_height()) / 2 * 0.6)

        pg.draw.rect(Window.surface, self.color, self.rect, 6, 10)
        Window.surface.blit(self.text, (self.pos[0] + center_text[0],
                            self.pos[1] + center_text[1]))

        self._collide()

    def _collide(self) -> None:

        mouse = pg.mouse.get_pos()

        if self.rect.collidepoint(mouse):

            if self.clickable is False:
                pg.mixer.Channel(1).play(self.sound)

            self.clickable = True
            pg.mouse.set_cursor(self.clickable_cursor)
            pg.Surface.fill(
                Window.surface, self.color_hover, self.rect, pg.BLEND_MIN)
            pg.Surface.fill(
                self.text, self.color_hover, special_flags=pg.BLEND_MIN)

            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        pg.event.post(pg.event.Event(self.action.value))
                        pg.mouse.set_cursor(self.arrow_cursor)

        elif self.clickable is True:
            self.clickable = False
            pg.mouse.set_cursor(self.arrow_cursor)


class SquareButton(Button):

    def __init__(self, pos: tuple[int, int], tag: str, action: Enum) -> None:

        super().__init__(pos, tag, scale_size(0.02, 0.02), action)

        self.font = pg.font.Font("assets/fonts/Oswald.ttf", scale_text(0.015))
        self.color = pg.Color(255, 255, 255)
        self.color_hover = pg.Color(255, 228, 54)

    def render(self) -> None:

        self.text = self.font.render(self.tag, True, self.color)
        center_text = ((self.rect.width - self.text.get_width()) / 2,
                       (self.rect.height - self.text.get_height()) / 2 * 0.6)

        pg.draw.rect(Window.surface, self.color, self.rect, 6, 10)
        Window.surface.blit(self.text, (self.pos[0] + center_text[0],
                            self.pos[1] + center_text[1]))

        self._collide()

    def _collide(self) -> None:
        mouse = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse):

            if self.clickable is False:
                pg.mixer.Channel(1).play(self.sound)
            self.clickable = True
            pg.mouse.set_cursor(self.clickable_cursor)
            pg.Surface.fill(
                Window.surface, self.color_hover, self.rect, pg.BLEND_MIN)
            pg.Surface.fill(
                self.text, self.color_hover, special_flags=pg.BLEND_MIN)

            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        pg.event.post(pg.event.Event(self.action.value))

        elif self.clickable is True:
            self.clickable = False
            pg.mouse.set_cursor(self.arrow_cursor)


class MapSelectionButton(Button):
    def __init__(self,
                 pos: tuple[int, int],
                 tag: str,
                 path: str,
                 action: Enum) -> None:

        super().__init__(pos, tag, scale_size(0.36, 0.07), action)

        self.path_tag = path
        self.color = pg.Color(255, 255, 255)
        self.color_hover = pg.Color(255, 228, 54)
        self.title_font = pg.font.Font("assets/fonts/Oswald.ttf", scale_text(0.02))
        self.path_font = pg.font.Font("assets/fonts/Oswald.ttf", scale_text(0.015))

    def render(self) -> None:

        self.title = self.title_font.render(self.tag, True, self.color)
        self.path = self.path_font.render(self.path_tag, True, self.color)

        pg.draw.rect(Window.surface, self.color, self.rect, 6, 10)
        pos_title = (self.pos[0] + (self.rect.width * 0.05),
                     self.pos[1] + (self.rect.height * 0.05))
        pos_path = (self.pos[0] + (self.rect.width * 0.05),
                    self.pos[1] + (self.rect.height * 0.4))

        Window.surface.blit(self.title, pos_title)
        Window.surface.blit(self.path, pos_path)

        self._collide()

    def _collide(self) -> None:

        mouse = pg.mouse.get_pos()

        if Window.surface.get_clip().collidepoint(mouse):

            for event in pg.event.get(pg.MOUSEWHEEL):
                if event.y < 0:
                    pg.event.post(pg.event.Event(Action.SCROLL_DOWN.value))
                if event.y > 0:
                    pg.event.post(pg.event.Event(Action.SCROLL_UP.value))

            if self.rect.collidepoint(mouse):

                if self.clickable is False:
                    pg.mixer.Channel(1).play(self.sound)

                self.clickable = True
                pg.mouse.set_cursor(self.clickable_cursor)
                pg.Surface.fill(
                    Window.surface, self.color_hover, self.rect, pg.BLEND_MIN)
                pg.Surface.fill(
                    self.title, self.color_hover, special_flags=pg.BLEND_MIN)
                pg.Surface.fill(
                    self.path, self.color_hover, special_flags=pg.BLEND_MIN)

                for event in pg.event.get(pg.MOUSEBUTTONUP):
                    if event.button == 1:
                        pg.event.post(pg.event.Event(self.action.value,
                                               {"path": self.path_tag}))

            elif self.clickable is True:
                self.clickable = False
                pg.mouse.set_cursor(self.arrow_cursor)


class MapPlayButton(Button):

    def __init__(self, pos: tuple[int, int], tag: str, action: Enum) -> None:

        super().__init__(pos, tag, scale_size(0.15, 0.05), action)

        self.color = pg.Color(0, 0, 0)
        self.color_hover = pg.Color(235, 33, 46)
        self.font = pg.font.Font("assets/fonts/Starjhol.ttf", scale_text(0.025))

    def render(self) -> None:

        self.text = self.font.render(self.tag, True, self.color)
        center_text = ((self.rect.width - self.text.get_width()) / 2,
                       (self.rect.height - self.text.get_height()) / 2 * 0.6)

        pg.draw.rect(Window.surface, self.color, self.rect, 6, 10)
        Window.surface.blit(self.text, (self.pos[0] + center_text[0],
                            self.pos[1] + center_text[1]))

        self._collide()

    def _collide(self) -> None:

        mouse = pg.mouse.get_pos()

        if self.rect.collidepoint(mouse):

            if self.clickable is False:
                pg.mixer.Channel(1).play(self.sound)

            self.clickable = True
            pg.mouse.set_cursor(self.clickable_cursor)
            pg.Surface.fill(
                Window.surface, self.color_hover, self.rect, pg.BLEND_ADD)
            pg.Surface.fill(
                self.text, self.color_hover, special_flags=pg.BLEND_ADD)

            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        pg.event.post(pg.event.Event(self.action.value))
                        pg.mouse.set_cursor(self.arrow_cursor)

        elif self.clickable is True:
            self.clickable = False
            pg.mouse.set_cursor(self.arrow_cursor)


class ButtonList(ABC):

    @abstractmethod
    def update(self) -> None:
        pass


class ButtonListMenu(ButtonList):
    def __init__(self) -> None:
        self.update()

    def update(self) -> None:
        self.menu_button_play = MenuButton(
            scale_pos(0.2, 0.33), "Play", ViewAction.MAP_SELECTION)

        self.menu_button_settings = MenuButton(
            scale_pos(0.2, 0.46), "Settings", ViewAction.SETTINGS)

        self.menu_button_exit = MenuButton(
            scale_pos(0.2, 0.59), "Exit", ViewAction.EXIT)


class ButtonListSettings(ButtonList):
    def __init__(self) -> None:
        self.update()

    def update(self) -> None:
        self.settings_button_fullscreen_on = SquareButton(
            scale_pos(0.355, 0.29), "x", Action.FULLSCREEN_BOOL)

        self.settings_button_fullscreen_off = SquareButton(
            scale_pos(0.355, 0.29), " ", Action.FULLSCREEN_BOOL)

        self.settings_button_minus_res = SquareButton(
            scale_pos(0.2, 0.41), "<", Action.MINUS_RES)

        self.settings_button_minus_sound = SquareButton(
            scale_pos(0.2, 0.53), "-", Action.MINUS_SOUND)

        self.settings_button_plus_res = SquareButton(
            scale_pos(0.3985, 0.41), ">", Action.PLUS_RES)

        self.settings_button_plus_sound = SquareButton(
            scale_pos(0.3985, 0.53), "+", Action.PLUS_SOUND)

        self.settings_button_back = MenuButton(
            scale_pos(0.2, 0.65), "Back", ViewAction.MENU)


class ButtonListMapSelection(ButtonList):
    def __init__(self) -> None:
        self._scroll = 0
        self.update()

    def setter_scroll(self, value) -> None:
        if self._scroll + value < 0:
            self._scroll = 0
        else:
            self._scroll += value

    def update(self) -> None:
        line_gap = 0.11 - self._scroll

        self.mapselections_buttons_maps = []

        for file in os.walk("assets/maps", False):
            for f in file[2]:
                if len(f) >= 5 and f[-4:] == ".txt":
                    self.mapselections_buttons_maps.append(
                        MapSelectionButton(
                            scale_pos(0.11, line_gap),
                            f[:-4], file[0]+"/"+f, ViewAction.PREVIEW_GAME)
                        )
                    line_gap += 0.14

        self.settings_button_back = MenuButton(
            scale_pos(0.635, 0.82), "Back", ViewAction.MENU)

        self.play_button = MapPlayButton(
            scale_pos(0.75, 0.5), "Play", ViewAction.GAME)

        self.visualizer_left_button = SquareButton(
            scale_pos(0.515, 0.43), "<", Action.SCROLL_VIS_RIGHT)

        self.visualizer_right_button = SquareButton(
            scale_pos(0.895, 0.43), ">", Action.SCROLL_VIS_LEFT)

        self.visualizer_reset_button = SquareButton(
            scale_pos(0.697, 0.43), "-", Action.SCROLL_VIS_RESET)
