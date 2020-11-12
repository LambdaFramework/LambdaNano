#!/bin/python
import os, sys

base=os.environ['NANOAODTOOLS_BASE']

from PhysicsTools.NanoAODTools.LambPlot.plotConfiguration.WH_SS.Full2017nanov6.cuts import cuts
from PhysicsTools.NanoAODTools.LambPlot.plotConfiguration.WH_SS.Full2017nanov6.variables import variables
from multiprocessing import Process

def run_unblind( base , ivar , cut , iyear ):
    os.system( 'python %s/python/LambPlot/scripts/whss.py -v %s -r %s -y %s --unblind' %( base , ivar , cut , iyear ) )
    pass

def run_blind( base , ivar , cut , iyear ):
    os.system( 'python %s/python/LambPlot/scripts/whss.py -v %s -r %s -y %s' %( base , ivar , cut , iyear ) )
    pass

'''
variables = {
    'nominal' : [ 'mlljj20_whss_bin4' ],
    'ugo' : [ 'MinMjjl' , 'MinMjl' ] ,
    'invest' : [ "mll" , "pt1" , "pt2" , "nJet" , "MinMjjl" , "Ele1_dz" , "Mu2_dz" , "Ele1_dxy" , "Mu2_dxy" , "Ele1_pfRelIso03_all" , "Mu2_pfRelIso03_all" , "Ele1_pfRelIso04_all" , "Mu2_pfRelIso04_all" ]
}

regions = {
    'nominal' : [ 'hww2l2v_13TeV_of2j_WH_SS_eu_2j' ], #, 'hww2l2v_13TeV_of2j_WH_SS_eu_2j' , 'hww2l2v_13TeV_of2j_WH_SS_uu_1j' , 'hww2l2v_13TeV_of2j_WH_SS_uu_2j' ],
    'ugo' : [ 'SSmumu_ugo_2jets' ] #, 'SSmumu_ugo_2jets_iso' , 'SSmumu_ugo_2jets_iso_ip' ]
}

variable_ = variables['nominal']
regions_ = regions['nominal']
'''
isblind = True
iyear = '2017'
procs =[]
for ivar in [
        'Ele1_sip3d',
        'Ele2_sip3d',
        'Mu1_sip3d',
        'Mu2_sip3d',
        'puppimet',
        'detall',
        'mth',
        'dphill',
        'ptll',
        'mtw1',
        'mtw2',
        'dphilljet',
        #'dphilljetjet',
        'dphilmet',
        'dphillmet',
        'dphilep1jet1',
        'dphilep1jet2',
        'dphilep2jet1',
        'dphilep2jet2',
        'dphijjmet',
        'ht'
] :
    for iregion in cuts :
        if isblind: proc = Process(target=run_blind, args=(base , ivar , iregion , iyear))
        else:  proc = Process(target=run_unblind, args=(base , ivar , iregion , iyear))
        procs.append(proc) ; proc.start()
            
[ r.join() for r in procs  ]


