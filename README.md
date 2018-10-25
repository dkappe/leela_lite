# leela_lite

Very simple PUCT to experiment with leela networks in Python.

## Quickstart

- setup a python virtual environment with python3
- clone the mcts branch of https://github.com/dkappe/lczero_tools/tree/mcts
- install so you can edit `pip -e install .`
- run leela_lite with weights file and number of nodes: `python leela_lite.py weights_9149.txt.gz 200` (for example)

## What it needs

- Non hacky clone of LeelaBoard so it doesn't run so darn slow
- UCI interface
- TBD
