import os
import inspect
from collections import Counter

from PhysicsTools.NanoAODTools.LambPlot.plotConfiguration.helper import addSampleWeight, nanoGetSampleFiles

# samples
try:
    len(samples)
except NameError:
    import collections
    samples = collections.OrderedDict()

##############################################
###### Tree base directory for the site ######
##############################################

mcDirectory = '/home/shoh/works/workbench/WHSS/analysis/LambdaNano/skimmed'
dataDirectory = mcDirectory
fakeDirectory = mcDirectory

################################################
############ DATA DECLARATION ##################
################################################

DataRun = [
    ['B','Run2016B-Nano1June2019_ver2-v1'],
    ['C','Run2016C-Nano1June2019-v1'],
    ['D','Run2016D-Nano1June2019-v1'],
    ['E','Run2016E-Nano1June2019-v1'],
    ['F','Run2016F-Nano1June2019-v1'],
    ['G','Run2016G-Nano1June2019-v1'],
    ['H','Run2016H-Nano1June2019-v1']
]

DataSets = ['MuonEG','SingleMuon','SingleElectron','DoubleMuon', 'DoubleEG']
#DataSets = [ 'SingleMuon' , 'SingleElectron' , 'DoubleMuon' , 'DoubleEG' ]
#DataSets = [ 'SingleMuon' , 'SingleElectron' , 'DoubleMuon' , 'DoubleEG' ]

DataTrig = {
    'MuonEG'         : ' Trigger_ElMu' ,
    'SingleMuon'     : '!Trigger_ElMu && Trigger_sngMu' ,
    'SingleElectron' : '!Trigger_ElMu && !Trigger_sngMu && Trigger_sngEl',
    'DoubleMuon'     : '!Trigger_ElMu && !Trigger_sngMu && !Trigger_sngEl && Trigger_dblMu',
    'DoubleEG'       : '!Trigger_ElMu && !Trigger_sngMu && !Trigger_sngEl && !Trigger_dblMu && Trigger_dblEl'
}

#########################################
############ MC COMMON ##################
#########################################

# SFweight does not include btag weights
mcCommonWeightNoMatch = 'XSWeight*SFweight*METFilter_MC'
mcCommonWeight = 'XSWeight*SFweight*PromptGenLepMatch2l*METFilter_MC'

###########################################
#############  BACKGROUNDS  ###############
###########################################

###### DY #######

ptllDYW_NLO = '(0.876979+gen_ptll*(4.11598e-03)-(2.35520e-05)*gen_ptll*gen_ptll)*(1.10211 * (0.958512 - 0.131835*TMath::Erf((gen_ptll-14.1972)/10.1525)))*(gen_ptll<140)+0.891188*(gen_ptll>=140)'
ptllDYW_LO  = '(8.61313e-01+gen_ptll*4.46807e-03-1.52324e-05*gen_ptll*gen_ptll)*(1.08683 * (0.95 - 0.0657370*TMath::Erf((gen_ptll-11.)/5.51582)))*(gen_ptll<140)+1.141996*(gen_ptll>=140)'

files = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50-LO_ext2') + \
    nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-10to50-LO')

samples['DY'] = {
    'name': files,
    'weight': mcCommonWeight + '*( !(Sum(PhotonGen_isPrompt==1 && PhotonGen_pt>15 && abs(PhotonGen_eta)<2.6) > 0))',
    'FilesPerJob': 4,
}

addSampleWeight(samples,'DY','DYJetsToLL_M-50-LO_ext2',ptllDYW_LO)
addSampleWeight(samples,'DY','DYJetsToLL_M-10to50-LO',ptllDYW_LO)

###### Top #######

files = nanoGetSampleFiles(mcDirectory, 'TTTo2L2Nu') + \
        nanoGetSampleFiles(mcDirectory, 'ST_s-channel') + \
        nanoGetSampleFiles(mcDirectory, 'ST_t-channel_antitop') + \
        nanoGetSampleFiles(mcDirectory, 'ST_t-channel_top') + \
        nanoGetSampleFiles(mcDirectory, 'ST_tW_antitop') + \
        nanoGetSampleFiles(mcDirectory, 'ST_tW_top')

samples['top'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 1,
    #'EventsPerJob': 100000
}

#addSampleWeight(samples,'top','TTTo2L2Nu','(topGenPt * antitopGenPt > 0.) * (TMath::Sqrt(TMath::Exp(0.0615 - 0.0005 * topGenPt) * TMath::Exp(0.0615 - 0.0005 * antitopGenPt))) + (topGenPt * antitopGenPt <= 0.)')
###### WW ########

samples['WW'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu'),
    'weight': mcCommonWeight + '*nllW', # temporary - nllW module not run on PS and UE variation samples
    #'weight': mcCommonWeight + '*nllWOTF', # temporary
    'FilesPerJob': 1
}

