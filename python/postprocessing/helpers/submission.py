import os, re, sys
import commands
import math, time
import importlib

class batchJob:
    def __init__(self, processor, queue, maxlsftime, eventspersec, samplelist, lsfoutput, base):
        self.processor    = processor
        self.queue        = queue
        self.maxlsftime  = maxlsftime
        self.eventspersec = eventspersec
        self.samplelist   = samplelist
        self.lsfoutput    = lsfoutput
        self.base         = base

    def addSL(self, samplelistmod):
        #samplelistmod = importlib.import_module('samplelist_%s' %samplelist)
        self.samplelistData = list(samplelistmod['data'])
        self.samplelistMC = list(samplelistmod['mc'])
        if 'test' in samplelistmod:
            self.samplelists = list(samplelistmod['test'])
        else:
            self.samplelists = self.samplelistData + self.samplelistMC

    def submit(self, dryrun=False):
        #1 job/1 dataset, possibly create job contains multiple root file
        var=0
        if '2016' in self.samplelist:
            dirdata='Run2016'
            dirmc='Summer16'
        elif '2017' in self.samplelist:
            dirdata='Run2017'
            dirmc='Fall17'
        elif '2018' in self.samplelist:
            dirdata='Run2018'
            dirmc='Autumn18'
            
        for l in self.samplelists:
            #tag=l.split("/")[-1].split('.')[0]
            print "Reading filelist --> %s" %l
            file=open(os.path.expandvars( self.base + 'python/postprocessing/data/filelists/Legnaro_T2/%s/' %(dirdata if 'Run' in l else dirmc) +l+'.txt' ),'r')            
            filelist = file.readlines()
            splitting= max(int(float(sel[0].nevent())/(self.maxlsftime*3600*self.eventspersec)),1)
            njobs    = int(len(filelist)/splitting)+1
            sublists = [filelist[i:i+njobs] for i in range(0, len(filelist), njobs)]
            print '\nSplitting',l,'in',len(sublists),'chunk(s) of approximately',njobs,'files each'

            lfold = options.output+'/'+l
            os.system('mkdir '+lfold)
            if lfold.find('lustre')!= -1: outputbase = ""
            else: outputbase = options.base
 
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
                    fout.write('export RUNYEAR=\"%s\"\n'%Cfg.era())
                    fout.write('export NANOVER=\"%s\"\n'%Cfg.nanover())
                    fout.write('echo "environment:"\n')
                    fout.write('echo\n')
                    fout.write('env > local.env\n')
                    fout.write('env\n')
                    fout.write('# ulimit -v 3000000 # NO\n')
                    fout.write('echo "copying job dir to worker"\n')
                    fout.write('eval `scram runtime -sh`\n')
                    fout.write('ls\n')
                    fout.write('echo "running"\n')
                    #fout.write('python '+options.base+options.cfg+' ./ '+l+' -c \"'+options.preselection+'\" -b \"'+options.base+options.keepdropmenu+'\" -I '+options.pythonmodule+'\n')
                    fout.write('python '+options.base+'scripts/'+options.cfg+' ./ '+outputbase+lsubfold+'/list.txt -c \"'+options.preselection+'\" -e %s\n' %options.Nevent)
                    fout.write('exit $?\n') 
                    fout.write('echo ""\n')
                os.system('chmod 755 job.sh')
    
                ########## SEND JOB ON LSF QUEUE ##########
                if not dryrun:
                    os.system('bsub -q '+options.queue+' -o logs < job.sh')
                    #print 'bsub -q '+options.queue+' -o logs < job.sh'
                    #print 'filelist ' + l + ' - job nr ' + str(x).zfill(4) + ' -> submitted'
                var+=1
                os.chdir('../../../')
        print
        print 'CURRENT JOB SUMMARY:'
        if not dryrun: os.system('bjobs')
        print var, "number of job has been submitted" if not dryrun else "number of job has been created."
        print
