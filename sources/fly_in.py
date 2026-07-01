# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#   main.py                                             :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#   By: lbordana <lbordana@student.42mulhouse.fr>   +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#   Created: 2026/06/02 10:40:23 by lbordana           #+#    #+#             #
#   Updated: 2026/06/17 00:11:30 by lbordana          ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

from .visualizer import Visualizer
from .parser import read_map
from .components.algorithms.a_star import start_algorithm

if __name__ == "__main__":
    visualizer = Visualizer()
    visualizer.start()
    start_algorithm(read_map("assets/maps/challenger/01_the_impossible_dream.txt"))
