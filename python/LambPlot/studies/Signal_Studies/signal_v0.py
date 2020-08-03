#! /usr/bin/env python

import os,sys
import copy
import math
from array import array
from ROOT import gROOT, gRandom, TSystemDirectory
from ROOT import TFile, TChain, TTree, TCut, TH1F, TH2F, THStack, TGraph
from ROOT import TStyle, TCanvas, TPad, TPaveStats
from ROOT import TLegend, TLatex, TText

cwd=os.getcwd()
sys.path.append(cwd+"/Utils/")

from drawLambda import *
from variables import variable
from selections_SSLep import *
from sampleslist import *

import color as col

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
LUMI        = 35800. #140000 #35800. # in pb-1
RATIO       = 4 # 0: No ratio plot; !=0: ratio between the top and bottom pads
#NTUPLEDIR   = '/Users/shoh/Projects/CMS/PhD/Analysis/SSL/signal-dev/'
NTUPLEDIR   = '/Users/shoh/Projects/CMS/PhD/Analysis/SSL/dataset-v19-VH/' 

back = ["WJetsToLNu_HT"]
#back = []
signals         = ['Wp', 'Wm'] #, 'WHWWp', 'WHWWm']
colors = [616+4, 632, 800+7, 800, 416+1, 860+10, 600, 616, 921, 922]
channels = ['Wp125','Wm200']
#channels = ['XVZmmlp', 'XVZmmhp', 'XVZeelp', 'XVZeehp']
#color = {"XVZmmlp" : 634, "XVZmmhp" : 410, "XVZeelp" : 856, "XVZeehp" : 418}

