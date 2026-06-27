# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  window.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/27 02:24:00 by lbordana        #+#    #+#               #
#  Updated: 2026/06/27 02:24:44 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pygame as pg
from sources.settings import Settings

pg.init()
pg.display.set_caption("Fly-in : Echoes of the galaxy")


class Window():
    settings = Settings()
    data = settings._get_settings()
    width, height = data["resolution"]
    if data["mode"] == "fullscreen":
        surface = pg.display.set_mode((width, height), pg.FULLSCREEN)
    else:
        surface = pg.display.set_mode((width, height))

    @classmethod
    def _rewrite(cls, new_config: dict):
        cls.settings._set_settings(new_config)
        cls.data = cls.settings._get_settings()
        cls.width, cls.height = cls.data["resolution"]
        if cls.data["mode"] == "fullscreen":
            cls.surface = pg.display.set_mode((cls.width, cls.height),
                                              pg.FULLSCREEN)
        else:
            cls.surface = pg.display.set_mode((cls.width, cls.height))