samples['WWewk'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'WpWmJJ_EWK_noTop'),
    'weight': mcCommonWeight + '*(Sum(abs(GenPart_pdgId)==6 || GenPart_pdgId==25)==0)*( TMath::Sqrt(2. * LHEPart_pt[0] * LHEPart_pt[1] * (TMath::CosH(LHEPart_eta[0] - LHEPart_eta[1]) - TMath::Cos(LHEPart_phi[0] - LHEPart_phi[1]))) > 60. && TMath::Sqrt(2. * LHEPart_pt[0] * LHEPart_pt[1] * (TMath::CosH(LHEPart_eta[0] - LHEPart_eta[1]) - TMath::Cos(LHEPart_phi[0] - LHEPart_phi[1]))) < 100. && TMath::Sqrt(2. * LHEPart_pt[2] * LHEPart_pt[3] * (TMath::CosH(LHEPart_eta[2] - LHEPart_eta[3]) - TMath::Cos(LHEPart_phi[2] - LHEPart_phi[3]))) > 60. && TMath::Sqrt(2. * LHEPart_pt[2] * LHEPart_pt[3] * (TMath::CosH(LHEPart_eta[2] - LHEPart_eta[3]) - TMath::Cos(LHEPart_phi[2] - LHEPart_phi[3]))) < 100.)', #filter tops and Higgs, limit w mass
    'FilesPerJob': 4
}

samples['ggWW'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluWWTo2L2Nu_MCFM'),
    'weight': mcCommonWeight + '*(1.53/1.4)', # updating k-factor
    'FilesPerJob': 4
}

######## Wg ########

files = nanoGetSampleFiles(mcDirectory, 'Wg_MADGRAPHMLM')

samples['Wg'] = {
    'name': files,
    'weight': mcCommonWeightNoMatch + '*(!(Gen_ZGstar_mass > 0))',
    'FilesPerJob': 4
}

######## Zg #######

files = nanoGetSampleFiles(mcDirectory, 'Zg')

samples['Zg'] = {
    'name': files,
    'weight': mcCommonWeightNoMatch + '*(!(Gen_ZGstar_mass > 0))',
    'FilesPerJob': 4
}

######## ZgS ########
files = nanoGetSampleFiles(mcDirectory, 'Zg')

samples['ZgS'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 4,
    }
addSampleWeight(samples, 'ZgS', 'Zg', '(Gen_ZGstar_mass > 0)')

######## WgS ########

files = nanoGetSampleFiles(mcDirectory, 'Wg_MADGRAPHMLM') + \
    nanoGetSampleFiles(mcDirectory, 'WZTo3LNu_mllmin01')

samples['WgS'] = {
    'name': files,
    'weight': mcCommonWeight + '*((Gen_ZGstar_mass >0 && Gen_ZGstar_mass < 4)*0.94)', 
    #'weight': mcCommonWeight + '*(gstarLow*0.94)', 
    'FilesPerJob': 4,
}   
addSampleWeight(samples, 'WgS', 'Wg_MADGRAPHMLM', '(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass < 0.1)')
addSampleWeight(samples, 'WgS', 'WZTo3LNu_mllmin01', '(Gen_ZGstar_mass > 0.1)')
    
######## WZ ########
    
files = nanoGetSampleFiles(mcDirectory, 'WZTo3LNu_mllmin01') + \
    nanoGetSampleFiles(mcDirectory, 'WZTo2L2Q')

samples['WZ'] = {
    'name': files,
    'weight': mcCommonWeight + '*gstarHigh',
    'FilesPerJob': 4,
}

############ ZZ ############

files = nanoGetSampleFiles(mcDirectory, 'ZZTo2L2Nu') + \
    nanoGetSampleFiles(mcDirectory, 'ZZTo2L2Q') + \
    nanoGetSampleFiles(mcDirectory, 'ZZTo4L')

samples['ZZ'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 4
}

########## VVV #########

files = nanoGetSampleFiles(mcDirectory, 'ZZZ') + \
    nanoGetSampleFiles(mcDirectory, 'WZZ') + \
    nanoGetSampleFiles(mcDirectory, 'WWZ') + \
    nanoGetSampleFiles(mcDirectory, 'WWW')
#+ nanoGetSampleFiles(mcDirectory, 'WWG'), #should this be included? or is it already taken into account in the WW sample?

samples['VVV'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 4
}


##########################################
################ SIGNALS #################
##########################################

signals = []

#### ggH -> WW

samples['ggH_hww'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2NuPowheg_M125'),
    'weight': mcCommonWeight, 
    'FilesPerJob': 4,
}

signals.append('ggH_hww')

#FIXME VBFHToWWTo2L2NuPowheg missing?
############ VBF H->WW ############
samples['qqH_hww'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 4
}

signals.append('qqH_hww')