def signal(var, cut):
    hist={}
    

    ## Project into histogram
    hist= ProjectDraw(var, cut, LUMI, signals, [], NTUPLEDIR)
    for i,s in enumerate(signals):
        print "s : ", s
        hist[s].SetLineWidth(2)
        
    ## We need the legends
    if not stats:
        leg = TLegend(0.7, 0.9-0.035*len(signals), 0.9, 0.9)
    else:
        leg = TLegend(0.4, 0.9-0.035*len(signals), 0.6, 0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(1001) #1001
    leg.SetFillColor(0)
    for i, s in enumerate(signals):
        leg.AddEntry(hist[s], samples[s]['label'], "l")

    # declare a canvas for this shit
    c1 = TCanvas("c1", "Signals", 800, 600)
    c1.cd().SetLogy() if variable[var]['log'] else c1.cd()
    c1.cd()
    c1.GetPad(0).SetTopMargin(0.06)
    c1.GetPad(0).SetRightMargin(0.05)
    c1.GetPad(0).SetTicks(1, 1)
    
    hmax = 0.
    ## Define a suitable height for the histogram taking into account of other signal samples
    for i, s in enumerate(signals):
        if hist[s].GetMaximum() > hmax: hmax = hist[s].GetMaximum()
    if not variable[var]['log']:
        hist[signals[0]].SetMaximum(hmax*1.2)
        hist[signals[0]].SetMinimum(0.)
    else:
        hist[signals[0]].SetMaximum(hmax*4)
    
    ### after that you fucking draw this shit
    for i, s in enumerate(signals):
        hist[s].Draw("HIST" if i==0 else "SAMES, HIST")
        if stats:
            c1.GetPad(0).Update()
            if i==1:
                lof = hist[s].GetListOfFunctions()
                statbox = lof.FindObject('stats')
                statbox.SetX1NDC(0.779026); statbox.SetX2NDC(0.979401)
                statbox.SetY1NDC(0.593168); statbox.SetY2NDC(0.754658)
    leg.Draw()
    
    drawCMS(LUMI, "Simulation")
    #drawRegion(cut)
    #drawAnalysis(channel)
    
#    
#    if variable[var]['log'] and not "X_mass" in var:
#        c1.GetPad(0).SetLogy()

    ## Fitting the mass shape of the variables
    
    if ('RecoLL' in var or 'RecoL2JJ' in var) and 'mass[0]' in var:
        fitOption="Q0"
        mean = {}
        width = {}
        for i, s in enumerate(signals):
            amean = hist[s].GetXaxis().GetBinCenter(hist[s].GetMaximumBin())
            sigma = hist[s].GetRMS()
            hist[s].Fit("gaus", "%s" %fitOption, "SAME", amean/sigma, amean*sigma) #(i+1)*1000-(i+1)*400, (i+1)*1000+(i+1)*400)
            hist[s].GetFunction("gaus").SetLineWidth(3)
            hist[s].GetFunction("gaus").SetLineColor(hist[s].GetLineColor())
            mean[s] = hist[s].GetFunction("gaus").GetParameter(1)
            width[s] = hist[s].GetFunction("gaus").GetParameter(2)
            #mean[s] = amean
            #width[s] = sigma
        print "Mass (GeV)",
        for i, s in enumerate(signals): print " &", s.replace("ZZhllbb_M", ""), "\t",
        print " \\\\"
        print "\\hline"
        print "Mean (GeV)",
        for i, s in enumerate(signals): print " & %.0f\t" % mean[s],
        print " \\\\"
        print "Width (GeV)",
        for i, s in enumerate(signals): print " & %.1f\t" % width[s],
        print " \\\\"
        print "Res (\\%)",
        for i, s in enumerate(signals): print " & %.1f\t" % (100.*width[s]/mean[s], ),
        print " \\\\"
        
        #hist[s].Draw()
    #c1.Print("plots/Signal/"+channel+".pdf")
    #c1.Print("plots/Signal/"+channel+".png")
    c1.Print("plots/Signal/"+var+".pdf")
    c1.Print("plots/Signal/"+var+".png")
    #c1.Delete()
    #if not options.runBash: raw_input("Press Enter to continue...")
    pass

'''
def btag():
    nbins = 500
    xmin = 0.
    xmax = 1.
    sel = "Z_pt>200 && Z_mass>70 && Z_mass<110 && fatjet1_pt>200 && (fatjet1_prunedMass>95 && fatjet1_prunedMass<130)"
    add = "fatjet1_CSV>0. && fatjet1_CSV1>0. && fatjet1_CSV2>0."
    
    tree = TChain("XZZ")
    for j, ss in enumerate(sample[back[0]]['files']):
        tree.Add(NTUPLEDIR + ss + ".root")
    bb = TH1F("bb", ";CSV;Arbitrary units", nbins, xmin, xmax)
    qq = TH1F("qq", ";CSV;Arbitrary units", nbins, xmin, xmax)
    bb12 = TH2F("bb12", ";CSV1;CSV2;Arbitrary units", nbins, xmin, xmax, nbins, xmin, xmax)
    qq12 = TH2F("qq12", ";CSV1;CSV2;Arbitrary units", nbins, xmin, xmax, nbins, xmin, xmax)
    tree.Project("bb", "fatjet1_CSV", sel+" && "+add+" && fatjet1_flavour==5")
    tree.Project("qq", "fatjet1_CSV", sel+" && "+add+" && fatjet1_flavour!=5")
    tree.Project("bb12", "fatjet1_CSV2:fatjet1_CSV1", sel+" && "+add+" && fatjet1_flavour==5")
    tree.Project("qq12", "fatjet1_CSV2:fatjet1_CSV1", sel+" && "+add+" && fatjet1_flavour!=5")
    #bb12.Draw("LEGO2")
    
    bb.Scale(1./bb.Integral())
    qq.Scale(1./qq.Integral())
    bb12.Scale(1./bb12.Integral())
    qq12.Scale(1./qq12.Integral())
    
    fatjet = TGraph(nbins)
    subjet = TGraph(nbins)
    loose = TGraph(2)
    medium = TGraph(2)
    tight = TGraph(2)
    
    fatjet.SetLineColor(633) #kRed+1
    fatjet.SetLineWidth(3)
    subjet.SetLineColor(418) #kGreen+2
    subjet.SetLineWidth(3)
    loose.SetMarkerStyle(29)
    loose.SetMarkerSize(2.)
    medium.SetMarkerStyle(23)
    medium.SetMarkerSize(2.)
    tight.SetMarkerStyle(20)
    tight.SetMarkerSize(2.)
    
    leg = TLegend(0.25, 0.7, 0.6, 0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0) #1001
    leg.SetFillColor(0)
    leg.AddEntry(fatjet, "fat-jet b-tagging", "l")
    leg.AddEntry(subjet, "sub-jet b-tagging", "l")
    leg.AddEntry(loose, "Loose WP", "p")
    leg.AddEntry(medium, "Medium WP", "p")
    leg.AddEntry(tight, "Tight WP", "p")
    
    for i in range(0, nbins):
        fatjet.SetPoint(i, 1.-bb.Integral(0, i), 1.-qq.Integral(0, i))
        subjet.SetPoint(i, 1.-bb12.Integral(0, i, 0, i), 1.-qq12.Integral(0, i, 0, i))
    
    lbin = bb12.GetXaxis().FindBin(0.605)
    mbin = bb12.GetXaxis().FindBin(0.890)
    tbin = bb12.GetXaxis().FindBin(0.970)
    loose.SetPoint(0, 1.-bb.Integral(0, lbin), 1.-qq.Integral(0, lbin))
    medium.SetPoint(0, 1.-bb.Integral(0, mbin), 1.-qq.Integral(0, mbin))
    tight.SetPoint(0, 1.-bb.Integral(0, tbin), 1.-qq.Integral(0, tbin))
    loose.SetPoint(1, 1.-bb12.Integral(0, lbin, 0, lbin), 1.-qq12.Integral(0, lbin, 0, lbin))
    medium.SetPoint(1, 1.-bb12.Integral(0, mbin, 0, mbin), 1.-qq12.Integral(0, mbin, 0, mbin))
    tight.SetPoint(1, 1.-bb12.Integral(0, tbin, 0, tbin), 1.-qq12.Integral(0, tbin, 0, tbin))
    
    c3 = TCanvas("c3", "sub-jet b-tagging", 800, 600)
    c3.cd()
    c3.GetPad(0).SetTopMargin(0.06)
    c3.GetPad(0).SetRightMargin(0.05)
    c3.GetPad(0).SetTicks(1, 1)
    c3.GetPad(0).SetLogy()
    subjet.SetTitle(";b-jet efficiency;udsg-jet efficiency")
    subjet.GetXaxis().SetRangeUser(0., 1.)
    #subjet.GetYaxis().SetRangeUser(5e-3, 1.)
    subjet.Draw("AL")
    fatjet.Draw("SAME, L")
    loose.Draw("SAME, P")
    medium.Draw("SAME, P")
    tight.Draw("SAME, P")
    leg.Draw()
    c3.Print("plots/Signal/ROC.pdf")
    c3.Print("plots/Signal/ROC.png")
    
    raw_input("Press Enter to continue...")
    pass
'''

def efficiency(cutlist, labellist):
    basecut=""
    if "SSmumu" in cutlist[0]: basecut = "SSmumu"
    if "SSee" in cutlist[0]: basecut = "SSee"
    if "SSemu" in cutlist[0]: basecut = "SSemu"
    #elif "isZtoMM" in cutlist[0]: basecut = "isZtoMM"
    ncuts = len(cutlist)
    file = {}
    tree = {}
    effs = {}
    hist = {}
    #Compute Eff on different cutlist
    for i, s in enumerate(signals):
        file[s] = TFile(NTUPLEDIR + samples[s]['files'][0] + ".root", "READ") # Read TFile
        tree[s] = file[s].Get("Events") # Read TTree                                                                                                                                                       
        effs[s] = [0]*(ncuts+1)
        hist[s] = TH1D(s,";Efficiency",ncuts,0,ncuts)
        for k, cs in enumerate(labellist): hist[s].GetXaxis().SetBinLabel(k+1, "%s" %labellist[k])
        for j, c in enumerate(cutlist):
            n = tree[s].GetEntries(cutlist[j])
            d = tree[s].GetEntries(basecut)
            effs[s][j] = float(n)/(d)
            print "effs[s][j] = ", effs[s][j]
            hist[s].Fill(j,effs[s][j])
        #hist[s].SetMarkerStyle(20)
        #hist[s].SetMarkerColor(colors[i])
        hist[s].SetLineColor(colors[i])
        hist[s].SetLineWidth(3)
        #hist[s].GetXaxis().SetTitleOffset(hist[s].GetXaxis().GetTitleOffset()*1.2)
        #hist[s].GetYaxis().SetTitleOffset(hist[s].GetYaxis().GetTitleOffset()*1.2)
        
    
    leg = TLegend(0.7, 0.9-0.035*len(signals), 0.9, 0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(1001)                                                                                                                                                                           
    leg.SetFillColor(0)
    for i, s in enumerate(signals):
        leg.AddEntry(hist[s], s, "l")
        #leg.AddEntry(hist[s], samples[s]['label'][0], "l")

    c1 = TCanvas("c1", "Signals", 800, 600)
    c1.cd()
    c1.GetPad(0).SetTopMargin(0.06)
    c1.GetPad(0).SetRightMargin(0.05)
    c1.GetPad(0).SetTicks(1, 1)

    hist[signals[0]].SetMaximum(1.3)
    hist[signals[0]].SetMinimum(0.)
    
    for i, s in enumerate(signals):
        if i==0:
            hist[s].GetXaxis().SetTitle("Selection")
            hist[s].GetYaxis().SetTitle("Efficiency")
            #hist[s].GetYaxis().SetRangeUser(0., 1.)
        hist[s].Draw("" if i==0 else "SAME")
    leg.Draw()
    drawCMS(LUMI, "Preliminary")
    drawRegion(basecut)
    
    c1.Print("plots/Signal/Efficiency_" + basecut + ".png")
    c1.Print("plots/Signal/Efficiency_" + basecut + ".pdf")
    if not options.runBash: raw_input("Press Enter to continue...")
    pass

def efficiencyHmass(cutlist, labellist):
    basecut = ""
    
    if "isZtoEE" in cutlist[0]: basecut = "isZtoEE"
    elif "isZtoMM" in cutlist[0]: basecut = "isZtoMM"

    ncuts = len(cutlist)
    
    file = {}
    tree = {}
    effs = {}
    for i, s in enumerate(signals):
        file[s] = TFile(NTUPLEDIR + samples[s]['files'][0] + ".root", "READ") # Read TFile
        tree[s] = file[s].Get("Events") # Read TTree
        effs[s] = [0]*(ncuts+1)
        for j, c in enumerate(cutlist):
            n = tree[s].GetEntries(cutlist[j])
            d = tree[s].GetEntries(basecut)
            effs[s][j] = float(n)/(d)
    
    line = []
    for j, c in enumerate(cutlist):
        line.append( TGraph(ncuts) )
        line[j].SetTitle(";m_{X} (GeV);Efficiency")
        for i, s in enumerate(signals):
            mass = int( ''.join(x for x in s if x.isdigit()) )
            #mass = str( ''.join(x for x in s) )
            line[j].SetPoint(i, mass, effs[s][j])
        line[j].SetMarkerStyle(20)
        line[j].SetMarkerColor(colors[j])
        line[j].SetLineColor(colors[j])
        line[j].SetLineWidth(3)
        line[j].GetXaxis().SetTitleOffset(line[j].GetXaxis().GetTitleOffset()*1.2)
        line[j].GetYaxis().SetTitleOffset(line[j].GetYaxis().GetTitleOffset()*1.2)
    
    leg = TLegend(0.6, 0.2, 0.9, 0.6)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0) #1001
    leg.SetFillColor(0)
    for i, c in enumerate(cutlist):
        leg.AddEntry(line[i], labellist[i], "lp")
    
    c1 = TCanvas("c1", "Signals", 800, 600)
    c1.cd()
    c1.GetPad(0).SetTopMargin(0.06)
    c1.GetPad(0).SetRightMargin(0.05)
    c1.GetPad(0).SetTicks(1, 1)
    line[0].GetXaxis().SetTitle("m_{X} (GeV)")
    line[0].GetYaxis().SetTitle("Efficiency")
    line[0].GetYaxis().SetRangeUser(0., 1.)
    
    for i, s in enumerate(cutlist):
        line[i].Draw("APL" if i==0 else "SAME, PL")
    leg.Draw()
    drawCMS(-1, "Simulation")
    
    c1.Print("plots/Signal/Efficiency_" + basecut + ".png")
    c1.Print("plots/Signal/Efficiency_" + basecut + ".pdf")
    if not options.runBash: raw_input("Press Enter to continue...")
    pass


def significance(precut, cutlist, labellist, testname):

    var = "Ele_pfRelIso03_all[1]"
    ncuts = len(cutlist)
    
    
    file = {}
    tree = {}
    hist = {}
    effs = {}
    psig = {}
    
    # Create and fill MC histograms
    for i, s in enumerate(back+signals):
        nevts = 0
        tree[s] = TChain("Events")
        for j, ss in enumerate(samples[s]['files']):
            print ss
            tree[s].Add(NTUPLEDIR + ss + ".root")
            tfile = TFile(NTUPLEDIR + ss + ".root", "READ")
            nevts += tfile.Get("Events").GetEntries()
            #nevts += tfile.Get("Counters/Counter").GetBinContent(0)
            tfile.Close()
        hist[s] = []
        effs[s] = []
        for j, c in enumerate(cutlist):
            ss = s + "_%d" % j
            if variable[var]['nbins']>0: hist[s].append( TH1F(ss, ";"+variable[var]['title']+";"+variable[var]['titleY'], variable[var]['nbins'], variable[var]['min'], variable[var]['max']) )
            else: hist[s].append( TH1F(ss,";"+variable[var]['title']+";"+variable[var]['titleY'], len(variable[var]['bins'])-1, array('f', variable[var]['bins'])) )            
            hist[s][j].Sumw2()
            effs[s].append( tree[s].Project(ss, var, "1*("+c+")") / float(nevts) )
            print "effs of ",s," for ",j,"th cutlist : ",c," is ", effs[s]
            hist[s][j].SetFillColor(samples[s]['fillcolor'])
            hist[s][j].SetFillStyle(samples[s]['fillstyle'])
            hist[s][j].SetLineColor(samples[s]['linecolor'])
            hist[s][j].SetLineStyle(samples[s]['linestyle'])
            if not 'Data' in s: hist[s][j].Scale(LUMI)
            if 'Wp' in s or 'Wm' in s: hist[s][j].Scale(1.e-2) #hist[s][j].Scale(1.e-2) # Scale to 10 fb
    
    
    hist['BkgSum'] = []
    for j, c in enumerate(cutlist):
        name = 'BkgSum' + "_%d" % j
        hist['BkgSum'].append( hist[back[0]][0].Clone(name) )
        hist['BkgSum'][j].Reset("MICES")
        hist['BkgSum'][j].SetFillStyle(0)
        for i, s in enumerate(back): # Add hist to BkgSum and stack
            hist['BkgSum'][j].Add(hist[s][j])
    
#    for j, c in enumerate(cutlist):
#        c1 = TCanvas("c1", "Signals", 800, 600)
#        c1.cd()
#        hist['BkgSum'][j].Draw("H")
#        for i, s in enumerate(sign): hist[s][j].Draw("SAME, H")
#        if not options.runBash: raw_input("Press Enter to continue...")
    
    for i, s in enumerate(signals):
        psig[s] = [0]*(ncuts+1)
        #mass = float( ''.join(x for x in s if x.isdigit()) )
        amean = hist[s][j].GetMean()
        rms = hist[s][j].GetRMS()
        print "HistName = ", hist[s][j].GetName()," ; meanvalue = ", amean," ; rms = ", rms
        cbin = hist[s][j].FindBin(amean)
        lbin = hist[s][j].FindBin(amean - 2*rms)
        hbin = hist[s][j].FindBin(amean + 2*rms)
        print "Meanvalue bin = ", cbin," ; Meanvalue - 2*rms bin  = ", lbin," ; Meanvalue + 2*rms bin = ", hbin 
        for j, c in enumerate(cutlist):
            n = hist[s][j].Integral(lbin, hbin)
            print j,"th cut ",c," integrate SIGNAL lowbin highbin = ", n
            d = hist['BkgSum'][j].Integral(lbin, hbin)
            print j,"th cut ",c," integrate BACKGROUND lowbin highbin = ", d
            psig[s][j] = effs[s][j]/(1.+math.sqrt(d)) #2.*(math.sqrt(n+d) - math.sqrt(d))
            print "effs[s][j]/(1.+math.sqrt(d)) = ", psig[s][j]
    
    line = []
    for j, c in enumerate(cutlist):
        
        line.append( TGraph(ncuts) )
        line[j].SetTitle(";m_{X} (GeV);Significance")
        line[j].SetTitle("")
        for i, s in enumerate(signals):
            #mass = int( ''.join(x for x in s if x.isdigit()) )
            line[j].SetPoint(i, i+1., psig[s][j])
            line[j].GetXaxis().SetBinLabel(line[j].GetXaxis().FindBin(i+1.), str(s) )
        line[j].SetMarkerStyle(20)
        line[j].SetMarkerColor(colors[j])
        line[j].SetLineColor(colors[j])
        line[j].SetLineWidth(3)
        line[j].GetXaxis().SetTitleOffset(line[j].GetXaxis().GetTitleOffset()*1.2)
        line[j].GetYaxis().SetTitleOffset(line[j].GetYaxis().GetTitleOffset()*1.2)
    
    leg = TLegend(0.12, 0.8-0.04*ncuts, 0.55, 0.8)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0) #1001
    leg.SetFillColor(0)
    for i, c in enumerate(cutlist):
        leg.AddEntry(line[i], labellist[i], "lp")
    
    c1 = TCanvas("c1", "Signals", 800, 600)
    c1.cd()
    c1.GetPad(0).SetTopMargin(0.06)
    c1.GetPad(0).SetRightMargin(0.05)
    c1.GetPad(0).SetTicks(1, 1)
    #line[0].GetYaxis().SetRangeUser(0., 1.)
    line[0].GetXaxis().SetTitle("m_{X} (GeV)")
    line[0].GetYaxis().SetTitle("Punzi FOM = #varepsilon_{s}/(1+#sqrt{B})") #"Q = 2(#sqrt{S+B}-#sqrt{B}) ")
    for i, s in enumerate(cutlist):
        line[i].Draw("APL" if i==0 else "SAME, PL")
    leg.Draw()
    drawCMS(LUMI, "Simulation")
    
    c1.Print("plots/Signal/sign_"+testname+".png")
    c1.Print("plots/Signal/sign_"+testname+".pdf")
    if not options.runBash: raw_input("Press Enter to continue...")
