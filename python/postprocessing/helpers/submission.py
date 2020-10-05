import os, re, sys
import commands
import math, time
from PhysicsTools.NanoAODTools.postprocessing.helpers.colors import *

class batchJob:
    def __init__( self , skimmer , queue , taskperproc ):
        # batchJob parameter
        self._skimmer      = skimmer
        self._queue        = queue
        self._ntask        = taskperproc

        #skimmer parameters
        self._dataset    = skimmer.dataset
        self._outfolder  = skimmer.outfolder
        self._processkey = skimmer.samples
        self._year       = skimmer.year
        self._modules    = skimmer.modules

        #global parameters
        if os.environ['NANOAODTOOLS_BASE']:
            print("ERROR, please setup NANOAODTOOLS_BASE")
            sys.exit()
            
        self._base      = os.environ['NANOAODTOOLS_BASE']
        
    pass

    '''
    def register(self, samplelist , cutter, modconfig , slimmer , slimmerin , slimmerout ):
        
        if '2016' in samplelist:
            self._dirdata='Run2016'
            self._dirmc='Summer16'
        elif '2017' in samplelist:
            self._dirdata='Run2017'
            self._dirmc='Fall17'
        elif '2018' in samplelist:
            self._dirdata='Run2018'
            self._dirmc='Autumn18'

        self._jsoner = '%s/python/postprocessing/data/json/%s' %( self._base, datasets[samplelist]['cert'] )
        if self._jsoner.split('.')[1:][0]!='txt': raise Exception('ERROR: Json file is not correctly loaded!')
        self._samplelistData = list(datasets[samplelist]['data'])
        self._samplelistMC = list(datasets[samplelist]['mc'])
        if 'test' in datasets[samplelist]:
            self._samplelists = list(datasets[samplelist]['test'])
        else:
            self._samplelists = self._samplelistData + self._samplelistMC
            
        self._cutter = cutter

        self._modules=[]
        
        for i,mod in enumerate(modconfig):
            if 'puWeight' in mod: 
                self._modules.append( '-I PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer %s'%mod )
            elif 'lepSFProducer' in mod:
                self._modules.append( '-I PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer %s'%mod )
            else:
                self._modules.append( '-I PhysicsTools.NanoAODTools.postprocessing.modules.analysis.%s %s'%(mod,mod) )
                #self.modules.append( '-I PhysicsTools.NanoAODTools.postprocessing.modules.%s %s'%(mod,mod) if i+1!= len(modconfig) \
                #                         else '-I PhysicsTools.NanoAODTools.postprocessing.analysis.%s %s'%(mod,mod) )

        self._slimmer = slimmer
        self._slimmerin = slimmerin
        self._slimmerout = slimmerout

    '''

    def makeJOb( self , sublists , key , counter_ , dryrun=True ):
        
        ######### LOOP ON LSF JOB ##########
        jobdir= '%s/%s/%s/jobs' %( self._base , self._outfolder , key )
        resultdir= jobdir.replace( '/'+jobdir.split('/')[-1] , '' )
        jobname = 'job_%s.sh' %counter_
        
        os.system('mkdir '+ jobdir)
        os.chdir(jobdir)
        with open( jobname , 'w') as fout:
            fout.write('#!/bin/bash\n')
            fout.write('echo "PWD:"\n')
            fout.write('pwd\n')
            fout.write('export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch\n')
            fout.write('source $VO_CMS_SW_DIR/cmsset_default.sh\n')
            fout.write('echo "environment:"\n')
            fout.write('echo\n')
            fout.write('env > local.env\n')
            fout.write('env\n')
            fout.write('# ulimit -v 3000000 # NO\n')
            fout.write('echo "copying job dir to worker"\n')
            fout.write('eval `scram runtime -sh`\n')
            fout.write('ls\n')
            fout.write('echo "running"\n')
            fout.write('python %s/scripts/postproc.py ./ %s/list.txt --cut=\"%s\" --bi %s/%s --bo /%s/%s ' %( self._base , lsubfold ,self._cutter, self._base, self._slimmerin, self._base, self._slimmerout ))

            #fout.write('%s\n'%moder if i+1==len(self._modules) else '%s '%moder )
            fout.write('exit $?\n')
            fout.write('echo ""\n')
            os.system( 'chmod 755 '+ jobname )
            
            ########## SEND JOB ON LSF QUEUE ##########
            if not dryrun:
                os.system('bsub -q '+ self._queue +' -o logs < job.sh')
                print 'bsub -q '+ self._queue +' -o logs < job.sh'
                print 'process ' + key + ' - job nr ' + counter_ + ' -> submitted'
            else:
                print 'process ' + key + ' - job nr ' + counter_ + ' -> prepared'
        os.chdir('../../../../')
    pass
            
#################################################################################################################
    def submit(self, dryrun=True ):
        #1 job/1 dataset, possibly create job contains multiple root file
        for ikey in self._processkey:
            filelist = self._processkey[ikey]
            splitting = max( int(float( len(filelist) ) / self._ntask ) , 1 )

            print "Total number of files : ", len(filelist)
    
            print WARNING+'--> Splitting', ikey ,'in', self._ntask ,'chunk(s) of approximately', splitting ,'files each'+ENDC
            tot =len(filelist) ; njobs = 0 ; counter = 0 ; sublist = []
            for ifile in filelist :
                counter+=1 ; sublist.append(ifile)
                # number of file per jobs
                if counter == nsplit or ( tot > 0 and tot < splitting ) :
                    makeJob( sublist , ikey , njobs , dryrun )
                    njobs+=1 ;
                    counter=0 ; tot-=nsplit ; sublist=[]
                    
        print
        print 'CURRENT JOB SUMMARY:'
        if not dryrun: os.system('bjobs')
        print var, "number of job has been submitted" if not dryrun else "number of job has been created."
        os.system('bqueues')
        print
