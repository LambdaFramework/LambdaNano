#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.helpers.submission import batchJob
from PhysicsTools.NanoAODTools.postprocessing.helpers.workflow import workflow
from PhysicsTools.NanoAODTools.postprocessing.helpers.colors import *

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] outputDir inputFiles")
    parser.add_option("-s"       , "--postfix"          , dest="postfix"   , type="string" , default=None, help="Postfix which will be appended to the file name (default: _Friend for friends, _Skim for skims)")
    parser.add_option("-J"       , "--json"             , dest="json"      , type="string" , default=None, help="Select events using this JSON file")
    parser.add_option("-c"       , "--cut"              , dest="cut"       , type="string" , default="", help="Cut string")
    parser.add_option("-b"       , "--branch-selection" , dest="branchsel" , type="string" , default="", help="Branch selection")
    parser.add_option('--bs'     , '--base'             , dest='base'      , type="string" , default='%s/src/PhysicsTools/NanoAODTools/' \
                          %os.environ['CMSSW_BASE'] if 'CMSSW_BASE' in os.environ else os.getcwd() , action='store' , help="Workin directory")

    parser.add_option("--bi"              , "--branch-selection-input"                  , dest="branchsel_in"  , type="string" , default=None , help="Branch selection input")
    parser.add_option("--bo"              , "--branch-selection-output"                 , dest="branchsel_out" , type="string" , default=None , help="Branch selection output")
    parser.add_option("--friend"          , dest="friend"        , action="store_true"  , default=False        , help="Produce friend trees in output (current default is to produce full trees)")
    parser.add_option("--full"            , dest="friend"        , action="store_false" , default=False        , help="Produce full trees in output (this is the current default)")
    parser.add_option("--noout"           , dest="noOut"         , action="store_true"  , default=False        , help="Do not produce output, just run modules")
    parser.add_option("-P"                , "--prefetch"         , dest="prefetch"      , action="store_true"  , default=False, help="Prefetch input files locally instead of accessing them via xrootd")
    parser.add_option("--long-term-cache" , dest="longTermCache" , action="store_true"  , default=False        , help="Keep prefetched files across runs instead of deleting them at the end")
    parser.add_option("-N"                , "--max-entries"      , dest="maxEntries"    , type="long"          , default=None, help="Maximum number of entries to process from any single given input tree")
    parser.add_option("--first-entry"     , dest="firstEntry"    , type="long"          , default=0            , help="First entry to process in the three (to be used together with --max-entries)")
    parser.add_option("--justcount"       , dest="justcount"     , default=False        , action="store_true"  , help="Just report the number of selected events") 
    parser.add_option("-I"                , "--import"           , dest="imports"       , type="string"        , default=[], action="append", nargs=2, \
                      help="Import modules (python package, comma-separated list of ");
    parser.add_option("-z"                , "--compression"      , dest="compression"   , type="string"        , default=("LZMA:9"), help="Compression: none, or (algo):(level) ")
    parser.add_option("-w"                , "--workflow"         , dest="workflow"      , type="string"        , default=""        , help="Specify the workflow of postprocessing step")    
    parser.add_option("--batch"           , dest="batch"         , action="store_true"  , default=False        , help="Submit to Padova batch processing")
    parser.add_option("--dryrun"          , dest="dryrun"        , action="store_true"  , default=False        , help="With batch option, dry run")
    #parser.add_option("--dataOnly"        , dest="dataOnly"      , action="store_true"  , default=False        , help="With batch option, make only data jobs, default make only mc job")
    parser.add_option('-m'                , '--maxlsftime'       , action='store'       , type='int'           , dest='maxlsftime'  ,   default=5, help="maximum life time in LSF")
    parser.add_option('-p'                , '--eventspersec'     , action='store'       , type='int'           , dest='eventspersec', default=100, help="event persec")
    parser.add_option('-q'                , '--queue'            , action='store'       , type='string'        , dest='queue'       , default='local-cms-short', help="queue")
    parser.add_option('-l'                , '--samplelists'      , action='store'       , type='string'        , dest='samplelists' , default='' , help="Sample list")
    parser.add_option('-o'                , '--lsfoutput'        , action='store'       , type='string'        , dest='lsfoutput'   , default='' , help="LSF output folder name")

    (options, args) = parser.parse_args()

    if os.getcwd().split('/')[-1] == "scripts":
        print "Please run the script from base directory: %s" %options.base
        sys.exit()

    if options.friend:
        if options.cut or options.json: raise RuntimeError("Can't apply JSON or cut selection when producing friends")

    if len(args) < 2 and not options.batch :
	 parser.print_help()
         print YELLOW+"For running in batch, example:"+ENDC
         print YELLOW+"python scripts/postproc.py --batch --dryrun -w WH_SS -l Run2_2016_v4 -o test -c \"( (Muon_pt[0]>5 && Muon_mediumId[0]>0) || (Electron_pt[0]>15 && Electron_cutBased[0]>0) )\" --bi scripts/slimming-in.txt --bo scripts/slimming-out.txt"+ENDC
         print YELLOW+"For running locally"+ENDC
         print YELLOW+"python scripts/postproc.py test/ test/WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8.root -c \"Muon_pt[0]>30\" --bi scripts/slimming-in.txt --bo scripts/slimming-out.txt"+ENDC
         sys.exit(1)
    if options.batch:
        outdir=[] ; args = []
    else:
        if '.txt' in args[1] and os.path.isfile(args[1]):
            file=open(os.path.expandvars('%s'%args[1]),'r')
            filelist = file.readlines()
            outdir = args[0] ; args = map(lambda s: s.strip(), filelist)
        else:
            outdir = args[0] ; args = args[1:]

    modules = []
    
    for mod, names in options.imports:
        import_module(mod)
        obj = sys.modules[mod]
        selnames = names.split(",")
        mods = dir(obj)
        for name in selnames:
            if name in mods:
                print OKGREEN+"Loading "+name+" from "+mod+ENDC
                if type(getattr(obj,name)) == list:
                    for mod in getattr(obj,name):
                        modules.append( mod())
                else:
                    modules.append(getattr(obj,name)())

    if options.noOut:
        if len(modules) == 0: 
            raise RuntimeError("Running with --noout and no modules does nothing!")
    if options.branchsel!=None:
        options.branchsel_in = options.branchsel
        options.branchsel_out = options.branchsel
    p=PostProcessor(outdir,args,
            cut = options.cut,
            branchsel = options.branchsel_in,
            modules = modules,
            compression = options.compression,
            friend = options.friend,
            postfix = options.postfix,
            jsonInput = options.json,
            noOut = options.noOut,
            justcount = options.justcount,
            prefetch = options.prefetch,
            longTermCache = options.longTermCache,
            maxEntries = options.maxEntries,
            firstEntry = options.firstEntry,
            outputbranchsel = options.branchsel_out)
    
    if options.batch and (options.workflow!='' or options.samplelists!=''):
        print HEADER+"batch initialization"+ENDC
        #Remaking processor
        #environmental check
        print
        if not os.path.exists(os.path.expandvars(options.base)):
            print '--- ERROR ---'
            print '  \''+options.base+'\' path not found expanding '+options.base
            print '  please point to the correct path to scripts/ using option \'--bs $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/\''
            print
            sys.exit()
	if len( options.lsfoutput) == 0 or os.path.exists("%s%s-%s"%( options.base , options.samplelists , options.lsfoutput ) ):
            print '--- ERROR ---'
            print '  \''+options.lsfoutput+'\' folder already exists or is null!'
            print '  please delete it or use a different name using option \'-o FOLDER-NAME\''
            print
            sys.exit()
        os.system('mkdir %s-%s'%(options.samplelists,options.lsfoutput))
        
        #making batch script, every variable is fed externally to postproc.py
        bj = batchJob( options.queue , options.maxlsftime , options.eventspersec , '%s-%s'%(options.samplelists,options.lsfoutput) , options.base )
        bj.register( options.samplelists, options.cut , workflow["%s_%s" %(options.workflow,options.samplelists.split('_')[1])] , options.branchsel )
        bj.submit(options.dryrun)
    elif options.batch and (options.workflow=='' or options.samplelists!=''):
        raise Exception('workflow or samplelists are empty, please specify workflow AND samplelist')
    else:
        p.run()

