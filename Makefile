# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  Makefile                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/02 08:09:16 by lbordana        #+#    #+#               #
#  Updated: 2026/06/02 12:39:55 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

install:
	uv sync

run:
	uv run /sources/main.py

debug:
	echo "wip"

clean:
	rm -rf sources/__pycache__/
	rm -rf sources/.mypy_cache/

lint:
	python3 -m flake8 .
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	python3 -m flake8 .
	python3 -m mypy . --strict