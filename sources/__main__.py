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

from .parser import read_map
from .visualizer import start_vizualizer

object = read_map()
start_vizualizer()
