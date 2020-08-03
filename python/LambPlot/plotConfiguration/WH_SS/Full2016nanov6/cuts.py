# cuts
supercut = 'mll>12  \
            && Lepton_pt[0]>25 && Lepton_pt[1]>20 \
            && bVeto \
            && PuppiMET_pt > 30 \
            '

cuts={}

cuts['OSee'] = 'nCleanJet>=2 && nLepton>=2 && isbVeto && ((Lepton_pdgId[0]*Lepton_pdgId[1]==11*-11)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*11)) \
&& Electron_pt[Lepton_electronIdx[0]]>25 && Electron_pt[Lepton_electronIdx[1]]>20 \
&& Electron_pfRelIso03_all[Lepton_electronIdx[0]]<0.15 && Electron_pfRelIso03_all[Lepton_electronIdx[1]]<0.15 \
&& mll>30 && ht>100 \
'

cuts['OSmumu'] = 'nCleanJet>=2 && nLepton>=2 && ((Lepton_pdgId[0]*Lepton_pdgId[1]==13*-13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-13*13)) \
&& Muon_pt[Lepton_muonIdx[0]]>25 && Muon_pt[Lepton_muonIdx[1]]>20 \
&& Muon_pfRelIso03_all[Lepton_muonIdx[0]]<0.15 && Muon_pfRelIso03_all[Lepton_muonIdx[1]]<0.15 \
&& mll>30 && ht>100 \
'

#cuts['OSemu'] = 'nCleanJet>=2 && nLepton>=2 && isbVeto && ((Lepton_pdgId[0]==11&&Lepton_pdgId[1]==-13)||(Lepton_pdgId[0]==-11&&Lepton_pdgId[1]==13)) \
#&& Electron_pt[Lepton_electronIdx[0]]>24 && Muon_pt[Lepton_muonIdx[1]]>20 \
#&& Electron_pfRelIso03_all[Lepton_electronIdx[0]]<0.05 && Muon_pfRelIso03_all[Lepton_muonIdx[1]]<0.01 \
#&& mll>15 \
#'

# without isolation cuts it capture tau decay
cuts['OSemu-showoff'] = 'nCleanJet>=2 && nLepton>=2 && ((Lepton_pdgId[0]*Lepton_pdgId[1]==13*-11)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-13*11)) \
&& Electron_pt[Lepton_electronIdx[0]]>30 && Muon_pt[Lepton_muonIdx[1]]>20 \
&& mll>15 \
'

## remember to remove bveto
cuts['OSemu'] = 'nCleanJet>=2 && nLepton>=2 && ((Lepton_pdgId[0]*Lepton_pdgId[1]==13*-11)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-13*11)) \
&& Electron_pt[Lepton_electronIdx[0]]>30 && Muon_pt[Lepton_muonIdx[1]]>20 \
&& Electron_pfRelIso03_all[Lepton_electronIdx[0]]<0.05 && Muon_pfRelIso03_all[Lepton_muonIdx[1]]<0.01 \
&& mll>15 \
'

cuts['SSemu'] = 'nCleanJet>=2 && nLepton>=2 \
&& ((Lepton_pdgId[0]==11&&Lepton_pdgId[1]==13)||(Lepton_pdgId[0]==-11&&Lepton_pdgId[1]==-13)) \
&& Electron_pt[Lepton_electronIdx[0]]>30 && Muon_pt[Lepton_muonIdx[1]]>25 \
&& Electron_pfRelIso03_all[Lepton_electronIdx[0]]<0.05 && Muon_pfRelIso03_all[Lepton_muonIdx[1]]<0.01 \
'

# Muon_pfRelIso03_all[Lepton_muonIdx[0]]<0.1
cuts['SSmumu'] = 'nCleanJet>=2 && nLepton>=2 \
&& ((Lepton_pdgId[0]*Lepton_pdgId[1]==13*13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-13*-13)) \
&& Muon_pt[Lepton_muonIdx[0]]>27 && Muon_pt[Lepton_muonIdx[1]]>15 \
&& Muon_pfRelIso03_all[Lepton_muonIdx[0]]<0.1 \
'

