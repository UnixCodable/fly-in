# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#   views.py                                            :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#   By: lbordana <lbordana@student.42mulhouse.fr>   +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#   Created: 2026/06/25 09:07:21 by lbordana           #+#    #+#             #
#   Updated: 2026/07/06 03:32:14 by lbordana          ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

import sys
from time import sleep, time
import pygame as pg

import sources.components.algorithms.a_star_backup
from sources.components.algorithms.a_star_backup import start_algorithm

from ...parser import GlobalParser, read_map
from typing import Optional, Union
from pyvidplayer2 import Video
from abc import ABC, abstractmethod
from sources.components.gui.buttons import (Action,
                                            ButtonListMapSelection,
                                            ButtonListMenu,
                                            ButtonListSettings,
                                            ViewAction)
from sources.components.tools.scales import scale_text, scale_pos, scale_size
from sources.visualizer import Window


class View(ABC):
    running = True

    @abstractmethod
    def _get_events(self):
        pass

    @abstractmethod
    def launch(self) -> None:
        pass

    def _render_text(self,
                     path: str,
                     text: str,
                     scaled_text: int,
                     scaled_pos: tuple[int, int],
                     color: pg.Color = pg.Color(255, 255, 255)):

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

    def launch(self) -> None:
        self.video.resize(Window.surface.get_size())
        while True:
            if self.video.frame == self.end_frame:
                break
            self._get_events()
            self.video.draw(Window.surface, (0, 0))
            pg.display.update()
        self.video.stop()


class MenuView(View):
    def _get_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type in [action.value for action in ViewAction]:
                pg.event.post(event)
                self.running = False

    def launch(self) -> None:
        self.buttons = ButtonListMenu()
        self.running = True
        pg.mixer.Channel(0).play(pg.mixer.Sound("assets/sound/menu.wav"), 1000)
        while self.running:
            Window.animated_background()
            Window.animated_drone()
            self._render_text(
                "assets/fonts/Starjhol.ttf",
                "Fly in",
                scale_text(0.06),
                scale_pos(0.385, 0.03)
            )
            self._render_text(
                "assets/fonts/Oswald.ttf",
                "Made with force by Lucas Bordanave, from 42 Mulhouse",
                scale_text(0.018),
                scale_pos(0.313, 0.92)
            )
            self.buttons.menu_button_play.render()
            self.buttons.menu_button_settings.render()
            self.buttons.menu_button_exit.render()
            self._get_events()
            pg.display.update()


class SettingsView(View):
    def _get_events(self) -> None:
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
                res_list = Window.data["res_list"]
                res_index = Window.data["res_index"]
                try:
                    new = res_list[res_index + 1]
                    Window.rewrite({"res_index": res_index + 1,
                                    "resolution": new})
                except IndexError:
                    new = Window.data["res_list"][0]
                    Window.rewrite({"res_index": 0, "resolution": new})
                self.buttons.update()
            if event.type == Action.PLUS_RES.value:
                res_list = Window.data["res_list"]
                res_index = Window.data["res_index"]
                if Window.data["res_index"] != 0:
                    new = res_list[res_index - 1]
                    Window.rewrite({"res_index": res_index - 1,
                                    "resolution": new})
                else:
                    new = res_list[len(res_list) - 1]
                    Window.rewrite({"res_index": len(res_list) - 1,
                                    "resolution": new})
                self.buttons.update()
            if event.type == Action.FULLSCREEN_BOOL.value:
                if Window.data["mode"] == "fullscreen":
                    Window.rewrite({"mode": "windowed"})
                else:
                    Window.rewrite({"mode": "fullscreen"})
                self.buttons.update()

    def launch(self) -> None:
        self.buttons = ButtonListSettings()
        self.running = True
        while self.running:
            Window.animated_background()
            Window.animated_drone()
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
                scale_pos(0.105, 0.52)
            )
            self._render_text(
                "assets/fonts/Starjhol.ttf",
                "fullscreen ",
                scale_text(0.015),
                scale_pos(0.23, 0.285)
            )
            if Window.data["mode"] == "fullscreen":
                self.buttons.settings_button_fullscreen_on.render()
            else:
                self.buttons.settings_button_fullscreen_off.render()
            self.buttons.settings_button_minus_res.render()
            self.buttons.settings_button_plus_res.render()
            self.buttons.settings_button_minus_sound.render()
            self.buttons.settings_button_plus_sound.render()
            self.buttons.settings_button_back.render()
            self._get_events()
            pg.display.update()


