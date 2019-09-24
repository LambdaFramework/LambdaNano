class Dataset():
    def __init__(self, name, filename, nevent, xsec, kfactor, matcheff=1):
        self._name      = name
        self._filename  = filename
        self._nevent    = nevent
        self._xsec      = xsec
        self._kfactor   = kfactor
        self._matcheff  =  matcheff

    def name(self):
        return self._name
    def filename(self):
        return self._filename
    def nevent(self):
        return self._nevent
    def xsec(self):
        return self._xsec
    def kfactor(self):
        return self._kfactor
    def matcheff(self):
        return self._matcheff
    pass

#dataset constructor format:
#legend name , dataset name , nevent , crosss section , kfactor , matcheff

datasets ={
    'Run2_2016_v4': {
        'cert' : 'Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt',
        'data' : {
            Dataset('data_obs' , 'SingleElectronRun2016B_ver1-Nano14Dec2018_ver1-v1' , 1422819 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleElectronRun2016B_ver2-Nano14Dec2018_ver2-v1' , 246440440 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleElectronRun2016C-Nano14Dec2018-v1' , 97259854 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleElectronRun2016D-Nano14Dec2018-v1' , 148167727 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleElectronRun2016E-Nano14Dec2018-v1' , 117321545 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleElectronRun2016F-Nano14Dec2018-v1' , 70593532 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleElectronRun2016G-Nano14Dec2018-v1' , 153363109 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleElectronRun2016H-Nano14Dec2018-v1' , 129021893 , 1.0 , 1.0),
            ##Single Muon
            Dataset('data_obs' , 'SingleMuonRun2016B_ver1-Nano14Dec2018_ver1-v1' , 2789243 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleMuonRun2016B_ver2-Nano14Dec2018_ver2-v1' , 158145722 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleMuonRun2016C-Nano14Dec2018-v1' , 67441308 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleMuonRun2016D-Nano14Dec2018-v1' , 98017996 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleMuonRun2016E-Nano14Dec2018-v1' , 90984718 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleMuonRun2016F-Nano14Dec2018-v1' , 65489554 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleMuonRun2016G-Nano14Dec2018-v1' , 149912248 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleMuonRun2016H-Nano14Dec2018-v1' , 174035164 , 1.0 , 1.0),
            ## Double Muon
            #Dataset('data_obs' , 'DoubleMuonRun2016B_ver1-Nano14Dec2018_ver1-v1' , 4199947 , 1.0 , 1.0),
            #Dataset('data_obs' , 'DoubleMuonRun2016B_ver2-Nano14Dec2018_ver2-v1' , 82535526 , 1.0 , 1.0),
            #Dataset('data_obs' , 'DoubleMuonRun2016C-Nano14Dec2018-v1' , 27934629 , 1.0 , 1.0),
            #Dataset('data_obs' , 'DoubleMuonRun2016D-Nano14Dec2018-v1' , 33861745 , 1.0 , 1.0),
            #Dataset('data_obs' , 'DoubleMuonRun2016E-Nano14Dec2018-v1' , 28246946 , 1.0 , 1.0),
            #Dataset('data_obs' , 'DoubleMuonRun2016F-Nano14Dec2018-v1' , 20329921 , 1.0 , 1.0),
            #Dataset('data_obs' , 'DoubleMuonRun2016G-Nano14Dec2018-v1' , 45235604 , 1.0 , 1.0),
            #Dataset('data_obs' , 'DoubleMuonRun2016H-Nano14Dec2018-v1' , 48912812 , 1.0 , 1.0),
            },
        'mc'   : {
            ##DYJets
            #Dataset('DYJetsToLL' , 'DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-v1' , 67981236 , 18810.0 , 1.0),
            #Dataset('DYJetsToLL' , 'DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext1-v1' , 40364234 , 18810.0 , 1.0),
            Dataset('DYJetsToLL' , 'DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 35114961 , 16270.0 , 1.0),
            #Dataset('DYJetsToLL' , 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext2-v1' , 120777245 , 5941.0 , 1.0),
            #Dataset('DYJetsToLL' , 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1' , 49748967 , 4963.0 , 1.0),
            Dataset('DYJetsToLL' , 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2-v1' , 96531428 , 4963.0 , 1.23),
            
            ##DYJets HT
            ##M-10to50
            Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 35114961 , 16270.0 , 1.0),
            ##HT-70to100
            Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-70to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 9691660 , 169.9 , 1.23),
            ##HT-100to200
            Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 2751187 , 147.4 , 1.23),
            #Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1' , 8265899 , 147.4 , 1.23),
            ##HT-200to400
            Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 962195 , 41.04 , 1.23),
            #Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1' , 8646942 , 41.04 , 1.23),
            ##HT-400to600
            Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 1070454 , 5.674 , 1.23),
            #Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1' , 8655207 , 5.674 , 1.23),
            ##HT-600to800
            Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 8292957 , 1.358 , 1.23),
            ##HT-800to1200
            Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 2673066 , 0.6229 , 1.23),
            ##HT-1200to2500
            Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 596079 , 0.1512 , 1.23),
            ##HT-2500toInf
            Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 399492 , 0.003659 , 1.23),
            
            ##WJetsToLNu
            #Dataset('WJetsToLNu' , 'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-v1' , 22606589 , 60430.0 , 1.0),
            #Dataset('WJetsToLNu' , 'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext2-v1' , 237263153 , 60430.0 , 1.0),
            Dataset('WJetsToLNu' , 'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 29514020 , 50260.0 , 1.0),
            #Dataset('WJetsToLNu' , 'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2-v1' , 57402435 , 50260.0 , 1.0),
            
            ##WJetsToLNu
            ##HT-70To100
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-70To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 10020533 , 1353.0 , 1.0),
            ##HT-100To200
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 9945478 , 1346.0 , 1.0),
            #Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1' , 29503700 , 1346.0 , 1.0),
            #Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2-v1' , 38593839 , 1346.0 , 1.0),
            ##HT-200To400
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 4963240 , 360.1 , 1.0),
            #Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1' , 14106492 , 360.1 , 1.0),
            #Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2-v1' , 19914590 , 360.1 , 1.0),
            ##HT-400To600
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 1963464 , 48.8 , 1.0),
            #Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1' , 5796237 , 48.8 , 1.0),
            ##HT-600To800
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 3779141 , 12.07 , 1.0),
            #Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1' , 14908339 , 12.07 , 1.0),
            ##HT-800To1200
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 1544513 , 5.497 , 1.0),
            #Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1' , 6286023 , 5.497 , 1.0),
            ##HT-1200To2500
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 244532 , 1.329 , 1.0),
            #Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1' , 6627909 , 1.329 , 1.0),
            ##HT-1200To2500
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 253561 , 0.03209 , 1.0),
            #Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1' , 2384260 , 0.03209 , 1.0),
            
            ##TTbar
            #Dataset('TTbar' , 'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8-v1' , 76915549 , 730.6 , 1.0),
            ##TTJets_Dilept
            Dataset('TTbar' , 'TTJets_Dilept_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8-v1' , 14529280 , 76.75 , 1.0),
            #Dataset('TTbar' , 'TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 6068369 , 56.86 , 1.0),
            #Dataset('TTbar' , 'TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1' , 24767666 , 56.86 , 1.0),
            ##TTJets_SingleLeptFromT
            Dataset('TTbar' , 'TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 11957043 , 114.0 , 1.0),
            #Dataset('TTbar' , 'TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1' , 49664175 , 114.0 , 1.0),
            ##TTJets_SingleLeptFromTbar
            Dataset('TTbar' , 'TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1' , 11955887 , 114.0 , 1.0),
            #Dataset('TTbar' , 'TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1' , 48387865 , 114.0 , 1.0),
            
            #ST_s-channel_4f_InclusiveDecays
            Dataset('ST' , 'ST_s-channel_4f_InclusiveDecays_13TeV-amcatnlo-pythia8-v1' , 2911199 , 10.12 , 1.0),
            #ST_s-channel_4f_leptonDecays
            #Dataset('ST' , 'ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1-v1' , 1000000 , 3.365 , 1.0),
            #ST_t-channel_antitop_4f_inclusiveDecays
            Dataset('ST' , 'ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1-v1' , 38811017 , 27.1 , 1.0),
            #ST_t-channel_top_4f_inclusiveDecays
            Dataset('ST' , 'ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1-v1' , 67105876 , 27.1 , 1.0),
            #ST_tW_antitop_5f_inclusiveDecays
            Dataset('ST' , 'ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4-v1' , 998276 , 38.06 , 1.0),
            #ST_tW_top_5f_inclusiveDecays
            Dataset('ST' , 'ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4-v1' , 992024 , 38.09 , 1.0),
            
            #WZ
            #Dataset('WZ' , 'WZ_TuneCUETP8M1_13TeV-pythia8-v1' , 1000000 , 23.43 , 1.0),
            #Dataset('WZ' , 'WZ_TuneCUETP8M1_13TeV-pythia8_ext1-v1' , 2997571 , 23.43 , 1.0),
            Dataset('WZ' , 'WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8-v1' , 24285386 , 10.73 , 1.0),
            Dataset('WZ' , 'WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8-v1' , 26517272 , 5.606 , 1.0),
            Dataset('WZ' , 'WZTo3LNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-v1' , 11928707 , 4.679 , 1.0),
            #Dataset('WZ' , 'WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8-v1' , 1993200 , 4.679 , 1.0),
            #Dataset('WZ' , 'WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8_ext1-v1' , 18000000 , 4.42965 , 1.0), #CHECK XS
            
            #WW
            #Dataset('WW' , 'WW_TuneCUETP8M1_13TeV-pythia8-v1' , 994012 , 64.3 , 1.0),
            #Dataset('WW' , 'WW_TuneCUETP8M1_13TeV-pythia8_ext1-v1' , 6988168 , 64.3 , 1.0),
            Dataset('WW' , 'WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8-v1' , 5246469 , 45.68 , 1.0),
            #Dataset('WW' , 'WWToLNuQQ_13TeV-powheg-v1' , 1999200 , 43.53 , 1.0),
            #Dataset('WW' , 'WWToLNuQQ_13TeV-powheg_ext1-v1' , 6655400 , 43.53 , 1.0),
            #Dataset('WW' , 'WWTo2L2Nu_13TeV-powheg-herwigpp-v1' , 1982372 , 10.48 , 1.0),
            Dataset('WW' , 'WWTo2L2Nu_13TeV-powheg-v1' , 1999000 , 10.48 , 1.0),
            Dataset('WW' , 'WWTo4Q_13TeV-powheg-v1' , 1998400 , 45.2 , 1.0),
            
            #ZZ
            #Dataset('ZZ' , 'ZZ_TuneCUETP8M1_13TeV-pythia8-v1' , 990064 , 10.16 , 1.0),
            #Dataset('ZZ' , 'ZZ_TuneCUETP8M1_13TeV-pythia8_ext1-v1' , 998034 , 10.16 , 1.0),
            Dataset('ZZ' , 'ZZTo2L2Nu_13TeV_powheg_pythia8-v1' , 8931750 , 0.5644 , 1.0),
            Dataset('ZZ' , 'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8-v1' , 15462693 , 3.222 , 1.0),
            
            ##TTV
            Dataset('ttV' , 'ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8-v1' , 3981250 , 0.5638 , 1.0),
            Dataset('ttV' , 'TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8-v1' , 833298 , 0.405 , 1.0),
            #Dataset('ttV' , 'TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_ext1-v1' , 2160168 , 0.2001 , 1.0),
            Dataset('ttV' , 'TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_ext2-v1' , 3120397 , 0.2001 , 1.0),
            Dataset('ttV' , 'TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8-v1' , 749400 , 0.5297 , 1.0),
            #Dataset('ttV' , 'TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8_ext1-v1' , 1992438 , 0.2529 , 1.0),
            #Dataset('ttV' , 'TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8_ext2-v1' , 5837781 , 0.2529 , 1.0),
            Dataset('ttV' , 'TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8_ext3-v1' , 5934228 , 0.2529 , 1.0),
            #Dataset('ttV' , 'TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8-v1' , 4870911 , 3.795 , 1.0),
            Dataset('ttV' , 'TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_ext1-v2' , 9877942 , 3.795 , 1.0),
            
            Dataset('VVV' , 'WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8-v1' , 240000 , 0.2086 , 1.0),
            Dataset('VVV' , 'ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8-v1' , 249237 , 0.01398 , 1.0),
            Dataset('VVV' , 'WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8-v1' , 250000 , 0.1651 , 1.0),
            Dataset('VVV' , 'WZG_TuneCUETP8M1_13TeV-amcatnlo-pythia8-v1' , 998200 , 0.04123 , 1.0),
            Dataset('VVV' , 'WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8-v1' , 246800 , 0.05565 , 1.0),
            
            Dataset('WWJJ' , 'WpWpJJ_13TeV-powheg-pythia8_TuneCUETP8M1-v1' , 146600 , 0.02093 , 1.0),
            Dataset('WWJJ' , 'WmWmJJ_13TeV-powheg-pythia8_TuneCUETP8M1-v1' , 150000 , 0.007868 , 1.0),
            #Dataset('WWJJ' , 'WWJJToLNuLNu_EWK_13TeV-madgraph-pythia8-v1' , 475300 , 0.5029 , 1.0),
            
            Dataset('Vg' , 'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext1-v1' , 5059865 , 510.6 , 1.0),
            #Dataset('Vg' , 'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext2-v1' , 10231994 , 510.6 , 1.0),
            #Dataset('Vg' , 'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext3-v1' , 12219986 , 510.6 , 1.0),
            Dataset('Vg' , 'ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext1-v1' , 14372682 , 123.8 , 1.0),
            
            Dataset('WHWW' , 'HWminusJ_HToWW_M125_13TeV_powheg_pythia8-v1' , 299799 , 0.5331 , 1.0),
            Dataset('WHWW' , 'HWplusJ_HToWW_M125_13TeV_powheg_pythia8-v1' , 299997 , 0.851 , 1.0),
            
            Dataset('QCD' , 'QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8-v1' , 22094081 , 269900.0 , 1.0),
            
            Dataset('tZq' , 'tZq_ll_4f_13TeV-amcatnlo-pythia8_ext1-v1' , 13656784 , 0.0758 , 1.0),
            
            Dataset('VH' , 'VHToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8-v1' , 1007898 , 2.127 , 1.0),
            },
        'test' : {
            Dataset('data_obs' , 'SingleElectronRun2016B_ver2-Nano14Dec2018_ver2-v1' , 246440440 , 1.0 , 1.0),
            Dataset('VVV' , 'WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8-v1' , 240000 , 0.2086 , 1.0),
            Dataset('ttV' , 'TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8_ext3-v1' , 5934228 , 0.2529 , 1.0),
            },
        },
    'Run2_2017_v2' : {
        'cert' : 'Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt',
        'data' : {
            Dataset('data_obs' , 'SingleElectronRun2017B-31Mar2018-v1' , 60537490 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleElectronRun2017C-31Mar2018-v1' , 136637888 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleElectronRun2017D-31Mar2018-v1' , 51526710 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleElectronRun2017E-31Mar2018-v1' , 102121689 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleElectronRun2017F-31Mar2018-v1' , 128467223 , 1.0 , 1.0),
            
            Dataset('data_obs' , 'SingleMuonRun2017B-31Mar2018-v1' , 136300266 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleMuonRun2017C-31Mar2018-v1' , 165652756 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleMuonRun2017D-31Mar2018-v1' , 70361660 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleMuonRun2017E-31Mar2018-v1' , 154630534 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleMuonRun2017F-31Mar2018-v1' , 242135500 , 1.0 , 1.0),
            
            #Dataset('data_obs' , 'DoubleMuonRun2017B-31Mar2018-v1' , 14501767 , 1.0 , 1.0),
            #Dataset('data_obs' , 'DoubleMuonRun2017C-31Mar2018-v1' , 49636525 , 1.0 , 1.0),
            #Dataset('data_obs' , 'DoubleMuonRun2017D-31Mar2018-v1' , 23075733 , 1.0 , 1.0),
            #Dataset('data_obs' , 'DoubleMuonRun2017E-31Mar2018-v1' , 51589091 , 1.0 , 1.0),
            #Dataset('data_obs' , 'DoubleMuonRun2017F-31Mar2018-v1' , 79756560 , 1.0 , 1.0),
            },
        'mc'   : {
            #DY
            Dataset('DYJetsToLL' , 'DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 39521230 , 18810.0 , 1.0), #check xs, using 2016
            #Dataset('DYJetsToLL' , 'DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8-v2' , 316134 , 18810.0 , 1.0), #check xs, using 2016
            #Dataset('DYJetsToLL' , 'DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8_ext1-v2' , 39536839 , 18810.0 , 1.0), #check xs, using 2016
            #Dataset('DYJetsToLL' , 'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8-v1' , 27413121 , 6529.0 , 1.0),
            Dataset('DYJetsToLL' , 'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8_ext1-v1' , 181511556 , 6529.0 , 1.0),
            #DY
            #M-10to50
            Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 39521230 , 18810.0 , 1.0), #check xs, using 2016
            #HT-70to100
            Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-70to100_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 9344037 , 169.9 , 1.0), #check xs, using 2016
            #HT-100to200
            Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 10235418 , 161.1 , 1.0),
            #Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8-v2' , 11197488 , 161.1 , 1.0),
            #Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8_ext1-v1' , 3950339 , 161.1 , 1.0),
            #HT-200to400
            Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 10181069 , 48.66 , 1.0),
            #Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8-v2' , 10728447 , 48.66 , 1.0),
            #Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8_ext1-v1' , 1200863 , 48.66 , 1.0),
            #HT-400to600
            Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 9365135 , 6.968 , 1.0),
            #Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8-v2' , 10219524 , 6.968 , 1.0),
            #Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8_ext1-v1' , 1124294 , 6.968 , 1.0),
            #HT-600to800
            Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 8225050 , 1.743 , 1.0),
            #Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8-v2' , 8743640 , 1.743 , 1.0),
            #HT-800to1200
            Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 3089861 , 0.8052 , 1.0),
            #Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8-v2' , 3114980 , 0.8052 , 1.0),
            #HT-1200to2500
            Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 625517 , 0.1933 , 1.0),
            #HT-2500toInf
            Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 404986 , 0.003468 , 1.0),
            #Dataset('DYJetsToLL_HT' , 'DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8-v2' , 419308 , 0.003468 , 1.0),
            
            #WJetsToLNu
            #Dataset('WJetsToLNu' , 'WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8-v2' , 33073306 , 52940.0 , 1.0),
            Dataset('WJetsToLNu' , 'WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8_ext1-v2' , 44767978 , 52940.0 , 1.0),
            #WJetsToLNu
            #HT
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-70To100_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 22255124 , 169.9 , 1.0),   #check this xsec, using 2016
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8-v2' , 35549343 , 1395.0 , 1.0),
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 21250517 , 407.9 , 1.0),
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 14313274 , 57.48 , 1.0),
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 21664301 , 12.87 , 1.0),
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 20466692 , 5.366 , 1.0),
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 19877812 , 1.074 , 1.0),
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8-v3' , 21379053 , 0.008001 , 1.0),
            
            #Dataset('TTbar' , 'TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8-v1' , 153531390 , 722.8 , 1.0),
            Dataset('TTbar' , 'TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 28380110 , 54.23 , 1.0),
            Dataset('TTbar' , 'TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 60222947 , 109.6 , 1.0),
            Dataset('TTbar' , 'TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 56697498 , 114.0 , 1.0),        #check this xsec, using 2016
            
            Dataset('ST' , 'ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8-v1' , 9568575 , 3.74 , 1.0),
            #Dataset('ST' , 'ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8-v2' , 9883805 , 3.74 , 1.0),
            #Dataset('ST' , 'ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8-v1' , 9738388 , 3.74 , 1.0),
            
            Dataset('ST' , 'ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8-v1' , 3939990 , 67.91 , 1.0),
            #Dataset('ST' , 'ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8-v2' , 3675910 , 67.91 , 1.0),
            
            Dataset('ST' , 'ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8-v1' , 122349400 , 27.1 , 1.0),     #check this xsec, using 2016
            
            #Dataset('ST' , 'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8-v1' , 7993682 , 34.97 , 1.0),
            #Dataset('ST' , 'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8-v2' , 7745276 , 34.97 , 1.0),
            Dataset('ST' , 'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8-v1' , 7780870 , 34.97 , 1.0),
            #Dataset('ST' , 'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8-v2' , 7977430 , 34.97 , 1.0),
            
            Dataset('ST' , 'ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8-v1' , 7581624 , 34.91 , 1.0),
            #Dataset('ST' , 'ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8-v2' , 7485152 , 34.91 , 1.0),
            #Dataset('ST' , 'ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8-v1' , 7660001 , 34.91 , 1.0),
            
            #Dataset('WZ' , 'WZ_TuneCP5_13TeV-pythia8-v1' , 3928630 , 27.6 , 1.0),
            Dataset('WZ' , 'WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8-v2' , 19017449 , 10.73 , 1.0),
            Dataset('WZ' , 'WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8-v1' , 27582164 , 5.606 , 1.0),
            Dataset('WZ' , 'WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8-v1' , 10881896 , 5.052 , 1.0),
            
            #Dataset('WW' , 'WW_TuneCP5_13TeV-pythia8-v1' , 7791498 , 75.8 , 1.0),
            #Dataset('WW' , 'WW_TuneCP5_13TeV-pythia8-v2' , 7765828 , 75.8 , 1.0),
            Dataset('WW' , 'WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8-v1' , 5054286 , 45.68 , 1.0),
            #Dataset('WW' , 'WWToLNuQQ_NNPDF31_TuneCP5_PSweights_13TeV-powheg-pythia8_ext1-v1' , 8785360 , 45.99 , 1.0),
            #Dataset('WW' , 'WWToLNuQQ_NNPDF31_TuneCP5_13TeV-powheg-pythia8-v1' , 8680425 , 45.99 , 1.0),
            #Dataset('WW' , 'WWToLNuQQ_NNPDF31_TuneCP5_13TeV-powheg-pythia8_ext1-v1' , 9994191 , 45.99 , 1.0),
            #Dataset('WW' , 'WWTo2L2Nu_NNPDF31_TuneCP5_PSweights_13TeV-powheg-pythia8_ext1-v1' , 2000000 , 11.08 , 1.0),
            #Dataset('WW' , 'WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8-v1' , 1915563 , 10.48 , 1.0),                         #check this xsec, using 2016
            #Dataset('WW' , 'WWTo4Q_NNPDF31_TuneCP5_PSweights_13TeV-powheg-pythia8_ext1-v1' , 1976360 , 47.73 , 1.0),
            
            #Dataset('ZZ' , 'ZZ_TuneCP5_13TeV-pythia8-v1' , 1949768 , 12.14 , 1.0),
            #Dataset('ZZ' , 'ZZ_TuneCP5_13TeV-pythia8-v2' , 1925931 , 12.14 , 1.0),
            Dataset('ZZ' , 'ZZTo2L2Nu_13TeV_powheg_pythia8-v1' , 8744768 , 0.5644 , 1.0),
            Dataset('ZZ' , 'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8-v1' , 27840918 , 3.222 , 1.0),
            
            Dataset('ttV' , 'ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8-v1' , 7669336 , 0.5638 , 1.0),
            #Dataset('ttV' , 'ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8_ext1-v2' , 8241489 , 0.5638 , 1.0),
            
            Dataset('ttV' , 'TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8-v1' , 811306 , 0.4316 , 1.0),
            #Dataset('ttV' , 'TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8-v2' , 811306 , 0.4316 , 1.0),
            Dataset('ttV' , 'TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8-v1' , 4925829 , 0.2149 , 1.0),
            #Dataset('ttV' , 'TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8-v2' , 4994543 , 0.2149 , 1.0),
            #Dataset('ttV' , 'TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8-v1' , 4919674 , 0.2198 , 1.0),
            
            Dataset('ttV' , 'TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8-v1' , 750000 , 0.5104 , 1.0),
            #Dataset('ttV' , 'TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8-v2' , 750000 , 0.5104 , 1.0),
            
            #Dataset('ttV' , 'TTZToLLNuNu_M-10_TuneCP5_PSweights_13TeV-amcatnlo-pythia8-v1' , 11092000 , 0.2432 , 1.0),
            Dataset('ttV' , 'TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8-v1' , 7563490 , 0.2432 , 1.0),
            #Dataset('ttV' , 'TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8-v2' , 7932650 , 0.2432 , 1.0),
            
            Dataset('ttV' , 'TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8-v1' , 4575621 , 4.078 , 1.0),
            #Dataset('ttV' , 'TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8-v2' , 4858971 , 4.078 , 1.0),
            #Dataset('ttV' , 'TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_ext1-v1' , 9402772 , 4.078 , 1.0),
            #Dataset('ttV' , 'TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_ext1-v2' , 8582640 , 4.078 , 1.0),
            
            Dataset('VVV' , 'WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8-v1' , 240000 , 0.2086 , 1.0),
            #Dataset('VVV' , 'WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8-v2' , 232300 , 0.2086 , 1.0),
            
            #Dataset('VVV' , 'ZZZ_TuneCP5_13TeV-amcatnlo-pythia8-v1' , 250000 , 0.01398 , 1.0),
            Dataset('VVV' , 'ZZZ_TuneCP5_13TeV-amcatnlo-pythia8-v2' , 250000 , 0.01398 , 1.0),
            
            Dataset('VVV' , 'WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8-v1' , 250000 , 0.1651 , 1.0),
            #Dataset('VVV' , 'WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8-v2' , 250000 , 0.1651 , 1.0),
            
            Dataset('VVV' , 'WZG_TuneCP5_13TeV-amcatnlo-pythia8-v1' , 1000000 , 0.04345 , 1.0),
            Dataset('VVV' , 'WZZ_TuneCP5_13TeV-amcatnlo-pythia8-v1' , 250000 , 0.05565 , 1.0),
            
            #Dataset('WWJJ' , 'WpWpJJ_EWK_TuneCP5_13TeV-madgraph-pythia8-v2' , 145800 , 0.02093 , 1.0),                  #check this xsec, using 2016
            Dataset('WWJJ' , 'WpWpJJ_EWK-QCD_TuneCP5_13TeV-madgraph-pythia8-v1' , 149000 , 0.04932 , 1.0),
            #Dataset('WWJJ' , 'WWJJToLNuLNu_EWK_TuneCP5_13TeV-madgraph-pythia8-v1' , 500000 , 1.0 , 1.0),
            
            Dataset('Vg' , 'WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 6283083 , 510.6 , 1.0),                 #check this xsec, using 2016
            Dataset('Vg' , 'ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8-v3' , 30490034 , 123.8 , 1.0),       #check this xsec, using 2016
            
            Dataset('WHWW' , 'HWminusJ_HToWW_M125_13TeV_powheg_pythia8_TuneCP5-v1' , 391794 , 0.5331 , 1.0),         #check this xsec, using 2016
            Dataset('WHWW' , 'HWplusJ_HToWW_M125_13TeV_powheg_pythia8_TuneCP5-v1' , 371096 , 0.851 , 1.0),          #check this xsec, using 2016
            
            #Dataset('tZq' , 'tZq_ll_4f_ckm_NLO_TuneCP5_PSweights_13TeV-amcatnlo-pythia8-v1' , 13044720 , 0.07358 , 1.0),
            Dataset('tZq' , 'tZq_ll_4f_ckm_NLO_TuneCP5_PSweights_13TeV-amcatnlo-pythia8-v2' , 13276146 , 0.07358 , 1.0),
            
            Dataset('VH' , 'VHToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8-v2' , 918508 , 2.127 , 1.0),
            
            ##Signal
            Dataset('Wm' ,"Wminushwwlvjj_M125_Madspin_Skim",  300000  ,  0.0069905587717  ,  1.0  ),
            Dataset('Wp' ,"Wplushwwlvjj_M125_Madspin_Skim",  300000  ,  0.0110211512166  ,  1.0  ),
            },
        },
    'Run2_2018_v4' : {
        'cert' : 'Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt',
        'data' : {
            Dataset('data_obs' , 'SingleMuonRun2018A-Nano14Dec2018-v1' , 241608232 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleMuonRun2018B-Nano14Dec2018-v1' , 119918017 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleMuonRun2018C-Nano14Dec2018-v1' , 110032072 , 1.0 , 1.0),
            Dataset('data_obs' , 'SingleMuonRun2018D-Nano14Dec2018_ver2-v1' , 506468530 , 1.0 , 1.0),
            Dataset('data_obs' , 'DoubleMuonRun2018A-Nano14Dec2018-v1' , 75499908 , 1.0 , 1.0),
            Dataset('data_obs' , 'DoubleMuonRun2018B-Nano14Dec2018-v1' , 35057758 , 1.0 , 1.0),
            Dataset('data_obs' , 'DoubleMuonRun2018C-Nano14Dec2018-v1' , 34565869 , 1.0 , 1.0),
            Dataset('data_obs' , 'DoubleMuonRun2018D-Nano14Dec2018_ver2-v1' , 168605834 , 1.0 , 1.0),
            },
        'mc'   : {
            Dataset('DYJetsToLL' , 'DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 39392062 , 1.0 , 1.0),
            Dataset('DYJetsToLL' , 'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8-v1' , 997561 , 6529.0 , 1.0),
            Dataset('DYJetsToLL' , 'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8-v2' , 100194597 , 5343.0 , 1.0),
            
            Dataset('WJetsToLNu' , 'WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 70168531 , 52940.0 , 1.0),
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-70To100_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 27935774 , 1.0 , 1.0),
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 29464191 , 1395.0 , 1.0),
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 25468933 , 407.9 , 1.0),
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 5932701 , 57.48 , 1.0),
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 19771294 , 12.87 , 1.0),
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 8402687 , 5.366 , 1.0),
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 7633949 , 1.074 , 1.0),
            Dataset('WJetsToLNu_HT' , 'WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 3273980 , 0.008001 , 1.0),
            
            Dataset('TTbar' , 'TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_ext1-v1' , 142081487 , 722.8 , 1.0),
            Dataset('TTbar' , 'TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 28701360 , 54.23 , 1.0),
            Dataset('TTbar' , 'TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 57259880 , 109.6 , 1.0),
            Dataset('TTbar' , 'TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 59929205 , 1.0 , 1.0),
            
            Dataset('ST' , 'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8_ext1-v1' , 7623000 , 34.97 , 1.0),
            Dataset('ST' , 'ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8_ext1-v1' , 9598000 , 34.91 , 1.0),
            
            Dataset('WZ' , 'WZ_TuneCP5_13TeV-pythia8-v1' , 3885000 , 27.6 , 1.0),
            Dataset('WZ' , 'WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8-v1' , 28193648 , 5.606 , 1.0),
            Dataset('WZ' , 'WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8-v1' , 10749269 , 5.052 , 1.0),
            Dataset('WZ' , 'WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8_ext1-v1' , 11248318 , 5.052 , 1.0),

            Dataset('WW' , 'WW_TuneCP5_13TeV-pythia8-v1' , 7850000 , 75.8 , 1.0),
            Dataset('WW' , 'WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8-v1' , 4683136 , 45.68 , 1.0),
            #Dataset('WW' , 'WWToLNuQQ_NNPDF31_TuneCP5_13TeV-powheg-pythia8-v1' , 19151100 , 45.99 , 1.0),
            Dataset('WW' , 'WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8-v1' , 7719200 , 1.0 , 1.0),

            Dataset('ZZ' , 'ZZ_TuneCP5_13TeV-pythia8-v1' , 1979000 , 12.14 , 1.0),
            Dataset('ZZ' , 'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8-v1' , 27900469 , 3.222 , 1.0),
            
            Dataset('ttV' , 'ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8-v1' , 7525991 , 0.5638 , 1.0),
            Dataset('ttV' , 'TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8-v1' , 835296 , 0.4316 , 1.0),
            Dataset('ttV' , 'TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_ext1-v1' , 4911941 , 0.2149 , 1.0),
            Dataset('ttV' , 'TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8-v1' , 750000 , 0.5104 , 1.0),
            Dataset('ttV' , 'TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8_ext1-v1' , 13280000 , 0.2432 , 1.0),
            Dataset('ttV' , 'TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8-v1' , 4691915 , 4.078 , 1.0),
            
            Dataset('VVV' , 'WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8_ext1-v1' , 240000 , 0.2086 , 1.0),
            Dataset('VVV' , 'ZZZ_TuneCP5_13TeV-amcatnlo-pythia8_ext1-v1' , 250000 , 0.01398 , 1.0),
            Dataset('VVV' , 'WZG_TuneCP5_13TeV-amcatnlo-pythia8-v1' , 1960000 , 0.04345 , 1.0),
            Dataset('VVV' , 'WZZ_TuneCP5_13TeV-amcatnlo-pythia8_ext1-v1' , 250000 , 0.05565 , 1.0),
            
            Dataset('WWJJ' , 'WpWpJJ_EWK-QCD_TuneCP5_13TeV-madgraph-pythia8-v1' , 150000 , 0.04932 , 1.0),
            Dataset('WWJJ' , 'WpWpJJ_EWK_TuneCP5_13TeV-madgraph-pythia8-v1' , 149400 , 1.0 , 1.0),
            
            Dataset('WWJJ' , 'WWJJToLNuLNu_EWK_TuneCP5_13TeV-madgraph-pythia8_ext1-v1' , 485000 , 1.0 , 1.0),
            
            Dataset('Vg' , 'WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8-v1' , 6108186 , 1.0 , 1.0),
            Dataset('Vg' , 'ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8_ext1-v1' , 13946364 , 1.0 , 1.0),
            
            Dataset('VH' , 'VHToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8-v1' , 1102578 , 2.127 , 1.0),
            
            ##Signal
            Dataset('Wm' ,"Wminushwwlvjj_M125_Madspin_Skim",  300000  ,  0.0069905587717  ,  1.0  ),
            Dataset('Wp' ,"Wplushwwlvjj_M125_Madspin_Skim",  300000  ,  0.0110211512166  ,  1.0  ),
            },
        },
    }
