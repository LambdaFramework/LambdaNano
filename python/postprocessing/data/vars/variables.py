from PhysicsTools.NanoAODTools.postprocessing.framework.output import OutputBranch

class Variable(object):

    def __init__(self, name, titleX, titleY, nbins, mins, maxs, log, getter, dtype, dimen=0):
        self._name    = name
        self._titleX  = titleX
        self._titleY  = titleY
        self._nbins   = nbins
        self._mins    = mins
        self._maxs    = maxs
        self._log     = log
        self._getter  = getter
        self._dtype   = dtype
        self._dimen   = dimen
    pass

    def name(self):
        return self._name
    def titleX(self):
        return self._titleX
    def titleY(self):
        return self._titleY
    def nbins(self):
        return self._nbins
    def mins(self):
        return self._mins
    def maxs(self):
        return self._maxs
    def log(self):
        return self._log
    def value(self, TVec):
        return self._getter(TVec)
    def lamb(self):
        return self._getter
    def _type(self):
        return self._dtype
    def dimen(self):
        return self._dimen
    pass

#################################################################################
## Producer (ANALYSIS)                                                          #
#################################################################################
###SCALAR
br_global = [
    Variable('nMu'            ,   "Number of Muon"          ,   "Events / XXX"                 ,   6     ,   -0.5   ,   5.5    , True    ,   lambda ev : ev , "I"),
    Variable('nEle'           ,   "Number of Electron"      ,   "Events / XXX"                 ,   6     ,   -0.5   ,   5.5    , True    ,   lambda ev : ev , "I" ),
    Variable('nTau'           ,   "Number of Tau"           ,   "Events / XXX"                 ,   6     ,   -0.5   ,   5.5    , True    ,   lambda ev : ev , "I" ),
    Variable('nPho'           ,   "Number of Photon"        ,   "Events / XXX"                 ,   6     ,   -0.5   ,   5.5    , True    ,   lambda ev : ev , "I" ),
    Variable('nCleanJet'     ,   "Number of CleanJets"     ,   "Events / XXX"                 ,   11    ,   -0.5   ,   10.5    , True    ,   lambda ev : ev , "I" ),
    Variable('nLepton'        ,   "Number of Lepton"        ,   "Events / XXX"                 ,   11    ,   -0.5   ,   10.5    , True    ,   lambda ev : ev , "I" ),

    ## Weight
    Variable('EventWeight'     ,   "Event Weight"            ,   "Events / XXX"                 ,   50   ,   -30.   ,   30.    , False   ,   lambda ev : ev , "F" ),
    Variable('TriggerWeight'   ,   "Trigger Weight"          ,   "Events / XXX"                 ,   50   ,   -30.   ,   30.    , False   ,   lambda ev : ev , "F" ),
    Variable('ZewkWeight'      ,   "Zewk Weight"             ,   "Events / XXX"                 ,   50   ,   -30.   ,   30.    , False   ,   lambda ev : ev , "F" ),
    Variable('WewkWeight'      ,   "Wewk Weight"             ,   "Events / XXX"                 ,   50   ,   -30.   ,   30.    , False   ,   lambda ev : ev , "F" ),
    ##MHT
    Variable('MHT_pt'          ,   "Hadronic Sum Pt [GeV]"            , "Events / XXX GeV"               , 100    , 0.       , 1000.     , True    , lambda ev : ev  ,"F" ),
    Variable('MHT_phi'         ,   "Hadronic Sum Phi"                 , "Events / XXX"                   , 30     , -3.5     , 3.5      , True   , lambda ev : ev ,"F" ),

    ##MET
    Variable('MET_pt'          ,   "MET Pt [GeV]"            , "Events / XXX GeV"               , 100    , 0.       , 500.     , True    , lambda ev : ev.pt  ,"F" ),
    Variable('MET_phi'         ,   "MET Phi"                 , "Events / XXX"                   , 30     , -3.5     , 3.5      , True   , lambda ev : ev.phi ,"F" ),
    #Composite
    Variable('mtw1'               , "mtw1 [GeV]"                  , "Events / XXX GeV" ,  100 , 0. , 500. , True       , lambda ev : ev          ,"F"),
    Variable('mtw2'               , "mtw2 [GeV]"                  , "Events / XXX GeV" ,  100 , 0. , 500. , True       , lambda ev : ev          ,"F"),
    Variable('dphilmet1'          , "dphilmet1"                   , "Events / XXX GeV" ,  30 , -3.5 , 3.5 , True       , lambda ev : ev          ,"F"),
    Variable('dphilmet2'          , "dphilmet2"                   , "Events / XXX GeV" ,  30 , -3.5 , 3.5 , True       , lambda ev : ev          ,"F"),
]

