# cuts
supercut = 'mll>12  \
            && Lepton_pt[0]>25 && Lepton_pt[1]>20 \
            && bVeto \
            && PuppiMET_pt > 30 \
            '
cuts={}

cuts['OSee'] = 'nCleanJet>=2 && nLepton>=2 && isbVeto && ((Lepton_pdgId[0]*Lepton_pdgId[1]==11*-11)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*11)) \
&& Electron_pt[Lepton_electronIdx[0]]>25 && Electron_pt[Lepton_electronIdx[1]]>20 \
&& mll>30 \
'

cuts['OSmumu'] = 'nCleanJet>=2 && nLepton>=2 && isbVeto && ((Lepton_pdgId[0]*Lepton_pdgId[1]==13*-13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-13*13)) \
&& Muon_pt[Lepton_muonIdx[0]]>25 && Muon_pt[Lepton_muonIdx[1]]>20 \
&& mll>30 \
'

cuts['OSemu-showoff'] = 'Sum(CleanJet_pt>30)>=2 && nLepton>=2 && isbVeto && ((Lepton_pdgId[0]*Lepton_pdgId[1]==13*-11)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-13*11)) \
&& Electron_pt[Lepton_electronIdx[0]]>30 && Muon_pt[Lepton_muonIdx[1]]>20 \
&& mll>15 \
'

cuts['SSmumu_ugo_2jets'] ='nLepton==2 && Sum(CleanJet_pt>30)<3 \
&& ((Lepton_pdgId[0]*Lepton_pdgId[1]==13*13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-13*-13)) \
&& Muon_pt[Lepton_muonIdx[0]]>25 && Muon_pt[Lepton_muonIdx[1]]>20 \
&& abs(Muon_eta[Lepton_muonIdx[0]])<2.1 && abs(Muon_eta[Lepton_muonIdx[1]])<2.1 \
'

cuts['SSmumu_ugo_2jets_iso_ip'] ='nLepton==2 && Sum(CleanJet_pt>30)<3 \
&& ((Lepton_pdgId[0]*Lepton_pdgId[1]==13*13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-13*-13)) \
&& Muon_pt[Lepton_muonIdx[0]]>25 && Muon_pt[Lepton_muonIdx[1]]>20 \
&& abs(Muon_eta[Lepton_muonIdx[0]])<2.1 && abs(Muon_eta[Lepton_muonIdx[1]])<2.1 \
&& abs(Muon_dz[Lepton_muonIdx[0]])<0.5 && abs(Muon_dz[Lepton_muonIdx[1]])<0.5 \
&& abs(Muon_dxy[Lepton_muonIdx[0]])<0.004 && abs(Muon_dxy[Lepton_muonIdx[1]])<0.004 \
&& Muon_pfRelIso03_all[Lepton_muonIdx[0]]<0.05 && Muon_pfRelIso03_all[Lepton_muonIdx[1]]<0.05 \
'

cuts['SSmumu_ugo_2jets_iso'] ='nLepton==2 && Sum(CleanJet_pt>30)<3 \
&& ((Lepton_pdgId[0]*Lepton_pdgId[1]==13*13)||(Lepton_pdgId[0]*Lepton_pdgId[1]==-13*-13)) \
&& Muon_pt[Lepton_muonIdx[0]]>25 && Muon_pt[Lepton_muonIdx[1]]>20 \
&& abs(Muon_eta[Lepton_muonIdx[0]])<2.1 && abs(Muon_eta[Lepton_muonIdx[1]])<2.1 \
&& Muon_pfRelIso03_all[Lepton_muonIdx[0]]<0.05 && Muon_pfRelIso03_all[Lepton_muonIdx[1]]<0.05 \
'


'''
## SR 2jets
cuts['hww2l2v_13TeV_of2j_WH_SS_uu_2j'] = '(Lepton_pdgId[0]*Lepton_pdgId[1] == 13*13) \
                                       && nLepton==2  \
                                       && Alt$(CleanJet_pt[0],0)>30 \
                                       && Alt$(CleanJet_pt[1],0)>30 \
                                       && mjj < 100 \
                                       && abs(Lepton_eta[0] - Lepton_eta[1])<2.0 \
                                       && abs(mll-91.2)>15 \
                                       && mlljj20_whss > 50. \
                                       '
cuts['hww2l2v_13TeV_of2j_WH_SS_eu_2j'] = '(Lepton_pdgId[0]*Lepton_pdgId[1] == 11*13) \
                                       && nLepton==2 \
                                       && Alt$(CleanJet_pt[0],0)>30 \
                                       && Alt$(CleanJet_pt[1],0)>30 \
                                       && mjj < 100 \
                                       && abs(Lepton_eta[0] - Lepton_eta[1])<2.0 \
                                       && mlljj20_whss > 50. \
                                       '
## SR 1jet

cuts['hww2l2v_13TeV_of2j_WH_SS_uu_1j'] = '(Lepton_pdgId[0]*Lepton_pdgId[1] == 13*13) \
                                       && nLepton==2 \
                                       && Alt$(CleanJet_pt[0],0)>30 \
                                       && Alt$(CleanJet_pt[1],0)<30 \
                                       && abs(Lepton_eta[0] - Lepton_eta[1])<2.0 \
                                       && abs(mll-91.2)>15 \
                                       && mlljj20_whss > 50. \
                                       '
cuts['hww2l2v_13TeV_of2j_WH_SS_eu_1j'] = '(Lepton_pdgId[0]*Lepton_pdgId[1] == 11*13) \
                                       && nLepton==2 \
                                       && Alt$(CleanJet_pt[0],0)>30 \
                                       && Alt$(CleanJet_pt[1],0)<30 \
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
'''
