# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#   visualizer.py                                       :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#   By: lbordana <lbordana@student.42mulhouse.fr>   +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#   Created: 2026/06/16 23:54:23 by lbordana           #+#    #+#             #
#   Updated: 2026/06/17 00:23:08 by lbordana          ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

import pygame
import moviepy.editor


def start_vizualizer():
    pygame.init()

    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Fly-in : Echoes of the galaxy")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
