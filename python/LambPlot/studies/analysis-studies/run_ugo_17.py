#!/bin/python
import os, sys
from PhysicsTools.NanoAODTools.LambPlot.plotConfiguration.WH_SS.Full2017nanov6.variables import variables
from PhysicsTools.NanoAODTools.LambPlot.plotConfiguration.WH_SS.Full2017nanov6.cuts import cuts

base=os.environ['NANOAODTOOLS_BASE']

iyear="2017"
    
#OSemu-showoff
#cut="OSemu-showoff"
#for ivar in [ "mll" , "pt1" , "pt2" , "nJet" , "MinMjjl" , "Ele1_dz" , "Mu2_dz" , "Ele1_dxy" , "Mu2_dxy" , "Ele1_pfRelIso03_all" , "Mu2_pfRelIso03_all" , "Ele1_pfRelIso04_all" , "Mu2_pfRelIso04_all" ]:
#    os.system( 'python %s/python/LambPlot/scripts/whss.py -v %s -r %s -y %s --unblind' %( base , ivar , cut , iyear ) )
#cut="OSee"
#for ivar in [ "Ele1_dz" , "Ele2_dz" , "Ele1_dxy" , "Ele2_dxy" , "Ele1_pfRelIso03_all" , "Ele2_pfRelIso03_all" , "mll" , "pt1" , "pt2" , "nJet" , "MinMjjl" ]:
#    os.system( 'python %s/python/LambPlot/scripts/whss.py -v %s -r %s -y %s --unblind' %( base , ivar , cut , iyear ) )
#cut="OSmumu"
#for ivar in [ "Mu1_dz" , "Mu2_dz" , "Mu1_dxy" , "Mu2_dxy" , "Mu1_pfRelIso03_all" , "Mu2_pfRelIso03_all" , "mll" , "pt1" , "pt2" , "nJet" , "MinMjjl" ]:
#for ivar in [ "Mu1_pfRelIso04_all" ]: #"Mu1_dz" , "Mu1_dxy" , "Mu1_pfRelIso03_all" ,  "mll" ]:
#    os.system( 'python %s/python/LambPlot/scripts/whss.py -v %s -r %s -y %s --unblind' %( base , ivar , cut , iyear ) )

#SSmumu ugo
#cut='SSmumu_ugo'
cut='OSee'
for ivar in [ "mll" , "pt1" , "pt2" , "nJet" , "MinMjjl" , "Mu1_dz" , "Mu2_dz" , "Mu1_dxy" , "Mu2_dxy" , "Mu1_pfRelIso03_all" , "Mu2_pfRelIso03_all" ]:
    if ivar!= 'MinMjjl': continue
    os.system( 'python %s/python/LambPlot/scripts/whss.py -v %s -r %s -y %s --unblind' %( base , ivar , cut , iyear ) )

#SSee
#cut='SSee_ugo'
#for ivar in [ "mll" , "pt1" , "pt2" , "nJet" , "MinMjjl" , "Ele1_dz" , "Ele2_dz" , "Ele1_dxy" , "Ele2_dxy" , "Ele1_pfRelIso03_all" , "Ele2_pfRelIso03_all" ]:
#    os.system( 'python %s/python/LambPlot/scripts/whss.py -v %s -r %s -y %s --unblind' %( base , ivar , cut , iyear ) )
