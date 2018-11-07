#!/bin/bash

DIR="/home/dkappe/work/src/leela_lite"

. ~/envs/lcztools/bin/activate

cd $DIR
exec python engine.py weights_9149.txt.gz 800 minimax
