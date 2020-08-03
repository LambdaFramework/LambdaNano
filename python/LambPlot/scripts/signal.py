#! /usr/bin/env python

import os,sys
import copy
import math
from array import array
from ROOT import gROOT, gRandom, TSystemDirectory
from ROOT import TFile, TChain, TTree, TCut, TH1F, TH2F, THStack, TGraph, TGraphAsymmErrors, TEfficiency
from ROOT import TStyle, TCanvas, TPad, TPaveStats
from ROOT import TLegend, TLatex, TText

cwd=os.getcwd()
sys.path.append(cwd+"/Utils/")

import PhysicsTools.NanoAODTools.plotter.Utils.color as col
from PhysicsTools.NanoAODTools.plotter.Utils.drawLambda import *
#from PhysicsTools.NanoAODTools.plotter.Utils.variables import variable
from PhysicsTools.NanoAODTools.plotter.Utils.selections import *
from PhysicsTools.NanoAODTools.plotter.Utils.sampleslist import *
#from PhysicsTools.NanoAODTools.Config import *
from PhysicsTools.NanoAODTools.plotter.lambPlot import cfg
import color as col

##################################
#YEAR = 'Run2_16'
#NanoVER = 'NanoV4'
#cfg=Config(YEAR,NanoVER)
#cfg.summary()
##################################

gROOT.Macro('functions.C')

import optparse
usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
parser.add_option("-b", "--bash", action="store_true", default=False, dest="runBash")
parser.add_option("-s", "--Psignal", action="store_true", default=False, dest="plot")
parser.add_option("-c", "--Acc", action="store_true", default=False, dest="acc")
parser.add_option("-x", "--signf", action="store_true", default=False, dest="significance")
parser.add_option("-d", "--cf", action="store_true", default=False, dest="cutflow")


(options, args) = parser.parse_args()

print options
print args

if options.runBash: gROOT.SetBatch(True)

########## SETTINGS ##########
stats=True
if not stats:
    gStyle.SetOptStat(0)
else:
    gStyle.SetOptStat(1111)
LUMI        = cfg.lumi() #35800. #140000 #35800. # in pb-1
RATIO       = 4 # 0: No ratio plot; !=0: ratio between the top and bottom pads
NTUPLEDIR   = cfg.ntuple()
NTUPLESIG   = '/Users/shoh/Projects/CMS/PhD/Analysis/SSL/NanoAODTools/test/'
#back = [ "tZq", "WWJJ", "VVV", "ttV" , "WW", "ZZ", "WZ", "Vg", "ST", "WJetsToLNu_HT", "TTbar", "DYJetsToLL_HT" ]
back = [ "tZq", "WWJJ", "VVV"]
#signals         = ['wmhww', 'wphww']
signals         = ['whww']
colors = [616+4, 632, 800+7, 800, 416+1, 860+10, 600, 616, 921, 922]

def plotsignal(var, cut):
    hist={}

    ## Project into histogram
    hist= ProjectDraw(var, cut, LUMI, signals, [], NTUPLESIG)
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
        hist[signals[0]].SetMaximum(hmax*6)

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

    if var.split('_')[0] in ['R','nR']:
        fol="RECO"
    elif var.split('_')[0] in ['G','nG']:
        fol="GEN"
    else:
        fol="ANALYSIS"

    drawCMS(LUMI, fol+" Simulation ")
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
    if not os.path.exists('plots/Signal/'+fol+'/'): os.system('mkdir -p plots/Signal/'+fol+'/')
    c1.Print("plots/Signal/"+fol+'/'+var+".pdf")
    c1.Print("plots/Signal/"+fol+'/'+var+".png")

    print col.WARNING+"PURGE OBJECTS IN MEMORY"+col.ENDC
    for process in hist:
        hist[process].Delete()

    #c1.Delete()
    #if not options.runBash: raw_input("Press Enter to continue...")
    pass

