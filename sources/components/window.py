# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  window.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/27 02:24:00 by lbordana        #+#    #+#               #
#  Updated: 2026/06/29 01:18:46 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pygame as pg
from sources.settings import Settings

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
    def rewrite(cls, new_config: dict, reload_surface: bool = True):
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
    def animated_background(cls):
        stars = pg.image.load("assets/gui/background.png").convert()
        stars = pg.transform.scale(stars, cls.surface.get_size())
        cls.surface.blit(stars, (0, cls.background_pos_y))
        cls.surface.blit(stars, (0, cls.height + cls.background_pos_y))
        if cls.background_pos_y <= -cls.height:
            cls.background_pos_y = 0
        else:
            cls.background_pos_y -= 2

    @classmethod
    def animated_drone(cls):
        drone = pg.image.load("assets/gui/drone.png").convert_alpha()
        drone = pg.transform.scale(drone, ((drone.width * cls.width) / 3840,
                                           (drone.height * cls.height) / 2160))
        cls.surface.blit(drone, (cls.width * 0.5, cls.height * 0.3 + cls.drone_pos_y))
        if cls.drone_up is False:
            cls.drone_pos_y -= 1
            if cls.drone_pos_y <= -int(drone.height * 0.025):
                cls.drone_up = True
        elif cls.drone_up is True:
            cls.drone_pos_y += 1
            if cls.drone_pos_y >= int(drone.height * 0.025):
                cls.drone_up = False
