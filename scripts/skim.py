#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.analysis.WHSS.bVetoProducer import bVetoer
from PhysicsTools.NanoAODTools.postprocessing.modules.analysis.WHSS.lepSFProducerCpp import lepSF
from PhysicsTools.NanoAODTools.postprocessing.modules.analysis.WHSS.pujetIdSFProducerCpp import pujetIdSF 

from multiprocessing import Process, Pool, Queue, Manager
import multiprocessing, time

class skimmer:

    def __init__(self, dataset_ , outfolder_ ):
        self.dataset_ = dataset_
        self.outfolder_ = outfolder_
        self.samples={}
        self.modules = [ lepSF() , pujetIdSF() , bVetoer() ]

        if not os.path.isdir('%s/%s' %( os.getcwd() , self.outfolder_ ) ): os.mkdir('%s/%s' %( os.getcwd() , self.outfolder_ ) )
        
        pass

    def _load(self, basename ):
        if "/%s_cc.so" %basename not in ROOT.gSystem.GetLibraries():
            print "Load C++ %s.cc worker module" %basename
            base = os.getenv("NANOAODTOOLS_BASE")
            ROOT.gROOT.ProcessLine(".L %s/src/%s.cc+O" %(base,basename) )
        pass

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
        
        #dummy = [ "ZZZ" , "WZZ" , "WWW" , "ZZTo2L2Q" , "ST_s-channel" ]
        #dummy = [ "TTTo2L2Nu" , "ZZTo4L" ]
        dummy = [ "TTTo2L2Nu" ]
        
        if self.dataset_ == 0 :
            fnames = data + mc # no, dont run this
            self.modules = []
        elif self.dataset_ == 1 :
            fnames = mc
        elif self.dataset_ == 2 :
            fnames = data ; self.modules = []
        else :    
            fnames = dummy # testing

        # load libraries only once
        if self.dataset_ == 1 or self.dataset_ > 2 :
            self._load("lepSFProducerCpp")
            self._load("pujetIdSFProducerCpp")
        
        print("Running on : " if self.dataset_ < 3 else "Running on dummy : ", fnames)
        
        for i in fnames:
            sample_files = open( "%s/scripts/filelists/%s.txt" %(os.getcwd(),i) , "r" )
            self.samples[i] = [ x.strip('\n') for x in sample_files.readlines() ]
            sample_files.close()
        pass
    
    def run( self , infiles , supercuts ):

        # data species
        isMC = False if 'Run' in infiles[0].split('/')[-1] else True
        
        p=PostProcessor(
            outputDir='%s/%s/%s/' %( os.getcwd() , self.outfolder_ , isample ) ,
            inputFiles=infiles ,
            cut=supercuts,
            branchsel= "%s/scripts/data/slimming-2016-in.txt" %os.getcwd(),
            modules= self.modules ,
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
            outputbranchsel = "%s/scripts/data/slimming-2016-out.txt" %os.getcwd(),
            maxEntries=None,
            firstEntry=0,
            prefetch=False,
            longTermCache=False
        )
        p.run()
        pass

    
## Parallelism helper
def putQueue( func , arg1 ,arg2 , queue ):
    queue.put( func(arg1,arg2) )
    pass
def readQueue( nbatch , queue ):
    print "Processing the ", nbatch  ,"th batch of files"
    queue.get()
    pass

def parallalizedByFiles( filelist , presel, q, target , nsplit=20 ):

    print "Total number of files : ", len(filelist)
    print "Total number of files per jobs : ", nsplit
    
    sublist=[] ; counter=0 ; njobs=0
    for i, ifile in enumerate(filelist):
        counter+=1 ; sublist.append(ifile)
        ## number of file perjobs                                                                                                                                                                   
        if counter == nsplit or i+1 == len(filelist) :
            Process(target=putQueue, args=( target , sublist , presel, q)).start()
            # reset
            njobs+=1 ; counter=0 ; sublist=[]
            
    print "Total number of jobs : ", njobs
    procs = []
    for j in range(njobs): procs.append(p.apply_async( readQueue , (j+1 , q) ))
    [ r.get() for r in procs ]
    
    pass

if __name__ == "__main__" :

    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] -d dataset -o outputfolder")

    usage = "usage: %prog [options]"
    parser.add_option("-d", "--dataset", action="store", type="int", dest="dataset", default=None , help="specify which dataset to run, 0 : all ; 1 : mc ; 2 : data ; >3 : dummy" )
    parser.add_option("-o", "--outfolder", action="store", type="string", dest="outfolder", default="skimmed" , help="name of the output folder [default: skimmed]")
    (options, args) = parser.parse_args()

    options.outfolder = options.outfolder if options.dataset < 3 else "dummy"
    
    if os.getcwd().split('/')[-1] != 'LambdaNano' :
        print "Please run the scripts from LambdaNano folder."
        sys.exit()
    
    if options.dataset == None :
        parser.print_help()
        sys.exit()

    start_time = time.time()

    ############################################################################
    presel="mll>12 && Lepton_pt[0]>25 && Lepton_pt[1]>20 && PuppiMET_pt > 30"
    skim = skimmer( options.dataset , options.outfolder )
    skim.initialization()
    
    print "Number of cpu : ", multiprocessing.cpu_count()

    # number of task/process
    nTask = 20

    # Parallelism
    if options.dataset == 1 : # mc
        procs = []
        for isample in skim.samples:
            # TTbar is a big file , parallizedByFile
            if isample== "TTTo2L2Nu" : continue
            filelist = skim.samples[isample]
            proc = Process(target=skim.run, args=(filelist,presel,))
            procs.append(proc) ; proc.start()

        [ r.join() for r in procs  ]
        
        ##
        if "TTTo2L2Nu" in skim.samples:
            m = Manager() ; q = m.Queue() ; p = Pool(12)
            for ittbar in skim.samples["TTTo2L2Nu"] : parallalizedByFiles( ittbar , presel, q , skim.run , round(float(len(filelist))/nTask) )
    
    elif options.dataset == 2 : # data
    
        m = Manager() ; q = m.Queue() ; p = Pool(12)
        for isample in skim.samples:
            filelist = skim.samples[isample]
            parallalizedByFiles( filelist , presel, q , skim.run , round(float(len(filelist))/nTask) )
    elif options.dataset == 0 : # run all

        procs = []
        for isample in skim.samples:
            # TTbar is a big file , parallizedByFile
            if isample== "TTTo2L2Nu" : continue
            if "Run" in isample : continue
            filelist = skim.samples[isample]
            proc = Process(target=skim.run, args=(filelist,presel,))
            procs.append(proc) ; proc.start()

        [ r.join() for r in procs  ]

        m = Manager() ; q = m.Queue() ; p = Pool(12)

        if "TTTo2L2Nu" in skim.samples:
            for ittbar in skim.samples["TTTo2L2Nu"] : parallalizedByFiles( ittbar , presel, q , skim.run , round(float(len(filelist))/nTask) )

        for isample in skim.samples:
            if "Run" not in isample : continue
            filelist = skim.samples[isample]
            parallalizedByFiles( filelist , presel, q , skim.run , round(float(len(filelist))/20) )
    else:
        m = Manager() ; q = m.Queue() ; p = Pool(12)
        for isample in skim.samples:
            filelist = skim.samples[isample]
            parallalizedByFiles( filelist , presel, q , skim.run , round(float(len(filelist))/nTask) )
        
    
    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- %s minutes ---" % ( (time.time() - start_time)/60. ))
    print("--- %s hours ---" % ( (time.time() - start_time)/3600. ))
