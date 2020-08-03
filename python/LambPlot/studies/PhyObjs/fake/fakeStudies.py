#! /usr/bin/env python

import os,sys
import copy
import math
from array import array
import collections
from ROOT import gROOT, gRandom, TSystemDirectory
from ROOT import TFile, TChain, TTree, TCut, TH1F, TH2F, THStack, TGraph
from ROOT import TStyle, TCanvas, TPad, TPaveStats
from ROOT import TLegend, TLatex, TText

from PhysicsTools.NanoAODTools.plotter.Utils.drawLambda import *
from PhysicsTools.NanoAODTools.plotter.Utils.variables import variable
from PhysicsTools.NanoAODTools.plotter.Utils.sampleslist import latino as samples
from PhysicsTools.NanoAODTools.plotter.Utils.Dataset import Run2_17_nanov2_la

import PhysicsTools.NanoAODTools.plotter.Utils.color as col

gROOT.Macro('functions.C')

import optparse
usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
parser.add_option("-b", "--bash", action="store_true", default=False, dest="runBash")
(options, args) = parser.parse_args()
if options.runBash: gROOT.SetBatch(True)

########## SETTINGS ##########
stats=False
if not stats:
    gStyle.SetOptStat(0)
else:
    gStyle.SetOptStat(1111)
LUMI        = 41.5 #fb-1 #35800. #140000 #35800. # in pb-1
RATIO       = 4 # 0: No ratio plot; !=0: ratio between the top and bottom pads
#NTUPLEDIR   = '/Users/shoh/Projects/CMS/PhD/Analysis/SSL/signal-dev/'
#NTUPLEDIR   = '/Users/shoh/Projects/CMS/PhD/Analysis/SSL/dataset-v19-VH/'
#NTUPLEDIR   = '/Users/shoh/Projects/CMS/PhD/Analysis/SSL/LATINO/datasetskim/'
NTUPLEDIR = '/lustre/cmswork/hoh/NANO/SSLep/nanoskim/final/CMSSW_9_4_13/src/PhysicsTools/NanoAODTools/latino-skim-v4-merge/'

signals = ['HWplusJ','HWminusJ']
#back = [key for key,value in samples.iteritems() if key not in signals]
#print back
back = ['WWZ', 'WZ', 'Wg', 'ZZZ', 'WJetsToLNu-LO', 'TTToSemiLeptonic', 'WZZ', 'ZZ', 'WWW', 'Zg', 'ST']
#back = [ 'Wg' , 'Zg' ]
colors = [616+4, 632, 800+7, 800, 416+1, 860+10, 600, 616, 921, 922]
channels = ['Wp125','Wm200']
#channels = ['XVZmmlp', 'XVZmmhp', 'XVZeelp', 'XVZeehp']
#color = {"XVZmmlp" : 634, "XVZmmhp" : 410, "XVZeelp" : 856, "XVZeehp" : 418}

