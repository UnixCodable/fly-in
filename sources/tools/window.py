# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#   window.py                                           :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#   By: lbordana <lbordana@student.42mulhouse.fr>   +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#   Created: 2026/06/27 02:24:00 by lbordana           #+#    #+#             #
#   Updated: 2026/07/01 13:40:30 by lbordana          ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

import pygame as pg
from sources.tools.settings import Settings

pg.init()
pg.display.set_caption("Fly-in : Echoes of the galaxy")


class Window():
    settings = Settings()
    background_pos_y = 0
    drone_pos_y = 0
    drone_up = False
    data = settings._get_settings()
    width, height = data["resolution"]
    pg.mixer.Channel(0).set_volume(data['sound'] / 10)
    pg.mixer.Channel(1).set_volume(data['sound'] / 10)
    if data["mode"] == "fullscreen":
        surface = pg.display.set_mode((width, height), pg.FULLSCREEN)
    else:
        surface = pg.display.set_mode((width, height))

    @classmethod
    def rewrite(cls, new_config: dict, reload_surface: bool = True) -> None:
        cls.settings._set_settings(new_config)
        cls.data = cls.settings._get_settings()
        cls.width, cls.height = cls.data["resolution"]
        pg.mixer.Channel(0).set_volume(cls.data['sound'] / 10)
        pg.mixer.Channel(1).set_volume(cls.data['sound'] / 10)
        if reload_surface is True:
            if cls.data["mode"] == "fullscreen":
                cls.surface = pg.display.set_mode((cls.width, cls.height),
                                                  pg.FULLSCREEN)
            else:
                cls.surface = pg.display.set_mode((cls.width, cls.height))

    @classmethod
    def animated_background(cls) -> None:
        cls.surface.blit(cls.stars, (cls.background_pos_y, 0))
        cls.surface.blit(cls.stars, (cls.height + cls.background_pos_y, 0))
        if cls.background_pos_y <= -cls.height:
            cls.background_pos_y = 0
        else:
            cls.background_pos_y -= 2

    @classmethod
    def animated_drone(cls) -> None:
        cls.surface.blit(cls.drone,
                         (cls.width * 0.5, cls.height * 0.3 + cls.drone_pos_y))
        if cls.drone_up is False:
            cls.drone_pos_y -= cls.drone.get_height() * .0005
            if cls.drone_pos_y <= -int(cls.drone.get_height() * 0.025):
                cls.drone_up = True
        elif cls.drone_up is True:
            cls.drone_pos_y += cls.drone.get_height() * .0005
            if cls.drone_pos_y >= int(cls.drone.get_height() * 0.025):
                cls.drone_up = False

    @classmethod
    def load_assets(cls) -> None:
        cls.stars = pg.image.load("assets/gui/background.png").convert()
        cls.stars = pg.transform.smoothscale(cls.stars, cls.surface.get_size())
        cls.drone = pg.image.load("assets/gui/drone.png").convert_alpha()
        cls.drone = pg.transform.smoothscale(
            cls.drone,
            ((cls.drone.get_width() * cls.width) / 3840,
             (cls.drone.get_height() * cls.height) / 2160))
