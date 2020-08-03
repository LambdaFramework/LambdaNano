#!/bin/bash

#for var in C_deltaPhill C_deltaRll C_deltaEtall Lepton_pt[0] Lepton_pt[1] Lepton_eta[0] Lepton_eta[1] nMu nEle CleanJet_pt[0] CleanJet_pt[1] CleanJet_pt[2] C_deltaPhijj C_deltaRjj C_deltaEtajj mtw1 mtw2 dphilmet1 dphilmet2 Vll_pt Vll_mass Vll_eta Vl2JJ_pt Vl2JJ_mass Vl2JJ_eta Vjj_pt Vjj_eta Vjj_mass C_Vllmass C_Vjjmass C_Vllpt C_Vjjpt
#do
#    echo "Plotting $var"
#    python lambPlot.py $var -c hist -s -l
#done

for region in SSemu SSmue SSee SSmumu
do
    echo $region
    #python lambPlot.py Vl2JJ_mass -c $region -B
    python lambPlot.py -u -c $region
done