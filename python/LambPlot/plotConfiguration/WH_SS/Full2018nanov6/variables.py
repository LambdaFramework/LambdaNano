# variables
# 0 = not fold (default), 1 = fold underflowbin, 2 = fold overflow bin, 3 = fold underflow and overflow

variables = {}
    
variables['events']  = {   'name': '1',      
                        'range' : (1,0,2),  
                        'xaxis' : 'events', 
                        'fold' : 3
                       }

variables['mll'] = { 'name' : 'mll' ,
                     'range' : ( 80 , 0. , 400. ) ,
                     'xaxis' : 'mll [GeV]',
                     'fold' : 3
}

#############################
variables['Ele1_tthmva'] = {
    'name' : 'Electron_mvaTTH[Lepton_electronIdx[0]]' ,
    'range' : ( 10 , 0. , 1. ),
    'xaxis' : 'Lepton1 electron ttHMVA',
    'fold' : 3
}

variables['Ele1_dz'] = { 'name' : 'Electron_dz[Lepton_electronIdx[0]]' ,
                         'range' : ( 20  , -0.01 , 0.01 ), # 10 micron in bin size
                         'xaxis' : 'Lepton1 electron dz [cm]',
                         'fold' : 3
}

variables['Ele2_dz'] = { 'name' : 'Electron_dz[Lepton_electronIdx[1]]' ,
                         'range' : ( 20  , -0.01 , 0.01 ),
                         'xaxis' : 'Lepton2 electron dz [cm]',
                         'fold' : 3
}

variables['Ele1_dxy'] = { 'name' : 'Electron_dxy[Lepton_electronIdx[0]]' ,
                          'range' : ( 20  , -0.01 , 0.01 ),
                         'xaxis' : 'Lepton1 electron dxy [cm]',
                         'fold' : 3
}

variables['Ele2_dxy'] = { 'name' : 'Electron_dxy[Lepton_electronIdx[1]]' ,
                          'range' : ( 20  , -0.01 , 0.01 ),
                         'xaxis' : 'Lepton2 electron dxy [cm]',
                         'fold' : 3
}


variables['Ele1_sip3d'] = { 'name' : 'Electron_sip3d[Lepton_electronIdx[0]]' ,
                          'range' : ( 100 , 0 , 10 ),
                         'xaxis' : 'Lepton1 electron sip3d',
                         'fold' : 3
}

variables['Ele2_sip3d'] = { 'name' : 'Electron_sip3d[Lepton_electronIdx[1]]' ,
                          'range' : ( 100 , 0 , 10 ),
                         'xaxis' : 'Lepton2 electron sip3d',
                         'fold' : 3
}

variables['Ele1_pfRelIso03_all'] = { 'name' : 'Electron_pfRelIso03_all[Lepton_electronIdx[0]]' ,
                          'range' : ( 20 , 0 , 0.1 ),
                         'xaxis' : 'Lepton1 electron pfRelIso03',
                         'fold' : 3
}

variables['Ele2_pfRelIso03_all'] = { 'name' : 'Electron_pfRelIso03_all[Lepton_electronIdx[1]]' ,
                          'range' : ( 20 , 0 , 0.1 ),
                         'xaxis' : 'Lepton2 electron pfRelIso03',
                         'fold' : 3
}

##########################
variables['Mu1_tthmva'] = {
    'name' : 'Muon_mvaTTH[Lepton_muonIdx[0]]' ,
    'range' : ( 10 , 0. , 1. ),
    'xaxis' : 'Lepton1 muon 1 ttHMVA',
    'fold' : 3
}

variables['Mu1_dz'] = { 'name' : 'Muon_dz[Lepton_muonIdx[0]]' ,
                         'range' : ( 20  , -0.01 , 0.01 ),
                         'xaxis' : 'Lepton1 muon dz [cm]',
                         'fold' : 3
}

variables['Mu2_dz'] = { 'name' : 'Muon_dz[Lepton_muonIdx[1]]' ,
                         'range' : ( 20  , -0.01 , 0.01 ),
                         'xaxis' : 'Lepton2 muon dz [cm]',
                         'fold' : 3
}