br_Vll = [
    Variable('Vll_pt'               , "V(ll) system Pt [GeV]"                  , "Events / XXX GeV" ,  50 , 0. , 500. , True       , lambda ev : ev.Pt()          ,"F"),
    Variable('Vll_eta'              , "V(ll) system #eta"                      , "Events / XXX" , 30 , -3. , 3. , False       , lambda ev : ev.Eta()         ,"F"),
    Variable('Vll_phi'              , "V(ll) system #phi"                      , "Events / XXX" , 30 , -3.5 , 3.5 , True       , lambda ev : ev.Phi()         ,"F"),
    Variable('Vll_mass'             , "V(ll) system mass [GeV/c^{2}]"               , "Events / XXX GeV/c^{2}" , 40 , 0. , 200. , True       , lambda ev : ev.M()          ,"F"),
]

br_Vl2JJ = [
    Variable('Vl2JJ_pt'             , "V(l2jj) system Pt [GeV]"                      , "Events / XXX GeV" , 50 , 0. , 500. , True        , lambda ev : ev.Pt()          ,"F"),
    Variable('Vl2JJ_eta'            , "V(l2jj) system #eta"                          , "Events / XXX" , 30 , -3. , 3. , False        , lambda ev : ev.Eta()         ,"F"),
    Variable('Vl2JJ_phi'            , "V(l2jj) system #phi"                          , "Events / XXX" , 30 , -3.5 , 3.5 , True        , lambda ev : ev.Phi()         ,"F"),
    Variable('Vl2JJ_mass'           , "V(l2jj) system mass [GeV/c^{2}]"              , "Events / XXX GeV/c^{2}" , 40 , 0. , 400. , True        , lambda ev : ev.M()          ,"F"),
]

br_Vjj = [
    Variable('Vjj_pt'               , "V(jj) system Pt [GeV]"                  , "Events / XXX GeV" ,  50 , 0. , 500. , True       , lambda ev : ev.Pt()          ,"F"),
    Variable('Vjj_eta'              , "V(jj) system #eta"                      , "Events / XXX" , 30 , -3. , 3. , False       , lambda ev : ev.Eta()         ,"F"),
    Variable('Vjj_phi'              , "V(jj) system #phi"                      , "Events / XXX" , 30 , -3.5 , 3.5 , True       , lambda ev : ev.Phi()         ,"F"),
    Variable('Vjj_mass'             , "V(jj) system mass [GeV/c^{2}]"               , "Events / XXX GeV/c^{2}" , 20 , 0. , 200. , True       , lambda ev : ev.M()          ,"F"),
]

