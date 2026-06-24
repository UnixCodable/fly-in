# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  settings.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/24 05:48:29 by lbordana        #+#    #+#               #
#  Updated: 2026/06/24 08:36:32 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import json
import pygame


def get_settings() -> dict:
    screen = pygame.display.Info()
    data = {}
    try:
        with open("settings.json", "x") as file:
            print('Creating settings file...')
            data = {"resolution": (screen.current_w, screen.current_h),
                    "mode": "windowed",
                    "sound": 10}
            json.dump(data, file)

    except FileExistsError:
        with open("settings.json", "r") as file:
            print("Reading settings...")
            data = json.load(file)

    return data