pass



#VOI
'''
from PhysicsTools.NanoAODTools.postprocessing.analysis.variables import *
megalist=[]

megalist += [ "%s"%ibranch.name() for ibranch in branches_global ]
megalist += [ "%s"%ibranch.name() for ibranch in branches_quanta ]
megalist += [ "%s[0]"%ibranch.name() for ibranch in branches_W1gen ]
megalist += [ "%s[0]"%ibranch.name() for ibranch in branches_W2gen ]
megalist += [ "%s[0]"%ibranch.name() for ibranch in branches_W3gen ]

for i in xrange(0,2):
    megalist += [ "%s[%s]"%(ibranch.name(),i) for ibranch in branches_W3gen ]

for i in xrange(0,3):
    megalist += [ "%s[%s]"%(ibranch.name(),i) for ibranch in branches_Genfsw ]

megalist += [ "%s[0]"%ibranch.name() for ibranch in branches_Genfsh ]
megalist += [ "%s[0]"%ibranch.name() for ibranch in branches_GenWstar ]

for i in xrange(0,2):
    megalist += [ "%s[%s]"%(ibranch.name(),i) for ibranch in branches_GenW3Jet ]
    
megalist += [ "%s[0]"%ibranch.name() for ibranch in branches_W1reco ]
megalist += [ "%s[0]"%ibranch.name() for ibranch in branches_W2reco ]
megalist += [ "%s[0]"%ibranch.name() for ibranch in branches_W3reco ]
#megalist += [ "%s[0]"%ibranch.name() for ibranch in branches_recoLL ]

for i in xrange(0,3):
    megalist += [ "%s[%s]"%(ibranch.name(),i) for ibranch in branches_Muons ]
    megalist += [ "%s[%s]"%(ibranch.name(),i) for ibranch in branches_Electrons ]
    megalist += [ "%s[%s]"%(ibranch.name(),i) for ibranch in branches_Taus ]
    megalist += [ "%s[%s]"%(ibranch.name(),i) for ibranch in branches_Photons ]
    megalist += [ "%s[%s]"%(ibranch.name(),i) for ibranch in branches_Jets ]
    
megalist += [ "%s[0]"%ibranch.name() for ibranch in branches_RecoV ]
megalist += [ "%s[0]"%ibranch.name() for ibranch in branches_RecoLJJ ]


#isSSmumu
for var in variable:
    signal(var, "isSSemu")
'''

