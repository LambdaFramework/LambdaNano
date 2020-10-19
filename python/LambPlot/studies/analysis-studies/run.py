#!/bin/python
import os, sys

base=os.environ['NANOAODTOOLS_BASE']


from multiprocessing import Process

def run_unblind( base , ivar , cut , iyear ):
    os.system( 'python %s/python/LambPlot/scripts/whss.py -v %s -r %s -y %s --unblind' %( base , ivar , cut , iyear ) )
    pass

def run_blind( base , ivar , cut , iyear ):
    os.system( 'python %s/python/LambPlot/scripts/whss.py -v %s -r %s -y %s' %( base , ivar , cut , iyear ) )
    pass


variables = {
    'nominal' : [ 'eta1' , 'eta2' , 'pt1' , 'pt2' , 'mll' ],
    'ugo' : [ 'MinMjjl' , 'MinMjl' , 'mlljj20_whss_bin4' ] ,
    'invest' : [ "mll" , "pt1" , "pt2" , "nJet" , "MinMjjl" , "Ele1_dz" , "Mu2_dz" , "Ele1_dxy" , "Mu2_dxy" , "Ele1_pfRelIso03_all" , "Mu2_pfRelIso03_all" , "Ele1_pfRelIso04_all" , "Mu2_pfRelIso04_all" ]
}

regions = {
    'nominal' : [ 'SS_ee' ], #'hww2l2v_13TeV_of2j_WH_SS_ee_1j' ], #'hww2l2v_13TeV_of2j_WH_SS_ee_1j' ] , #'hww2l2v_13TeV_of2j_WH_SS_eu_1j' ] , #'hww2l2v_13TeV_of2j_WH_SS_eu_2j' ], #, 'hww2l2v_13TeV_of2j_WH_SS_eu_2j' , 'hww2l2v_13TeV_of2j_WH_SS_uu_1j' , 'hww2l2v_13TeV_of2j_WH_SS_uu_2j' ],
    'ugo' : [ 'SSmumu_ugo_2jets' ] #, 'SSmumu_ugo_2jets_iso' , 'SSmumu_ugo_2jets_iso_ip' ]
}

variable_ = variables['nominal']
regions_ = regions['nominal']
isblind = False

procs =[]
for ivar in variable_ :
    for iregion in regions_ :
        for iyear in [ '2016' , '2017' , '2018' ] :
            if iyear != '2017' : continue
            if isblind: proc = Process(target=run_blind, args=(base , ivar , iregion , iyear))
            else:  proc = Process(target=run_unblind, args=(base , ivar , iregion , iyear))
            procs.append(proc) ; proc.start()
            
[ r.join() for r in procs  ]


