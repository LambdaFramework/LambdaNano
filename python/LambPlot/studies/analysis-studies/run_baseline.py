#!/bin/python
import os, sys
from multiprocessing import Process

base=os.environ['NANOAODTOOLS_BASE']

def run_unblind( base , ivar , cut , iyear ):
    os.system( 'python %s/python/LambPlot/scripts/whss.py -o baseline_unblinded -v %s -r %s -y %s --unblind' %( base , ivar , cut , iyear ) )
    pass

def run_blind( base , ivar , cut , iyear ):
    os.system( 'python %s/python/LambPlot/scripts/whss.py -o baseline_blind -v %s -r %s -y %s' %( base , ivar , cut , iyear ) )
    pass

elevar = [ "Ele1_dz" , "Ele1_dxy" , "Ele1_pfRelIso03_all" , "Ele2_dz" , "Ele2_dxy" , "Ele2_pfRelIso03_all" ]
muvar  = [ "Mu1_dz" , "Mu1_dxy" , "Mu1_pfRelIso03_all" , "Mu1_pfRelIso04_all" , "Mu2_dz" , "Mu2_dxy" , "Mu2_pfRelIso03_all" , "Mu2_pfRelIso04_all" ]
elemuvar = [ "Ele1_dz" , "Ele1_dxy" , "Ele1_pfRelIso03_all" , "Ele2_dz" , "Ele2_dxy" , "Ele2_pfRelIso03_all" , "Mu1_dz" , "Mu1_dxy" , "Mu1_pfRelIso03_all" , "Mu1_pfRelIso04_all" ]
globalvar = [ "mll" , "pt1" , "pt2" , "jetpt1" , "jetpt2" ,"eta1" , "eta2" , "mlljj20_whss_bin4" , "MinMjjl" , "MinMjl" ]

customvar = [ "mlljj20_whss_bin4" , "MinMjjl" , "MinMjl" , "MindRjjl" , "MindRjl" ]
#customvar = [ "Ele1_tthmva" , ]#"Ele1_tthmva" ]
customvar = [ 'mlljj20_whss_bin4' ]

regions = {
    "hww2l2v_13TeV_of2j_WH_SS_eu_2j" :
    [ "Ele1_dz" , "Ele1_dxy" , "Ele1_pfRelIso03_all" , "Mu2_dz" , "Mu2_dxy" , "Mu2_pfRelIso03_all" , "Mu2_pfRelIso04_all" , "mlljj20_whss_bin3" , "MinMjjl" , "MindRjjl" ],
    "hww2l2v_13TeV_of2j_WH_SS_eu_1j" :
    [ "Ele1_dz" , "Ele1_dxy" , "Ele1_pfRelIso03_all" , "Mu2_dz" , "Mu2_dxy" , "Mu2_pfRelIso03_all" , "Mu2_pfRelIso04_all" , "mlljj20_whss" , "MinMjl" , "MindRjl" ],
    "hww2l2v_13TeV_of2j_WH_SS_uu_2j" :
    [ "Mu1_dz" , "Mu1_dxy" , "Mu1_pfRelIso03_all" , "Mu2_dz" , "Mu2_dxy" , "Mu2_pfRelIso03_all" , "Mu2_pfRelIso04_all" , "mlljj20_whss_bin3" , "MinMjjl" , "MindRjjl" ],
    "hww2l2v_13TeV_of2j_WH_SS_uu_1j" :
    [ "Mu1_dz" , "Mu1_dxy" , "Mu1_pfRelIso03_all" , "Mu2_dz" , "Mu2_dxy" , "Mu2_pfRelIso03_all" , "Mu2_pfRelIso04_all" , "mlljj20_whss" , "MinMjl" , "MindRjl" ],
    #"hww2l2v_13TeV_of2j_WH_SS_ee_2j" : customvar, #globalvar + elemuvar ,
    #"hww2l2v_13TeV_of2j_WH_SS_ee_1j" : customvar, #globalvar + elemuvar ,
    #"fake_CR"                        : customvar ,
}

def run( iyear_ , iregion_ , blind_ ):
    procs=[]
    for ivar in regions[iregion_] :
        if blind_: proc = Process(target=run_blind, args=(base , ivar , iregion_ , iyear_))
        else:  proc = Process(target=run_unblind, args=(base , ivar , iregion_ , iyear_))
        procs.append(proc) ; proc.start()
    [ r.join() for r in procs ]
    pass

isblind=True

#run( '2016' , 'fake_CR' , isblind )

#run ( '2016' , 'hww2l2v_13TeV_of2j_WH_SS_eu_1j' , isblind )

run( '2016' , 'hww2l2v_13TeV_of2j_WH_SS_eu_2j' , isblind )
run( '2016' , 'hww2l2v_13TeV_of2j_WH_SS_eu_1j' , isblind )
run( '2016' , 'hww2l2v_13TeV_of2j_WH_SS_uu_2j' , isblind )
run( '2016' , 'hww2l2v_13TeV_of2j_WH_SS_uu_1j' , isblind )
#run( '2016' , 'hww2l2v_13TeV_of2j_WH_SS_ee_2j' , isblind )
#run( '2016' , 'hww2l2v_13TeV_of2j_WH_SS_ee_1j' , isblind )

run( '2017' , 'hww2l2v_13TeV_of2j_WH_SS_eu_2j' , isblind )
run( '2017' , 'hww2l2v_13TeV_of2j_WH_SS_eu_1j' , isblind )
run( '2017' , 'hww2l2v_13TeV_of2j_WH_SS_uu_2j' , isblind )
run( '2017' , 'hww2l2v_13TeV_of2j_WH_SS_uu_1j' , isblind )
#run( '2017' , 'hww2l2v_13TeV_of2j_WH_SS_ee_2j' , isblind )
#run( '2017' , 'hww2l2v_13TeV_of2j_WH_SS_ee_1j' , isblind )

run( '2018' , 'hww2l2v_13TeV_of2j_WH_SS_eu_2j' , isblind )
run( '2018' , 'hww2l2v_13TeV_of2j_WH_SS_eu_1j' , isblind )
run( '2018' , 'hww2l2v_13TeV_of2j_WH_SS_uu_2j' , isblind )
run( '2018' , 'hww2l2v_13TeV_of2j_WH_SS_uu_1j' , isblind )
#run( '2018' , 'hww2l2v_13TeV_of2j_WH_SS_ee_2j' , isblind )
#run( '2018' , 'hww2l2v_13TeV_of2j_WH_SS_ee_1j' , isblind )

