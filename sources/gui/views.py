# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#   views.py                                            :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#   By: lbordana <lbordana@student.42mulhouse.fr>   +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#   Created: 2026/06/25 09:07:21 by lbordana           #+#    #+#             #
#   Updated: 2026/07/06 20:08:54 by lbordana          ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

import re
from sqlite3 import connect
import sys
from time import time
import pygame as pg

from sources.game.algorithm import Algorithm
from sources.game.map_objects import Connection, Drone, Hub

from ..tools.parser import GlobalParser, read_map
from typing import Optional, Union
from pyvidplayer2 import Video
from abc import ABC, abstractmethod
from sources.gui.buttons import (Action,
                                 ButtonListMapSelection,
                                 ButtonListMenu,
                                 ButtonListSettings,
                                 ViewAction)
from sources.tools.scales import scale_text, scale_pos, scale_size
from sources.tools.window import Window


class RenderText():
    def __init__(self,
                 path: str,
                 text: str,
                 scaled_text: int,
                 color: pg.Color = pg.Color(255, 255, 255)):
        self.path = path
        self.text = text
        self.scaled_text = scaled_text
        self.color = color

        self.font = pg.font.Font(path, scaled_text)
        self.render = self.font.render(self.text,  True, color)

    def blit(self, scaled_pos: tuple[int, int], new_text: str = None, new_size: int = None):
        if new_size is not None:
            self.font = pg.font.Font(self.path, new_size)
            self.render = self.font.render(self.text, True, self.color)
    
        if new_text is not None and new_text != self.text:
            self.text = new_text
            self.render = self.font.render(self.text, True, self.color)

        Window.surface.blit(self.render, scaled_pos)