#signal("isSSmumu","hist")
#signal("isSSee","hist")
#signal("isSSemu","hist")

##genssmumu
#for var in [ \
#             "GenMu_pt[0]" , "GenMu_pt[1]" ,  "GenNeuMu_pt[0]" , "GenNeuMu_pt[1]",  "GenJet_pt[0]" , "GenJet_pt[1]" , \
#             "GenfsW_pt[0]" , "GenfsW_pt[1]" , "GenfsW_pt[2]" , "GenfsW_mass[0]" , "GenfsW_mass[1]" , "GenfsW_mass[2]" , \
#             "GenfsH_pt[0]" ,  "GenfsH_eta[0]" , "GenfsH_mass[0]" , "GenWstar_pt[0]" , "GenWstar_eta[0]" , "GenWstar_mass[0]" , \
#             "GenW1sysdR" , "GenW2sysdR" , "GenW1sysdPhi" , "GenW2sysdPhi" , "GenW3sysdR" , "GenW3sysdPhi" , "GenWHsysdR" , "GenWHsysdPhi" , "GenWWsysdR" , "GenWWsysdPhi" , \
#             "GenLL_pt[0]" , "GenLL_mass[0]" , "GenL2JJ_pt[0]" , "GenL2JJ_mass[0]" , \
#             "GenLLsysdR" , "GenLLsysdPhi" , "GenLsysLJJsysdR" , "GenLsysLJJsysdPhi" \
#]:
#    signal(var, "genssmumu")
#signal("RecoW1Lep_pt[0]", "isSSmumu")
#signal("RecoW2Lep_pt[0]", "isSSmumu")
#signal("RecoW3Jet_pt[0]", "isSSmumu")
#signal("RecoW3Jet_pt[1]", "isSSmumu")
##genssee
#for var in [ \
#             "GenEle_pt[0]" , "GenEle_pt[1]" ,  "GenNeuEle_pt[0]" , "GenNeuEle_pt[1]",  "GenJet_pt[0]" , "GenJet_pt[1]" , \
#             "GenfsW_pt[0]" , "GenfsW_pt[1]" , "GenfsW_pt[2]" , "GenfsW_mass[0]" , "GenfsW_mass[1]" , "GenfsW_mass[2]" , \
#             "GenfsH_pt[0]" ,  "GenfsH_mass[0]" , "GenWstar_pt[0]" , "GenWstar_mass[0]" , \
#             "GenW1sysdR" , "GenW2sysdR" , "GenW1sysdPhi" , "GenW2sysdPhi" , "GenW3sysdR" , "GenW3sysdPhi" , "GenWHsysdR" , "GenWHsysdPhi" , "GenWWsysdR" , "GenWWsysdPhi" , \
#             "GenLL_pt[0]" , "GenLL_mass[0]" , "GenL2JJ_pt[0]" , "GenL2JJ_mass[0]" , \
#             "GenLLsysdR" , "GenLLsysdPhi" , "GenLsysLJJsysdR" , "GenLsysLJJsysdPhi" \
#]:
#    signal(var, "genssee")