######VECTOR
br_Muons = [
    #Variable('Mu_Weight'           , "Muon[N] Weight"                    , "Events / XXX"           ,   50   ,   -30.   ,   30.  , False   ,   lambda ev : ev.effSF , "F" , 1 ),
    Variable('Mu_pt'               , "Muon[N] Pt [GeV]"                  , "Events / XXX GeV"       , 100 , 0.   , 500. , True  , lambda ev : ev.pt              ,"F",1),
    Variable('Mu_eta'              , "Muon[N] #eta"                      , "Events / XXX"           , 30  , -3.  , 3.   , False , lambda ev : ev.eta             ,"F",1),
    Variable('Mu_phi'              , "Muon[N] #phi"                      , "Events / XXX"           , 30  , -3.5 , 3.5  , True , lambda ev : ev.phi             ,"F",1),
    Variable('Mu_mass'             , "Muon[N] mass [GeV/c^{2}]"          , "Events / XXX GeV/c^{2}" , 100 , 0.   , 200. , False , lambda ev : ev.mass            ,"F",1),
    Variable('Mu_charge'           , "Muon[N] charge"                    , "Events / XXX"           , 3   , -1.5 , 1.5  , False , lambda ev : ev.charge          ,"I",1),
    Variable('Mu_mediumId'         , "Muon[N] mediumId"                  , "Events / XXX"           , 2   , -0.5 , 1.5  , False , lambda ev : ev.mediumId        ,"I",1),
    Variable('Mu_tightId'          , "Muon[N] tightId"                   , "Events / XXX"           , 2   , -0.5 , 1.5  , False , lambda ev : ev.tightId         ,"I",1),
    Variable('Mu_dxy'              , "Muon[N] dxy [cm]"                  , "Events / XXX cm"        , 100 , -0.05  , 0.05   , True , lambda ev : ev.dxy             ,"F",1),
    Variable('Mu_dz'               , "Muon[N] dz [cm]"                   , "Events / XXX cm"        , 100 , -0.05  , 0.05   , True , lambda ev : ev.dz              ,"F",1),
    Variable('Mu_isPFcand'         , "Muon[N] isPFcand"                  , "Events / XXX"           , 2   , -0.5 , 1.5  , False , lambda ev : ev.isPFcand        ,"I",1),
    Variable('Mu_pfRelIso03_all'   , "Muon[N] pfRelIso03_all [GeV]"      , "Events / XXX GeV"       , 80  , 0.   , 0.5  , True  , lambda ev : ev.pfRelIso03_all  ,"F",1),
    Variable('Mu_pfRelIso04_all'   , "Muon[N] pfRelIso04_all [GeV]"      , "Events / XXX GeV"       , 80  , 0.   , 0.5  , True  , lambda ev : ev.pfRelIso04_all  ,"F",1),
]

