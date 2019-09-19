import os, re, sys
import commands
import math, time
from PhysicsTools.NanoAODTools.postprocessing.modules.datasets import datasets
from PhysicsTools.NanoAODTools.postprocessing.helpers.colors import *

class batchJob:
    def __init__(self, processor, queue, maxlsftime, eventspersec, lsfoutput, base):
        self.processor    = processor
        self.queue        = queue
        self.maxlsftime  = maxlsftime
        self.eventspersec = eventspersec
        self.lsfoutput    = lsfoutput
        self.base         = base
    
    def addModule(self, modules):
        self.modules = modules

    def addSL(self, samplelist):
        if '2016' in samplelist:
            self.dirdata='Run2016'
            self.dirmc='Summer16'
        elif '2017' in samplelist:
            self.dirdata='Run2017'
            self.dirmc='Fall17'
        elif '2018' in samplelist:
            self.dirdata='Run2018'
            self.dirmc='Autumn18'

        self.samplelistData = list(datasets[samplelist]['data'])
        self.samplelistMC = list(datasets[samplelist]['mc'])
        if 'test' in datasets[samplelist]:
            self.samplelists = list(datasets[samplelist]['test'])
        else:
            self.samplelists = self.samplelistData + self.samplelistMC


    def submit(self, dryrun=False):
        #1 job/1 dataset, possibly create job contains multiple root file
        var=0            
        for l in self.samplelists:
            #tag=l.split("/")[-1].split('.')[0]
            file=open(os.path.expandvars( self.base + 'python/postprocessing/data/filelists/Legnaro_T2/%s/' %(self.dirdata if 'Run' in l.filename() else self.dirmc) +l.filename()+'.txt' ),'r')            
            filelist = file.readlines()
            splitting= max(int(float(l.nevent())/(self.maxlsftime*3600*self.eventspersec)),1)
            njobs    = int(len(filelist)/splitting)+1
            sublists = [filelist[i:i+njobs] for i in range(0, len(filelist), njobs)]
            print WARNING+'--> Splitting',l.filename(),'in',len(sublists),'chunk(s) of approximately',njobs,'files each'+ENDC
            
            lfold = self.base + self.lsfoutput+'/'+l.filename()
            os.system('mkdir '+lfold)
            #if lfold.find('lustre')!= -1: outputbase = ""
            #else: outputbase = options.base
 
            ######### LOOP ON LSF JOB ##########
            for x in range(len(sublists)):
                lsubfold = lfold+'/'+str(x).zfill(4)
                os.system('mkdir '+lsubfold)
                os.chdir(lsubfold)
                splitlist=open('list.txt','w')  
                splitlist.write(''.join(str(x) for x in sublists[x]))
                splitlist.close()
        
                with open('job.sh', 'w') as fout:
                    #fout.write('#!/bin/bash\n')
                    #fout.write('#BSUB -J '+l+'_'+str(x).zfill(4)+'\n')
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
                    fout.write('python %s/scripts/postproc.py ./ %s/list.txt --cut=%s --branch-selection=%s --import=%s --json=%s\n' \
                                   %( self.base ,\
                                          lsubfold ,\
                                          self.processor.cut , \
                                          self.processor.branchsel , \
                                          self.modules , \
                                          self.processor.json\
                                          ))
                    fout.write('exit $?\n') 
                    fout.write('echo ""\n')
                os.system('chmod 755 job.sh')
    
                ########## SEND JOB ON LSF QUEUE ##########
                if not dryrun:
                    os.system('bsub -q '+ self.queue +' -o logs < job.sh')
                    #print 'bsub -q '+options.queue+' -o logs < job.sh'
                    #print 'filelist ' + l + ' - job nr ' + str(x).zfill(4) + ' -> submitted'
                var+=1
                os.chdir('../../../')
        print
        print 'CURRENT JOB SUMMARY:'
        if not dryrun: os.system('bjobs')
        print var, "number of job has been submitted" if not dryrun else "number of job has been created."
        print