##genssemu
#for var in [ \
#             "GenEle_pt[0]" , "GenMu_pt[0]" ,  "GenNeuEle_pt[0]" , "GenNeuMu_pt[0]",  "GenJet_pt[0]" , "GenJet_pt[1]" , \
#             "GenfsW_pt[0]" , "GenfsW_pt[1]" , "GenfsW_pt[2]" , "GenfsW_mass[0]" , "GenfsW_mass[1]" , "GenfsW_mass[2]" , \
#             "GenfsH_pt[0]" ,  "GenfsH_mass[0]" , "GenWstar_pt[0]" , "GenWstar_mass[0]" , \
#             "GenW1sysdR" , "GenW2sysdR" , "GenW1sysdPhi" , "GenW2sysdPhi" , "GenW3sysdR" , "GenW3sysdPhi" , "GenWHsysdR" , "GenWHsysdPhi" , "GenWWsysdR" , "GenWWsysdPhi" , \
#             "GenLL_pt[0]" , "GenLL_mass[0]" , "GenL2JJ_pt[0]" , "GenL2JJ_mass[0]" , \
#             "GenLLsysdR" , "GenLLsysdPhi" , "GenLsysLJJsysdR" , "GenLsysLJJsysdPhi" \
#]:
#    signal(var, "genssemu")