#&& Sum( abs(Lepton_pdgId)==11 && abs(Electron_dz[Lepton_electronIdx])<0.5 && Electron_pfRelIso03_all[Lepton_electronIdx]<0.15 && Electron_pt[Lepton_electronIdx]>15 )==0 \
#&& ((Lepton_pdgId[0]*Lepton_pdgId[1]==13*13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-13*-13)) \
#&& Muon_pt[Lepton_muonIdx[0]]>27 && Muon_pt[Lepton_muonIdx[1]]>15 \
#&& abs(Muon_eta[Lepton_muonIdx[0]])<2.1 && abs(Muon_eta[Lepton_muonIdx[1]])<2.1 \
#&& abs(Muon_dz[Lepton_muonIdx[0]])<0.5 && abs(Muon_dz[Lepton_muonIdx[1]])<0.5 \
#&& abs(Muon_dxy[Lepton_muonIdx[0]])<0.005 && abs(Muon_dxy[Lepton_muonIdx[1]])<0.005 \
#&& Muon_pfRelIso03_all[Lepton_muonIdx[0]]<0.05 && Muon_pfRelIso03_all[Lepton_muonIdx[1]]<0.05 \
#&& ht<150 \
#&& mjj > 60 && mjj < 100 \
#'

cuts['SSee'] = 'nCleanJet>=2 && nLepton>=2 && ((Lepton_pdgId[0]*Lepton_pdgId[1]==11*11)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*-11)) \
&& Electron_pt[Lepton_electronIdx[0]]>30 && Electron_pt[Lepton_electronIdx[1]]>25 \
&& Electron_pfRelIso03_all[Lepton_electronIdx[0]]<0.1 \
'

cuts['WZCR'] = 'nCleanJet>=2 && nLepton>=2 && ( \
( Sum(abs(Lepton_pdgId)==13)>2 && Muon_pfRelIso03_all[Lepton_muonIdx[0]]<0.15 && Muon_pfRelIso03_all[Lepton_muonIdx[1]]<0.15 && abs(mll-91.19)<10 ) || \
( Sum(abs(Lepton_pdgId)==11)>0 && Electron_pt[Lepton_electronIdx[0]]>25 && Electron_pfRelIso03_all[Lepton_electronIdx[0]]<0.1 && Sum(abs(Lepton_pdgId)==13)>2 && Muon_pfRelIso03_all[Lepton_muonIdx[1]]<0.15 && Muon_pfRelIso03_all[Lepton_muonIdx[2]]<0.15 && abs(mll-91.19)<10 ) || \
( Sum(abs(Lepton_pdgId)==13)>0 && Sum(abs(Lepton_pdgId)==11)>1 && Muon_pt[Lepton_muonIdx[0]]>25 && Muon_pfRelIso03_all[Lepton_muonIdx[0]]<0.1 && Electron_pt[Lepton_electronIdx[1]]>25 && Electron_pt[Lepton_electronIdx[2]]>20 ) \
) \
'

cuts['VgCR'] = 'nCleanJet>=2 && nLepton>=2 && isbVeto && ( \
( Sum(abs(Lepton_pdgId==13))==4 && Muon_pt[Lepton_muonIdx[3]]>5 && Muon_pfRelIso03_all[Lepton_muonIdx[3]]<0.2 ) || \
( Sum(abs(Lepton_pdgId==13))==2 && Sum(abs(Lepton_pdgId==11))>0 && Electron_pt[Lepton_electronIdx[0]]>25 && Electron_pfRelIso03_all[Lepton_electronIdx[0]]<0.1 && Muon_pt[Lepton_muonIdx[1]]>20 && Muon_pfRelIso03_all[Lepton_muonIdx[1]]<0.1 && Muon_pt[Lepton_muonIdx[2]]>10 && Muon_pfRelIso03_all[Lepton_muonIdx[2]]<0.15 ) \
) \
'