variables['Mu1_dxy'] = { 'name' : 'Muon_dxy[Lepton_muonIdx[0]]' ,
                         'range' : ( 20  , -0.01 , 0.01 ),
                         'xaxis' : 'Lepton1 muon dxy [cm]',
                         'fold' : 3
}

variables['Mu2_dxy'] = { 'name' : 'Muon_dxy[Lepton_muonIdx[1]]' ,
                         'range' : ( 20  , -0.01 , 0.01 ),
                         'xaxis' : 'Lepton2 muon dxy [cm]',
                         'fold' : 3
}

variables['Mu1_sip3d'] = { 'name' : 'Muon_sip3d[Lepton_muonIdx[0]]' ,
                          'range' : ( 100 , 0 , 10 ),
                         'xaxis' : 'Lepton1 muon sip3d',
                         'fold' : 3
}

variables['Mu2_sip3d'] = { 'name' : 'Muon_sip3d[Lepton_muonIdx[1]]' ,
                          'range' : ( 100 , 0 , 10 ),
                         'xaxis' : 'Lepton2 muon sip3d',
                         'fold' : 3
}

variables['Mu1_pfRelIso03_all'] = { 'name' : 'Muon_pfRelIso03_all[Lepton_muonIdx[0]]' ,
                          'range' : ( 20 , 0 , 0.1 ),
                         'xaxis' : 'Lepton1 muon pfRelIso03',
                         'fold' : 3
}

variables['Mu2_pfRelIso03_all'] = { 'name' : 'Muon_pfRelIso03_all[Lepton_muonIdx[1]]' ,
                          'range' : ( 20 , 0 , 0.1 ),
                         'xaxis' : 'Lepton2 muon pfRelIso03',
                         'fold' : 3
}

variables['Mu1_pfRelIso04_all'] = { 'name' : 'Muon_pfRelIso04_all[Lepton_muonIdx[0]]' ,
                         'range' : ( 20 , 0 , 0.1 ),
                         'xaxis' : 'Lepton1 muon pfRelIso04',
                         'fold' : 3
}

variables['Mu2_pfRelIso04_all'] = { 'name' : 'Muon_pfRelIso04_all[Lepton_muonIdx[1]]' ,
                        'range' : ( 20 , 0 , 0.1 ),
                        'xaxis' : 'Lepton2 muon pfRelIso04',
                        'fold' : 3
}

####################################

variables['MinMjjl'] = { 'name' : 'TMath::Min(mjjL1,mjjL2)' ,
                         'range' : ( 40 , 0. , 200. ),
                         #'range' : ( 50 , 0. , 500. ),
                         'xaxis' : 'Min(mjjl1,mjjl2) [GeV/c2]',
                         'fold' : 3
}

variables['MinMjl'] = { 'name' : 'TMath::Min(mjL1,mjL2)' ,
                        'range' : ( 40 , 0. , 200. ),
                         #'range' : ( 50 , 0. , 500. ),
                         'xaxis' : 'Min(mjl1,mjl2) [GeV/c2]',
                         'fold' : 3
}

variables['MindRjjl'] = { 'name' : 'TMath::Min(dRjjL1,dRjjL2)' ,
                         'range' : ( 30 , 0. , 6 ),
                         #'range' : ( 50 , 0. , 500. ),
                         'xaxis' : 'Min(dRjjL1,dRjjL2)',
                         'fold' : 3
}

variables['MindRjl'] = { 'name' : 'TMath::Min(dRjL1,dRjL2)' ,
                        'range' : ( 30 , 0. , 6. ),
                        #'range' : ( 50 , 0. , 500. ),                                                               
                         'xaxis' : 'Min(dRjL1,dRjL2)',
                         'fold' : 3
}


variables['nJet'] = { 'name' : 'Sum(CleanJet_pt>30)' ,
                        'range' : ( 15 , 0 , 15 ),
                        'xaxis' : 'nCleanJet',
                        'fold' : 3
}

variables['mlljj20_whss']  = {   'name': 'mlljj20_whss',
                        #'range' : ( 40 , 0. , 200. ),
                        'range' : ( 50 , 0. , 500. ),
                        'xaxis' : 'mlljj20_whss [GeV]',
			'fold' : 3
                        }

