#!/usr/bin/env python
import os, sys
import ROOT
from datetime import datetime
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.bVetoProducer import  bVetoProducer
from PhysicsTools.NanoAODTools.postprocessing.modules.lepSFProducerCpp import lepSFProducerCpp
from PhysicsTools.NanoAODTools.postprocessing.modules.pujetIdSFProducerCpp import pujetIdSFProducerCpp
from PhysicsTools.NanoAODTools.postprocessing.modules.aliasProducer import aliasProducer
from PhysicsTools.NanoAODTools.postprocessing.modules.eleFlipSFProducerCpp import eleFlipSFProducerCpp

from multiprocessing import Process, Pool, Queue, Manager
import multiprocessing, time
import random

class skimmer:

    def __init__(self, dataset_ , outfolder_ , year_ , presel_ = "mll>12 && Lepton_pt[0]>25 && Lepton_pt[1]>20 && PuppiMET_pt > 30" ):
        self.dataset = dataset_
        self.outfolder = outfolder_
        self.year = year_
        self.presel = presel_
        self.samples = {}
        self.modules = []

        if not os.path.isdir('%s/%s' %( os.getcwd() , self.outfolder ) ): os.mkdir('%s/%s' %( os.getcwd() , self.outfolder ) )

        ########### getting filelist according to year ##############
        if not os.environ['NANOAODTOOLS_BASE']: print("ERROR: NANOAODTOOLS_BASE not set"); sys.exit();

        theList = map( lambda x: x.split('.')[0] , os.listdir( '%s/scripts/filelists/%s' %( os.environ["NANOAODTOOLS_BASE"] , self.year ) ) )
        data = [ x for x in theList if any(y in x for y in [ 'Single' ,'Double' , 'EG' ]) ]
        mc = list(set(theList)^set(data))

        #### modules ####
        bVetoer   = lambda : bVetoProducer        ( self.year                  )
        lepSF     = lambda : lepSFProducerCpp     ( self.year , 2 , 'total_SF' )
        pujetIdSF = lambda : pujetIdSFProducerCpp ( self.year , 'loose'        )
        flipSF    = lambda : eleFlipSFProducerCpp ( self.year , 2 , 'total_SF' )
        aliaser   = lambda : aliasProducer        ( self.year                  )

        modules_MC = [ lepSF() , pujetIdSF() , bVetoer() , flipSF() , aliaser() ]
        modules_DATA = [ bVetoer() , aliaser() ]
        #################

        allDict ={} ; mcDict={} ; dataDict={}
        for iname in theList :
            sample_files = open( "%s/scripts/filelists/%s/%s.txt" %( os.environ["NANOAODTOOLS_BASE"] , self.year , iname ) , "r" )
            unpacklists = [ x.strip('\n') for x in sample_files.readlines() ]
            allDict[iname] = unpacklists
            if iname in data : dataDict[iname] = unpacklists
            elif iname in mc : mcDict[iname]   = unpacklists
            sample_files.close()


        if   self.dataset == 0 :
            self.samples = allDict
            self.modules = modules_MC + modules_DATA
        elif self.dataset == 1 :
            self.samples = mcDict
            self.modules = modules_MC
        elif self.dataset == 2 :
            self.samples = dataDict
            self.modules = modules_DATA
        elif self.dataset >= 3 :
            self.samples = allDict
            self.modules = modules_MC
        else:
            print("ERROR: data type not found"); sys.exit();

        pass

    def run( self , infiles , isample=None ):

        p=PostProcessor(
            outputDir='%s/%s/%s/' %( os.getcwd() , self.outfolder , isample ) if isample is not None else '%s/%s/' %( os.getcwd() , self.outfolder ) ,
            inputFiles=infiles ,
            cut= self.presel ,
            branchsel= "%s/scripts/data/slimming-%s-in.txt" %( os.getcwd() , self.year ),
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
            outputbranchsel = "%s/scripts/data/slimming-%s-in.txt" %( os.getcwd() , self.year ),
            maxEntries=None,
            firstEntry=0,
            prefetch=False,
            longTermCache=False
        )
        p.run()
        pass


## Parallelism helper
def putQueue( func , arg1 , arg2 , queue ):
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

def parallalizedByFiles( filelist , procname , q , target , nsplit ):

    print "Total number of files : ", len(filelist)
    print "Total number of files per jobs : ", round(nsplit)

    tot = len(filelist) ; njobs = 0 ; counter = 0 ; sublist=[]
    for ifile in filelist :
        counter+=1 ; sublist.append(ifile)
        ## number of file per jobs
        if counter == nsplit or ( tot > 0 and tot < nsplit ) :
            Process(target=putQueue, args=( target , sublist , procname , q)).start()
            # reset
            njobs+=1 ;
            counter=0 ; tot-=nsplit ; sublist=[]

    print "Total number of jobs : ", njobs

    procs = []
    for j in range(njobs): procs.append(p.apply_async( readQueue , (j+1 , q) ))
    [ r.get() for r in procs ]

    pass

