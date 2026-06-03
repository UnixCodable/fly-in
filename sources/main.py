# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/02 10:40:23 by lbordana        #+#    #+#               #
#  Updated: 2026/06/02 11:07:58 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from config_parser import read_map, LineParser

object = LineParser(lines=read_map())
