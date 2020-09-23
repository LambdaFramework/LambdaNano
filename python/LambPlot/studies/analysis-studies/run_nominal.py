#!/bin/python
import os, sys
from PhysicsTools.NanoAODTools.LambPlot.plotConfiguration.WH_SS.Full2016nanov6.variables import variables
from PhysicsTools.NanoAODTools.LambPlot.plotConfiguration.WH_SS.Full2016nanov6.cuts import cuts

base=os.environ['NANOAODTOOLS_BASE']

iyear="2016"
    
cut="hww2l2v_13TeV_of2j_WH_SS_eu_2j"
for ivar in [ "mll" , "pt1" , "pt2" , "nJet" , "mlljj20_whss_bin2" , "Ele1_dz" , "Mu2_dz" , "Ele1_dxy" , "Mu2_dxy" , "Ele1_pfRelIso03_all" , "Mu2_pfRelIso03_all" , "Ele1_pfRelIso04_all" , "Mu2_pfRelIso04_all" ]:
    os.system( 'python %s/python/LambPlot/scripts/whss.py -v %s -r %s -y %s --unblind' %( base , ivar , cut , iyear ) )
cut="hww2l2v_13TeV_of2j_WH_SS_eu_1j"
for ivar in [ "mll" , "pt1" , "pt2" , "nJet" , "mlljj20_whss_bin2" , "Ele1_dz" , "Mu2_dz" , "Ele1_dxy" , "Mu2_dxy" , "Ele1_pfRelIso03_all" , "Mu2_pfRelIso03_all" , "Ele1_pfRelIso04_all" , "Mu2_pfRelIso04_all" ]:
    os.system( 'python %s/python/LambPlot/scripts/whss.py -v %s -r %s -y %s --unblind' %( base , ivar , cut , iyear ) )
cut="hww2l2v_13TeV_of2j_WH_SS_uu_2j"
for ivar in [ "mll" , "pt1" , "pt2" , "nJet" , "mlljj20_whss_bin2" , "Mu1_dz" , "Mu2_dz" , "Mu1_dxy" , "Mu2_dxy" , "Mu1_pfRelIso03_all" , "Mu2_pfRelIso03_all" ]:
    os.system( 'python %s/python/LambPlot/scripts/whss.py -v %s -r %s -y %s --unblind' %( base , ivar , cut , iyear ) )
cut='hww2l2v_13TeV_of2j_WH_SS_uu_1j'
for ivar in [ "mll" , "pt1" , "pt2" , "nJet" , "mlljj20_whss_bin2" , "Mu1_dz" , "Mu2_dz" , "Mu1_dxy" , "Mu2_dxy" , "Mu1_pfRelIso03_all" , "Mu2_pfRelIso03_all" ]:
    os.system( 'python %s/python/LambPlot/scripts/whss.py -v %s -r %s -y %s --unblind' %( base , ivar , cut , iyear ) )