#recossmumu
#for var in [ \
#             "RecoMu_pt[0]" , "RecoMu_pt[1]" ,  "RecoJet_pt[0]" , "RecoJet_pt[1]" , \
#             "RecoMu_mediumId[0]" , "RecoMu_mediumId[1]" , "RecoMu_pfRelIso03_all[0]" , "RecoMu_pfRelIso03_all[1]" , \
#             "RecoL2JJ_pt[0]" , "RecoL2JJ_mass[0]" , "RecoLL_pt[0]" , "RecoLL_mass[0]" , "RecoLLsysdR" , "RecoLLsysdPhi" , "RecoLsysLJJsysdR" , "RecoLsysLJJsysdPhi" \
#]:
#    signal(var, "recossmumu")

#recossee
#for var in [ \
#             "RecoEle_pt[0]" , "RecoEle_pt[1]" ,  "RecoJet_pt[0]" , "RecoJet_pt[1]" , \
#             "RecoEle_cutBased[0]" , "RecoEle_cutBased[1]" , "RecoEle_pfRelIso03_all[0]" , "RecoEle_pfRelIso03_all[1]" , \
#             "RecoL2JJ_pt[0]" , "RecoL2JJ_mass[0]" , "RecoLL_pt[0]" , "RecoLL_mass[0]" , "RecoLLsysdR" , "RecoLLsysdPhi" , "RecoLsysLJJsysdR" , "RecoLsysLJJsysdPhi" \
#]:
#    signal(var, "recossee")

#for var in [ \
#             "RecoEle_pt[0]" , "RecoMu_pt[0]" ,  "RecoJet_pt[0]" , "RecoJet_pt[1]" , \
#             "RecoEle_cutBased[0]" , "RecoMu_mediumId[0]" , "RecoEle_pfRelIso03_all[0]" , "RecoMu_pfRelIso03_all[0]" , \
#             "RecoL2JJ_pt[0]" , "RecoL2JJ_mass[0]" , "RecoLL_pt[0]" , "RecoLL_mass[0]" , "RecoLLsysdR" , "RecoLLsysdPhi" , "RecoLsysLJJsysdR" , "RecoLsysLJJsysdPhi" \
#]:
#    signal(var, "recossemu")
    
#signal("Mu_pt[0]", "OSmumu")

##SSmumu
#trigger="(HLT_IsoMu24 || HLT_IsoTkMu24)"
#trigger="HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL"
Jet="nJets>=2"
#Mu="Mu_pt[0]>25 && Mu_pt[1]>15 && Mu_pfRelIso03_all[0]<0.1"

flag="SSee"
##
#Lcuts=[ flag , flag+"&&"+trigger , flag+"&&"+trigger+" && "+Jet , flag+"&&"+trigger+" && "+Jet+" && "+Mu ]
#Llabs = ["%s"%flag,"Iso/IsoTkMu24", "nJet>=2", "Mu1 Iso03 < 0.1"]
##
#Lcuts=[ flag+" && (HLT_IsoMu24 || HLT_IsoTkMu24)" , flag+" && HLT_IsoMu20" , flag+" && HLT_IsoMu22" , flag+" && HLT_IsoMu22_eta2p1" , flag+" && HLT_IsoTkMu22_eta2p1" , flag+" && HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL" , flag+" && HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ" , flag+" && HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL" , flag+" && HLT_Mu27_TkMu8" , flag+" && HLT_Mu45_eta2p1" , flag+" && HLT_Mu50" ]
#Llabs=[ "(HLT_IsoMu24 || HLT_IsoTkMu24)" , "HLT_IsoMu20" , "HLT_IsoMu22" , "HLT_IsoMu22_eta2p1" , "HLT_IsoTkMu22_eta2p1" , "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL" , "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ" , "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL" , "HLT_Mu27_TkMu8" , "HLT_Mu45_eta2p1" , "HLT_Mu50" ]
#Lcuts=[ flag+" && HLT_Ele27_WPTight_Gsf" , flag+" && HLT_Ele27_WPLoose_Gsf" , flag+" && HLT_Ele27_eta2p1_WPLoose_Gsf" , flag+" && HLT_Ele23_WPLoose_Gsf" , flag+" && HLT_Ele25_WPTight_Gsf" , flag+" && HLT_Ele105_CaloIdVT_GsfTrkIdT" ]
#Llabs=[ "HLT_Ele27_WPTight_Gsf" , "HLT_Ele27_WPLoose_Gsf" , "HLT_Ele27_eta2p1_WPLoose_Gsf" , "HLT_Ele23_WPLoose_Gsf" , "HLT_Ele25_WPTight_Gsf" , "HLT_Ele105_CaloIdVT_GsfTrkIdT" ]
#efficiency(Lcuts, Llabs)

##SSee
#trigger="(HLT_Ele25_WPTight_Gsf)"
#Ele="Ele_pt[0]>25 && Ele_pt[1]>15 && Ele_cutBased[0]>3 && Ele_cutBased[1]>3 && Ele_pfRelIso03_all[0]<0.1"
#flag="SSee"
#Lcuts=[ flag , flag+"&&"+trigger , flag+"&&"+trigger+" && "+Jet , flag+"&&"+trigger+" && "+Jet+" && "+Ele ]
#Llabs = ["SSee","Ele25_WPTight", "nJet>=2", "Ele1 Iso03 < 0.1"]
#efficiency(Lcuts, Llabs)