def significanceSB(cutlist, labellist):

    basecut=labellist[0]
    dim = len(cutlist)
    significance = [0]*(dim+1)

    file = {}
    tree = {}
    effs = {}
    hist = {}
    GrAsym = {}
    yErrorUp = {}
    yErrorDown = {}
    totEve=0
    GrAsym = TGraphAsymmErrors()
    cuts=""

    for j, c in enumerate(cutlist):
        s=0. ; b=0.
        cuts+=cutlist[0] if j==0 else " && "+cutlist[j]
        print "cuts = ", cuts
        for num1,v in enumerate(signals):
            #print "Signal = ", v
            for num2,filename in enumerate(samples[v]['files']):
                #print "Signal rootfile read = ",  filename
                file[filename] = TFile(NTUPLESIG + filename + ".root", "READ") # Read TFile
                tree[filename] = file[filename].Get("Events") # Read TTree
                nevents = float(sample[filename]['nevents'])
                xs = float(sample[filename]['xsec'])*float(sample[filename]['kfactor'])
                LumiMC = nevents/xs
                Weight = float(LUMI) / float(LumiMC)

                sig_entries = tree[filename].GetEntries(cuts)
                #print "s = ", float(sig_entries) * float(Weight)
                s+= float(sig_entries) * float(Weight)
            print "TOT SIG = ", s

        for num1,k in enumerate(back):
            #print "backgrounds = ", k
            for num2,filename in enumerate(samples[k]['files']):
                #print "backgrounds rootfile read = ",  filename
                file[filename] = TFile(NTUPLEDIR + filename + ".root", "READ") # Read TFile
                tree[filename] = file[filename].Get("Events") # Read TTree
                nevents = float(sample[filename]['nevents'])
                xs = float(sample[filename]['xsec'])*float(sample[filename]['kfactor'])
                LumiMC = nevents/xs
                Weight = float(LUMI) / float(LumiMC)

                bkg_entries = tree[filename].GetEntries(cuts)
                #print "b = ", float(bkg_entries) * float(Weight)
                b+= float(bkg_entries) * float(Weight)
            print "TOT BKG = ", b

        ##End of cutlist
        #COMPUTE
        #print "s = ", s
        #print "b = ", b
        #print "sqrt(b) = ",  math.sqrt(b)
        #print "significance = ",  float(s/math.sqrt(b))
        significance[j] = float(s/math.sqrt(b))
        yErrorUp[j] = float(TEfficiency.ClopperPearson(math.sqrt(b),s,0.68, True) - significance[j])
        yErrorDown[j] = float(significance[j] - TEfficiency.ClopperPearson(math.sqrt(b),s,0.68, False))
        GrAsym.SetPoint(j,j+0.5,significance[j])
        GrAsym.SetPointError(j,0,0,yErrorUp[j],yErrorDown[j])

    for k, cs in enumerate(labellist):
        GrAsym.GetHistogram().GetXaxis().Set(dim,0,dim);
        GrAsym.GetHistogram().GetXaxis().SetBinLabel(k+1, "%s" %labellist[k])

    GrAsym.SetLineColor(2)
    GrAsym.SetLineWidth(3)
    GrAsym.SetMarkerStyle(8)
    GrAsym.SetMarkerColor(2)

    c1 = TCanvas("c1", "Signals Acceptance", 800, 600)
    c1.cd()
    c1.GetPad(0).SetTopMargin(0.06)
    c1.GetPad(0).SetRightMargin(0.05)
    c1.GetPad(0).SetTicks(1, 1)

    gStyle.SetOptStat(0)

    #GrAsym.SetMaximum(1.3)
    #GrAsym.SetMinimum(0.)

    GrAsym.GetHistogram().GetXaxis().SetTitle("")
    GrAsym.GetHistogram().GetYaxis().SetTitle("Significance (S/#sqrt{B})")

    GrAsym.Draw("pa")
    drawCMS(LUMI, "Work In Progress")
    drawRegion(basecut)

    if not os.path.exists('plots/Signal/Significance/'): os.system('mkdir -p plots/Signal/Significance/')
    c1.Print("plots/Signal/Significance/Sigf_SB_" + basecut + ".png")
    c1.Print("plots/Signal/Significance/Sigf_SB_" + basecut + ".pdf")
    #if not options.runBash: raw_input("Press Enter to continue...")
    pass

