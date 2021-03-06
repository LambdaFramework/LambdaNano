import os
import inspect
from collections import Counter

from PhysicsTools.NanoAODTools.LambPlot.plotConfiguration.helper import addSampleWeight, nanoGetSampleFiles

# sample
try:
    len(samples)
except NameError:
    import collections
    samples = collections.OrderedDict()


mcDirectory = '/home/shoh/works/workbench/WHSS/analysis/LambdaNano/skimmed-2017'
dataDirectory = mcDirectory
fakeDirectory = mcDirectory

################################################
############ DATA DECLARATION ##################
################################################

DataRun = [
    ['B','Run2017B-Nano1June2019-v1'],
    ['C','Run2017C-Nano1June2019-v1'],
    ['D','Run2017D-Nano1June2019-v1'],
    ['E','Run2017E-Nano1June2019-v1'],
    ['F','Run2017F-Nano1June2019-v1']
]

DataSets = ['MuonEG','SingleMuon','SingleElectron','DoubleMuon', 'DoubleEG']

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

# SFweight
#IDcutMC='SFweight' # SFweight
#IDcutDATA='LepWPCut' # LepWPCut
#IDcutFAKE='fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW'

IDcutMC='SFweight_tthmva'
IDcutDATA='LepWPCut_tthmva'
IDcutFAKE='fakeW2l_ele_mvaFall17V1Iso_WP90_tthmva_70_mu_cut_Tight_HWWW_tthmva_80'

btag_ver='v1'
BTAG_VETO='bVeto_%s*bVetoSF_%s' %( btag_ver , btag_ver )

flav="1" #"isSS_2l"

mcCommonWeightNoMatch = 'XSWeight*%s*METFilter_MC*(%s)*%s' %( IDcutMC , BTAG_VETO , flav )
mcCommonWeight = 'XSWeight*%s*PromptGenLepMatch2l*METFilter_MC*(%s)*%s' %( IDcutMC , BTAG_VETO , flav )

mcFlip_os = 'flip_ele_HWW_WP_2l' if 'tthmva' not in mcCommonWeight or 'tthmva' not in mcCommonWeightNoMatch else 'flip_ele_HWW_tthMVA_WP_2l'

mcCommonWeight_os = 'XSWeight*%s*PromptGenLepMatch2l*METFilter_MC*(%s)*(%s)*isOS_2l' %( IDcutMC , BTAG_VETO , mcFlip_os )

###########################################
#############  BACKGROUNDS  ###############
###########################################

###### DY #######

useDYtt = False

ptllDYW_NLO = '(((0.623108 + 0.0722934*gen_ptll - 0.00364918*gen_ptll*gen_ptll + 6.97227e-05*gen_ptll*gen_ptll*gen_ptll - 4.52903e-07*gen_ptll*gen_ptll*gen_ptll*gen_ptll)*(gen_ptll<45)*(gen_ptll>0) + 1*(gen_ptll>=45))*(abs(gen_mll-90)<3) + (abs(gen_mll-90)>3))'
ptllDYW_LO = '((0.632927+0.0456956*gen_ptll-0.00154485*gen_ptll*gen_ptll+2.64397e-05*gen_ptll*gen_ptll*gen_ptll-2.19374e-07*gen_ptll*gen_ptll*gen_ptll*gen_ptll+6.99751e-10*gen_ptll*gen_ptll*gen_ptll*gen_ptll*gen_ptll)*(gen_ptll>0)*(gen_ptll<100)+(1.41713-0.00165342*gen_ptll)*(gen_ptll>=100)*(gen_ptll<300)+1*(gen_ptll>=300))'