#SSemu
#trigger="(HLT_IsoMu24 || HLT_IsoTkMu24)"
#trigger="(HLT_Ele25_WPTight_Gsf)"
#Ele="Ele_pt[0]>25 && Mu_pt[1]>15 && Ele_pfRelIso03_all[0]<0.1"
#flag="SSemu"
#Lcuts=[ flag , flag+"&&"+trigger , flag+"&&"+trigger+" && "+Jet , flag+"&&"+trigger+" && "+Jet+" && "+Ele ]
#Llabs = ["SSemu","Ele25_WPTight", "nJet>=2", "Ele1 Iso03 < 0.1"]
#efficiency(Lcuts, Llabs) 

Scut = "SSee && Ele_pt[0]>25 && Ele_pt[1]>15"
Scuts = [Scut, Scut+" && Ele_cutBased[0]>3 && Ele_pfRelIso03_all[0]<0.1", Scut+" && Ele_cutBased[0]==4 && Ele_pfRelIso03_all[0]<0.1"]
Slabs = ["base cut", "Ele_cutBased[0]>3", "Ele_cutBased[0]==4"]
Sname = "ssmumuDefault"
significance(Scut, Scuts, Slabs, Sname)

############################################
#btag()


#Ecuts = [TriEle, TriEle+" && "+PreEle, TriEle+" && "+PreEle+" && "+Zcut, TriEle+" && "+PreEle+" && "+Zcut+" && "+Hcut, TriEle+" && "+PreEle+" && "+Zcut+" && "+Hcut+" && "+Bcut]
#Mcuts = [TriMuo, TriMuo+" && "+PreMuo, TriMuo+" && "+PreMuo+" && "+Zcut, TriMuo+" && "+PreMuo+" && "+Zcut+" && "+Hcut, TriMuo+" && "+PreMuo+" && "+Zcut+" && "+Hcut+" && "+Bcut]
#Lcuts = [TriLep, PreLep, PreLep+" && "+Zcut, PreLep+" && "+Zcut+" && "+Hcut, PreLep+" && "+Zcut+" && "+Hcut+" && "+Bcut]
#Llabs = ["Trigger", "Id + Iso", "Z cand", "H mass", "b-tag"]
#efficiency(Lcuts, Llabs, "XZZ")


#Scut = "isZtoLL && "+PreLep+" && "+Zcut

# Mass
#Scuts = [Scut, Scut+" && (fatjet1_softdropMass>90 && fatjet1_softdropMass<145)", Scut+" && (fatjet1_softdropMass>90 && fatjet1_softdropMass<140)", Scut+" && (fatjet1_softdropMass>95 && fatjet1_softdropMass<140)", Scut+" && (fatjet1_softdropMass>95 && fatjet1_softdropMass<135)", Scut+" && (fatjet1_softdropMass>95 && fatjet1_softdropMass<130)", Scut+" && (fatjet1_softdropMass>100 && fatjet1_softdropMass<135)", Scut+" && (fatjet1_softdropMass>100 && fatjet1_softdropMass<130)"]
#Scuts = [Scut, Scut+" && (fatjet1_prunedMass>90 && fatjet1_prunedMass<145)", Scut+" && (fatjet1_prunedMass>90 && fatjet1_prunedMass<140)", Scut+" && (fatjet1_prunedMass>95 && fatjet1_prunedMass<140)", Scut+" && (fatjet1_prunedMass>95 && fatjet1_prunedMass<135)", Scut+" && (fatjet1_prunedMass>95 && fatjet1_prunedMass<130)", Scut+" && (fatjet1_prunedMass>100 && fatjet1_prunedMass<135)", Scut+" && (fatjet1_prunedMass>100 && fatjet1_prunedMass<130)"]
#Slabs = ["no cut (pruned)", "90<m_{j}<145 GeV", "90<m_{j}<140 GeV", "95<m_{j}<140 GeV", "95<m_{j}<135 GeV", "95<m_{j}<130 GeV", "100<m_{j}<135 GeV", "100<m_{j}<130 GeV"]
#Scuts = [Scut, Scut+" && (fatjet1_prunedMassCorr>90 && fatjet1_prunedMassCorr<135)", Scut+" && (fatjet1_prunedMassCorr>90 && fatjet1_prunedMassCorr<140)", Scut+" && (fatjet1_prunedMassCorr>95 && fatjet1_prunedMassCorr<135)", Scut+" && (fatjet1_prunedMassCorr>100 && fatjet1_prunedMassCorr<130)", Scut+" && (fatjet1_prunedMassCorr>105 && fatjet1_prunedMassCorr<135)", Scut+" && (fatjet1_prunedMassCorr>105 && fatjet1_prunedMassCorr<140)", Scut+" && (fatjet1_prunedMassCorr>105 && fatjet1_prunedMassCorr<145)"]
#Slabs = ["no cut (pruned)", "90<m_{j}<135 GeV", "90<m_{j}<140 GeV", "95<m_{j}<135 GeV", "100<m_{j}<130 GeV", "105<m_{j}<135 GeV", "105<m_{j}<140 GeV", "105<m_{j}<145 GeV"]
#significance(Scut, Scuts, Slabs, Sname)


#Scut = "isZtoLL && "+PreLep+" && "+Zcut+" && "+Hcut