############ ZH H->WW ############

samples['ZH_hww'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'HZJ_HToWW_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 4
}

signals.append('ZH_hww')

samples['ggZH_hww'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'ggZH_HToWW_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 4
}

signals.append('ggZH_hww')

############ WH H->WW ############

samples['WH_hww'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'HWplusJ_HToWW_M125') + nanoGetSampleFiles(mcDirectory, 'HWminusJ_HToWW_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 4
}

signals.append('WH_hww')

############ H->TauTau ############

samples['ggH_htt'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToTauTau_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 4
}

signals.append('ggH_htt')

samples['qqH_htt'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToTauTau_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 4
}

signals.append('qqH_htt')

samples['ZH_htt'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'HZJ_HToTauTau_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 4
}

signals.append('ZH_htt')

samples['WH_htt'] = {
    'name':  nanoGetSampleFiles(mcDirectory, 'HWplusJ_HToTauTau_M125') + nanoGetSampleFiles(mcDirectory, 'HWminusJ_HToTauTau_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 4
}

signals.append('WH_htt')

###########################################
################## FAKE ###################
###########################################
'''
samples['Fake'] = {
    'name': [],
    'weight': 'fakeW' ,#'METFilter_DATA*fakeW',
    'isData': ['all'],
    'FilesPerJob': 50
}
'''

samples['Fake_em'] = {
    'name': [],
    'weight': 'METFilter_DATA*fakeW2l_ele_mva_90p_Iso2016_mu_cut_Tight80x*( ( (Lepton_pdgId[0]==11 && Lepton_pdgId[1]==13) || (Lepton_pdgId[0]==13 && Lepton_pdgId[1]==11) ) || ( (Lepton_pdgId[0]==-11 && Lepton_pdgId[1]==-13) || (Lepton_pdgId[0]==-13 && Lepton_pdgId[1]==-11) ) )' ,
    'isData': ['all'],
    'FilesPerJob': 50
}

samples['Fake_mm'] = {
    'name': [],
    'weight': 'METFilter_DATA*fakeW2l_ele_mva_90p_Iso2016_mu_cut_Tight80x*( ( Lepton_pdgId[0]==13 && Lepton_pdgId[1]==13 ) || ( Lepton_pdgId[0]==-13 && Lepton_pdgId[1]==-13 ) )' ,
    'isData': ['all'],
    'FilesPerJob': 50
}

samples['Fake_ee'] = {
    'name': [],
    'weight': 'METFilter_DATA*fakeW2l_ele_mva_90p_Iso2016_mu_cut_Tight80x*( ( Lepton_pdgId[0]==11 && Lepton_pdgId[1]==11 ) || ( Lepton_pdgId[0]==-11 && Lepton_pdgId[1]==-11 ) )' ,
    'isData': ['all'],
    'FilesPerJob': 50
}

for _, sd in DataRun:
    for pd in DataSets:
        # only this file is v3
        if ('2016E' in sd and 'MuonEG' in pd):
            files = nanoGetSampleFiles(fakeDirectory, pd + '_' + sd.replace('v1', 'v3') , True)  
        else:
            files = nanoGetSampleFiles(fakeDirectory, pd + '_' + sd , True)

        samples['Fake_em']['name'].extend(files)
        samples['Fake_mm']['name'].extend(files)
        samples['Fake_ee']['name'].extend(files)

for _, sd in DataRun:
    for pd in DataSets:
        pd_name = pd + '_' + sd
        if ('2016E' in sd and 'MuonEG' in pd): pd_name = pd_name.replace('v1', 'v3') # only this file is v3
        addSampleWeight( samples , 'Fake_em' , pd_name , DataTrig[pd]  )
        addSampleWeight( samples , 'Fake_mm' , pd_name , DataTrig[pd]  )
        addSampleWeight( samples , 'Fake_ee' , pd_name , DataTrig[pd]  )

###########################################
################## DATA ###################
###########################################

samples['DATA'] = {
  'name': [],
  'weight': 'METFilter_DATA*LepWPCut',
  'isData': ['all'],
  'FilesPerJob': 50
}

for _, sd in DataRun:
  for pd in DataSets:
    # only this file is v3
    if ('2016E' in sd and 'MuonEG' in pd):
        files = nanoGetSampleFiles(dataDirectory, pd + '_' + sd.replace('v1', 'v3'))
    else:
        files = nanoGetSampleFiles(dataDirectory, pd + '_' + sd)
    
    samples['DATA']['name'].extend(files)

for _, sd in DataRun:
    for pd in DataSets:
        pd_name = pd + '_' + sd
        if ('2016E' in sd and 'MuonEG' in pd): pd_name = pd_name.replace('v1', 'v3') # only this file is v3
        addSampleWeight( samples , 'DATA' , pd_name , DataTrig[pd]  )