class MapSelectionView(View):
    def __init__(self) -> None:
        self.preview: Optional[Union[str, GlobalParser]] = None
        self.p_start = 0.54

    def _get_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type in [action.value for action in ViewAction]:
                if event.type == ViewAction.PREVIEW_GAME.value:
                    self.preview = read_map(event.path)
                elif event.type == ViewAction.GAME.value:
                    pg.event.post(pg.Event(event.type,
                                           {"objects": self.preview}))
                    self.running = False
                else:
                    pg.event.post(event)
                    self.running = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    self.preview = None
            if event.type == Action.SCROLL_DOWN.value:
                self.buttons.setter_scroll(0.03)
                self.buttons.update()
            if event.type == Action.SCROLL_UP.value:
                self.buttons.setter_scroll(-0.03)
                self.buttons.update()
            if event.type == Action.SCROLL_VIS_LEFT.value:
                self.p_start -= 0.02
            if event.type == Action.SCROLL_VIS_RIGHT.value:
                self.p_start += 0.02
            if event.type == Action.SCROLL_VIS_RESET.value:
                self.p_start = 0.54

    def _read_preview(self) -> None:
        viewer = pg.Rect(scale_pos(0.51, 0.12), scale_size(0.41, 0.2))
        pop_up = pg.Rect(scale_pos(0.5, 0.1), scale_size(0.43, 0.30))
        pg.draw.rect(Window.surface, (255, 228, 54), pop_up, 0, 10)
        pg.draw.rect(Window.surface, (12, 14, 45), viewer, 0, 10)
        if self.preview is None:
            return
        if isinstance(self.preview, str):
            self._render_text(
                "assets/fonts/Oswald.ttf",
                self.preview,
                scale_text(0.013),
                scale_pos(0.515, 0.51),
                pg.Color(235, 33, 46)
            )
            return

        self._render_text(
            "assets/fonts/Oswald.ttf",
            f"Number of drones : {self.preview.total_drone}",
            scale_text(0.015),
            scale_pos(0.52, 0.49),
            pg.Color(0, 0, 0)
        )
        self._render_text(
            "assets/fonts/Oswald.ttf",
            f"Number of hubs : {len(self.preview.hubs)}",
            scale_text(0.015),
            scale_pos(0.52, 0.53),
            pg.Color(0, 0, 0)
        )
        self._render_text(
            "assets/fonts/Oswald.ttf",
            f"Number of connections : {len(self.preview.connections)}",
            scale_text(0.015),
            scale_pos(0.52, 0.57),
            pg.Color(0, 0, 0)
        )

        for hub in self.preview.hubs:
            preview_scale = scale_pos(self.p_start + (hub.coordinates[0] / 30),
                                      0.3 + (hub.coordinates[1] / 30))
            if viewer.collidepoint(preview_scale):
                try:
                    pg.draw.circle(Window.surface,
                                   hub.color,
                                   preview_scale,
                                   scale_text(0.007))
                except ValueError:
                    pg.draw.circle(Window.surface,
                                   "white",
                                   preview_scale,
                                   scale_text(0.007))

        for connection in self.preview.connections:
            zone_1 = self.preview.get_hub(connection.first_zone)
            zone_1_pos = scale_pos(self.p_start + (zone_1.coordinates[0] / 30),
                                   0.3 + (zone_1.coordinates[1] / 30))
            zone_2 = self.preview.get_hub(connection.second_zone)
            zone_2_pos = scale_pos(self.p_start + (zone_2.coordinates[0] / 30),
                                   0.3 + (zone_2.coordinates[1] / 30))
            if (viewer.collidepoint(zone_1_pos)
                    and viewer.collidepoint(zone_2_pos)):
                pg.draw.line(Window.surface, "grey", zone_1_pos, zone_2_pos, 3)

        self.buttons.play_button.render()
        self.buttons.visualizer_right_button.render()
        self.buttons.visualizer_left_button.render()
        self.buttons.visualizer_reset_button.render()

    def launch(self) -> None:
        self.buttons = ButtonListMapSelection()
        self.running = True
        while self.running:
            Window.animated_background()
            Window.animated_drone()
            Window.surface.set_clip(
                pg.Rect(scale_pos(0.1, 0.1), scale_size(0.38, 0.45)))
            for map in self.buttons.mapselections_buttons_maps:
                map.render()
            clip = Window.surface.get_clip()
            pg.draw.rect(Window.surface, (255, 228, 54), clip, 10, 20)
            Window.surface.set_clip(None)
            self.buttons.settings_button_back.render()
            if self.preview is not None:
                self._read_preview()
            self._get_events()
            pg.display.update()


