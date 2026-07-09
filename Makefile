# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  Makefile                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: lbordana <lbordana@student.42mulhouse.f   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/02 08:09:16 by lbordana        #+#    #+#               #
#  Updated: 2026/07/09 13:46:35 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

install:
	uv sync

run:
	uv run python3 -m sources.fly_in

run_no_cache:
	uv run python3 -m sources.fly_in
	make clean_cache

debug:
	echo "wip"

clean:
	rm -rf sources/__pycache__/
	rm -rf sources/.mypy_cache/

clean_cache:
	rm -rf */__pycache__ */*/__pycache__ */*/*/__pycache__

lint:
	python3 -m flake8 . --exclude=.venv/*
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	python3 -m flake8 . --exclude=.venv/*
	python3 -m mypy . --strict