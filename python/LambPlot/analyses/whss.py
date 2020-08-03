#! /usr/bin/env python

import os, multiprocessing, sys
import copy
import math
from array import array
from ROOT import ROOT, gROOT, gStyle, gRandom, TSystemDirectory
from ROOT import TFile, TChain, TTree, TCut, TH1, TH1F, TH2F, THStack, TGraph, TGraphAsymmErrors, TEfficiency
from ROOT import TStyle, TCanvas, TPad
from ROOT import TLegend, TLatex, TText, TLine, TBox
from multiprocessing import Pool, cpu_count
import time, os
from functools import partial
from collections import OrderedDict

from PhysicsTools.NanoAODTools.LambPlot.Utils.configs import Config
import PhysicsTools.NanoAODTools.LambPlot.Utils.color as col
from PhysicsTools.NanoAODTools.LambPlot.Utils.drawLambda import *
import importlib

if '%s' %os.getcwd().split('/')[-1] != 'LambPlot':
    print('EXIT: Please run the plotter in LambPlot folder')
    sys.exit()

########## SETTINGS ##########
import optparse
usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
parser.add_option("-v", "--variable", action="store", type="string", dest="variable", default="")
parser.add_option("-c", "--cut", action="store", type="string", dest="cut", default="")
parser.add_option("-r", "--region", action="store", type="string", dest="region", default="")
parser.add_option("-b", "--bash", action="store_true", default=False, dest="bash")
parser.add_option("-B", "--blind", action="store_true", default=True, dest="blind")
#parser.add_option("-s", "--signal", action="store_true", default=False, dest="signal")
parser.add_option("-x", "--Statebox", action="store_true", default=False, dest="Statebox")
parser.add_option("-d", "--debug", action="store_true", default=False, dest="debug")
#parser.add_option("-u", "--User_cutflow", action="store_true", dest="cutflow", default=False)
parser.add_option("-V", "--PrintVar", action="store_true", dest="printVar", default=False)
#parser.add_option("-m", "--multiprocessing", action="store_true", dest="multiprocessing", default=False)
parser.add_option("-l", "--logy", action="store_true", dest="logy", default=True)
parser.add_option("-y", "--year", action="store", type="string", dest="year", default="2016")
(options, args) = parser.parse_args()
if options.bash: gROOT.SetBatch(True)

if not options.Statebox:
    gStyle.SetOptStat(0)
else:
    gStyle.SetOptStat(1111111)

#### Initialize cfg
cfg = Config(options.year)
samples = cfg.getModule('samples')
variables = cfg.getModule('variables')
groupPlot = cfg.getModule('groupPlot')

########## PLOTTER SETTINGS ##########
#NTUPLEDIR   = '/home/shoh/works/Projects/Analysis/LambdaNano/pilot/';
PLOTDIR     = "plots/Run2_%s"%options.year
LUMI        = cfg.lumi() #41860. #35800. # pb-1 Inquire via brilcalc lumi --begin 272007 --end 275376 -u /pb #https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmV2016Analysis
data        = [ 'DATA' ]
sign        = [ x for x in groupPlot if groupPlot[x]['isSignal'] == 1 ]
back        = [ x for x in groupPlot if groupPlot[x]['isSignal'] == 0 ]
#back.remove("Fake")
#BLIND       = True if options.blind else False
BLIND = False
SIGNAL      = 1. #500. # rescaling factor 1/35800
RATIO       = 4 if not BLIND else 0 #4 # default=4 # 0: No ratio plot; !=0: ratio between the top and bottom pads
POISSON     = False

def plot(var, cut, norm=False):

    #PD = getPrimaryDataset(selection[cut])
    if cut in selection: plotdir = cut
    pathname = PLOTDIR+"/"+plotdir
    if not os.path.exists(pathname): os.system('mkdir -p %s'%pathname)

    PROC=data+back if not BLIND else back
    PD=""
    #print col.OKGREEN+"Primary Dataset    : "+col.ENDC, PD
    print col.OKGREEN+"PROC : "+col.ENDC, PROC
    
    if not sign:
        Histlist=ProjectDraw(var, cut, LUMI, PROC, PD)
    else:
        Histlist=ProjectDraw(var, cut, LUMI, PROC+sign, PD)

    if len(back)>0:
        #If data_obs present, dummy BkgSum == first background process
        Histlist['BkgSum'] = Histlist['DATA'].Clone("BkgSum") if 'DATA' in Histlist else Histlist[back[0]].Clone("BkgSum")
        Histlist['BkgSum'].Reset("MICES")
        Histlist['BkgSum'].SetFillStyle(3003)
        Histlist['BkgSum'].SetFillColor(1)
    for i, s in enumerate(back): Histlist['BkgSum'].Add( Histlist[s] )

    if len(back)==0 and len(data)==0:
        for i, s in enumerate(sign):
            #Normalize signal to 1
            #Histlist[s].Scale(1./Histlist[s].Integral())
            Histlist[s].SetLineWidth(2)
            Histlist[s].SetFillStyle(0)

    if norm:
        sfnorm = hist['data_obs'].Integral()/hist['BkgSum'].Integral()
        for i, s in enumerate(back+['BkgSum']): hist[s].Scale(sfnorm)
        
    if len(data+back)>0:
        out = draw(Histlist, data if not BLIND else [], back, sign, SIGNAL, RATIO, POISSON, options.logy )
        out[0].cd(1)
        drawCMS(LUMI, "Preliminary")
        drawRegion(cut)
        printTable( Histlist , pathname , '%s_%s.txt' %(plotdir,var) , sign )
        
    else:
        out = drawSignal(Histlist, sign, options.logy )
        out[0].cd(1)
        drawCMS(LUMI, "Simulation")
        drawRegion(cut)

    out[0].Update()

    if gROOT.IsBatch():
            out[0].Print(pathname+"/"+var.replace('.', '_')+".png")
            out[0].Print(pathname+"/"+var.replace('.', '_')+".pdf")
    else:
        out[0].Draw()

    #if options.all:
    print col.WARNING+"PURGE OBJECTS IN MEMORY"+col.ENDC
    for process in Histlist:
        Histlist[process].Delete()

###########################################

if __name__ == "__main__":

    cfg.summary()
    
    start_time = time.time()
    
    gROOT.Macro('%s/scripts/functions.C' %os.getcwd())
    if options.variable =="" or options.region =="":
        print col.WARNING + "ERROR: variable or region are empty" + col.ENDC
        sys.exit()
    print ""
    print col.OKGREEN+"Variable : "+col.ENDC, options.variable
    print col.OKGREEN+"Region : "+col.ENDC, options.region 
    plot( options.variable , options.region )
    
    #plot( 'mlljj20_whss' , 'hww2l2v_13TeV_of2j_WH_SS_eu_2j' )
    #plot( 'mll' , 'OSmumu' )
    #for iregion in [ 'WZCR', 'VgCR' , 'OSemu' , 'SSee' , 'OSmumu' , 'SSmumu' , 'OSmue' , 'SSemu' , 'SSmue' , 'OSee' ]:
    #    plot( 'mll' , iregion )
    #plot( 'MinMjjl' , 'SSmumu' )
    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- %s minutes ---" % ( (time.time() - start_time)/60. ))
    print("--- %s hours ---" % ( (time.time() - start_time)/3600. ))
