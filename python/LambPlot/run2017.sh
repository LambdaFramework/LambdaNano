#!/bin/bash

for ireg in OSee #OSmumu OSemu OSemu-showoff
do
    for ivar in mll #ht pt1 pt2
    do
	echo "Running on region $ireg on $ivar"
	python analyses/whss.py -v $ivar -r $ireg -y 2017
    done
done
