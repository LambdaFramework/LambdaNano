#!/bin/bash

time python scripts/skimmer.py -d 2 -y 2017 -o "Cf_skimmed" -p "Lepton_pt[0]>12 && Lepton_pt[1]>12 && ( Lepton_pdgId[0]*Lepton_pdgId[1] == 11*13 ) && ( nLepton==2 || ( nLepton>=3 && Lepton_pt[2]<10 ) ) && abs(mll-91.2)<15"
time python scripts/skimmer.py -d 1 -y 2017 -o "Cf_skimmed" -p "Lepton_pt[0]>12 && Lepton_pt[1]>12 && ( Lepton_pdgId[0]*Lepton_pdgId[1] == 11*13 ) && ( nLepton==2 || ( nLepton>=3 && Lepton_pt[2]<10 ) ) && abs(mll-91.2)<15"
