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
from PhysicsTools.NanoAODTools.postprocessing.data.vars.variables import br_all as variable
from PhysicsTools.NanoAODTools.LambPlot.Utils.selections import *
from PhysicsTools.NanoAODTools.LambPlot.Utils.alias import alias

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
parser.add_option("-B", "--blind", action="store_true", default=False, dest="blind")
#parser.add_option("-s", "--signal", action="store_true", default=False, dest="signal")
parser.add_option("-x", "--Statebox", action="store_true", default=False, dest="Statebox")
parser.add_option("-d", "--debug", action="store_true", default=False, dest="debug")
#parser.add_option("-u", "--User_cutflow", action="store_true", dest="cutflow", default=False)
parser.add_option("-V", "--PrintVar", action="store_true", dest="printVar", default=False)
#parser.add_option("-m", "--multiprocessing", action="store_true", dest="multiprocessing", default=False)
parser.add_option("-l", "--logy", action="store_true", dest="logy", default=False)
parser.add_option("-e", "--era", action="store", type="string", dest="dataset", default="Run2_2016_v4")
(options, args) = parser.parse_args()
if options.bash: gROOT.SetBatch(True)

if not options.Statebox:
    gStyle.SetOptStat(0)
else:
    gStyle.SetOptStat(1111111)

cfg = Config(options.dataset)
########## PLOTTER SETTINGS ##########
NTUPLEDIR   = '/home/shoh/works/Projects/Analysis/LambdaNano/pilot/';
PLOTDIR     = "plots/%s"%options.dataset
LUMI        = cfg.lumi() #41860. #35800. # pb-1 Inquire via brilcalc lumi --begin 272007 --end 275376 -u /pb #https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmV2016Analysis
#data = []
data        = ["data_obs"]
back        = [ "VVV", "ttV" , "WW", "VZ", "Vg", "ST", "WJetsToLNu", "TTbar", "DYJetsToLL" ]
sign=[]
BLIND       = True if options.blind else False
SIGNAL      = 1. #500. # rescaling factor 1/35800
RATIO       = 4 if not BLIND else 0 #4 # default=4 # 0: No ratio plot; !=0: ratio between the top and bottom pads
POISSON     = False
selection=eval(cfg.era())['selection']
weight=eval(cfg.era())['weight']
cfg.register(data+back)

def plot(var, cut, norm=False):

    PD = getPrimaryDataset(selection[cut])
    if cut in selection: plotdir = cut

    PROC=data+back if not BLIND else back
    print col.OKGREEN+"Primary Dataset    : "+col.ENDC, PD
    print col.OKGREEN+"CUT    : "+col.ENDC, selection[cut]
    print col.OKGREEN+"WEIGHT : "+col.ENDC, weight[cut]
    if not sign:
        Histlist=ProjectDraw(var, cut, LUMI, PROC, PD, NTUPLEDIR)
    else:
        Histlist=ProjectDraw(var, cut, LUMI, PROC+sign, PD, NTUPLEDIR)

    if len(back)>0:
        #If data_obs present, dummy BkgSum == first background process
        Histlist['BkgSum'] = Histlist['data_obs'].Clone("BkgSum") if 'data_obs' in Histlist else Histlist[back[0]].Clone("BkgSum")
        Histlist['BkgSum'].Reset("MICES")
        Histlist['BkgSum'].SetFillStyle(3003)
        Histlist['BkgSum'].SetFillColor(1)

    for i, s in enumerate(back): Histlist['BkgSum'].Add( Histlist[s].GetPtr() )

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
        out = draw(Histlist, data if not BLIND else [], back, sign, SIGNAL, RATIO, POISSON, True if options.logy else (filter(lambda x:x.name()==var.split('[')[0],variable)[0]).log())
        out[0].cd(1)
        drawCMS(LUMI, "Preliminary")
        drawRegion(cut)
        printTable(Histlist, sign)
    else:
        out = drawSignal(Histlist, sign, True if options.logy else (filter(lambda x:x.name()==var,variable)[0]).log())
        out[0].cd(1)
        drawCMS(LUMI, "Simulation")
        drawRegion(cut)

    out[0].Update()

    if gROOT.IsBatch():
            #pathname = PLOTDIR+"/Signal/"+cut if options.signal else PLOTDIR+"/"+plotdir
            pathname = PLOTDIR+"/"+plotdir
            if not os.path.exists(pathname): os.system('mkdir -p %s'%pathname)
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

    check=True
    filelist=cfg.getSamplelist()
    for itag in data+back:
        for iroot in filelist[itag]['files']:
            if not os.path.exists(NTUPLEDIR+iroot+".root"):
                print col.FAIL+NTUPLEDIR+iroot+".root does not exit!", col.ENDC
                check=False
    if not check:
        print "EXIT"
        exit()
    #####
    
    start_time = time.time()
    if options.variable =="" and not options.printVar:
        parser.print_help()
        print(col.WARNING+'Example:'+col.ENDC)
        print(col.WARNING+'python scripts/plotter.py -v MHT_pt -r OSmumu -e Run2_2016_v4'+col.ENDC)
        sys.exit(1)

    if options.printVar:
        print(col.OKGREEN+'Predefined Variables for plotting'+col.ENDC)
        print(map(lambda x: x.name(), br_all)+list(alias.keys()))
        print(col.OKGREEN+'Predefined region for plotting'+col.ENDC)
        print(selection.keys())
        sys.exit(1)

    cfg.summary()
    print(col.OKGREEN+"PLOTTING variable ",options.variable+col.ENDC)
    gROOT.Macro('%s/scripts/functions.C' %os.getcwd())
    if options.cut != "":
        print col.CYAN+"with Cuts : ",options.cut+col.ENDC
        plot( options.variable , options.cut )
    else:
        print col.CYAN+"In selection region : ",options.region+col.ENDC
        plot( options.variable , options.region )

    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- %s minutes ---" % ( (time.time() - start_time)/60. ))
    print("--- %s hours ---" % ( (time.time() - start_time)/3600. ))