if __name__ == "__main__" :

    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] -d dataset -y year -o outfolder -m mode")

    usage = "usage: %prog [options]"
    parser.add_option( "-d" , "--dataset"   , action="store" , type="int"    , dest="dataset"   , default=None      ,
                       help="specify which dataset to run\
                       #################################\
                       # 0 = all                       #\
                       # 1 = mc                        #\
                       # 2 = data                      #\
                       # 3 = dummy (testing code)      #\
                       # 4 = reprocess sel. files      #\
                       # 5 = single run                #\
                       #################################\
                       " )
    parser.add_option( "-y" , "--year"      , action="store" , type="string" , dest="year"      , default="2016"    , help="data-taking year [default: 2016]"             )
    parser.add_option( "-o" , "--outfolder" , action="store" , type="string" , dest="outfolder" , default="skimmed" , help="name of the output folder [default: skimmed]" )
    parser.add_option( "-b" , "--batch"     , action="store_true" , dest="batch" , default=False , help="Submit to cluster [Default: False]"                              )

    (options, args) = parser.parse_args()

    options.outfolder = "dummy" if options.dataset == 3 else options.outfolder

    if os.getcwd().split('/')[-1] != 'LambdaNano' :
        print "Please run the scripts from LambdaNano folder."
        sys.exit()

    if options.dataset == None :
        parser.print_help()
        sys.exit()

    start_time = time.time()
    nTask=60

    if not options.batch :
        ###### single run files
        if options.dataset == 5 :
            skim = skimmer( options.dataset , 'testRun-%s' %( options.year ) , options.year )
            rootfile="/media/shoh/02A1ACF427292FC0/nanov5/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6/nanoLatino_TTTo2L2Nu__part4.root"
            skim.run([rootfile],'test')
        ###### reprocessing or testing
        if options.dataset == 3 or options.dataset == 4 :
            print "Reprocessing dataset"
            skim = skimmer( options.dataset , '%s-%s' %( options.outfolder , options.year ) , options.year )

            inputs = []
            #inpui missing file
            if options.dataset == 4 :
                inputs = [''] #INPUT HERE FOR REPROCESSING
            elif options.dataset == 3 :
                inputs = [ "WWZ" , "WZZ" ] # , "WWW" , "ZZTo2L2Q" , "ST_s-channel"
            # WWZ broke for 2017
            m = Manager() ; q = m.Queue() ; p = Pool( multiprocessing.cpu_count() )
            for isample in skim.samples:
                if isample in inputs:
                    filelist = skim.samples[isample]
                    parallalizedByFiles( filelist , isample , q , skim.run , round( float( len(filelist) ) / nTask ) if len(filelist) >= nTask else 1 )
        ###### data
        elif options.dataset == 2 :
            print "Postprocessing Data"
            skim = skimmer( options.dataset , '%s-%s' %( options.outfolder , options.year ) , options.year )

            m = Manager() ; q = m.Queue() ; p = Pool( multiprocessing.cpu_count() )
            for isample in skim.samples:
                filelist = skim.samples[isample]
                parallalizedByFiles( filelist , isample , q , skim.run , round( float( len(filelist) ) / nTask ) if len(filelist) >= nTask else 1 )
        ###### MC
        elif options.dataset == 1 :
            print "Postprocessing MC"
            skim = skimmer( options.dataset , '%s-%s' %( options.outfolder , options.year ) , options.year )

            procs = [] ; BigFiles = []
            if options.year == '2016'   : BigFiles = [ "TTTo2L2Nu" , "DYJetsToLL_M-50-LO_ext2" , "ZZTo2L2Nu_ext1" , "ZZTo4L_ext1" ]
            elif options.year == '2017' : BigFiles = [ "TTTo2L2Nu" , "DYJetsToLL_M-50-LO_ext1" , "WZTo2L2Q" , "ZZTo2L2Nu" , "ZGToLLG" ]
            elif options.year == '2018' : BigFiles = [ "TTTo2L2Nu" , "DYJetsToLL_M-50-LO" , "ZZTo2L2Q" , "ZZTo2L2Nu_ext1" , "WZTo3LNu_mllmin01" ]

            for isample in skim.samples:
                if any ( x in isample for x in BigFiles ): continue
                # 2017 "WWZ" faulty
                if options.year == '2017' and isample == 'WWZ' : continue

                filelist = skim.samples[isample]
                proc = Process(target=skim.run, args=( filelist , isample , ))
                procs.append(proc) ; proc.start()

            # Parallellizes per process
            [ r.join() for r in procs  ]

            # Parallellizes per file
            if len(BigFiles) != 0 :
                m = Manager() ; q = m.Queue() ; p = Pool( multiprocessing.cpu_count() )
                for ibg in BigFiles:
                    filelist = skim.samples[ibg]
                    parallalizedByFiles( filelist , ibg , q , skim.run , round( float( len(filelist) ) / nTask ) if len(filelist) > nTask else 1 )
    ############################################################################
    else :
        print "submitting to LSF batch"
        if '/lustre/cmswork/hoh' not in os.getcwd():
            print "ERROR, use batch on cluster"
            sys.exit()
            
        #Data (longer queue)
        skim_mc = skimmer( 1 , '/lustre/cmsdata/hoh/homebrew_latino/%s-%s' %( options.outfolder , options.year ) , options.year )
        #MC (short queue)
        skim_data = skimmer( 2 , '/lustre/cmsdata/hoh/homebrew_latino/%s-%s' %( options.outfolder , options.year ) , options.year )
        

    #########################
    ## benchmarking proram ##
    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- %s minutes ---" % ( (time.time() - start_time)/60. ))
    print("--- %s hours ---" % ( (time.time() - start_time)/3600. ))
