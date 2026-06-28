# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  views.py                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/25 09:07:21 by lbordana        #+#    #+#               #
#  Updated: 2026/06/28 04:23:38 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys
import pygame as pg

from typing import Optional
from pyvidplayer2 import Video
from abc import ABC, abstractmethod
from sources.components.gui.buttons import Action, ButtonListMapSelection, ButtonListMenu, ButtonListSettings, ViewAction
from sources.components.tools.scales import scale_text, scale_pos, scale_size
from sources.visualizer import Window


class View(ABC):
    running = True

    @abstractmethod
    def _get_events(self):
        pass

    @abstractmethod
    def launch(self) -> int:
        pass

    def _render_image(self, path: str, coord: tuple[int, int] = (0, 0)):
        img = pg.image.load(path).convert()
        img = pg.transform.scale(img, Window.surface.get_size())
        Window.surface.blit(img, coord)

    def _render_text(self, path: str, text: str, scaled_text: tuple[int, int],
                     scaled_pos: tuple[int, int], color: pg.Color = (255, 255, 255)):
        font = pg.Font(path, scaled_text)
        text = font.render(text,  True, color)
        Window.surface.blit(text, scaled_pos)


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

    def launch(self) -> int:
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

    def launch(self):
        self.buttons = ButtonListMenu()
        self.running = True
        pg.mixer.Channel(0).play(pg.mixer.Sound("assets/sound/menu.wav"), 1000)
        while self.running:
            self._render_image("assets/gui/menu_background.png")
            self.buttons._menu_button_play.render()
            self.buttons._menu_button_settings.render()
            self.buttons._menu_button_exit.render()
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
            if event.type == Action.MINUS_SOUND.value:
                if Window.data['sound'] > 0:
                    Window.rewrite({"sound": Window.data['sound'] - 1}, False)
            if event.type == Action.PLUS_SOUND.value:
                if Window.data['sound'] < 10:
                    Window.rewrite({"sound": Window.data['sound'] + 1}, False)
            if event.type == Action.MINUS_RES.value:
                try:
                    new = Window.data["res_list"][Window.data["res_index"] + 1]
                    Window.rewrite({"res_index": Window.data["res_index"] + 1,
                                    "resolution": new})
                except IndexError:
                    new = Window.data["res_list"][0]
                    Window.rewrite({"res_index": 0, "resolution": new})
                self.buttons.update()
            if event.type == Action.PLUS_RES.value:
                if Window.data["res_index"] != 0:
                    new = Window.data["res_list"][Window.data["res_index"] - 1]
                    Window.rewrite({"res_index": Window.data["res_index"] - 1,
                                    "resolution": new})
                else:
                    new = Window.data["res_list"][len(Window.data["res_list"]) - 1]
                    Window.rewrite({"res_index": len(Window.data["res_list"]) - 1,
                                    "resolution": new})
                self.buttons.update()
            
    def launch(self):
        self.buttons = ButtonListSettings()
        self.running = True
        while self.running:
            self._render_image("assets/gui/menu_background.png")
            self._render_text(
                "assets/fonts/Starjhol.ttf",
                "+" * Window.data['sound'],
                scale_text(0.025),
                scale_pos(0.219, 0.518)
            )
            self._render_text(
                "assets/fonts/Starjhol.ttf",
                str(Window.data['resolution'])[1:-1].replace(',', ' x'),
                scale_text(0.015),
                scale_pos(0.26, 0.403)
            )
            self._render_text(
                "assets/fonts/Starjhol.ttf",
                "resolution :",
                scale_text(0.015),
                scale_pos(0.06, 0.403)
            )
            self._render_text(
                "assets/fonts/Starjhol.ttf",
                "sound :",
                scale_text(0.015),
                scale_pos(0.105, 0.518)
            )
            self._render_text(
                "assets/fonts/Starjhol.ttf",
                "fullscreen :",
                scale_text(0.015),
                scale_pos(0.06, 0.288)
            )
            self.buttons._settings_button_minus_res.render()
            self.buttons._settings_button_plus_res.render()
            self.buttons._settings_button_minus_sound.render()
            self.buttons._settings_button_plus_sound.render()
            self.buttons._settings_button_back.render()
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

    def launch(self):
        self.buttons = ButtonListMapSelection()
        self.running = True
        while self.running:
            self.render_image("assets/gui/menu_background.png")
            self.buttons._mapselection_button_back.render()
            self._get_events()
            pg.display.update()