'''
## SR 2jets
cuts['hww2l2v_13TeV_of2j_WH_SS_uu_2j'] = 'isbVeto \
                                       &&(Lepton_pdgId[0]*Lepton_pdgId[1] == 13*13) \
                                       && nLepton==2  \
                                       && nCleanJet>1 \
                                       && CleanJet_pt[0]>30 \
                                       && CleanJet_pt[1]>30 \
                                       && mjj < 100 \
                                       && abs(Lepton_eta[0] - Lepton_eta[1])<2.0 \
                                       && abs(mll-91.2)>15 \
                                       && mlljj20_whss > 50. \
                                       '
cuts['hww2l2v_13TeV_of2j_WH_SS_eu_2j'] = 'isbVeto \
                                       && (Lepton_pdgId[0]*Lepton_pdgId[1] == 11*13) \
                                       && nLepton==2 \
                                       && nCleanJet>1 \
                                       && CleanJet_pt[0]>30 \
                                       && CleanJet_pt[1]>30 \
                                       && mjj < 100 \
                                       && abs(Lepton_eta[0] - Lepton_eta[1])<2.0 \
                                       && mlljj20_whss > 50. \
                                       '
## SR 1jet

cuts['hww2l2v_13TeV_of2j_WH_SS_uu_1j'] = 'isbVeto \
                                       && (Lepton_pdgId[0]*Lepton_pdgId[1] == 13*13) \
                                       && nLepton==2 \
                                       && ( (nCleanJet==1 && CleanJet_pt[0]>30) || (nCleanJet>1 && CleanJet_pt[0]>30 && CleanJet_pt[1]<30) ) \
                                       && abs(Lepton_eta[0] - Lepton_eta[1])<2.0 \
                                       && abs(mll-91.2)>15 \
                                       && mlljj20_whss > 50. \
                                       '
cuts['hww2l2v_13TeV_of2j_WH_SS_eu_1j'] = 'isbVeto \
                                       && (Lepton_pdgId[0]*Lepton_pdgId[1] == 11*13) \
                                       && nLepton==2 \
                                       && ( (nCleanJet==1 && CleanJet_pt[0]>30) || (nCleanJet>1 && CleanJet_pt[0]>30 && CleanJet_pt[1]<30) ) \
                                       && abs(Lepton_eta[0] - Lepton_eta[1])<2.0 \
                                       && mlljj20_whss > 50. \
                                       '
'''
### WZ CR

'''
cuts['hww2l2v_13TeV_of2j_WH_SS_WZ_1j'] = '((Lepton_pdgId[0]*Lepton_pdgId[1] == 13*13) || (Lepton_pdgId[0]*Lepton_pdgId[1] == 11*13))\
                                       && (nLepton>=3 && Alt$(Lepton_pt[3],0)<10) \
                                       && Lepton_pt[2]>15 \
                                       && Alt$(CleanJet_pt[0],0)>30 \
                                       && Alt$(CleanJet_pt[1],0)<30 \
                                       && WH3l_mlll > 100 \
                                       && abs(WH3l_chlll) == 1 \
                                       '

cuts['hww2l2v_13TeV_of2j_WH_SS_WZ_2j'] = '((Lepton_pdgId[0]*Lepton_pdgId[1] == 13*13) || (Lepton_pdgId[0]*Lepton_pdgId[1] == 11*13)) \
                                       && (nLepton>=3 && Alt$(Lepton_pt[3],0)<10) \
                                       && Lepton_pt[2]>15 \
                                       && Alt$(CleanJet_pt[0],0)>30 \
                                       && Alt$(CleanJet_pt[1],0)>30 \
                                       && WH3l_mlll > 100 \
                                       && abs(WH3l_chlll) == 1 \
                                       '


cuts['zh3l_WZ_CR_2j'] = ' Alt$( CleanJet_pt[0], 0) >= 30 \
                       && Alt$( CleanJet_pt[1], 0) >= 30 \
                       && WH3l_ZVeto < 25 \
                       && bVeto \
                       && ZH3l_Z4lveto > 20 \
                       && ZH3l_dphilmetjj_test > 3.14159/2 \
                       '

cuts['zh3l_WZ_CR_1j'] = ' Alt$( CleanJet_pt[0], 0) >= 30 \
                       && Alt$( CleanJet_pt[1], 0) < 30 \
                       && WH3l_ZVeto < 25 \
                       && bVeto \
                       && ZH3l_Z4lveto > 20 \
                       && ZH3l_dphilmetj_test > 3.14159/2 \
                       '
'''
