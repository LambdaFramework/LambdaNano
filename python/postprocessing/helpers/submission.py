import os, re, sys
import commands
import math, time
from PhysicsTools.NanoAODTools.postprocessing.helpers.colors import *

class batchJob:
    def __init__( self , skimmer , queue , taskperproc=60 ):
        # batchJob parameter
        self._skimmer      = skimmer
        self._queue        = queue
        self._MaxNjob      = taskperproc

        #skimmer parameters
        self._dataset    = skimmer.dataset
        self._outfolder  = skimmer.outfolder
        self._processkey = skimmer.samples
        self._year       = skimmer.year
        self._modules    = skimmer.modules
        self._presel     = skimmer.presel

        #global parameters
        if not os.environ['NANOAODTOOLS_BASE']:
            print("ERROR, please setup NANOAODTOOLS_BASE")
            sys.exit()
            
        self._base      = os.environ['NANOAODTOOLS_BASE']
        
    pass

    def makeJob( self , sublists , key , counter_ , dryrun=True ):
        
        ######### LOOP ON LSF JOB ##########
        jobdir= '%s/%s/%s/jobs' %( self._base , self._outfolder , key )
        resultdir= jobdir.replace( '/'+jobdir.split('/')[-1] , '' ).replace( self._base , '' )
        jobname = 'job_%s.sh' %counter_
        listname = 'list_%s.txt' %counter_
        
        os.system('mkdir -p '+ jobdir)
        os.chdir(jobdir)
        
        # make list
        listfile = open(listname , 'w')
        listfile.write( '\n'.join(sublists) )
        listfile.close()

        with open( jobname , 'w') as fout:
            fout.write('#!/bin/bash\n')
            fout.write('echo "PWD:"\n')
            fout.write('export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch\n')
            fout.write('source $VO_CMS_SW_DIR/cmsset_default.sh\n')
            fout.write('cd $PWD/../../../../CMSSW_11_2_0_pre6_ROOT622/src\n')
            fout.write('ls .\n')
            fout.write('eval `scram runtime -sh`\n')
            fout.write('cd $PWD\n')
            fout.write('echo "environment:"\n')
            fout.write('echo\n')
            fout.write('env > local.env\n')
            fout.write('env\n')
            fout.write('# ulimit -v 3000000 # NO\n')
            fout.write('cd $NANOAODTOOLS_BASE\n')
            fout.write('ls\n')
            fout.write('echo "running"\n')
            fout.write('python $NANOAODTOOLS_BASE/scripts/skimmer.py -b -o %s -d %s -y %s -p "%s" -t %s/%s\n' %( resultdir , self._dataset , self._year , self._presel , os.getcwd() , listname  ) )
            fout.write('exit $?\n')
            fout.write('echo ""\n')
            os.system( 'chmod 755 '+ jobname )
            
            ########## SEND JOB ON LSF QUEUE ##########
            if not dryrun:
                os.system('bsub -q %s -o %s/log_%s < %s' %( self._queue , jobdir , counter_ , jobname ) )
                print 'bsub -q %s -o %s/log_%s < %s  --> submitted' %( self._queue , jobdir , counter_ , jobname )
            else:
                print 'process %s - job nr %s -> Prepared' % ( key , counter_ )
        os.chdir('../../../../')
    pass
            
#################################################################################################################
    def submit(self, dryrun=True ):
        
        var=0 ; FileperJob = 3
        for ikey in self._processkey:
            filelist = self._processkey[ikey]
            
            # keeping below MaxNjob for one process
            nfilelist =len(filelist)
            njob = int( nfilelist / FileperJob )
            
            if njob > self._MaxNjob: 
                FileperJob = int( nfilelist / self._MaxNjob )
                njob = self._MaxNjob

            divlist = [ filelist[ x:x+FileperJob ] for x in range(0, nfilelist, FileperJob) ]
            
            print "number of file : ", nfilelist
            print WARNING+'--> Splitting process : ', ikey , 'into ' , len(divlist) , 'chunk(s) of approximately ', FileperJob ,' files per chunk'+ENDC

            for jdiv ,  idivlist in enumerate(divlist):
                jdiv = jdiv+1
                self.makeJob( idivlist , ikey , jdiv , dryrun )
                    
        print
        print 'CURRENT JOB SUMMARY:'
        if not dryrun: os.system('bjobs')
        print var, "number of job has been submitted" if not dryrun else "number of job has been created."
        os.system('bqueues')
        print