## Btag
#Scuts = [Scut, Scut+" && fatjet1_CSV>0.605", Scut+" && fatjet1_CSV>0.890", Scut+" && fatjet1_CSV>0.970", Scut+" && fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605", Scut+" && fatjet1_CSV1>0.890 && fatjet1_CSV2>0.890", Scut+" && fatjet1_CSV1>0.970 && fatjet1_CSV2>0.970"] #, Scut+" && (fatjet1_dR>0.3 ? fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605 : fatjet1_CSV>0.605)"
#Slabs = ["No b-tag", "fat-jet CSVL", "fat-jet CSVM", "fat-jet CSVT", "sub-jet CSVLL", "sub-jet CSVMM", "sub-jet CSVTT"] #, "sub/fat-jet CSVLL/L"
#Sname = "btagDefault"
#significance(Scut, Scuts, Slabs, Sname)

## Switch Sub/Fat-jet
#Scuts = [Scut, Scut+" && fatjet1_CSV>0.605", Scut+" && fatjet1_CSV>0.890", Scut+" && fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605", Scut+" && fatjet1_CSV1>0.890 && fatjet1_CSV2>0.890", Scut+" && (fatjet1_dR>0.3 ? fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605 : fatjet1_CSV>0.605)", Scut+" && (fatjet1_dR>0.3 ? fatjet1_CSV1>0.890 && fatjet1_CSV2>0.890 : fatjet1_CSV>0.890)"]
#Slabs = ["No b-tag", "fat-jet CSVL", "fat-jet CSVM", "sub-jet CSVLL", "sub-jet CSVMM", "sub/fat-jet CSVLL/L", "sub/fat-jet CSVMM/M"]
#Sname = "btagSubFat"
#significance(Scut, Scuts, Slabs, Sname)

## Btag Ultraloose
#Scuts = [Scut, Scut+" && fatjet1_CSV>0.3", Scut+" && fatjet1_CSV>0.605", Scut+" && fatjet1_CSV1>0.3 && fatjet1_CSV2>0.3", Scut+" && fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605", Scut+" && (fatjet1_dR>0.3 ? fatjet1_CSV1>0.3 && fatjet1_CSV2>0.3 : fatjet1_CSV>0.3)", Scut+" && (fatjet1_dR>0.3 ? fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605 : fatjet1_CSV>0.605)"]
#Slabs = ["No b-tag", "fat-jet CSVU", "fat-jet CSVL", "sub-jet CSVUU", "sub-jet CSVLL", "sub/fat-jet CSVUU/U", "sub/fat-jet CSVLL/L"]
#Sname = "btagUltra"
#significance(Scut, Scuts, Slabs, Sname)

## Btag asymm
#Scuts = [Scut, Scut+" && fatjet1_CSV>0.605", Scut+" && fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605", Scut+" && (fatjet1_dR>0.3 ? fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605 : fatjet1_CSV>0.605)", Scut+" && (fatjet1_dR>0.3 ? fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605 : fatjet1_CSV1>0.605 || fatjet1_CSV2>0.605)", Scut+" && fatjet1_CSV>0.3", Scut+" && fatjet1_CSV1>0.3 && fatjet1_CSV2>0.3", Scut+" && (fatjet1_dR>0.3 ? fatjet1_CSV1>0.3 && fatjet1_CSV2>0.3 : fatjet1_CSV>0.3)", Scut+" && (fatjet1_dR>0.3 ? fatjet1_CSV1>0.3 && fatjet1_CSV2>0.3 : fatjet1_CSV1>0.3 || fatjet1_CSV2>0.3)"]
#Slabs = ["No b-tag", "fat-jet CSVL", "sub-jet CSVLL", "sub/fat-jet CSVLL/L", "sub-jet CSVL(L)", "fat-jet CSVU", "sub-jet CSVUU", "sub/fat-jet CSVUU/U", "sub-jet CSVU(U)"]
#Sname = "btagAsymm"
#significance(Scut, Scuts, Slabs, Sname)

## Btag dR
#Scuts = [Scut, Scut+" && (fatjet1_dR>0.2 ? fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605 : fatjet1_CSV1>0.605 || fatjet1_CSV2>0.605)", Scut+" && (fatjet1_dR>0.25 ? fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605 : fatjet1_CSV1>0.605 || fatjet1_CSV2>0.605)", Scut+" && (fatjet1_dR>0.3 ? fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605 : fatjet1_CSV1>0.605 || fatjet1_CSV2>0.605)", Scut+" && (fatjet1_dR>0.35 ? fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605 : fatjet1_CSV1>0.605 || fatjet1_CSV2>0.605)", Scut+" && (fatjet1_dR>0.4 ? fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605 : fatjet1_CSV1>0.605 || fatjet1_CSV2>0.605)", Scut+" && (fatjet1_dR>0.5 ? fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605 : fatjet1_CSV1>0.605 || fatjet1_CSV2>0.605)"]
#Slabs = ["No b-tag", "sub-jet CSVL(L) #Delta R=0.2", "sub-jet CSVL(L) #Delta R=0.25", "sub-jet CSVL(L) #Delta R=0.3", "sub-jet CSVL(L) #Delta R=0.35", "sub-jet CSVL(L) #Delta R=0.4", "sub-jet CSVL(L) #Delta R=0.5"]
#Sname = "btagDR"
#significance(Scut, Scuts, Slabs, Sname)

##Scut = "isZtoLL && "+PreLep+" && "+Zcut+" && "+Hcut+" && "+Bcut

## Tau21
#Scuts = [Scut, Scut+" && fatjet1_tau21<0.3", Scut+" && fatjet1_tau21<0.4", Scut+" && fatjet1_tau21<0.45", Scut+" && fatjet1_tau21<0.5", Scut+" && fatjet1_tau21<0.55", Scut+" && fatjet1_tau21<0.6", Scut+" && fatjet1_tau21<0.7"]
#Slabs = ["no cut", "#tau_{21}<0.3", "#tau_{21}<0.4", "#tau_{21}<0.45", "#tau_{21}<0.5", "#tau_{21}<0.55", "#tau_{21}<0.6", "#tau_{21}<0.7"]
#Sname = "tau21"
#significance(Scut, Scuts, Slabs, Sname)

