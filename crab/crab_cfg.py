from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

config = Configuration()
config.section_("General")
config.General.requestName = 'NanoPost1'
config.General.transferLogs=True
config.General.transferOutputs = True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['../../../nano_postproc.py','../../../removeDuplicate.txt']
config.JobType.sendPythonFolder	 = True
config.JobType.sendExternalFolder = True
config.section_("Data")
config.Data.userInputFiles = ['/lustre/cmswork/hoh/NANO/SSLep/data/SingleElectronRun2016B-03Feb2017_ver2-v2.root']
#config.Data.userInputFiles = ['/lustre/cmswork/hoh/NANO/SSLep/data/SingleElectronRun2016C-03Feb2017-v1.root']
#config.Data.inputDataset = '/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PUMoriond17_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM'
config.Data.inputDBS = 'global'
#config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 100
config.Data.totalUnits = 2000
#config.Data.outLFNDirBase = '/store/user/hoh/'
config.Data.outLFNDirBase = '/store/user/shoh/'
config.Data.outputPrimaryDataset ='SingleElectronRun2016B-03Feb2017_ver2-v2'
config.Data.publication = False
config.Data.outputDatasetTag = 'NanoTestPost'
config.section_("Site")
config.Site.storageSite = "T2_IT_Legnaro"
config.Site.whitelist = ['T3_US_FNALLPC']
config.Site.ignoreGlobalBlacklist = True
