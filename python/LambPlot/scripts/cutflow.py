#! /usr/bin/env python

import os, multiprocessing
import copy
import math
from array import array
from ROOT import ROOT, gROOT, gStyle, gRandom, TSystemDirectory
from ROOT import TFile, TChain, TTree, TCut, TH1, TH1F, TH2F, THStack, TGraph, TGraphAsymmErrors
from ROOT import TStyle, TCanvas, TPad
from ROOT import TLegend, TLatex, TText, TLine, TBox

from PhysicsTools.NanoAODTools.LambPlot.Utils.configs import Config
import PhysicsTools.NanoAODTools.LambPlot.Utils.color as col
from PhysicsTools.NanoAODTools.LambPlot.Utils.drawLambda import *
import importlib

from collections import OrderedDict
ROOT.EnableImplicitMT(12)

########## SETTINGS ##########

import optparse
usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
parser.add_option("-v", "--variable", action="store", type="string", dest="variable", default="")
parser.add_option("-c", "--cut", action="store", type="string", dest="cut", default="")
parser.add_option("-r", "--region", action="store", type="string", dest="region", default="")
parser.add_option("-b", "--bash", action="store_true", default=False, dest="bash")
parser.add_option("-z", "--backgrounds", action="append", type="string", default=[], dest="backgrounds" )
parser.add_option("-l", "--cutfile",  dest="cutfile", type="string", default=None)
parser.add_option("-y", "--year", action="store", type="string", dest="year", default="2016")

(options, args) = parser.parse_args()
if options.bash: gROOT.SetBatch(True)

cfg = Config(options.year)
samples = cfg.getModule('samples')
variables = cfg.getModule('variables')
groupPlot = cfg.getModule('groupPlot')

base=os.environ['NANOAODTOOLS_BASE']

########## SETTINGS ##########

#NTUPLEDIR   = "/Users/shoh/Projects/CMS/PhD/Analysis/SSL/datav8-skim/"
LUMI        = cfg.lumi()
sign        = [ x for x in groupPlot if groupPlot[x]['isSignal'] == 1 ]
#back        = [ x for x in groupPlot if groupPlot[x]['isSignal'] == 0 ] if len(options.backgrounds)==0 else options.backgrounds
back = [ 'Fake' , 'WZ' , 'VgS' ]

# for fake
cacheList=[
    "Fake_mm",
    "Fake_em",
    "Fake_ee",
    "Lepton_pt",
    "Lepton_pdgId",
    "Lepton_eta",
    "nCleanJet",
    "nLepton",
    "CleanJet_pt",
    "CleanJet_eta"
    ]
########## ######## ##########

def printTablev1(hist, sign=[]):
    samplelist = [x for x in hist.keys() if not 'data' in x and not 'BkgSum' in x and not x in sign and not x=="files"]
    for x in hist.keys():
        if 'data_obs' in x:
            datalist=hist['data_obs']
        else:
            datalist=["0",1]
    #print(datalist)
    #print(len(datalist))
    print "|\t\t|",
    for i in samplelist:
        print "%s\t |" %i,
    print " MC\t | DATA\t | DATA/MC\t |"
    print "-"*80
    count=0

        #print (samplelist[i]) # bkg key
        #print (hist[samplelist[i]]) #list of value in bkg key
        #print (len(hist[samplelist[i]])) #number of cut in pair
        #print((hist[samplelist[i]][0])[0]) # first cut first element -> triggerbit
        #print (len(samplelist)) -> 2
    for l in range(0,len(hist[samplelist[0]])):
        print "|%s\t|" %((hist[samplelist[0]][l])[0]), # order cut
        count=0
        MC=0
        for i in range(0,len(samplelist)):
            print "%-10.2f |" %((hist[samplelist[i]][l])[1]),
            MC+=(hist[samplelist[i]][l])[1]
        print "%-10.2f |" %MC,
        if len(data)==0:
            print "%-10.2f |" %datalist[1],
            print "%-10.2f |" %((datalist[1]/MC)*100)
        else:
            print "%-10.2f |" %datalist[l][1],
            print "%-10.2f |" %((datalist[l][1]/MC)*100)
    print "-"*80

def printTable_html(hist,sign=[]):
    samplelist = [x for x in hist.keys() if not 'data' in x and not 'BkgSum' in x and not x in sign and not x=="files"]
    ###SORRY, its not working, will check 
    if len(data)>0:
        datalist=hist['data_obs']
    #for x in hist.keys():
    #    if 'data_obs' in x:
    #        datalist=hist['data_obs']
    #    else:
    #        datalist=["0",1]
    #print(datalist)
    #print(len(datalist))

    print '<!DOCTYPE html>'
    print '<html>'
    print '<head>'
    print '<style>'
    print 'table, th, td {'
    print 'border: 1px solid black;}'
    print 'background-color: lemonchiffon;'
    print '</style>'
    print '<table>'
    print '<tr>'
    print '<th></th>'

    for i in samplelist:
        print "<th>%s</th>" %i,
    if len(data)==0:
        print "<th>MC</th>"
    else:
        print "<th>MC</th><th>DATA</th><th>DATA/MC</th>"
    print '</tr>'

    for l in range(0,len(hist[samplelist[0]])):
        print '<tr>'
        print "<th>%s</th>" %((hist[samplelist[0]][l])[0]) # order cut 
        count=0
        MC=0
        for i in range(0,len(samplelist)):
            print "<th>%-10.2f</th>" %((hist[samplelist[i]][l])[1])
            MC+=(hist[samplelist[i]][l])[1]
        print "<th>%-10.2f</th>" %MC
        if len(data)>0:
        #    print "<th>%-10.2f</th>" %datalist[1]
        #    print "<th>%-10.2f</th>" %((datalist[1]/MC)*100)
        #else:
            print "<th>%-10.2f</th>" %datalist[l][1]
            print "<th>%-10.2f</th>" %((datalist[l][1]/MC)*100)
        print '</tr>'
    print '</table>'
    print '</head>'
    print '</html>'
    