class View(ABC):
    running = True

    @abstractmethod
    def _get_events(self):
        pass

    @abstractmethod
    def launch(self) -> None:
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
        title = RenderText(
                    "assets/fonts/Starjhol.ttf",
                    "Fly in",
                    scale_text(0.06)
                )
        footer = RenderText(
                    "assets/fonts/Oswald.ttf",
                    "Made with force by Lucas Bordanave, from 42 Mulhouse",
                    scale_text(0.018)
                )

        pg.mixer.Channel(0).play(pg.mixer.Sound("assets/sound/menu.wav"), 1000)
        while self.running:
            Window.animated_background()
            Window.animated_drone()
            title.blit(scale_pos(0.385, 0.03))
            footer.blit(scale_pos(0.313, 0.92))
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
        sound_indicator = RenderText(
                        "assets/fonts/Starjhol.ttf",
                        "+" * Window.data['sound'],
                        scale_text(0.025)
                    )
        resolution_current = RenderText(
                        "assets/fonts/Starjhol.ttf",
                        str(Window.data['resolution'])[1:-1].replace(',', ' x'),
                        scale_text(0.015),
                    )
        resolution_title = RenderText(
                        "assets/fonts/Starjhol.ttf",
                        "resolution :",
                        scale_text(0.015)
                    )
        sound_title = RenderText(
                        "assets/fonts/Starjhol.ttf",
                        "sound :",
                        scale_text(0.015)
                    )
        fullscreen_title = RenderText(
                        "assets/fonts/Starjhol.ttf",
                        "fullscreen ",
                        scale_text(0.015)
                    )
        while self.running:
            Window.animated_background()
            Window.animated_drone()
            sound_indicator.blit(scale_pos(0.219, 0.518), "+" * Window.data['sound'], scale_text(0.025))
            resolution_title.blit(scale_pos(0.06, 0.403), new_size=scale_text(0.015))
            resolution_current.blit(scale_pos(0.26, 0.403), str(Window.data['resolution'])[1:-1].replace(',', ' x'), scale_text(0.015))
            sound_title.blit(scale_pos(0.105, 0.52), new_size=scale_text(0.015))
            fullscreen_title.blit(scale_pos(0.23, 0.285), new_size=scale_text(0.015))
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
                    pg.event.post(pg.event.Event(
                        event.type, {"objects": self.preview}))
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
            RenderText(
                "assets/fonts/Oswald.ttf",
                self.preview,
                scale_text(0.013),
                pg.Color(235, 33, 46)
            ).blit(scale_pos(0.515, 0.51))
            return

        RenderText(
            "assets/fonts/Oswald.ttf",
            f"Number of drones : {self.preview.total_drone}",
            scale_text(0.015),
            pg.Color(0, 0, 0)
        ).blit(scale_pos(0.52, 0.49))
        RenderText(
            "assets/fonts/Oswald.ttf",
            f"Number of hubs : {len(self.preview.hubs)}",
            scale_text(0.015),
            pg.Color(0, 0, 0)
        ).blit(scale_pos(0.52, 0.53))
        RenderText(
            "assets/fonts/Oswald.ttf",
            f"Number of connections : {len(self.preview.connections)}",
            scale_text(0.015),
            pg.Color(0, 0, 0)
        ).blit(scale_pos(0.52, 0.57))

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
                    pg.event.post(pg.event.Event(ViewAction.MENU.value))
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

    def _get_drones(self):
        drones = []
        start_hub = self.object.get_start_hub()
        for nb in range(self.object.total_drone):
            drones.append(Drone(f"D{nb}", start_hub))
            start_hub.add_occupant(drones[-1].id)
        return drones

    def _execute_turns(self):
        algorithm = Algorithm(self.object)
        end_hub = self.object.get_end_hub()
        active_connection = []
        restricted_drone = []
        turn = 0

        while True:
            self.drones = sorted(self.drones, key=lambda x: x.distance, reverse=True)
            if len([d for d in self.drones if d.is_running() is True]) != 0:
                turn += 1
                print(f"\nTurn {turn} : ")
            for drone in self.drones:
                if drone.is_running() is False:
                    continue

                if drone in restricted_drone:
                    pos = drone.get_next_pos()
                    # if pos is not None:
                    print(f"{drone.id}-{pos.name}", end=" ")
                    connection = self.object.get_connection(drone.get_current_pos(),
                                                            drone.get_next_pos())
                    restricted_drone.pop(restricted_drone.index(drone))
                    active_connection.pop(active_connection.index(connection))
                    drone.set_next_pos()
                    drone.get_current_pos().remove_occupant(drone.id)
                    drone.set_current_pos(pos)
                    continue
                elif drone.get_next_pos() is None:
                    pos = algorithm.run(drone)
                    drone.set_next_pos(pos)
                else:
                    pos = drone.get_next_pos()

                connection = self.object.get_connection(drone.get_current_pos(),
                                                        drone.get_next_pos())
                if connection is None:
                    pg.quit
                    sys.exit(1)
                if len(pos.occupants) < pos.max_drones or pos == end_hub:

                    if pos.zone == "restricted":
                        restricted_drone.append(drone)
                        active_connection.append(connection)
                        print(f"{drone.id}-{connection.first_zone}-{connection.second_zone}", end=" ")
                    else:
                        print(f"{drone.id}-{pos.name}", end=" ")
                        drone.set_next_pos()
                        drone.get_current_pos().remove_occupant(drone.id)
                        drone.set_current_pos(pos)

                    pos.add_occupant(drone.id)
                    connection.set_passages(1)

            for connection in self.object.connections:
                if connection not in active_connection:
                    connection.reset_passages()

            yield

    def launch(self) -> None:

        self.running = True
        self.drones: list[Drone] = self._get_drones()
        self.p_x = 0.1
        self.p_y = 0.46
        # initialized = False
        turns = self._execute_turns()
        last_time = 0.0

        # drone_asset = pg.image.load("assets/gui/drone_top.png").convert_alpha()
        # drone_asset = pg.transform.smoothscale(drone_asset,
        #                                        scale_size(0.04, 0.04))
        initialised_text = False
        hub_names_text = []
        hub_zones_text = []
        hub_occupation_text = []
        connection_passages_text = []
        drone_id_text = []

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

            for index, connection in enumerate(self.object.connections):
                zone_1 = self.object.get_hub(connection.first_zone)
                zone_2 = self.object.get_hub(connection.second_zone)
                zone_1_pos = scale_pos(self.p_x + (zone_1.coordinates[0] / 6),
                                       self.p_y + (zone_1.coordinates[1] / 6))
                zone_2_pos = scale_pos(self.p_x + (zone_2.coordinates[0] / 6),
                                       self.p_y + (zone_2.coordinates[1] / 6))
                pg.draw.line(Window.surface, "grey", zone_1_pos, zone_2_pos, 6)
                if initialised_text is False:
                    connection_passages_text.append(RenderText("assets/fonts/Oswald.ttf", str(connection.get_passages()) + "/" + str(connection.max_link), scale_text(.01), "white"))
                connection_passages_text[index].blit((zone_1_pos[0] + int((zone_2_pos[0] - zone_1_pos[0]) / 2), zone_1_pos[1] + int((zone_2_pos[1] - zone_1_pos[1]) / 2)), str(connection.get_passages()) + "/" + str(connection.max_link))

            for index, hub in enumerate(self.object.hubs):
                game_pos = scale_pos(self.p_x + (hub.coordinates[0] / 6),
                                     self.p_y + (hub.coordinates[1] / 6))
                if hub.color in pg.color.THECOLORS.keys():
                    color = hub.color
                else:
                    color = "wheat"

                pg.draw.circle(Window.surface,
                               color,
                               game_pos,
                               scale_text(0.04), 20)
                pg.draw.circle(Window.surface,
                               "wheat",
                               game_pos,
                               scale_text(0.035))
                if initialised_text is False:
                    hub_names_text.append(RenderText("assets/fonts/Oswald.ttf", hub.name, scale_text(.01), "black"))
                    hub_zones_text.append(RenderText("assets/fonts/Oswald.ttf", hub.zone, scale_text(.01), "black"))
                    hub_occupation_text.append(RenderText("assets/fonts/Oswald.ttf", str(len(hub.occupants)) + "/" + str(hub.max_drones), scale_text(.01), "white"))
                hub_names_text[index].blit((game_pos[0] - scale_text(0.02), game_pos[1] - scale_text(0.017)), hub.name)
                hub_zones_text[index].blit((game_pos[0] - scale_text(0.02), game_pos[1] - scale_text(0.002)), hub.zone)
                hub_occupation_text[index].blit((game_pos[0] - scale_text(0.02), game_pos[1] - scale_text(-0.036)), str(len(hub.occupants)) + "/" + str(hub.max_drones))

            if time() > (last_time + .3):
                try:
                    next(turns)
                except StopIteration:
                    pass
                last_time = time()
            for index, drone in enumerate(self.drones):
                hub = drone.get_current_pos()
                drone_pos = scale_pos(self.p_x + (hub.coordinates[0] / 6),
                                      self.p_y + (hub.coordinates[1] / 6))

                pg.draw.circle(Window.surface,
                               "white",
                               drone_pos,
                               scale_text(0.03))
                if initialised_text is False:
                    drone_id_text.append(RenderText("assets/fonts/Oswald.ttf", drone.id, scale_text(.02), "darkred"))
                drone_id_text[index].blit((drone_pos[0] - scale_text(0.02), drone_pos[1] - scale_text(0.017)), drone.id)

            self._get_events()
            pg.display.update()
            initialised_text = True

    def set_object(self, object: GlobalParser) -> None:
        self.object = object
