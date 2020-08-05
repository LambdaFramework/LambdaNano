#!/bin/bash

for ireg in SSmumu #OSee OSmumu OSemu OSemu-showoff
do
    for ivar in Mu1_dz Mu2_dz Mu1_dxy Mu2_dxy Mu1_sip3d Mu2_sip3d #mll ht pt1 pt2
    do
	echo "Running on region $ireg on $ivar"
	python analyses/whss.py -v $ivar -r $ireg -y 2016
    done
done