'''
if useDYtt:
    files = nanoGetSampleFiles(mcDirectory, 'DYJetsToTT_MuEle_M-50_fix') + \
        nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-10to50-LO')

    samples['DY'] = {
        'name': files,
        'weight': mcCommonWeight + '*( !(Sum$(PhotonGen_isPrompt==1 && PhotonGen_pt>15 && abs(PhotonGen_eta)<2.6) > 0 &&\
                                         Sum$(LeptonGen_isPrompt==1 && LeptonGen_pt>15)>=2) )',
        'FilesPerJob': 5,
    }
    addSampleWeight(samples,'DY','DYJetsToTT_MuEle_M-50_fix',ptllDYW_NLO)
    addSampleWeight(samples,'DY','DYJetsToLL_M-10to50-LO',ptllDYW_LO)

    ## Remove OF from inclusive sample (is it needed?)
    #cutSF = '(abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11)||(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13)'
    #addSampleWeight(samples,'DY','DYJetsToLL_M-50',cutSF)

else:
'''
files = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-10to50-LO_ext1') + \
        nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50-LO_ext1')

samples['DY'] = {
    'name': files,
    'weight': mcCommonWeight + '*(Sum(GenPart_pdgId == 22 && (GenPart_statusFlags % 2) && GenPart_pt > 20.) == 0)' ,
    'FilesPerJob': 8,
}
addSampleWeight(samples,'DY','DYJetsToLL_M-10to50-LO_ext1',ptllDYW_LO)
addSampleWeight(samples,'DY','DYJetsToLL_M-50-LO_ext1',ptllDYW_LO)

## chargeflip samples
samples['mischar'] = {
    'name': files,
    'weight': mcCommonWeight + '*(Sum(GenPart_pdgId == 22 && (GenPart_statusFlags % 2) && GenPart_pt > 20.) == 0)',
    #'weight': mcCommonWeightNoMatch + '*flip_ele_HWW_tthMVA_WP_2l',
    'FilesPerJob': 8,
}
addSampleWeight(samples,'mischar','DYJetsToLL_M-10to50-LO_ext1',ptllDYW_LO)
addSampleWeight(samples,'mischar','DYJetsToLL_M-50-LO_ext1',ptllDYW_LO)

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
}

addSampleWeight(samples,'top','TTTo2L2Nu','(topGenPt * antitopGenPt > 0.) * (TMath::Sqrt(TMath::Exp(0.0615 - 0.0005 * topGenPt) * TMath::Exp(0.0615 - 0.0005 * antitopGenPt))) + (topGenPt * antitopGenPt <= 0.)')
#addSampleWeight(samples,'top','TTTo2L2Nu', mcFlip_os.split('*')[-1] )
#addSampleWeight(samples,'top','ST_tW_antitop', mcFlip_os.split('*')[-1] )
#addSampleWeight(samples,'top','ST_tW_top', mcFlip_os.split('*')[-1] )

###### WW ########

samples['WW'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu'),
    'weight': mcCommonWeight + '*nllW',
    'FilesPerJob': 1
}

#addSampleWeight(samples,'WW','WWTo2L2Nu', mcFlip_os.split('*')[-1] )

samples['WWewk'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'WpWmJJ_EWK_noTop'),
    'weight': mcCommonWeight + '*(Sum(abs(GenPart_pdgId)==6 || GenPart_pdgId==25)==0)', #filter tops and Higgs
    'FilesPerJob': 2
}

#addSampleWeight(samples,'WW','WpWmJJ_EWK_noTop', mcFlip_os.split('*')[-1] )

# k-factor 1.4 already taken into account in XSWeight
files = nanoGetSampleFiles(mcDirectory, 'GluGluToWWToENEN') + \
    nanoGetSampleFiles(mcDirectory, 'GluGluToWWToENMN') + \
    nanoGetSampleFiles(mcDirectory, 'GluGluToWWToENTN') + \
    nanoGetSampleFiles(mcDirectory, 'GluGluToWWToMNEN') + \
    nanoGetSampleFiles(mcDirectory, 'GluGluToWWToMNMN') + \
    nanoGetSampleFiles(mcDirectory, 'GluGluToWWToMNTN') + \
    nanoGetSampleFiles(mcDirectory, 'GluGluToWWToTNEN') + \
    nanoGetSampleFiles(mcDirectory, 'GluGluToWWToTNMN') + \
    nanoGetSampleFiles(mcDirectory, 'GluGluToWWToTNTN')

samples['ggWW'] = {
    'name': files,
    'weight': mcCommonWeight + '*(1.53/1.4)' ,#+ mcFlip_os , # updating k-factor
    'FilesPerJob': 10
}

