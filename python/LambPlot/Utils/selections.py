#import PhysicsTools.NanoAODTools.LambPlot.scripts.plotter as plt
#from PhysicsTools.NanoAODTools.LambPlot.Utils.Misc import *
from re import sub
AND=' && '
#dataset
#MuTrig='(HLT_IsoMu22 || HLT_IsoMu22_eta2p1 || HLT_IsoTkMu22_eta2p1 || HLT_IsoMu24 || HLT_IsoTkMu24 || HLT_Mu45_eta2p1 || HLT_Mu50)'
MuTrig='(HLT_IsoMu24 || HLT_IsoTkMu24)'
MuTrig17='(HLT_IsoMu20 || HLT_IsoMu24)'
#EleTrig='(HLT_Ele25_WPTight_Gsf || HLT_Ele27_WPLoose_Gsf || HLT_Ele27_WPTight_Gsf)'
EleTrig='(HLT_Ele25_WPTight_Gsf || HLT_Ele27_eta2p1_WPLoose_Gsf || HLT_Ele27_eta2p1_WPLoose_Gsf)'
EleTrig17='(HLT_Ele27_WPTight_Gsf)'

#Preselection
#presel='nLepton>=2 && nCleanJet>=2'
presel='nLepton>=2 && nCleanJet>=2'

Run2_2016_v4={
    'selection' : {
        'OSmumu'    : MuTrig  +AND+presel+AND+'((Lepton_pdgId[0]*Lepton_pdgId[1]==13*-13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-13*13)) && Lepton_pt[0]>30 && Lepton_pt[1]>20 && Lepton_pfRelIso03_all[0]<0.15 && Lepton_pfRelIso03_all[1]<0.15 && Vll_mass>30 && MHT_pt>50',
        'OSee'      : EleTrig +AND+presel+AND+'((Lepton_pdgId[0]*Lepton_pdgId[1]==11*-11)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*11)) && Lepton_pt[0]>25 && Lepton_pt[1]>15 && Lepton_pfRelIso03_all[0]<0.15 && Lepton_pfRelIso03_all[1]<0.15 && Vll_mass>30 && MHT_pt>50',
        'OSemu'     : MuTrig  +AND+presel+AND+'((Lepton_pdgId[0]*Lepton_pdgId[1]==11*-13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*13)) && Lepton_pt[0]>30 && Lepton_pt[1]>20 && Vll_mass>15',
        'SSemu'     : MuTrig  +AND+presel+AND+'((Lepton_pdgId[0]*Lepton_pdgId[1]==11*13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*-13)) && Lepton_pt[0]>30 && Lepton_pt[1]>20 && Vll_mass>15 && Lepton_pfRelIso03_all[0]<0.15',
        'SSmumu'    : MuTrig  +AND+presel+AND+'((Lepton_pdgId[0]*Lepton_pdgId[1]==13*13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-13*-13)) && Lepton_pt[0]>25 && Lepton_pt[1]>15 && Lepton_pfRelIso03_all[0]<0.1 && abs(Mu_dxy[0])<0.004 && abs(Mu_dxy[1])<0.004 && abs(Mu_dz[0])<0.01 && abs(Mu_dz[1])<0.01',
        'SSee'      : EleTrig +AND+presel+AND+'((Lepton_pdgId[0]*Lepton_pdgId[1]==11*11)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*-11)) && Lepton_pt[0]>30 && Lepton_pt[1]>20 && Lepton_pfRelIso03_all[0]<0.1',
        'WZCR'      : MuTrig  +AND+presel+AND+'(nMu>2 && Vll_mass-91.19 && Lepton_pfRelIso03_all[0]<0.15 && Lepton_pfRelIso03_all[1]<0.15) || (nMu>2 && Vll_mass-91.19 && Lepton_pfRelIso03_all[0]<0.15 && Lepton_pfRelIso03_all[1]<0.15 && nEle>0 && Ele_pt[0]>20 && Ele_pfRelIso03_all[0]<0.1) || (nMu>0 && nEle>1 && Mu_pt[0]>25 && Mu_pfRelIso03_all[0]<0.1 && Ele_pt[0]>25 && Ele_pt[1]>20 )',
        'VgCR'      : MuTrig  +AND+presel+AND+'(nMu==4 && Mu_pt[3]>5 && Mu_pfRelIso03_all[3]<0.2) || (nMu==2 && nEle>0 && Mu_pt[0]>20 && Mu_pfRelIso03_all[0]<0.1 && Mu_pt[1]>10 && Mu_pfRelIso03_all[1]<0.15 && Ele_pt[0]>25 && Ele_pfRelIso03_all[0]<0.1)',
        },
    'weight' : {
        'OSmumu'  : '1*puWeight*Lepton_Weight[0]*Lepton_Weight[1]',
        'OSee'    : '1*puWeight*Lepton_Weight[0]*Lepton_Weight[1]',
        'OSemu'   : '1*puWeight*Lepton_Weight[0]*Lepton_Weight[1]',
        'SSemu'   : '1*puWeight*Lepton_Weight[0]*Lepton_Weight[1]',
        'SSmumu'  : '1*puWeight*Lepton_Weight[0]*Lepton_Weight[1]',
        'SSee'    : '1*puWeight*Lepton_Weight[0]*Lepton_Weight[1]',
        'WZCR'    : '1*puWeight*Lepton_Weight[0]*Lepton_Weight[1]',
        'VgCR'    : '1*puWeight*Lepton_Weight[0]*Lepton_Weight[1]',
    },
}