if __name__ == "__main__":

    fake=False
    cfile = open( options.cutfile ,'r')
    cutlist = OrderedDict()
    cutlist['default'] = '1==1'
    for iline in cfile.readlines():
        line = iline.strip("\n")
        cutlist[line.split('$')[0]] = line.split('$')[1]
    cfile.close()

    if 'Fake' in back:
        back.remove('Fake')
        fake=True
    
    DF=OrderedDict()
    for itag in back+sign:
        print " --> itag : ", itag 
        DF[itag]=OrderedDict()
        for isample in groupPlot[itag]['samples']:
            DF[itag][isample] = OrderedDict() ; isptr= False
            if 'weights' in samples[isample].keys() :
                for jsample in samples[isample]['weights'].keys() :
                    WEIGHTS = '(%s)*(%s)' %( expressAliases(samples[isample]['weight']) , samples[isample]['weights'][jsample] )
                    if itag not in [ 'Fake' , 'DATA' ]: WEIGHTS = "%s*(%s)" %( str(float(LUMI)/1000.) , WEIGHTS )
                    filelist = [ x for x in samples[isample]['name'] if os.path.basename(x).split('_',1)[-1].replace('.root','').split('__part')[0] == jsample ]
                    files = makeVectorList(filelist)
                    #print " --> Caching in subsamples : ", jsample
                    DF[itag][isample][jsample] = ROOT.RDataFrame("Events", files).Define( "weight" , WEIGHTS ) #.Cache();
            else:
                isptr = True
                WEIGHTS = expressAliases(samples[isample]['weight'])
                if itag not in [ 'Fake' , 'DATA' ]: WEIGHTS = "%s*(%s)" %( str(float(LUMI)/1000.) , WEIGHTS )
                filelist = samples[isample]['name']
                files = makeVectorList(filelist)
                #print " --> Caching in samples : ", isample
                DF[itag][isample] = ROOT.RDataFrame("Events", files).Define( "weight" , WEIGHTS ) #.Cache();
    ###########################################################
    df_result= OrderedDict()
    
    if fake:
        DF_fake=OrderedDict()
        DF_fake['Fake']=OrderedDict()
        # only one fake sample will do
        for jsample in samples['Fake_em']['weights'].keys() :
            filelist = [ x for x in samples['Fake_em']['name'] if os.path.basename(x).split('_',1)[-1].replace('.root','').split('__part')[0] == jsample ]
            files = makeVectorList(filelist) ; commonWeight = samples['Fake_em']['weights'][jsample]
            DF_fake['Fake'][jsample] = ROOT.RDataFrame("Events", files).Define( 'W1', commonWeight )
            for ifake in [ 'Fake_mm' , 'Fake_em' , 'Fake_ee' ]:
                DF_fake['Fake'][jsample] = DF_fake['Fake'][jsample].Define( ifake , 'W1*(%s)' % ( expressAliases(samples[ifake]['weight']) ) )
            # caching Fake
            print "caching fake : ", jsample
            DF_fake['Fake'][jsample] = DF_fake['Fake'][jsample].Cache(cacheList)
        
        df_result['Fake'] = OrderedDict()
        for jsample in DF_fake['Fake']:
            print "Fake : jsample : ", jsample
            icutter=[]
            for i, labcut in enumerate(cutlist) :
                icut = cutlist[labcut]
                icutter.append(icut)
                if i==0: icut_ = icut
                else: icut_ = ' && '.join(icutter)
                print "icut_ : ", icut_
                df_result['Fake'][labcut]=0.
                for ifake in [ 'Fake_mm' , 'Fake_em' , 'Fake_ee' ]:
                    print "ifake : ", ifake
                    df_result['Fake'][labcut] += float(DF_fake['Fake'][jsample].Filter( icut_ ).Sum(ifake).GetValue())
                
    #############################################################

    for itag in DF:
        print "itag : ", itag
        df_result[itag]=OrderedDict()
        # iterate cut                                                                                                                                                                                       
        icutter=[]
        for i, labcut in enumerate(cutlist) :
            icut = cutlist[labcut]
            icutter.append(icut)
            if i==0: icut_ = icut
            else: icut_ = ' && '.join(icutter)
            print "icut_ : ", icut_
            # dict[Fake][Cut1]=number                                                                                                                                                                       
            df_result[itag][labcut]=0.
            # Fake_mm/em                                                                                                                                                                                    
            for isample in DF[itag]:
                print "isample : ", isample
                # weighted subsamples                                                                                                                                                                       
                if isinstance(DF[itag][isample],OrderedDict):
                    for jsample in DF[itag][isample]:
                        df_result[itag][labcut] += float(DF[itag][isample][jsample].Filter( icut_ ).Sum('weight').GetValue())
                else:
                    df_result[itag][labcut] += float(DF[itag][isample].Filter( icut_ ).Sum('weight').GetValue())
    print "*"*80
    for itag in df_result:
        print itag
        for icut in df_result[itag]:
            print "icut : ", icut , " ; events : ", df_result[itag][icut]

