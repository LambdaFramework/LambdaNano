#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.analysis.WHSS.bVetoProducer import  bVetoProducer #bVetoer
from PhysicsTools.NanoAODTools.postprocessing.modules.analysis.WHSS.lepSFProducerCpp import lepSFProducerCpp #lepSF
from PhysicsTools.NanoAODTools.postprocessing.modules.analysis.WHSS.pujetIdSFProducerCpp import pujetIdSFProducerCpp #pujetIdSF
from PhysicsTools.NanoAODTools.postprocessing.modules.analysis.WHSS.aliasProducer import alias
from PhysicsTools.NanoAODTools.postprocessing.modules.analysis.WHSS.eleFlipSFProducerCpp import eleFlipSFProducerCpp
#from PhysicsTools.NanoAODTools.postprocessing.modules.analysis.ChargeFlips.ChargeFlipWeight import ChargeFlipWeight #flipSF

from multiprocessing import Process, Pool, Queue, Manager
import multiprocessing, time
import random

class skimmer:

    def __init__(self, dataset_ , outfolder_ , year_ ):
        self.dataset_ = dataset_
        self.outfolder_ = outfolder_
        self.year_ = year_
        self.samples={}
        self.modules = []

        if not os.path.isdir('%s/%s' %( os.getcwd() , self.outfolder_ ) ): os.mkdir('%s/%s' %( os.getcwd() , self.outfolder_ ) )

        pass

    def _load(self, basename ):
        if "/%s_cc.so" %basename not in ROOT.gSystem.GetLibraries():
            print "Load C++ %s.cc worker module" %basename
            base = os.getenv("NANOAODTOOLS_BASE")
            ROOT.gROOT.ProcessLine(".L %s/src/%s.cc+O" %(base,basename) )
        pass

    def initialization(self):
        if not os.environ['NANOAODTOOLS_BASE']:
            print("ERROR: NANOAODTOOLS_BASE not set"); sys.exit();

        theList = map( lambda x: x.split('.')[0] , os.listdir( '%s/scripts/filelists/%s' %( os.environ["NANOAODTOOLS_BASE"] , self.year_ ) ) )
        data = [ x for x in theList if any(y in x for y in [ 'Single' ,'Double' , 'EG' ]) ]
        mc = list(set(theList)^set(data))

        dummy = [ "ZZZ" ] #, "WZZ" , "WWW" , "ZZTo2L2Q" , "ST_s-channel" ]

        if   self.dataset_ == 0 : fnames = data + mc ; # no, dont run this
        elif self.dataset_ == 1 : fnames = mc ;
        elif self.dataset_ == 2 : fnames = data ;
        else : fnames = dummy # testing

        ###### modules ############
        bVetoer   = lambda : bVetoProducer        ( self.year_ )
        lepSF     = lambda : lepSFProducerCpp     ( self.year_ , 2 , 'total_SF' )
        pujetIdSF = lambda : pujetIdSFProducerCpp ( self.year_ , 'loose' )
        flipSF    = lambda : eleFlipSFProducerCpp ( self.year_ , 2 , 'total_SF' )

        if self.dataset_ == 1 or self.dataset_ > 2 : self.modules = [ lepSF() , pujetIdSF() , bVetoer() , flipSF() , alias() ]
        if self.dataset_ == 2 : self.modules = [ bVetoer() , alias() ]

        # load libraries only once
        if self.dataset_ == 1 or self.dataset_ > 2 :
            self._load("lepSFProducerCpp")
            self._load("pujetIdSFProducerCpp")

        print("Running on : " if self.dataset_ < 3 else "Running on dummy : ", fnames)

        for i in fnames :
            sample_files = open( "%s/scripts/filelists/%s/%s.txt" %( os.environ["NANOAODTOOLS_BASE"] , self.year_ , i ) , "r" )
            self.samples[i] = [ x.strip('\n') for x in sample_files.readlines() ]
            sample_files.close()
        pass

    def run( self , infiles , supercuts ):

        p=PostProcessor(
            outputDir='%s/%s/%s/' %( os.getcwd() , self.outfolder_ , isample ) ,
            inputFiles=infiles ,
            cut=supercuts,
            branchsel= "%s/scripts/data/slimming-%s-in.txt" %( os.getcwd() , self.year_ ),
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
            outputbranchsel = "%s/scripts/data/slimming-%s-in.txt" %( os.getcwd() , self.year_ ),
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
    try:
        queue.get()
    except queue.Empty:
        print 'ERROR occur at processing the ', nbatch , "th batch of files"
        sys.exit();
    pass

def parallalizedByFiles( filelist , presel, q, target , nsplit=20 ):

    print "Total number of files : ", len(filelist)
    print "Total number of files per jobs : ", round(nsplit)

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
    parser.add_option("-y", "--year", action="store", type="string", dest="year", default="2016" , help="data-taking year [default: 2016]")
    parser.add_option("-o", "--outfolder", action="store", type="string", dest="outfolder", default="skimmed" , help="name of the output folder [default: skimmed]")
    parser.add_option("-s", "--serialism", action="store_true", dest="serialism", default=False , help="toggle parallelism/serialism in python, useful for testing [default: False]")

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
    # Preselection
    presel="mll>12 && Lepton_pt[0]>25 && Lepton_pt[1]>20 && PuppiMET_pt > 30"

    skim = skimmer( options.dataset , '%s-%s' %(options.outfolder,options.year) , options.year )
    skim.initialization()

    print "Number of cpu : ", multiprocessing.cpu_count()

    # number of task/process
    #nTask = 30
    nTask = 40

    # Parallelism (in production mode, parallelism always on)
    if options.dataset == 1 : # mc

        procs = []

        ## Big files, needed parallisim at process level
        BigFile_16 = [ "TTTo2L2Nu" , "DYJetsToLL_M-50-LO_ext2" ]
        BigFile_17 = [ "TTTo2L2Nu" , "DYJetsToLL_M-50-LO_ext1" , "ttHToNonbb_M125" ]
        BigFile_18 = [ "TTTo2L2Nu" , "DYJetsToLL_M-50-LO" ]
        BigFiles = BigFile_16+BigFile_17+BigFile_18
        BFs=[]
        for isample in skim.samples:
            if isample != "ttHToNonbb_M125": continue
            # skip big files
            if any ( x in isample for x in BigFiles ):
                BFs.append(isample)
                continue
            filelist = skim.samples[isample]
            proc = Process(target=skim.run, args=(filelist,presel,))
            procs.append(proc) ; proc.start()

        [ r.join() for r in procs  ]

        if len(BFs)!=0:
            m = Manager() ; q = m.Queue() ; p = Pool(12)
            print "only running on :", BFs
            for isample in BFs:
                filelist = skim.samples[isample]
                parallalizedByFiles( filelist , presel, q , skim.run , 1 ) #round(float(len(filelist))/nTask) if isample != "TTTo2L2Nu" else 1 )

    elif options.dataset == 2 : # data

        m = Manager() ; q = m.Queue() ; p = Pool(12)
        for isample in skim.samples:
            filelist = skim.samples[isample]
            parallalizedByFiles( filelist , presel, q , skim.run , round(float(len(filelist))/nTask) )
    elif options.dataset == 0 : # run all

        procs = []
        m = Manager() ; q = m.Queue() ; p = Pool(12)
        for isample in skim.samples:
            print("isample : ", isample)
            filelist = skim.samples[isample]
            parallalizedByFiles( filelist , presel, q , skim.run , round(float(len(filelist))/nTask) )

    else:

        if not options.serialism:
            print " --> DUMMY : Running with parallelism"
            procs = []
            for isample in skim.samples:
                filelist = skim.samples[isample]
                for ifile in filelist:
                    #if 'MuonEG_Run2016B' not in ifile: continue
                    proc = Process(target=skim.run, args=([ifile],presel,))
                    procs.append(proc) ; proc.start()
            [ r.join() for r in procs  ]
        else:
            print " --> DUMMY : Running with serialism"
            for isample in skim.samples:
                filelist = skim.samples[isample]
                skim.run( filelist , presel )

    ## benchmarking proram ##
    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- %s minutes ---" % ( (time.time() - start_time)/60. ))
    print("--- %s hours ---" % ( (time.time() - start_time)/3600. ))