def cutflow(cutlist, labellist):

    #Plot and table

    basecut=labellist[0]
    ncuts = len(cutlist)
    #significance = [0]*(dim+1)

    file = {}
    tree = {}
    Sig_hist = TH1D('Sig_hist',";Sig_hist",ncuts,0,ncuts)
    Bkg_hist = TH1D('Bkg_hist',";Bkg_hist",ncuts,0,ncuts)

    for k, cs in enumerate(labellist): Sig_hist.GetXaxis().SetBinLabel(k+1, "%s" %labellist[k])
    for k, cs in enumerate(labellist): Bkg_hist.GetXaxis().SetBinLabel(k+1, "%s" %labellist[k])

    cuts=""

    for j, c in enumerate(cutlist):
        s=0. ; b=0.
        cuts+=cutlist[0] if j==0 else " && "+cutlist[j]
        print "cuts = ", cuts
        for num1,v in enumerate(signals):
            #print "Signal = ", v
            for num2,filename in enumerate(samples[v]['files']):
                #print "Signal rootfile read = ",  filename
                file[filename] = TFile(NTUPLESIG + filename + ".root", "READ") # Read TFile
                tree[filename] = file[filename].Get("Events") # Read TTree
                nevents = float(sample[filename]['nevents'])
                xs = float(sample[filename]['xsec'])*float(sample[filename]['kfactor'])
                LumiMC = nevents/xs
                Weight = float(LUMI) / float(LumiMC)

                sig_entries = tree[filename].GetEntries(cuts)
                #print "s = ", float(sig_entries) * float(Weight)
                s+= float(sig_entries) * float(Weight)
            print "TOT SIG = ", s

        for num1,k in enumerate(back):
            #print "backgrounds = ", k
            for num2,filename in enumerate(samples[k]['files']):
                #print "backgrounds rootfile read = ",  filename
                file[filename] = TFile(NTUPLEDIR + filename + ".root", "READ") # Read TFile
                tree[filename] = file[filename].Get("Events") # Read TTree
                nevents = float(sample[filename]['nevents'])
                xs = float(sample[filename]['xsec'])*float(sample[filename]['kfactor'])
                LumiMC = nevents/xs
                Weight = float(LUMI) / float(LumiMC)

                bkg_entries = tree[filename].GetEntries(cuts)
                #print "b = ", float(bkg_entries) * float(Weight)
                b+= float(bkg_entries) * float(Weight)
            print "TOT BKG = ", b

        ##Fill signal and backgrounds
        Sig_hist.Fill(j,s)
        Bkg_hist.Fill(j,b)

    Sig_hist.SetLineColor(2)
    Sig_hist.SetLineWidth(3)
    Bkg_hist.SetLineColor(3)
    Bkg_hist.SetLineWidth(3)

    leg = TLegend(0.7, 0.9-0.035*len(signals), 0.9, 0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(1001)
    leg.SetFillColor(0)
    leg.AddEntry(Sig_hist, "signal event", "l")
    leg.AddEntry(Bkg_hist, "background event", "l")
    leg.SetTextSize(0.03)

    c1 = TCanvas("c1", "cutflow", 800, 600)
    c1.cd()
    c1.GetPad(0).SetTopMargin(0.06)
    c1.GetPad(0).SetRightMargin(0.05)
    c1.GetPad(0).SetTicks(1, 1)
    gStyle.SetOptStat(0)

    c1.SetLogy()

    Sig_hist.GetXaxis().SetTitle("Selection")
    Sig_hist.GetYaxis().SetTitle("Events")

    Bkg_hist.Draw()
    Sig_hist.Draw("SAME")
    leg.Draw()
    drawCMS(LUMI, "Work In Progress")
    drawRegion(basecut)

    if not os.path.exists('plots/Signal/Cutflow/'): os.system('mkdir -p plots/Signal/Cutflow/')
    c1.Print("plots/Signal/Cutflow/Cf_" + basecut + ".png")
    c1.Print("plots/Signal/Cutflow/Cf_" + basecut + ".pdf")
    #if not options.runBash: raw_input("Press Enter to continue...")
    pass
'''
def printTable(hist, sign=[]):
    samplelist = [x for x in hist.keys() if not 'data' in x and not 'BkgSum' in x and not x in sign and not x=="files"]
    print "Sample                  Events          Entries         %"
    print "-"*80
    for i, s in enumerate(['data_obs']+samplelist+['BkgSum'] if 'data_obs' in hist.keys() else samplelist+['BkgSum']):
        if i==1 or s=="data_obs" or i==len(samplelist)+1: print "-"*80
        #Events                           #Entries
        print "%-20s" % s, "\t%-10.2f" % hist[s].Integral(), "\t%-10.0f" % (hist[s].GetEntries()-2), "\t%-10.2f" % (100.*hist[s].Integral()/hist['BkgSum'].Integral()) if hist['BkgSum'].Integral() > 0 els\
e 0, "%"
    print "-"*80
    for i, s in enumerate(sign):
        if not samples[s]['plot']: continue
        #print "%-20s" % s, "\t%-10.2f" % hist[s].Integral(), "\t%-10.0f" % (hist[s].GetEntries()-2), "\t%-10.2f" % (100.*hist[s].GetEntries()/float(hist[s].GetOption())) if float(hist[s].GetOption()) > \
0 else 0, "%"
        print "%-20s" % s, "\t%-10.2f" % hist[s].Integral(), "\t%-10.0f" % (hist[s].GetEntries()-2), "\t%-10.2f" % (hist[s].GetEntries()) if float(hist[s].GetEntries()) > 0 else 0, "%"
    print "-"*80
pass
'''

def cutflowAnalysis(cutlist, labellist):

    #Plot and table
    basecut=labellist[0]
    ncuts = len(cutlist)
    #significance = [0]*(dim+1)

    file = {}
    tree = {}
    Sig_hist = TH1D('Sig_hist',";Sig_hist",ncuts,0,ncuts)
    Bkg_hist = {}
    b={};

    for k, cs in enumerate(labellist): Sig_hist.GetXaxis().SetBinLabel(k+1, "%s" %labellist[k])
    for num1,k in enumerate(back):
        Bkg_hist[k]=TH1D(k,";Bkg_hist",ncuts,0,ncuts)
        for z, cs in enumerate(labellist): Bkg_hist[k].GetXaxis().SetBinLabel(z+1, "%s" %labellist[z])

    cuts=""

    for j, c in enumerate(cutlist):
        s=0. ; b[j]={};
        cuts+=cutlist[0] if j==0 else " && "+cutlist[j]
        print "cuts = ", cuts
        for num1,v in enumerate(signals):
            #print "Signal = ", v
            for num2,filename in enumerate(samples[v]['files']):
                #print "Signal rootfile read = ",  filename
                file[filename] = TFile(NTUPLESIG + filename + ".root", "READ") # Read TFile
                tree[filename] = file[filename].Get("Events") # Read TTree
                nevents = float(sample[filename]['nevents'])
                xs = float(sample[filename]['xsec'])*float(sample[filename]['kfactor'])
                LumiMC = nevents/xs
                Weight = float(LUMI) / float(LumiMC)

                sig_entries = tree[filename].GetEntries(cuts)
                #print "s = ", float(sig_entries) * float(Weight)
                s+= float(sig_entries) * float(Weight)
            print "TOT SIG = ", s

        Sig_hist.Fill(j,s)

        ##Each background process has TH1D
        for num1,k in enumerate(back):
            print "backgrounds = ", k
            b[j][k]=0.

            for num2,filename in enumerate(samples[k]['files']):
                file[filename] = TFile(NTUPLEDIR + filename + ".root", "READ") # Read TFile
                tree[filename] = file[filename].Get("Events") # Read TTree
                nevents = float(sample[filename]['nevents'])
                xs = float(sample[filename]['xsec'])*float(sample[filename]['kfactor'])
                LumiMC = nevents/xs
                Weight = float(LUMI) / float(LumiMC)

                bkg_entries = tree[filename].GetEntries(cuts)
                b[j][k]+= float(bkg_entries) * float(Weight)
            print "TOT BKG = ", b

            #Creat histogram for filling
            Bkg_hist[k].Fill(j,b[j][k])


    '''
    Sig_hist.SetLineColor(2)
    Sig_hist.SetLineWidth(3)

    leg = TLegend(0.7, 0.9-0.035*len(signals), 0.9, 0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(1001)
    leg.SetFillColor(0)
    leg.AddEntry(Sig_hist, "signal event", "l")
    #leg.AddEntry(Bkg_hist, "background event", "l")
    leg.SetTextSize(0.03)

    print "len(Bkg_hist) = ", len(Bkg_hist)
    for num,k in enumerate(Bkg_hist):
        Bkg_hist[k].SetLineColor(colors[num])
        Bkg_hist[k].SetLineWidth(3)
        leg.AddEntry(Bkg_hist[k], k, "l")

    c1 = TCanvas("c1", "cutflow", 800, 600)
    c1.cd()
    c1.GetPad(0).SetTopMargin(0.06)
    c1.GetPad(0).SetRightMargin(0.05)
    c1.GetPad(0).SetTicks(1, 1)
    gStyle.SetOptStat(0)

    c1.SetLogy()

    Sig_hist.GetXaxis().SetTitle("Selection")
    Sig_hist.GetYaxis().SetTitle("Events")

    for num,k in enumerate(Bkg_hist):
        Bkg_hist[k].Draw("" if num==0 else "SAME")
    Sig_hist.Draw("SAME")
    leg.Draw()
    drawCMS(LUMI, "Work In Progress")
    drawRegion(basecut)

    if not os.path.exists('plots/Signal/Cutflow/'): os.system('mkdir -p plots/Signal/Cutflow/')
    c1.Print("plots/Signal/Cutflow/Cf_" + basecut + ".png")
    c1.Print("plots/Signal/Cutflow/Cf_" + basecut + ".pdf")
    '''
    #if not options.runBash: raw_input("Press Enter to continue...")
    pass

def acceptance(cutlist, labellist):
    basecut=cutlist[0]
    dim = len(cutlist)
    #cutlist.remove(cutlist[:1][0])

    if basecut=='SSemu':
        basecutstr='((Lepton_pdgId[0]*Lepton_pdgId[1]==11*13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*-13))'
    elif basecut=='SSmue':
        basecutstr='((Lepton_pdgId[0]*Lepton_pdgId[1]==13*11)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-13*-11))'
    elif basecut=='SSee':
        basecutstr='((Lepton_pdgId[0]*Lepton_pdgId[1]==11*11)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*-11))'
    elif basecut=='SSmumu':
        basecutstr='((Lepton_pdgId[0]*Lepton_pdgId[1]==13*13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-13*-13))'

    cutlist = [ basecutstr if x==basecut else x for x in cutlist ]

    file = {}
    tree = {}
    effs = {}
    hist = {}
    GrAsym = {}
    yErrorUp = {}
    yErrorDown = {}
    totEve=0

    #Compute Eff on different triggers
    for i, s in enumerate(signals):
        file[s] = TFile(NTUPLESIG + samples[s]['files'][0] + ".root", "READ") # Read TFile
        tree[s] = file[s].Get("Events") # Read TTree
        effs[s] = [0]*(dim+1)
        yErrorUp[s] = [0]*(dim+1)
        yErrorDown[s] = [0]*(dim+1)
        totEve = tree[s].GetEntries(basecutstr)
        GrAsym[s] = TGraphAsymmErrors()
        for j, c in enumerate(cutlist):
            n = tree[s].GetEntries(basecutstr+" && "+cutlist[j])
            effs[s][j] = float(n)/(totEve)
            yErrorUp[s][j] = float(TEfficiency.ClopperPearson(totEve,n,0.68, True) - effs[s][j])
            yErrorDown[s][j] = float(effs[s][j] - TEfficiency.ClopperPearson(totEve,n,0.68, False))
            GrAsym[s].SetPoint(j,j+0.5,effs[s][j])
            # i , exl, exh, eyl, eyh
            GrAsym[s].SetPointError(j,0,0,yErrorUp[s][j],yErrorDown[s][j])

        GrAsym[s].SetLineColor(colors[i])
        GrAsym[s].SetLineWidth(3)
        GrAsym[s].SetMarkerStyle(8)
        GrAsym[s].SetMarkerColor(colors[i])

        for k, cs in enumerate(labellist):
            GrAsym[s].GetHistogram().GetXaxis().Set(dim,0,dim);
            GrAsym[s].GetHistogram().GetXaxis().SetBinLabel(k+1, "%s" %labellist[k])



    leg = TLegend(0.7, 0.9-0.035*len(signals), 0.9, 0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(1001)
    leg.SetFillColor(0)
    for i, s in enumerate(signals):
        leg.AddEntry(GrAsym[s], s, "l")
        #leg.AddEntry(hist[s], samples[s]['label'][0], "l")

    c1 = TCanvas("c1", "Signals Acceptance", 800, 600)
    c1.cd()
    c1.GetPad(0).SetTopMargin(0.06)
    c1.GetPad(0).SetRightMargin(0.05)
    c1.GetPad(0).SetTicks(1, 1)

    gStyle.SetOptStat(0)

    GrAsym[signals[0]].SetMaximum(1.3)
    GrAsym[signals[0]].SetMinimum(0.)

    for i, s in enumerate(signals):
        if i==0:
            GrAsym[s].GetHistogram().GetXaxis().SetTitle("Trigg")
            GrAsym[s].GetHistogram().GetYaxis().SetTitle("Signal Acceptance")
            #hist[s].GetYaxis().SetRangeUser(0., 1.)
        GrAsym[s].Draw("pa" if i==0 else "SAME p")
    leg.Draw()
    drawCMS(LUMI, "Work In Progress")
    drawRegion(basecut)

    if not os.path.exists('plots/Signal/Acceptance/'): os.system('mkdir -p plots/Signal/Acceptance/')
    c1.Print("plots/Signal/Acceptance/Acc_" + basecut + ".png")
    c1.Print("plots/Signal/Acceptance/Acc_" + basecut + ".pdf")

    #if not options.runBash: raw_input("Press Enter to continue...")
    pass

dict={
    'SSemu': {
        'cutlist' : ['((Lepton_pdgId[0]*Lepton_pdgId[1]==11*13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*-13))', '(HLT_IsoMu24 || HLT_IsoTkMu24)', 'nLepton>=2','nCleanJet>=2', 'Lepton_pt[0]>30','Lepton_pt[1]>20','Vll_mass>15','Lepton_pfRelIso03_all[0]<0.15'],
        'labellist' : ['SSemu','HLT_IsoMu24','nLepton>=2','nCleanJet>=2','Lepton_pt[0]>30','Lepton_pt[1]>20','Vll_mass>15','Lepton_pfRelIso03_all[0]<0.15'],
        'efflist' : ['SSemu', 'HLT_IsoMu20', 'HLT_IsoMu22', '(HLT_IsoMu22_eta2p1 || HLT_IsoTkMu22_eta2p1)' ,'(HLT_IsoMu24 || HLT_IsoTkMu24)', 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL','HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ','HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL','HLT_Mu27_TkMu8','HLT_Mu45_eta2p1','HLT_Mu50', \
            'HLT_Ele23_WPLoose_Gsf','HLT_Ele25_WPTight_Gsf','HLT_Ele27_WPLoose_Gsf','HLT_Ele27_WPTight_Gsf','HLT_Ele27_eta2p1_WPLoose_Gsf','HLT_Ele27_eta2p1_WPLoose_Gsf','HLT_Ele105_CaloIdVT_GsfTrkIdT'],
        },
    'SSmue': {
        'cutlist' : ['((Lepton_pdgId[0]*Lepton_pdgId[1]==13*11)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-13*-11))', '(HLT_IsoMu24 || HLT_IsoTkMu24)', 'nLepton>=2','nCleanJet>=2', 'Lepton_pt[0]>30','Lepton_pt[1]>20','Vll_mass>15'],
        'labellist' : ['SSmue','HLT_IsoMu24','nLepton>=2','nCleanJet>=2','Lepton_pt[0]>30','Lepton_pt[1]>20','Vll_mass>15'],
        'efflist' : ['SSmue', 'HLT_IsoMu20', 'HLT_IsoMu22', '(HLT_IsoMu22_eta2p1 || HLT_IsoTkMu22_eta2p1)' ,'(HLT_IsoMu24 || HLT_IsoTkMu24)', 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL','HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ','HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL','HLT_Mu27_TkMu8','HLT_Mu45_eta2p1','HLT_Mu50', \
            'HLT_Ele23_WPLoose_Gsf','HLT_Ele25_WPTight_Gsf','HLT_Ele27_WPLoose_Gsf','HLT_Ele27_WPTight_Gsf','HLT_Ele27_eta2p1_WPLoose_Gsf','HLT_Ele27_eta2p1_WPLoose_Gsf','HLT_Ele105_CaloIdVT_GsfTrkIdT'],
            },
    'SSee': {
        'cutlist' : ['((Lepton_pdgId[0]*Lepton_pdgId[1]==11*11)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*-11))' ,'(HLT_Ele25_WPTight_Gsf || HLT_Ele27_eta2p1_WPLoose_Gsf || HLT_Ele27_eta2p1_WPLoose_Gsf)' , 'nLepton>=2', 'nCleanJet>=2' , 'Lepton_pt[0]>30', 'Lepton_pt[1]>20','Lepton_pfRelIso03_all[0]<0.1'],
        'labellist' : ['SSee','HLT_Ele25/27','nLepton>=2','nCleanJet>=2','Lepton_pt[0]>30', 'Lepton_pt[1]>20','Lepton_Iso03[0]<0.1'],
        'efflist' : ['SSee', 'HLT_IsoMu20', 'HLT_IsoMu22', '(HLT_IsoMu22_eta2p1 || HLT_IsoTkMu22_eta2p1)' ,'(HLT_IsoMu24 || HLT_IsoTkMu24)', 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL','HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ','HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL','HLT_Mu27_TkMu8','HLT_Mu45_eta2p1','HLT_Mu50', \
            'HLT_Ele23_WPLoose_Gsf','HLT_Ele25_WPTight_Gsf','HLT_Ele27_WPLoose_Gsf','HLT_Ele27_WPTight_Gsf','HLT_Ele27_eta2p1_WPLoose_Gsf','HLT_Ele27_eta2p1_WPLoose_Gsf','HLT_Ele105_CaloIdVT_GsfTrkIdT'],
        },
    'SSmumu': {
        'cutlist' : ['((Lepton_pdgId[0]*Lepton_pdgId[1]==13*13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-13*-13))' , '(HLT_IsoMu24 || HLT_IsoTkMu24)' , 'nLepton>=2', 'nCleanJet>=2' , 'Lepton_pt[0]>25','Lepton_pt[1]>15','Lepton_pfRelIso03_all[0]<0.1' ],
        'labellist' : ['SSmumu','HLT_IsoMu24','nLepton>=2','nCleanJet>=2','Lepton_pt[0]>25','Lepton_pt[1]>15','Lepton_Iso03_[0]<0.1'],
        'efflist' : ['SSmumu', 'HLT_IsoMu20', 'HLT_IsoMu22', '(HLT_IsoMu22_eta2p1 || HLT_IsoTkMu22_eta2p1)' ,'(HLT_IsoMu24 || HLT_IsoTkMu24)', 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL','HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ','HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL','HLT_Mu27_TkMu8','HLT_Mu45_eta2p1','HLT_Mu50', \
            'HLT_Ele23_WPLoose_Gsf','HLT_Ele25_WPTight_Gsf','HLT_Ele27_WPLoose_Gsf','HLT_Ele27_WPTight_Gsf','HLT_Ele27_eta2p1_WPLoose_Gsf','HLT_Ele27_eta2p1_WPLoose_Gsf','HLT_Ele105_CaloIdVT_GsfTrkIdT'],
        },

    }

if options.plot:
    print "Plotting Gen-level, Reco-level and Analysis-level Signal kinematics"
    #VOI
    ##Run2_16.NanoV4
    from PhysicsTools.NanoAODTools.postprocessing.analysis.Run2_16.NanoV4.genvariables import *
    from PhysicsTools.NanoAODTools.postprocessing.analysis.Run2_16.NanoV4.genvariables import br_global as genGlobal
    from PhysicsTools.NanoAODTools.postprocessing.analysis.Run2_16.NanoV4.variables import *
    from PhysicsTools.NanoAODTools.postprocessing.analysis.Run2_16.NanoV4.variables import br_global as anaGlobal

    megalist=[]

    megalist += [ ibranch.name() for ibranch in genGlobal+br_RecoVll+br_RecoVl2JJ+br_RecoVjj+anaGlobal+br_Vll + br_Vl2JJ + br_Vjj ]
    vectorbranch = [ br_GenLeptons1 , br_GenLeptons2 , br_GenJets , br_RecoLeptons1 , br_RecoLeptons2 , br_RecoJets , br_RecoJetGamma , br_GenJetGamma , br_RecoISR, br_GenISR, br_CleanJets, br_Leptons ]
    for v in vectorbranch:
        for i in xrange(0,3):
            megalist += [ "%s[%s]"%(ibranch.name(),i) for ibranch in v ]

    for var in megalist:
        plotsignal(var, "reco")

#########
elif options.significance:
    print "Plotting Significance of signal on background in different cuts"

    #significanceSB(dict['SSmumu']['cutlist'],dict['SSmumu']['labellist'])
    for key,value in dict.iteritems():
        print key
        significanceSB(value['cutlist'],value['labellist'])

elif options.cutflow:
    print "Plotting cutflow of signal and background in different cuts"

    #cutflow(dict['SSemu']['cutlist'],dict['SSemu']['labellist'])
    cutflowAnalysis(dict['SSemu']['cutlist'],dict['SSemu']['labellist'])
    #for key,value in dict.iteritems():
    #    print key
    #    cutflow(value['cutlist'],value['labellist'])

elif options.acc:
    print "Plotting on Signal Acceptance with different trigger on different signal region"

    for key,value in dict.iteritems():
        print key
        acceptance(dict[key]['efflist'],dict[key]['efflist'])

else:
    print "Input please..."