class Game(View):
    def __init__(self):
        self.object = None
        self.p_x = 0.1
        self.p_y = 0.46
        self.moving_up = False
        self.moving_left = False
        self.moving_right = False
        self.moving_down = False

    def _get_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type in [action.value for action in ViewAction]:
                pg.event.post(event)
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.moving_left = True
                if event.key == pg.K_UP or event.key == pg.K_w:
                    self.moving_up = True
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.moving_right = True
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.moving_down = True
                if event.key == pg.K_ESCAPE:
                    pg.event.post(pg.Event(ViewAction.MENU.value))
                    self.running = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.moving_left = False
                if event.key == pg.K_UP or event.key == pg.K_w:
                    self.moving_up = False
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.moving_right = False
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.moving_down = False

    def _read_movements(self):
        line_number = 0
        with open("output.txt", "w") as file:
            pass

        start_algorithm(self.object)

        with open("output.txt", "r") as file:
            lines = file.readlines()
            while True:
                line = lines[line_number].strip().split()
                if line_number < len(lines) - 1:
                    line_number += 1
                yield [li.split("-") for li in line]

    def launch(self) -> None:

        self.running = True
        last_time = 0
        turn = self._read_movements()

        while self.running:
            Window.animated_background()

            if self.moving_up is True:
                self.p_y -= 0.01
            if self.moving_left is True:
                self.p_x -= 0.01
            if self.moving_down is True:
                self.p_y += 0.01
            if self.moving_right is True:
                self.p_x += 0.01

            for connection in self.object.connections:
                zone_1 = self.object.get_hub(connection.first_zone)
                zone_2 = self.object.get_hub(connection.second_zone)
                zone_1_pos = scale_pos(self.p_x + (zone_1.coordinates[0] / 6),
                                       self.p_y + (zone_1.coordinates[1] / 6))
                zone_2_pos = scale_pos(self.p_x + (zone_2.coordinates[0] / 6),
                                       self.p_y + (zone_2.coordinates[1] / 6))
                pg.draw.line(Window.surface, "grey", zone_1_pos, zone_2_pos, 6)

            for hub in self.object.hubs:
                game_pos = scale_pos(self.p_x + (hub.coordinates[0] / 6),
                                     self.p_y + (hub.coordinates[1] / 6))

                try:
                    pg.draw.circle(Window.surface,
                                   hub.color,
                                   game_pos,
                                   scale_text(0.04))

                except ValueError:
                    pg.draw.circle(Window.surface,
                                   "white",
                                   game_pos,
                                   scale_text(0.04))

            if time() > last_time + 1.2:
                drones = next(turn)
                last_time = time()
            for drone in drones:
                hub = self.object.get_hub(drone[1])
                drone_pos = scale_pos(self.p_x + (hub.coordinates[0] / 6),
                                      self.p_y + (hub.coordinates[1] / 6))

                pg.draw.circle(Window.surface,
                               "white",
                               drone_pos,
                               scale_text(0.02))

            self._get_events()
            pg.display.update()

    def set_object(self, object: GlobalParser) -> None:
        self.object = object