def significanceSB(cutlist, labellist):
    basecut=""

    ncuts = len(cutlist)
    effs = [0]*(ncuts+1)
    hist = TH1D('eff',";Significance",ncuts,0,ncuts)

    for k, cs in enumerate(labellist): hist.GetXaxis().SetBinLabel(k+1, "%s" %labellist[k])

    for j, c in enumerate(cutlist):
        chainbkg ={}; chainsig={};
        n = 0.; d =0.
        ##signal
        for s,v in enumerate(signals):
            chainsig[v] = TChain("Events")
            for rootfiles in samples[v]['files']:
                chainsig[v].AddFile("%s%s"%(NTUPLEDIR,rootfiles))

            #signalmatch = [x for x in Run2_17_nanov2_la if x.name()==v][0]
            #if float(signalmatch.matcheff())==1.:
            #    XSWeight= float( (signalmatch.xsec())*1000. / (signalmatch.nevent()) )
            #    Norm= XSWeight*LUMI
            #elif float(signalmatch.matcheff())!=1.:
            #XSWeight=signalmatch.matcheff()
            #Norm = float(XSWeight*LUMI)
            #print "k = ", k," : signalmatch.matcheff() = ", float(signalmatch.matcheff())," ; Norm = %f"%Norm
            #elif float(matches.matcheff())==1.:
            #    print "1.) ERROR 404"
            #    sys.exit()
            print v," : n = ", chainsig[v].GetEntries( "%s*XSWeight*(%s)" %(LUMI,cutlist[j]) )
            n+= chainsig[v].GetEntries( "%s*XSWeight*(%s)" %(LUMI,cutlist[j]) )
            print "tot = ", n

        ##backgrounds
        for b,k in enumerate(back):
            chainbkg[k] = TChain("Events")
            for rootfiles in samples[k]['files']:
                chainbkg[k].AddFile("%s%s"%(NTUPLEDIR,rootfiles))
                
            #matches = [x for x in Run2_17_nanov2_la if x.name()==k][0]
            #if float(matches.matcheff())!=1.:
            #XSWeight=matches.matcheff()
            #Norm = float(XSWeight*LUMI)
            #print "k = ", k," : matches.matcheff() = ", float(matches.matcheff())," ; Norm = ",Norm
            #elif float(matches.matcheff())==1.:
            #    print "k = ", k
            #    print "matches.matcheff() = ", float(matches.matcheff())
            #    print "2.) ERROR 404"
            #    sys.exit()
            print k," : d = ", chainbkg[k].GetEntries( "%s*XSWeight*(%s)" %(LUMI,cutlist[j]) )
            d+= chainbkg[k].GetEntries( "%s*XSWeight*(%s)" %(LUMI,cutlist[j]) )
            print "tot = ", d

        print "s = ", float(n)
        print "d = ", float(d)
        print "sqrt(d) = ", math.sqrt(d)
        effs[j] = float(n/math.sqrt(d))
        print "effs[j] = ", effs[j]
        hist.Fill(j,effs[j])
    #hist[s].SetMarkerStyle(20)
    #hist[s].SetMarkerColor(colors[i])
    hist.SetLineColor(colors[2])
    hist.SetLineWidth(3)
    #hist[s].GetXaxis().SetTitleOffset(hist[s].GetXaxis().GetTitleOffset()*1.2)
    #hist[s].GetYaxis().SetTitleOffset(hist[s].GetYaxis().GetTitleOffset()*1.2)


    leg = TLegend(0.7, 0.9-0.035*len(signals), 0.9, 0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(1001)
    leg.SetFillColor(0)
    leg.AddEntry('label', "l")

    c1 = TCanvas("c1", "Signals", 800, 600)
    c1.cd()
    c1.GetPad(0).SetTopMargin(0.06)
    c1.GetPad(0).SetRightMargin(0.05)
    c1.GetPad(0).SetTicks(1, 1)

    #hist[signals[0]].SetMaximum(1.3)
    #hist[signals[0]].SetMinimum(0.)

    hist.GetXaxis().SetTitle("Selection")
    hist.GetYaxis().SetTitle("Significance (#frac{S}{#sqrt{B}})")
    #hist.GetYaxis().SetRangeUser(0., 1.)
    hist.Draw()
    leg.Draw()
    drawCMS("41.5", "Preliminary")
    drawRegion(basecut)

    c1.Print("./SignificanceSB_" + basecut + ".png")
    c1.Print("./SignificanceSB_" + basecut + ".pdf")
    #if not options.runBash: raw_input("Press Enter to continue...")
    pass        
'''
def printTable(hist, sign=[]):
    samplelist = [x for x in hist.keys() if not 'data' in x and not 'BkgSum' in x and not x in sign and not x=="files"]
    print "Sample                  Events          Entries         %"
    print "-"*80
    for i, s in enumerate(['data_obs']+samplelist+['BkgSum']):
        if i==1 or i==len(samplelist)+1: print "-"*80
        #Events                           #Entries                                                                                               
        print "%-20s" % s, "\t%-10.2f" % hist[s].Integral(), "\t%-10.0f" % (hist[s].GetEntries()-2), "\t%-10.2f" % (100.*hist[s].Integral()/hist['BkgSum'].Integral()) if hist['BkgSum'].Integral() > 0 else 0, "%"
    print "-"*80
    for i, s in enumerate(sign):
        if not samples[s]['plot']: continue
        #print "%-20s" % s, "\t%-10.2f" % hist[s].Integral(), "\t%-10.0f" % (hist[s].GetEntries()-2), "\t%-10.2f" % (100.*hist[s].GetEntries()/float(hist[s].GetOption())) if float(hist[s].GetOption()) > 0 else 0, "%"                                                                                                       
        print "%-20s" % s, "\t%-10.2f" % hist[s].Integral(), "\t%-10.0f" % (hist[s].GetEntries()-2), "\t%-10.2f" % (hist[s].GetEntries()) if float(hist[s].GetEntries()) > 0 else 0,"%"
    print "-"*80
pass
'''
#produce three N(Scuts) of cutflow histogram
def cutflow(cutlist, labellist, SRs):
    basecut=""

    WPcut=[ x.split(' && ')[-1] for x in cutlist]
    baseline=cutlist[0].split()
    baseline=filter(lambda x: x!="&&",baseline)
    baseline=filter(lambda x: x not in WPcut,baseline)
    print baseline
    Chain={}
    hist={}
    evDict=collections.OrderedDict()
    WPdict=collections.OrderedDict()
    n=0.; d=0.
    for iwp in labellist: WPdict[iwp] = {'s': 0. , 'b': 0. , 'syield': 0. , 'byield': 0.} 
    ncuts = len(cutlist)
    #effs = [0]*(ncuts+1)
    effhist = TH1D('eff',";Significance",ncuts,0,ncuts)
    ## samplelist
    for i, s in enumerate(back+signals):
        Chain[s]=TChain("Events")
        evDict['%s'%s]={}
        print s
        for rootfiles in samples[s]['files']:
            print rootfiles
            Chain[s].AddFile("%s%s"%(NTUPLEDIR,rootfiles))

        hist[s] = TH1F('%s'%s,"dum",100,-0.5,99.5)

        ## looping on cut
        cutsq=""
        subdict=collections.OrderedDict()
        for j, cut in enumerate(baseline):
            dummy=hist
            if len(cutsq)==0:
                cutsq+=cut
            else:
                cutsq+=" && "+cut
            #Chain[s].Project(s, "PV_npvs", "%s*XSWeight*(%s)"%(LUMI,cutsq))
            ##dummy[s].SetOption("%s" % Chain[s].GetTree().GetEntriesFast())
            #subdict['%s'%cut]=dummy[s].Integral()
            #print cut," : ",dummy[s].Integral()," : ",dummy[s].GetEntries()
            if j+1 == len(baseline):
                wpcut=""
                for k, wp in enumerate(WPcut):
                    wpcut= cutsq + " && " + wp
                    #print wpcut
                    Chain[s].Project(s, "PV_npvs", "%s*XSWeight*(%s)"%(LUMI,wpcut))
                    subdict['%s'%labellist[k]]=dummy[s].Integral()
                    print labellist[k]," : ",dummy[s].Integral()," : ",dummy[s].GetEntries()
                    #signal/bkg
                    WPdict['%s'%labellist[k]]['s' if s in signals else 'b']+=dummy[s].GetEntries()
                    WPdict['%s'%labellist[k]]['syield' if s in signals else 'byield']+=dummy[s].Integral()
                    wpcut=""
        evDict['%s'%s]=subdict

    for k, cs in enumerate(labellist): effhist.GetXaxis().SetBinLabel(k+1, "%s" %labellist[k])

    print "-"*80
    print SRs
    print "-"*80
    for key in WPdict:
        print "-----> ",key
        print "syield = ", WPdict[key]['syield']
        print "byield = ", WPdict[key]['byield']
        print "s entries = ", WPdict[key]['s']
        print "d entires = ", WPdict[key]['b']
        print "sqrt(byield) = ", math.sqrt(WPdict[key]['byield'])
        print "float(syield/math.sqrt(byield)) = ", float( WPdict[key]['syield'] / math.sqrt(WPdict[key]['byield']) )
        effs= float( WPdict[key]['syield'] / math.sqrt(WPdict[key]['byield']) )
        effhist.Fill(key,effs)
    print "-"*80

    effhist.SetLineColor(colors[2])
    effhist.SetLineWidth(3)
    leg = TLegend(0.7, 0.9-0.035*len(signals), 0.9, 0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(1001)
    leg.SetFillColor(0)
    leg.AddEntry('label', "l")

    c1 = TCanvas("c1", "Signals", 800, 600)
    c1.cd()
    c1.GetPad(0).SetTopMargin(0.06)
    c1.GetPad(0).SetRightMargin(0.05)
    c1.GetPad(0).SetTicks(1, 1)
    effhist.GetXaxis().SetTitle("Selection")
    effhist.GetYaxis().SetTitle("Significance (#frac{S}{#sqrt{B}})")
    effhist.Draw()
    leg.Draw()
    drawCMS("41.5", "Preliminary")
    drawRegion("%s"%SRs)
    
    #process: cut: value
    #printTable(evDict)

    c1.Print("./SignificanceSB_"+ SRs + basecut + ".png")
    c1.Print("./SignificanceSB_"+ SRs + basecut + ".pdf")
    #if not options.runBash: raw_input("Press Enter to continue...")
    pass


Trig="1==1"

Scut="Vll_mass>12 && Lepton_pt[0]>25 && Lepton_pt[1]>15 && (nLepton>=2&&Alt$(Lepton_pt[2],0)<10) && MET_pt>20"

#Scut="MET_pt>20 && Sum$(CleanJet_pt>30)>=1"

#region="(Lepton_pdgId[0]*Lepton_pdgId[1] == 11*11) && Lepton_pt[1]>20 && abs(Lepton_eta[0] - Lepton_eta[1])<2.0 && abs(Vll_mass-91.2)>15 && Alt$(CleanJet_pt[0],0)>30 && (Sum$(CleanJet_pt>30)>=2 || Vjj_mass < 100)"

SR={
    'sseej' : "((Lepton_pdgId[0]*Lepton_pdgId[1]==11*11)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*-11)) && abs(Lepton_eta[0]-Lepton_eta[1])<2.0 && abs(Vll_mass-91.2)>15 && Alt$(CleanJet_pt[0],0)>30 && Alt$(CleanJet_pt[1],0)>20 && Alt$(CleanJet_pt[1],0)<30",
    'sseejj' : "((Lepton_pdgId[0]*Lepton_pdgId[1]==11*11)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*-11)) && abs(Lepton_eta[0]-Lepton_eta[1])<2.0 && abs(Vll_mass-91.2)>15 && Alt$(CleanJet_pt[0],0)>30 && Alt$(CleanJet_pt[1],0)>30",
    'sseuj' : "((abs(Lepton_pdgId[0])==11&&abs(Lepton_pdgId[1])==13)) && abs(Lepton_eta[0]-Lepton_eta[1])<2.0 && Alt$(CleanJet_pt[0],0)>30 && Alt$(CleanJet_pt[1],0)>20 && Alt$(CleanJet_pt[1],0)<30",
    'sseujj' : "((abs(Lepton_pdgId[0])==11&&abs(Lepton_pdgId[1])==13)) && abs(Lepton_eta[0]-Lepton_eta[1])<2.0 && Alt$(CleanJet_pt[0],0)>30 && Alt$(CleanJet_pt[1],0)>30",
    }

##ee
for rg in ['sseej','sseejj']:
    region=SR['%s'%rg]

    Scuts = [\
        Trig+" && "+Scut+" && "+region+" && (Lepton_isTightElectron_mvaFall17V1Iso_WP90_HWW[0]==1&&Lepton_isTightElectron_mvaFall17V1Iso_WP90_HWW[1]==1 )", \
            Trig+" && "+Scut+" && "+region+" && (Lepton_isTightElectron_mvaFall17V1Iso_WP90_SS_HWW[0]==1&&Lepton_isTightElectron_mvaFall17V1Iso_WP90_SS_HWW[1]==1)", \
            Trig+" && "+Scut+" && "+region+" && (Lepton_isTightElectron_cutBasedV1_WPTight_HWW[0]==1&&Lepton_isTightElectron_cutBasedV1_WPTight_HWW[1]==1)"
        ]
    Slabs = ["mvaFall17V1Iso_WP90", "mvaFall17V1Iso_WP90_SS", "cutBasedV1_WPTight"]
    cutflow(Scuts, Slabs, '%s'%rg)

##emu
for rg in ['sseuj','sseujj']:
    region=SR['%s'%rg]

    Scuts = [\
        Trig+" && "+Scut+" && "+region+" && (Lepton_isTightElectron_mvaFall17V1Iso_WP90_HWW[0]==1)", \
            Trig+" && "+Scut+" && "+region+" && (Lepton_isTightElectron_mvaFall17V1Iso_WP90_SS_HWW[0]==1)", \
            Trig+" && "+Scut+" && "+region+" && (Lepton_isTightElectron_cutBasedV1_WPTight_HWW[0]==1)"
        ]
    Slabs = ["mvaFall17V1Iso_WP90", "mvaFall17V1Iso_WP90_SS", "cutBasedV1_WPTight"]
    cutflow(Scuts, Slabs, '%s'%rg)