br_Electrons = [
    #Variable('Ele_Weight'       , "Electron[N] Weight"                , "Events / XXX"           ,   50   ,   -30.   ,   30.  , False   ,   lambda ev : ev.effSF , "F" , 1 ),
    Variable('Ele_pt'              , "Electron[N] Pt [GeV]"              , "Events / XXX GeV"       , 100 , 0.   , 500. , True  , lambda ev : ev.pt              ,"F",1),
    Variable('Ele_eta'             , "Electron[N] #eta"                  , "Events / XXX"           , 30  , -3.  , 3.   , False , lambda ev : ev.eta             ,"F",1),
    Variable('Ele_phi'             , "Electron[N] #phi"                  , "Events / XXX"           , 30  , -3.5 , 3.5  , True , lambda ev : ev.phi             ,"F",1),
    Variable('Ele_mass'            , "Electron[N] mass [GeV/c^{2}]"      , "Events / XXX GeV/c^{2}" , 100 , 0.   , 200. , False , lambda ev : ev.mass            ,"F",1),
    Variable('Ele_charge'          , "Electron[N] charge"                , "Events / XXX"           , 3   , -1.5 , 1.5  , False , lambda ev : ev.charge          ,"I",1),
    Variable('Ele_cutBased'        , "Electron[N] cutBased"              , "Events / XXX"           , 6   , 0    , 6    , False , lambda ev : ev.cutBased        ,"I",1),
    Variable('Ele_dxy'             , "Electron[N] dxy [cm]"              , "Events / XXX cm"        , 100 , -0.05  , 0.05   , True , lambda ev : ev.dxy             ,"F",1),
    Variable('Ele_dz'              , "Electron[N] dz [cm]"               , "Events / XXX cm"        , 100 , -0.05  , 0.05   , True , lambda ev : ev.dz              ,"F",1),
    Variable('Ele_isPFcand'        , "Electron[N] isPFcand"              , "Events / XXX"           , 2   , -0.5 , 1.5  , False , lambda ev : ev.isPFcand        ,"I",1),
    Variable('Ele_pfRelIso03_all'  , "Electron[N] pfRelIso03_all [GeV]"  , "Events / XXX GeV"       , 80  , 0.   , 0.5  , True  , lambda ev : ev.pfRelIso03_all  ,"F",1),
    #Variable('Ele_cutBasedV1_WPLoose_HWW' , "Electron[N] cutBasedV1_WPLoose_HWW"                  , "Events / XXX"           , 2   , -0.5 , 1.5  , False , lambda ev : ev.cutBasedV1_WPLoose_HWW        ,"I",1),
    #Variable('Ele_cutBasedV1_WPTight_HWW' , "Electron[N] cutBasedV1_WPTight_HWW"                  , "Events / XXX"           , 2   , -0.5 , 1.5  , False , lambda ev : ev.cutBasedV1_WPTight_HWW        ,"I",1),
    #Variable('Ele_mvaFall17V1Iso_WP90_HWW' , "Electron[N] mvaFall17V1Iso_WP90_HWW"                  , "Events / XXX"           , 2   , -0.5 , 1.5  , False , lambda ev : ev.mvaFall17V1Iso_WP90_HWW        ,"I",1),
    #Variable('Ele_mvaFall17V1Iso_WP90_SS_HWW' , "Electron[N] mvaFall17V1Iso_WP90_SS_HWW"                  , "Events / XXX"           , 2   , -0.5 , 1.5  , False , lambda ev : ev.mvaFall17V1Iso_WP90_SS_HWW        ,"I",1),
]

br_Taus = [
    Variable('Tau_pt'              , "Tau[N] Pt [GeV]"              , "Events / XXX GeV"       , 100 , 0.   , 500. , True  , lambda ev : ev.pt              ,"F",1),
    Variable('Tau_eta'             , "Tau[N] #eta"                  , "Events / XXX"           , 30  , -3.  , 3.   , False , lambda ev : ev.eta             ,"F",1),
    Variable('Tau_phi'             , "Tau[N] #phi"                  , "Events / XXX"           , 30  , -3.5 , 3.5  , True , lambda ev : ev.phi             ,"F",1),
    Variable('Tau_mass'            , "Tau[N] mass [GeV/c^{2}]"      , "Events / XXX GeV/c^{2}" , 100 , 0.   , 200. , False , lambda ev : ev.mass            ,"F",1),
]

br_Photons = [
    Variable('Pho_pt'              , "Pho[N] Pt [GeV]"              , "Events / XXX GeV"       , 100 , 0.   , 500. , True  , lambda ev : ev.pt              ,"F",1),
    Variable('Pho_eta'             , "Pho[N] #eta"                  , "Events / XXX"           , 30  , -3.  , 3.   , False , lambda ev : ev.eta             ,"F",1),
    Variable('Pho_phi'             , "Pho[N] #phi"                  , "Events / XXX"           , 30  , -3.5 , 3.5  , False , lambda ev : ev.phi             ,"F",1),
    Variable('Pho_mass'            , "Pho[N] mass [GeV/c^{2}]"      , "Events / XXX GeV/c^{2}" , 100 , 0.   , 200. , False , lambda ev : ev.mass            ,"F",1),
]

