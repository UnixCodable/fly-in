# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  settings.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/24 05:48:29 by lbordana        #+#    #+#               #
#  Updated: 2026/06/24 11:58:38 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import json
import pygame
from typing import Any


class Settings():
    def _get_settings(self) -> dict:
        screen = [mode for mode in pygame.display.list_modes()
                  if int(mode[1] * (16/9)) == mode[0]]
        try:
            with open("settings.json", "x") as file:
                print('Creating settings file...')
                self.__data = {"resolution": (screen[0][0], screen[0][1]),
                               "mode": "windowed",
                               "sound": 10}
                json.dump(self.__data, file)

        except FileExistsError:
            with open("settings.json", "r") as file:
                print("Reading settings...")
                self.__data = json.load(file)

        return self.__data

    def _set_settings(self, new_config: dict[str, Any]) -> None:
        with open("settings.json", "w") as file:
            print('Rewriting settings file...')
            self.__data.update(new_config)
            json.dump(self.__data, file)
