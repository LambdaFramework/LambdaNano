#!/bin/python
import os, sys

base=os.environ['NANOAODTOOLS_BASE']


from multiprocessing import Process

def run_command( base , ivar , cut , iyear ):
    os.system( 'python %s/python/LambPlot/scripts/whss.py -v %s -r %s -y %s --unblind' %( base , ivar , cut , iyear ) )
    pass

variables = {
    'nominal' : [ 'mlljj20_whss_bin4' ],
    'ugo' : [ 'MinMjjl' , 'MinMjl' ] ,
    'invest' : [ "mll" , "pt1" , "pt2" , "nJet" , "MinMjjl" , "Ele1_dz" , "Mu2_dz" , "Ele1_dxy" , "Mu2_dxy" , "Ele1_pfRelIso03_all" , "Mu2_pfRelIso03_all" , "Ele1_pfRelIso04_all" , "Mu2_pfRelIso04_all" ]
}

regions = {
    'nominal' : [ 'hww2l2v_13TeV_of2j_WH_SS_eu_1j' , 'hww2l2v_13TeV_of2j_WH_SS_eu_2j' , 'hww2l2v_13TeV_of2j_WH_SS_uu_1j' , 'hww2l2v_13TeV_of2j_WH_SS_uu_2j' ],
    'ugo' : [ 'SSmumu_ugo_2jets' , 'SSmumu_ugo_2jets_iso' , 'SSmumu_ugo_2jets_iso_ip' ]
}

procs =[]
for ivar in variables['ugo'] :
    for iregion in regions['ugo'] :
        for iyear in [ '2016' , '2017' , '2018' ] :
            proc = Process(target=run_command, args=(base , ivar , iregion , iyear))
            procs.append(proc) ; proc.start()
            
[ r.join() for r in procs  ]


