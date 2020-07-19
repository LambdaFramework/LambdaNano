#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from whss import whssConstr

class skimmer:

    def __init__(self):
        self.samples={}

    def initialization(self):

        data = [
            'Run2016_SingleMuon',
            'Run2016_SingleElectron',
            'Run2016_SingleMuon_fake',
            'Run2016_SingleElectron_fake'
        ]

        mc = [
            "DYJetsToLL_M-50-LO_ext2",
            "DYJetsToLL_M-10to50-LO",
            "TTTo2L2Nu",
            "ST_s-channel",
            "ST_t-channel_antitop",
            "ST_t-channel_top",
            "ST_tW_antitop",
            "ST_tW_top",
            "WWTo2L2Nu",
            "WpWmJJ_EWK_noTop",
            "GluGluWWTo2L2Nu_MCFM",
            "Wg_MADGRAPHMLM",
            "Zg",
            "WZTo3LNu_mllmin01",
            "WZTo2L2Q",
            "ZZTo2L2Nu",
            "ZZTo2L2Q",
            "ZZTo4L",
            "ZZZ",
            "WZZ",
            "WWZ",
            "WWW",
            "GluGluHToWWTo2L2NuPowheg_M125",
            "VBFHToWWTo2L2Nu_M125",
            "HZJ_HToWW_M125",
            "ggZH_HToWW_M125",
            "HWplusJ_HToWW_M125",
            "HWminusJ_HToWW_M125",
            "GluGluHToTauTau_M125",
            "VBFHToTauTau_M125",
            "HZJ_HToTauTau_M125",
            "HWplusJ_HToTauTau_M125",
            "HWminusJ_HToTauTau_M125"
        ]

        fnames= mc + data
        
        for i in fnames:
            sample_files = open( "%s/scripts/filelists/%s.txt" %(os.getcwd(),i) , "r" )
            self.samples[i] = [ x.strip('\n') for x in sample_files.readlines() ]
            sample_files.close()
    
    def run(self):
    
        for isample in self.samples:
            if not os.path.isdir( '%s/skimmed/%s/' %(os.getcwd(),isample) ): os.mkdir( '%s/skimmed/%s/' %(os.getcwd(),isample) )

            print(self.samples[isample])
            p=PostProcessor(
                outputDir='%s/skimmed/%s/' %(os.getcwd(),isample) ,
                inputFiles=self.samples[isample] ,
                cut="mll>12 && Lepton_pt[0]>25 && Lepton_pt[1]>20 && bVeto && PuppiMET_pt > 30",
                branchsel="%s/scripts/slimming-in.txt" %os.getcwd() ,
                modules=[ whssConstr() ] ,
                compression="LZMA:9",
                friend=False,
                postfix=None,
                jsonInput=None,
                noOut=False,
                justcount=False,
                provenance=False,
                haddFileName=None,
                fwkJobReport=False,
                histFileName=None,
                histDirName=None,
                outputbranchsel="%s/scripts/slimming-out.txt" %os.getcwd() ,
                maxEntries=None,
                firstEntry=0,
                prefetch=False,
                longTermCache=False
            )
            p.run()

if __name__ == "__main__" :
    
    if os.getcwd().split('/')[-1] != 'NanoAODTools' :
        print "Please run the scripts from NanoAODTools folder."
        sys.exit()
        
    if not os.path.isdir('%s/skimmed' %os.getcwd()):
        os.mkdir('%s/skimmed' %os.getcwd())

    skim = skimmer()
    skim.initialization()
    skim.run()
