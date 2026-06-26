# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  view_objects.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/25 09:07:21 by lbordana        #+#    #+#               #
#  Updated: 2026/06/26 04:16:34 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import ABC, abstractmethod
from typing import Optional
from pyvidplayer2 import Video
from sources.visualizer import Window, SURFACE, WIN_WIDTH, WIN_HEIGHT
from sources.components.gui_objects import Action, MenuButton
import sys
import pygame as pg


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
        img = pg.transform.scale(img, SURFACE.get_size())
        SURFACE.blit(img, coord)

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
        self.video.resize(SURFACE.get_size())
        while True:
            if self.video.frame == self.end_frame:
                break
            self._get_events()
            self.video.draw(SURFACE, (0, 0))
            pg.display.update()
        self.video.stop()
        return 0


class MenuView(View):

    def _get_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type in [action.value for action in Action]:
                pg.event.post(event)
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    if Window.data["resolution"] == [4096, 2304]:
                        Window._rewrite({"resolution": [1920, 1080]})
                    elif Window.data["resolution"] == [1920, 1080]:
                        Window._rewrite({"resolution": [4096, 2304]})

    def _launch(self):
        self.running = True
        pg.mixer.Channel(0).play(pg.mixer.Sound("assets/sound/menu.wav"), 1000)
        play = MenuButton((int(WIN_WIDTH * 0.2), int(WIN_HEIGHT * 0.33)),
                          (WIN_WIDTH * 0.1, WIN_WIDTH * 0.05), "Play", Action.MAP_SELECTION, 6, 10)
        settings = MenuButton((int(WIN_WIDTH * 0.2), int(WIN_HEIGHT * 0.45)),
                              (WIN_WIDTH * 0.1, WIN_WIDTH * 0.05), "Settings", Action.SETTINGS, 6, 10)
        exit = MenuButton((int(WIN_WIDTH * 0.2), int(WIN_HEIGHT * 0.57)),
                          (WIN_WIDTH * 0.1, WIN_WIDTH * 0.05), "Exit", Action.EXIT, 6, 10)
        while self.running:
            self._render_image("assets/gui/menu_background.png")
            play._render()
            settings._render()
            exit._render()
            self._get_events()
            pg.display.update()


class SettingsView(View):
    def _get_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type in [action.value for action in Action]:
                pg.event.post(event)
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    if Window.data["resolution"] == [4096, 2304]:
                        Window._rewrite({"resolution": [1920, 1080]})
                    elif Window.data["resolution"] == [1920, 1080]:
                        Window._rewrite({"resolution": [4096, 2304]})

    def _launch(self):
        self.running = True
        back = MenuButton((int(WIN_WIDTH * 0.2), int(WIN_HEIGHT * 0.33)),
                          (450, 200), "Back", Action.MENU, 6, 10)
        while self.running:
            self._render_image("assets/gui/menu_background.png")
            back._render()
            self._get_events()
            pg.display.update()


class MapSelectionView(View):
    def _get_events(self):
        pass

    def _launch(self):
        pass