######## Zg ########

files = nanoGetSampleFiles(mcDirectory, 'ZGToLLG')

samples['Zg'] = {
    'name': files,
    'weight': mcCommonWeightNoMatch + '*(!(Gen_ZGstar_mass > 0))',
    'FilesPerJob': 10
}

######## Wg ########

files = nanoGetSampleFiles(mcDirectory, 'Wg_MADGRAPHMLM')

samples['Wg'] = {
    'name': files,
    'weight': mcCommonWeightNoMatch + '*(!(Gen_ZGstar_mass > 0))',
    'FilesPerJob': 10
}

######## ZgS ########

files = nanoGetSampleFiles(mcDirectory, 'ZGToLLG')

samples['ZgS'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 1,
    }
addSampleWeight(samples, 'ZgS', 'ZGToLLG', '(Gen_ZGstar_mass > 0)')

######## WgS ########

files = nanoGetSampleFiles(mcDirectory, 'Wg_MADGRAPHMLM') + \
    nanoGetSampleFiles(mcDirectory, 'WZTo3LNu_mllmin01')

samples['WgS'] = {
    'name': files,
    'weight': mcCommonWeight + '*((Gen_ZGstar_mass >0 && Gen_ZGstar_mass < 4)*0.94)',
    #'weight': mcCommonWeight + ' * (gstarLow * 0.94)',
    'FilesPerJob': 4,
}
addSampleWeight(samples, 'WgS', 'Wg_MADGRAPHMLM', '(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass < 0.1)')
addSampleWeight(samples, 'WgS', 'WZTo3LNu_mllmin01', '(Gen_ZGstar_mass > 0.1)')

######## WZ ########

files = nanoGetSampleFiles(mcDirectory, 'WZTo3LNu_mllmin01') + \
    nanoGetSampleFiles(mcDirectory, 'WZTo2L2Q')

samples['WZ'] = {
    'name': files,
    'weight': mcCommonWeight + ' *gstarHigh',
    'FilesPerJob': 4,
}

############ ZZ ############

files = nanoGetSampleFiles(mcDirectory, 'ZZTo2L2Nu') + \
    nanoGetSampleFiles(mcDirectory, 'ZZTo2L2Q') + \
    nanoGetSampleFiles(mcDirectory, 'ZZTo4L')

samples['ZZ'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 2
}

########## VVV #########
# nanoGetSampleFiles(mcDirectory, 'WWZ')
files = nanoGetSampleFiles(mcDirectory, 'ZZZ') + \
    nanoGetSampleFiles(mcDirectory, 'WZZ') + \
    nanoGetSampleFiles(mcDirectory, 'WWW')
#+ nanoGetSampleFiles(mcDirectory, 'WWG'), #should this be included? or is it already taken into account in the WW sample?

samples['VVV'] = {
    'name': files,
    'weight': mcCommonWeight
}

###########################################
#############   SIGNALS  ##################
###########################################

signals = []

#### ggH -> WW

samples['ggH_hww'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2NuPowheg_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 4,
}

signals.append('ggH_hww')

############ VBF H->WW ############
samples['qqH_hww'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2NuPowheg_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 3
}

signals.append('qqH_hww')

############# ZH H->WW ############

samples['ZH_hww'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'HZJ_HToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 1
}

signals.append('ZH_hww')

samples['ggZH_hww'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'GluGluZH_HToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 2
}

signals.append('ggZH_hww')

############ WH H->WW ############

samples['WH_hww'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'HWplusJ_HToWW_M125') + nanoGetSampleFiles(mcDirectory, 'HWminusJ_HToWW_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 2
}

signals.append('WH_hww')

############ ttH ############

samples['ttH_hww'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'ttHToNonbb_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 1
}

signals.append('ttH_hww')

############ H->TauTau ############

samples['ggH_htt'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToTauTau_M125_ext1'),
    'weight': mcCommonWeight,
    'FilesPerJob': 1
}

signals.append('ggH_htt')

samples['qqH_htt'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToTauTau_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 2
}

signals.append('qqH_htt')

samples['ZH_htt'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'HZJ_HToTauTau_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 2
}