Run2_2017_v4={
    'selection' : {
        'hist'    : 'HLT_IsoMu22 && (1==1)',
        'OSmumu'    : MuTrig17  +AND+presel+AND+'((Lepton_pdgId[0]*Lepton_pdgId[1]==13*-13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-13*13)) && Lepton_pt[0]>25 && Lepton_pt[1]>20 && Lepton_pfRelIso03_all[0]<0.15 && Lepton_pfRelIso03_all[1]<0.15 && Vll_mass>30 && MHT_pt>50',
        'OSee'      : EleTrig17 +AND+presel+AND+'((Lepton_pdgId[0]*Lepton_pdgId[1]==11*-11)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*11)) && MHT_pt>100 && Lepton_pt[0]>30 && Lepton_pt[1]>25 && Lepton_pfRelIso03_all[0]<0.15 && Lepton_pfRelIso03_all[1]<0.15 && Vll_mass>30 && MHT_pt>50',
        'OSemu'     : MuTrig17  +AND+presel+AND+'((Lepton_pdgId[0]*Lepton_pdgId[1]==11*-13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*13)) && Lepton_pt[0]>24 && Lepton_pt[1]>20 && Vll_mass>15',
        'SSemu'     : MuTrig17  +AND+presel+AND+'((Lepton_pdgId[0]*Lepton_pdgId[1]==11*13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*-13)) && Lepton_pt[0]>24 && Lepton_pt[1]>20 && Vll_mass>15 && Lepton_pfRelIso03_all[0]<0.15',
        'SSmumu'    : MuTrig17  +AND+presel+AND+'((Lepton_pdgId[0]*Lepton_pdgId[1]==13*13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-13*-13)) && Lepton_pt[0]>25 && Lepton_pt[1]>15 && Lepton_pfRelIso03_all[0]<0.1',
        'SSee'      : EleTrig17 +AND+presel+AND+'((Lepton_pdgId[0]*Lepton_pdgId[1]==11*11)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*-11)) && Lepton_pt[0]>25 && Lepton_pt[1]>15 && Lepton_pfRelIso03_all[0]<0.1',
        'WZCR'      : MuTrig17  +AND+presel+AND+'(nMu>2 && Vll_mass-91.19 && Lepton_pfRelIso03_all[0]<0.15 && Lepton_pfRelIso03_all[1]<0.15) || (nMu>2 && Vll_mass-91.19 && Lepton_pfRelIso03_all[0]<0.15 && Lepton_pfRelIso03_all[1]<0.15 && nEle>0 && Ele_pt[0]>20 && Ele_pfRelIso03_all[0]<0.1) || (nMu>0 && nEle>1 && Mu_pt[0]>25 && Mu_pfRelIso03_all[0]<0.1 && Ele_pt[0]>25 && Ele_pt[1]>20 )',
        'VgCR'      : MuTrig17  +AND+presel+AND+'(nMu==4 && Mu_pt[3]>5 && Mu_pfRelIso03_all[3]<0.2) || (nMu==2 && nEle>0 && Mu_pt[0]>20 && Mu_pfRelIso03_all[0]<0.1 && Mu_pt[1]>10 && Mu_pfRelIso03_all[1]<0.15 && Ele_pt[0]>25 && Ele_pfRelIso03_all[0]<0.1)',
        },
    'weight' : {
        'hist'    : '1*puWeight*Lepton_Weight[0]*Lepton_Weight[1]',
        'OSmumu'  : '1',
        'OSee'    : '1',
        'OSemu'   : '1',
        'SSemu'   : '1',
        'SSmumu'  : '1',
        'SSee'    : '1',
        'WZCR'    : '1',
        'VgCR'    : '1',
    },
}