br_CleanJets = [
    Variable('CleanJet_pt'              , "Jet[N] Pt [GeV]"                        , "Events / XXX GeV"       , 100 , 0.   , 500.  , True        , lambda ev : ev.pt             ,"F",1),
    Variable('CleanJet_eta'             , "Jet[N] #eta"                            , "Events / XXX"           , 30  , -3.  , 3.    , False       , lambda ev : ev.eta            ,"F",1),
    Variable('CleanJet_phi'             , "Jet[N] #phi"                            , "Events / XXX"           , 30  , -3.5 , 3.5   , True       , lambda ev : ev.phi            ,"F",1),
    Variable('CleanJet_mass'            , "Jet[N] mass [GeV/c^{2}]"                , "Events / XXX GeV/c^{2}" , 100 , 0.   , 200.  , False       , lambda ev : ev.mass           ,"F",1),
    Variable('CleanJet_chEmEF'          , "Jet[N] Charged EM Energy Fraction"      , "Events / XXX"           , 100 , 0.   , 1.    , True       , lambda ev : ev.chEmEF         ,"F",1), # charged Electromagnetic Energy Fraction
    Variable('CleanJet_chHEF'           , "Jet[N] Charged Hadron Energy Fraction"  , "Events / XXX"           , 100 , 0.   , 1.    , True       , lambda ev : ev.chHEF          ,"F",1),    # charged Hadron Energy Fraction
    Variable('CleanJet_neEmEF'          , "Jet[N] Neutral EM Energy Fraction"      , "Events / XXX"           , 100 , 0.   , 1.    , True       , lambda ev : ev.neEmEF         ,"F",1), # neutral Electromagnetic Energy Fraction
    Variable('CleanJet_neHEF'           , "Jet[N] Neutral Hadron Energy Fraction"  , "Events / XXX"           , 100 , 0.   , 1.    , True       , lambda ev : ev.neHEF          ,"F",1),    # neutral Hadron Energy Fraction
    Variable('CleanJet_nElectrons'      , "Jet[N] nElectrons"                      , "Events / XXX"           , 6   , -0.5 , 5.5   , False       , lambda ev : ev.nElectrons     ,"I",1),
    Variable('CleanJet_nMuons'          , "Jet[N] nMuons"                          , "Events / XXX"           , 6   , -0.5 , 5.5   , False       , lambda ev : ev.nMuons         ,"I",1),
    Variable('CleanJet_puId'            , "Jet[N] puId"                            , "Events / XXX"           , 9   , -0.5 , 8.5   , False       , lambda ev : ev.puId           ,"I",1),
    Variable('CleanJet_jetId'           , "Jet[N] jetId"                           , "Events / XXX"           , 5   , -0.5 , 4.5   , False       , lambda ev : ev.jetId          ,"I",1),
    Variable('CleanJet_nConstituents'   , "Jet[N] nConstituents"                   , "Events / XXX"           , 16  , -0.5 , 15.5  , False       , lambda ev : ev.nConstituents  ,"I",1),
    Variable('CleanJet_btagCMVA'        , "Jet[N] btagCMVA"                        , "Events / XXX"           , 100 , 0.   , 1.    , False       , lambda ev : ev.btagCMVA       ,"F",1),
    Variable('CleanJet_btagCSVV2'       , "Jet[N] btagCSVV2"                       , "Events / XXX"           , 100 , 0.   , 1.    , False       , lambda ev : ev.btagCSVV2     ,"F",1),
]