variables['mlljj20_whss_bin1']  = {   'name': 'mlljj20_whss',
                        'range' : ([60.,70.,80.,90.,100.,110.,120.,130.,140.,150.,160.,170.,180.,190.,200.,250.,300.],),
                        'xaxis' : 'mlljj20_whss [GeV]',
                        'fold' : 3
                        }

variables['mlljj20_whss_bin2']  = {   'name': 'mlljj20_whss',
                        'range' : ([60.,100.,110.,120.,130.,140.,150.,160.,170.,180.,190.,200.,250.,300.],),
                        'xaxis' : 'mlljj20_whss [GeV]',
                        'fold' : 3
                        }

variables['mlljj20_whss_bin3']  = {   'name': 'mlljj20_whss',
                        'range' : ([60.,120.,130.,140.,150.,160.,170.,180.,190.,200.,250.,300.],),
                        'xaxis' : 'mlljj20_whss [GeV]',
                        'fold' : 3
                        }

variables['mlljj20_whss_bin4']  = {   'name': 'mlljj20_whss',
                        'range' : (8,60.,300.),
                        'xaxis' : 'mlljj20_whss [GeV]',
                        'fold' : 3
                        }

variables['ZH3l_dphilmetjj']  = {  'name': 'ZH3l_dphilmetjj*(CleanJet_pt[1]>30)',
                        'range' : (20,0,3.2),
                        'xaxis' : 'ZH3l_dphilmetjj',
                         'fold' : 3
                        }

variables['ZH3l_dphilmetj']  = {  'name': 'ZH3l_dphilmetj*(CleanJet_pt[1]>30)',
                        'range' : (20,0,3.2),
                        'xaxis' : 'ZH3l_dphilmetj',
                         'fold' : 3
                        }

#variables['WH3l_ZVeto']  = {   'name': 'WH3l_ZVeto',            #   variable name    
#                        'range' : (20,0,100),    #   variable range
#                        'xaxis' : 'WH3l_ZVeto',  #   x axis name
#                         'fold' : 0
#                        }

variables['puppimet']  = {
                        'name': 'PuppiMET_pt',    
                        'range' : (20,0,200),
                        'xaxis' : 'pfmet [GeV]',
                        'fold'  : 3
                        }
#variables['mll']  = {   'name': 'mll',            #   variable name    
#                        'range' : (20, 40,120),    #   variable range
#                        'xaxis' : 'm_{ll} [GeV]',  #   x axis name
#                         'fold' : 0
#                        }

variables['detall']  = {   'name': 'detall',            #   variable name    
                        'range' : (20,0.,10.),    #   variable range
                        'xaxis' : 'detall',  #   x axis name
                        'fold' : 3
                        }


variables['mth']  = {   'name': 'mth',            #   variable name    
                        'range' : (40,0,200),    #   variable range
                        'xaxis' : 'm_{T}^{H} [GeV]',  #   x axis name
                         'fold' : 0
                        }

variables['dphill']  = {   'name': 'abs(dphill)',     
                        'range' : (20,0,3.14),   
                        'xaxis' : '#Delta#phi_{ll}',
                        'fold' : 3
                        }


variables['ptll']  = {   'name': 'ptll',     
                        'range' : (40, 0,200),   
                        'xaxis' : 'p_{T}^{ll} [GeV]',
                        'fold' : 0
                        }
variables['pt1']  = {   'name': 'Lepton_pt[0]',     
                        'range' : (40,0,200),   
                        'xaxis' : 'p_{T} 1st lep',
                        'fold'  : 3                         
                        }

variables['pt2']  = {   'name': 'Lepton_pt[1]',     
                        'range' : (40,0,200),   
                         'xaxis' : 'p_{T} 2nd lep',
                        'fold'  : 3                         
                        }
variables['eta1']  = {  'name': 'Lepton_eta[0]',     
                        'range' : (10,-2.5,2.5),   
                        'xaxis' : '#eta 1st lep',
                        'fold'  : 3                         
                        }

variables['eta2']  = {  'name': 'Lepton_eta[1]',     
                        'range' : (10,-2.5,2.5),   
                        'xaxis' : '#eta 2nd lep',
                        'fold'  : 3                         
                        }