Run2_2018_v4={
    'selection' : {
        'hist'    : 'HLT_IsoMu22 && (1==1)',
        'OSmumu'    : MuTrig  +AND+presel+AND+'((Lepton_pdgId[0]*Lepton_pdgId[1]==13*-13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-13*13)) && Lepton_pt[0]>25 && Lepton_pt[1]>20 && Lepton_pfRelIso03_all[0]<0.15 && Lepton_pfRelIso03_all[1]<0.15 && Vll_mass>30 && MHT_pt>50',
        'OSee'      : EleTrig +AND+presel+AND+'((Lepton_pdgId[0]*Lepton_pdgId[1]==11*-11)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*11)) && Lepton_pt[0]>25 && Lepton_pt[1]>15 && Lepton_pfRelIso03_all[0]<0.15 && Lepton_pfRelIso03_all[1]<0.15 && Vll_mass>30 && MHT_pt>50',
        'OSemu'     : MuTrig  +AND+presel+AND+'((Lepton_pdgId[0]*Lepton_pdgId[1]==11*-13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*13)) && Lepton_pt[0]>30 && Lepton_pt[1]>20 && Vll_mass>15',
        'SSemu'     : MuTrig  +AND+presel+AND+'((Lepton_pdgId[0]*Lepton_pdgId[1]==11*13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*-13)) && Lepton_pt[0]>30 && Lepton_pt[1]>20 && Vll_mass>15 && Lepton_pfRelIso03_all[0]<0.15',
        'SSmumu'    : MuTrig  +AND+presel+AND+'((Lepton_pdgId[0]*Lepton_pdgId[1]==13*13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-13*-13)) && Lepton_pt[0]>25 && Lepton_pt[1]>15 && Lepton_pfRelIso03_all[0]<0.1',
        'SSee'      : EleTrig +AND+presel+AND+'((Lepton_pdgId[0]*Lepton_pdgId[1]==11*11)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*-11)) && Lepton_pt[0]>30 && Lepton_pt[1]>20 && Lepton_pfRelIso03_all[0]<0.1',
        'WZCR'      : MuTrig  +AND+presel+AND+'(nMu>2 && Vll_mass-91.19 && Lepton_pfRelIso03_all[0]<0.15 && Lepton_pfRelIso03_all[1]<0.15) || (nMu>2 && Vll_mass-91.19 && Lepton_pfRelIso03_all[0]<0.15 && Lepton_pfRelIso03_all[1]<0.15 && nEle>0 && Ele_pt[0]>20 && Ele_pfRelIso03_all[0]<0.1) || (nMu>0 && nEle>1 && Mu_pt[0]>25 && Mu_pfRelIso03_all[0]<0.1 && Ele_pt[0]>25 && Ele_pt[1]>20 )',
        'VgCR'      : MuTrig  +AND+presel+AND+'(nMu==4 && Mu_pt[3]>5 && Mu_pfRelIso03_all[3]<0.2) || (nMu==2 && nEle>0 && Mu_pt[0]>20 && Mu_pfRelIso03_all[0]<0.1 && Mu_pt[1]>10 && Mu_pfRelIso03_all[1]<0.15 && Ele_pt[0]>25 && Ele_pfRelIso03_all[0]<0.1)',
        },
    'weight' : {
        'hist'    : '1*puWeight*Lepton_Weight[0]*Lepton_Weight[1]',
        'OSmumu'  : '1*puWeight',
        'OSee'    : '1*puWeight',
        'OSemu'   : '1*puWeight',
        'SSemu'   : '1*puWeight',
        'SSmumu'  : '1*puWeight',
        'SSee'    : '1*puWeight',
        'WZCR'    : '1*puWeight',
        'VgCR'    : '1*puWeight',
    },
}

#selection=eval(plt.cfg.era())['selection']
#weight=eval(plt.cfg.era())['weight']