br_Leptons = [
    #Variable('Lepton_Weight'              , "Lepton[N] Weight"                , "Events / XXX"           , 50  , -30. , 30.  , False , lambda ev : ev.effSF , "F" , 1 ),
    Variable('Lepton_pt'                  , "Lepton[N] Pt [GeV]"              , "Events / XXX GeV"       , 100 , 0.   , 500. , True  , lambda ev : ev.pt              ,"F",1),
    Variable('Lepton_eta'                 , "Lepton[N] #eta"                  , "Events / XXX"           , 30  , -3.  , 3.   , False , lambda ev : ev.eta             ,"F",1),
    Variable('Lepton_phi'                 , "Lepton[N] #phi"                  , "Events / XXX"           , 30  , -3.5 , 3.5  , False , lambda ev : ev.phi             ,"F",1),
    Variable('Lepton_mass'                , "Lepton[N] mass [GeV/c^{2}]"      , "Events / XXX GeV/c^{2}" , 100 , 0.   , 200. , False , lambda ev : ev.mass            ,"F",1),
    Variable('Lepton_pdgId'               , "Lepton[N] pdgId"                 , "Events / XXX"           , 40 , -20   , 20   , False , lambda ev : ev.pdgId           ,"I",1),
    Variable('Lepton_Ele_cutBased'            , "Lepton[N] cutBased"              , "Events / XXX"           , 6   , 0    , 6    , False , lambda ev : ev.cutBased if abs(ev.pdgId)==11 else -1        ,"I",1),
    #Variable('Lepton_Ele_cutBased_Fall17_V1'  , "Lepton[N] cutBased_Fall17_V1"    , "Events / XXX"           , 6   , 0    , 6    , False , lambda ev : ev.cutBased_Fall17_V1 if abs(ev.pdgId)==11 else -1         ,"I",1),
    #Variable('Lepton_Ele_mvaFall17V1Iso'      , "Lepton[N] mvaFall17V1Iso"        , "Events / XXX"           , 2   , -0.5 , 1.5  , False , lambda ev : ev.mvaFall17V1Iso if abs(ev.pdgId)==11 else -1        ,"I",1),
    #Variable('Lepton_Ele_mvaFall17V1Iso_WP90' , "Lepton[N] mvaFall17V1Iso_WP90"   , "Events / XXX"           , 2   , -0.5 , 1.5  , False , lambda ev : ev.mvaFall17V1Iso_WP90 if abs(ev.pdgId)==11 else -1        ,"I",1),
    #Variable('Lepton_Ele_mvaFall17V2Iso'      , "Lepton[N] mvaFall17V2Iso"        , "Events / XXX"           , 2   , -0.5 , 1.5  , False , lambda ev : ev.mvaFall17V2Iso if abs(ev.pdgId)==11 else -1        ,"I",1),
    #Variable('Lepton_Ele_mvaFall17V2Iso_WP90' , "Lepton[N] mvaFall17V2Iso_WP90"   , "Events / XXX"           , 2   , -0.5 , 1.5  , False , lambda ev : ev.mvaFall17V2Iso_WP90 if abs(ev.pdgId)==11 else -1        ,"I",1),
    Variable('Lepton_pfRelIso03_all'      , "Lepton[N] pfRelIso03_all [GeV]"  , "Events / XXX GeV"       , 80  , 0.   , 0.5  , True  , lambda ev : ev.pfRelIso03_all  ,"F",1),
    Variable('Lepton_Mu_pfRelIso04_all'      , "Lepton[N] pfRelIso04_all [GeV]"  , "Events / XXX GeV"       , 80  , 0.   , 0.5  , True  , lambda ev : ev.pfRelIso04_all if abs(ev.pdgId)==13 else -1   ,"F",1),
    #Variable('Lepton_Mu_looseId'             , "Lepton[N] looseId"               , "Events / XXX"           , 2   , -0.5 , 1.5  , False , lambda ev : ev.looseId if abs(ev.pdgId)==13 else -1         ,"I",1),
    Variable('Lepton_Mu_mediumId'            , "Lepton[N] mediumId"              , "Events / XXX"           , 2   , -0.5 , 1.5  , False , lambda ev : ev.mediumId if abs(ev.pdgId)==13 else -1         ,"I",1),
    Variable('Lepton_Mu_tightId'             , "Lepton[N] tightId"               , "Events / XXX"           , 2   , -0.5 , 1.5  , False , lambda ev : ev.tightId if abs(ev.pdgId)==13 else -1          ,"I",1),

]

br_all = br_global + br_Muons + br_Electrons + br_Taus + br_Photons + br_CleanJets + br_Leptons + br_Vll + br_Vl2JJ + br_Vjj
