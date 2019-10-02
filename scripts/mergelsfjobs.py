#!/usr/bin/env python
import os, re
import multiprocessing
import commands
import math, time
import sys
from ROOT import TObject, TFile, TH1, TH1F
from array import array
from PhysicsTools.NanoAODTools.postprocessing.modules.datasets import *

# use the following lists to include/exclude samples to be merged

blacklist = []

whitelist = [
#    'GluGluToAToZhToLLBB_M900_13TeV-amcatnlo',
#    'GluGluToAToZhToLLBB_M1000_13TeV-amcatnlo',
]



########## DO NOT TOUCH BELOW THIS POINT ##########

import argparse

parser = argparse.ArgumentParser(description='combine the LSF outputs into one tree')
parser.add_argument('folder', help='the folder containing the LSF output')
args = parser.parse_args()

if not os.path.exists(os.path.expandvars(args.folder)):
    print '--- ERROR ---'
    print '  \''+args.folder+'\' path not found'
    print '  please point to the correct path to the folder containing the LSF output' 
    print 
    exit()

jobs = []


def nanoHadd(name):
    if len(whitelist)>0 and not name in whitelist: return
    if len(blacklist)>0 and name in blacklist: return
    
    os.system(\
              'python '+os.environ["CMSSW_BASE"]+'/src/PhysicsTools/NanoAODTools/scripts/haddnano.py '+name+'.root '+name+'/*/*.root' \
              if 'CMSSW_BASE' in os.environ else \
              'python '+os.environ['NANOAODTOOLS_BASE']+'/scripts/haddnano.py '+name+'.root '+name+'/*/*.root' \
    )
    
    #Add weight
    era=args.folder.split('-')[0]
    files = TFile('%s.root' %name,"UPDATE")
    if 'Run' in name:
        weight = 1.
    else:
        mc = list(filter(lambda x : x.filename()==name, datasets[era]['mc']))[0]
        nevents = files.Get('Events').GetEntries('counter==1')
        xs = float(mc.xsec()) * float(mc.kfactor())
        weight = float(datasets[era]['lumi']) * xs / nevents

    tree = files.Get("Events")
    tree.SetWeight(weight)
    tree.AutoSave()
    
pass

subdirs = [x for x in os.listdir(args.folder) if os.path.isdir(os.path.join(args.folder, x))]

os.chdir(args.folder)

for s in subdirs:
    p = multiprocessing.Process(target=nanoHadd, args=(s,))
    jobs.append(p)
    p.start()

os.system('cd ..')
