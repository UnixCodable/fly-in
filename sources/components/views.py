# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  views.py                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/25 09:07:21 by lbordana        #+#    #+#               #
#  Updated: 2026/06/27 03:54:44 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys
import pygame as pg

from typing import Optional
from pyvidplayer2 import Video
from abc import ABC, abstractmethod
from sources.components.buttons import ButtonListMapSelection, ButtonListMenu, ButtonListSettings, ViewAction
from sources.components.scales import Scale
from sources.visualizer import Window


class View(ABC):
    running = True

    @abstractmethod
    def _get_events(self):
        pass

    @abstractmethod
    def _launch(self) -> int:
        pass

    def _render_image(self, path: str, coord: tuple[int, int] = (0, 0)):
        img = pg.image.load(path).convert()
        img = pg.transform.scale(img, Window.surface.get_size())
        Window.surface.blit(img, coord)

    def _render_button(self):
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
        self.end_frame = end_frame if end_frame else 0

    def _get_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.video.stop()
                pg.quit()
                sys.exit(0)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.video.set_speed(1)
                    if self.end_frame > 0:
                        self.video.seek_frame(self.end_frame - 2)
                    else:
                        self.video.seek_frame(self.video.frame_count - 2)

    def _launch(self) -> int:
        self.video.resize(Window.surface.get_size())
        while True:
            if self.video.frame == self.end_frame:
                break
            self._get_events()
            self.video.draw(Window.surface, (0, 0))
            pg.display.update()
        self.video.stop()
        return 0


class MenuView(View):
    def _get_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type in [action.value for action in ViewAction]:
                pg.event.post(event)
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    if Window.data["resolution"] == [4096, 2304]:
                        Window._rewrite({"resolution": [1920, 1080]})
                    elif Window.data["resolution"] == [1920, 1080]:
                        Window._rewrite({"resolution": [4096, 2304]})
                    self.buttons._update()
                    print(Scale().menu_button)

    def _launch(self):
        self.buttons = ButtonListMenu()
        self.running = True
        pg.mixer.Channel(0).play(pg.mixer.Sound("assets/sound/menu.wav"), 1000)
        while self.running:
            self._render_image("assets/gui/menu_background.png")
            self.buttons._menu_button_play._render()
            self.buttons._menu_button_settings._render()
            self.buttons._menu_button_exit._render()
            self._get_events()
            pg.display.update()


class SettingsView(View):
    def _get_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type in [action.value for action in ViewAction]:
                pg.event.post(event)
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    if Window.data["resolution"] == [4096, 2304]:
                        Window._rewrite({"resolution": [1920, 1080]})
                    elif Window.data["resolution"] == [1920, 1080]:
                        Window._rewrite({"resolution": [4096, 2304]})
                    self.buttons._update()

    def _launch(self):
        self.buttons = ButtonListSettings()
        self.running = True
        while self.running:
            self._render_image("assets/gui/menu_background.png")
            self.buttons._settings_button_minus_res._render()
            self.buttons._settings_button_plus_res._render()
            self.buttons._settings_button_minus_sound._render()
            self.buttons._settings_button_plus_sound._render()
            self.buttons._settings_button_back._render()
            self._get_events()
            pg.display.update()


class MapSelectionView(View):
    def _get_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type in [action.value for action in ViewAction]:
                pg.event.post(event)
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    if Window.data["resolution"] == [4096, 2304]:
                        Window._rewrite({"resolution": [1920, 1080]})
                    elif Window.data["resolution"] == [1920, 1080]:
                        Window._rewrite({"resolution": [4096, 2304]})
                    self.buttons._update()

    def _launch(self):
        self.buttons = ButtonListMapSelection()
        self.running = True
        while self.running:
            self._render_image("assets/gui/menu_background.png")
            self.buttons._mapselection_button_back._render()
            self._get_events()
            pg.display.update()