signals.append('ZH_htt')

samples['WH_htt'] = {
    'name':  nanoGetSampleFiles(mcDirectory, 'HWplusJ_HToTauTau_M125') + nanoGetSampleFiles(mcDirectory, 'HWminusJ_HToTauTau_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 2
}
signals.append('WH_htt')

###########################################
################## FAKE ###################
###########################################

samples['Fake'] = {
    'name': [],
    'weight': 'METFilter_DATA*%s*%s*%s' %( IDcutFAKE , BTAG_VETO.split('*')[0] , flav ),
    'isData': ['all'],
    'FilesPerJob': 10
}


'''

for _, sd in DataRun:
  for pd in DataSets:
    files = nanoGetSampleFiles(fakeDirectory, pd + '_' + sd)
    samples['Fake']['name'].extend(files)
    samples['Fake']['weights'].extend([DataTrig[pd]] * len(files))

samples['Fake']['subsamples'] = {
  'em': 'Lepton_pdgId[0]*Lepton_pdgId[1] == 11*13',
  'mm': 'Lepton_pdgId[0]*Lepton_pdgId[1] == 13*13'
#  'ee': 'Lepton_pdgId[0]*Lepton_pdgId[1] == 11*11'
}
'''

samples['Fake_em'] = {
    'name': [],
    'weight': 'METFilter_DATA*%s*%s && ( Lepton_pdgId[0]*Lepton_pdgId[1] == 11*13 )' %( IDcutFAKE , BTAG_VETO.split('*')[0] ) ,
    'isData': ['all'],
    'FilesPerJob': 50
}

samples['Fake_mm'] = {
    'name': [],
    'weight': 'METFilter_DATA*%s*%s && ( Lepton_pdgId[0]*Lepton_pdgId[1] == 13*13 )' %( IDcutFAKE , BTAG_VETO.split('*')[0] ) ,
    'isData': ['all'],
    'FilesPerJob': 50
}

samples['Fake_ee'] = {
    'name': [],
    'weight': 'METFilter_DATA*%s*%s && ( Lepton_pdgId[0]*Lepton_pdgId[1] == 11*11 )' %( IDcutFAKE , BTAG_VETO.split('*')[0] ) ,
    'isData': ['all'],
    'FilesPerJob': 50
}

for _, sd in DataRun:
    for pd in DataSets:
        files = nanoGetSampleFiles(fakeDirectory, pd + '_' + sd , True)
        samples['Fake_em']['name'].extend(files)
        samples['Fake_mm']['name'].extend(files)
        samples['Fake_ee']['name'].extend(files)
        samples['Fake']['name'].extend(files)

for _, sd in DataRun:
    for pd in DataSets:
        pd_name = pd + '_' + sd
        addSampleWeight( samples , 'Fake_em' , pd_name , DataTrig[pd]  )
        addSampleWeight( samples , 'Fake_mm' , pd_name , DataTrig[pd]  )
        addSampleWeight( samples , 'Fake_ee' , pd_name , DataTrig[pd]  )
        addSampleWeight( samples , 'Fake'    , pd_name , DataTrig[pd]  )

###########################################
################## DATA ###################
###########################################

samples['DATA'] = {
  'name': [],
    'weight': 'METFilter_DATA*%s*%s*%s' %( IDcutDATA , BTAG_VETO.split('*')[0] , flav ),
  'isData': ['all'],
  'FilesPerJob': 40
}

'''
for _, sd in DataRun:
  for pd in DataSets:
    files = nanoGetSampleFiles(dataDirectory, pd + '_' + sd)
    samples['DATA']['name'].extend(files)
    samples['DATA']['weights'].extend([DataTrig[pd]] * len(files))
'''

for _, sd in DataRun:
    for pd in DataSets:
        files = nanoGetSampleFiles(dataDirectory, pd + '_' + sd)
        samples['DATA']['name'].extend(files)
        #samples['DATA']['weights'].extend([DataTrig[pd]] * len(files))

for _, sd in DataRun:
    for pd in DataSets:
        pd_name = pd + '_' + sd
        addSampleWeight( samples , 'DATA' , pd_name , DataTrig[pd]  )