variables['jetpt1']  = {
                        'name': 'CleanJet_pt[0]*(CleanJet_pt[0]>30)',     
                        'range' : (20,0,400),   
                        'xaxis' : 'p_{T} 1st jet',
                        'fold' : 2   # 0 = not fold (default), 1 = fold underflowbin, 2 = fold overflow bin, 3 = fold underflow and overflow
                        }

variables['jetpt2']  = {
                        'name': 'CleanJet_pt[1]*(CleanJet_pt[1]>30)',     
                        'range' : (20,0,400),   
                        'xaxis' : 'p_{T} 2nd jet',
                        'fold' : 0   # 0 = not fold (default), 1 = fold underflowbin, 2 = fold overflow bin, 3 = fold underflow and overflow
                        }

variables['mjj']  = {  'name': 'mjj',
                        'range' : (50,0,400),
                        'xaxis' : 'm_{jj} [GeV]',
                         'fold' : 3
                        }

variables['puppimet']  = {
                        'name': 'PuppiMET_pt',    
                        'range' : (40,0,200),
                        'xaxis' : 'pfmet [GeV]',
                        'fold'  : 3
                        } 


variables['mth']  = {   'name': 'mth',            #   variable name    
                        'range' : (40,0,200),    #   variable range
                        'xaxis' : 'm_{T}^{H} [GeV]',  #   x axis name
                         'fold' : 0
                        }

variables['dphill']  = {   'name': 'abs(dphill)',     
                        'range' : (20,0,3.14),   
                        'xaxis' : '#Delta#phi_{ll}',
                        'fold' : 3
                        }


variables['ptll']  = {   'name': 'ptll',     
                        'range' : (40, 0,200),   
                        'xaxis' : 'p_{T}^{ll} [GeV]',
                        'fold' : 0
                        }

variables['mtw1']  = {  'name': 'mtw1',
                        'range' : (40,0,200),
                        'xaxis' : 'm_{T}^{W_{1}} [GeV]',
                         'fold' : 3
                        }

variables['mtw2']  = {  'name': 'mtw2',
                        'range' : (40,0,200),
                        'xaxis' : 'm_{T}^{W_{2}} [GeV]',
                         'fold' : 3
                        }


variables['dphilljet']  = {  'name': 'dphilljet',
                        'range' : (20,0,3.2),
                        'xaxis' : 'dphilljet',
                         'fold' : 3
                        }

#variables['dphilljetjet']  = {  'name': 'dphilljetjet*(CleanJet_pt[1]>30)',
#                        'range' : (20,0,3.2),
#                        'xaxis' : 'dphilljetjet',
#                         'fold' : 3
#                        }

variables['dphilmet']  = {  'name': 'dphilmet',
                        'range' : (20,0,3.2),
                        'xaxis' : 'dphilmet',
                         'fold' : 3
                        }


variables['dphillmet']  = {  'name': 'dphillmet',
                        'range' : (20,0,3.2),
                        'xaxis' : 'dphillmet',
                         'fold' : 3
                        }

variables['dphilep1jet1']  = {  'name': 'dphilep1jet1',
                        'range' : (20,0,3.2),
                        'xaxis' : 'dphilep1jet1',
                         'fold' : 3
                        }

variables['dphilep1jet2']  = {  'name': 'dphilep1jet2',
                        'range' : (20,0,3.2),
                        'xaxis' : 'dphilep1jet2',
                         'fold' : 3
                        }

variables['dphilep2jet1']  = {  'name': 'dphilep2jet1',
                        'range' : (20,0,3.2),
                        'xaxis' : 'dphilep2jet1',
                         'fold' : 3
                        }

variables['dphilep2jet2']  = {  'name': 'dphilep2jet2',
                        'range' : (20,0,3.2),
                        'xaxis' : 'dphilep1jet2',
                         'fold' : 3
                        }

variables['dphijjmet']  = {  'name': 'dphijjmet',
                        'range' : (20,0,3.2),
                        'xaxis' : 'dphijjmet',
                         'fold' : 3
                        }

variables['ht']  = {  'name': 'ht',
                        'range' : (100,0,1000),
                        'xaxis' : 'ht [GeV]',
                         'fold' : 3
                        }

