import os, re, sys
import commands
import math, time
from PhysicsTools.NanoAODTools.postprocessing.helpers.colors import *

class batchJob:
    def __init__(self, queue, maxlsftime, eventspersec, lsfoutput, base):
        self._queue        = queue
        self._maxlsftime  = maxlsftime
        self._eventspersec = eventspersec
        self._lsfoutput    = lsfoutput
        self._base         = base

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
        
    def submit(self, dryrun=False):
        #1 job/1 dataset, possibly create job contains multiple root file
        var=0            
        for l in self._samplelists:
            #tag=l.split("/")[-1].split('.')[0]
            file=open(os.path.expandvars( self._base + 'python/postprocessing/data/filelists/Legnaro_T2/%s/' %(self._dirdata if 'Run' in l.filename() else self._dirmc) +l.filename()+'.txt' ),'r')            
            filelist = file.readlines()
            splitting= max(int(float(l.nevent())/(self._maxlsftime*3600*self._eventspersec)),1)
            njobs    = int(len(filelist)/splitting)+1
            sublists = [filelist[i:i+njobs] for i in range(0, len(filelist), njobs)]
            print WARNING+'--> Splitting',l.filename(),'in',len(sublists),'chunk(s) of approximately',njobs,'files each'+ENDC
            
            lfold = self._base + self._lsfoutput+'/'+l.filename()
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
                    if 'Run' in l.filename(): fout.write('--json=%s ' %(self._jsoner))
                    for i,moder in enumerate(self._modules): 
                        #remove module does nothing to the DATA
                        if 'Run' in l.filename() and 'lepSF' in moder: continue;
                        if 'Run' in l.filename() and 'puWeight' in moder: continue;
                        fout.write('%s\n'%moder if i+1==len(self._modules) else '%s '%moder )
                    fout.write('exit $?\n') 
                    fout.write('echo ""\n')
                os.system('chmod 755 job.sh')
    
                ########## SEND JOB ON LSF QUEUE ##########
                if not dryrun:
                    os.system('bsub -q '+ self._queue +' -o logs < job.sh')
                    #print 'bsub -q '+options.queue+' -o logs < job.sh'
                    #print 'filelist ' + l + ' - job nr ' + str(x).zfill(4) + ' -> submitted'
                var+=1
                os.chdir('../../../')
        print
        print 'CURRENT JOB SUMMARY:'
        if not dryrun: os.system('bjobs')
        print var, "number of job has been submitted" if not dryrun else "number of job has been created."
        os.system('bqueues')
        print
