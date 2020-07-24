import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
#from PhysicsTools.NanoAODTools.postprocessing.helper.anaFunc import *
from PhysicsTools.NanoAODTools.postprocessing.helpers.tools import * #closest, deltaPhi, deltaR, matchObjectCollection

from PhysicsTools.NanoAODTools.postprocessing.data.vars.variables import br_all, br_global, br_Muons, br_Electrons, br_Taus, br_Photons, br_CleanJets, \
    br_Leptons, br_Vll, br_Vl2JJ, br_Vjj

import sys
from math import fabs, sqrt, cos
from ROOT import TLorentzVector
from collections import OrderedDict

class Producer(Module):
    def __init__(self, elePresel, muPresel, tauPresel, phoPresel, jetPresel, ewkCorrection, DEBUG=False, writeobj=4):
        self.eleSel = elePresel
        self.muSel = muPresel
        self.tauSel = tauPresel
        self.phoSel = phoPresel
        self.jetSel = jetPresel
        self.ewk = ewkCorrection
        self.debug = DEBUG
        self.nWrite = writeobj
        self.isMC = True
        self.events = 0
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        #self.initReaders(inputTree) # initReaders must be called in beginFile
        self.out = wrappedOutputTree
        self.FilesName=inputFile
        self.InputTree=inputTree
        self.OutputFile=outputFile
        if any (x in self.FilesName.GetName() for x in ['SingleMuon','SingleElectron','DoubleMuon']):
            print "Looking at DATA"
            self.isMC = False
        else:
            print "Looking at MC"

        ## ---------- Plots Initialization ----------
        self.br_scalar = [ ibranch for ibranch in br_all if ibranch.dimen()==0 ]
        self.br_vector = [ ibranch for ibranch in br_all if ibranch.dimen()==1 ]
        ##scalar
        self.out.branch('counter', 'I')
        for ibranch in self.br_scalar:
            self.out.branch("%s"%ibranch.name(), "%s"%ibranch._type())
        ##vector
        for ibranch in self.br_vector:
            self.out.branch("%s"%ibranch.name(), "%s"%ibranch._type(), lenVar="n%s"%ibranch.name().split('_')[0])

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        self.out.fillBranch('counter' , 1)
        self.events+=1
        if self.debug: print " === No. %s EVENT Begin === " % self.events
        ########################################
        # Initialization
        ########################################
        if self.debug: print " === Initializing per Event variables === "
        #Initialize only per event variables.
        gVar={}; gVar={ Svar: -999. for Svar in [ ibranch.name() for ibranch in self.br_scalar ] }
        cnjet=0
        mht = ROOT.TLorentzVector()
        mht.SetPtEtaPhiM(0.,0.,0.,0.)
        ########################################
        #            READ OBJECTS
        ########################################
        ##READ Collection
        if self.isMC: genparts = Collection(event, "GenPart")
        if self.isMC: genjets = Collection(event, "GenJet")
        electrons = Collection(event, "Electron") ;
        muons = Collection(event, "Muon") ;
        taus = Collection(event, "Tau")
        photons = Collection(event, "Photon");
        jets = Collection(event, "Jet");

        ##READ Variables from other module
        ## PU
        #puweight = event.puWeight

        ## GenProducer
        ## Trigger
        ####

        ## Electron
        #TIGHT WP
        ElecList = filter(self.eleSel, electrons); ElecList.sort(key=getPt, reverse=True)
        nElectrons = len(ElecList); gVar['nEle'] = nElectrons

        ## Muon
        MuonList = filter(self.muSel, muons); MuonList.sort(key=getPt, reverse=True)
        nMuons = len(MuonList); gVar['nMu'] = nMuons

        ## Lepton
        LeptonList = MuonList+ElecList; LeptonList.sort(key=getPt, reverse=True)
        nLepton = len(MuonList+ElecList); gVar['nLepton'] = nLepton

        ## Tau
        TauList = filter(self.tauSel, taus); TauList.sort(key=getPt, reverse=True)
        nTaus= len(TauList); gVar['nTau'] = nTaus

        ## Photon
        PhotonList = filter(self.phoSel, photons); PhotonList.sort(key=getPt, reverse=True)
        nPhotons = len(PhotonList); gVar["nPho"] = nPhotons

        ## CleanJets
        CleanJet = filter(self.jetSel, jets); CleanJet.sort(key=getPt, reverse=True)
        nCleanJets = len(CleanJet); gVar["nCleanJet"] = nCleanJets;

        ## CleanJets MHT
        for ijet in CleanJet: mht += ijet.p4()
        gVar["MHT_pt"] = mht.Pt() ; gVar["MHT_phi"] = -mht.Phi()

        ## MET
        gVar['MET_pt'] = event.MET_pt
        gVar['MET_phi'] = event.MET_phi

        ########################################
        #   ANALYSIS
        ########################################
        #Composite Variables
        #Vll = TLorentzVector(); Vjj = TLorentzVector(); Vl2JJ = TLorentzVector();
        #Vll.SetPtEtaPhiM(0.,0.,0.,0.); Vjj.SetPtEtaPhiM(0.,0.,0.,0.); Vl2JJ.SetPtEtaPhiM(0.,0.,0.,0.);
        if nLepton>=1:
            gVar['dphilmet1'] = deltaPhi(LeptonList[0].phi,event.MET_phi)
            gVar['mtw1'] = sqrt( 2*LeptonList[0].pt*event.MET_pt*(1-cos(fabs(deltaPhi(LeptonList[0].phi,event.MET_phi)))) )

        if nLepton>=2:
            gVar['dphilmet2'] = deltaPhi(LeptonList[1].phi,event.MET_phi)
            gVar['mtw2'] = sqrt( 2*LeptonList[1].pt*event.MET_pt*(1-cos(fabs(deltaPhi(LeptonList[1].phi,event.MET_phi)))) )
            Vll = LeptonList[0].p4() + LeptonList[1].p4()
            for ibranch in br_Vll: gVar[ibranch.name()] = ibranch.value(Vll)

        if nCleanJets>=2:
            Vjj = CleanJet[0].p4() + CleanJet[1].p4()
            for ibranch in br_Vjj: gVar[ibranch.name()] = ibranch.value(Vjj)

        if nLepton>=2 and nCleanJets>=2:
            Vl2JJ = LeptonList[1].p4() + CleanJet[0].p4() + CleanJet[1].p4()
            for ibranch in br_Vl2JJ: gVar[ibranch.name()] = ibranch.value(Vl2JJ)

        #######################################
        #    FILL TREE
        #######################################

        #Fill GLOBAL (Per Event)
        for i, ibranch in enumerate(self.br_scalar):
            self.out.fillBranch( ibranch.name() , gVar[ibranch.name()] )

        #Fill Local (Per Physics Objects)
        # Electron #[:self.nWrite]
        for ibranch in br_Electrons:
            self.out.fillBranch( ibranch.name(), map( ibranch.lamb(), ElecList ) )

        # Muon
        for ibranch in br_Muons:
            self.out.fillBranch( ibranch.name(), map( ibranch.lamb(), MuonList ) )

        # Lepton
        for ibranch in br_Leptons:
            self.out.fillBranch( ibranch.name(), map( ibranch.lamb(), LeptonList ) )

        # Tau
        for ibranch in br_Taus:
            self.out.fillBranch( ibranch.name(), map( ibranch.lamb(), TauList ) )

        # Photon
        for ibranch in br_Photons:
            self.out.fillBranch( ibranch.name(), map( ibranch.lamb(), PhotonList ) )

        # CleanJet
        for i, ibranch in enumerate(br_CleanJets):
            self.out.fillBranch( ibranch.name(),  map( ibranch.lamb() , CleanJet ) )

        #################################################
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

producer = lambda : Producer(
    ####PRESELECTION
    elePresel = lambda el : el.pt>15 and fabs(el.eta)<2.4 and el.cutBased>0 and el.isClean==1,
    muPresel  = lambda mu : mu.pt>5  and fabs(mu.eta)<2.4 and mu.mediumId>0 and mu.isClean==1,
    tauPresel = lambda tau : tau.pt>18 and fabs(tau.eta)<2.3,
    phoPresel = lambda pho : pho.pt>15 and fabs(pho.eta)<2.5,
    jetPresel = lambda je : je.pt>30 and fabs(je.eta)<2.5 and je.jetId>0 and je.puId>4 and je.isClean==1,
    ewkCorrection=False,
    DEBUG=False,
    writeobj=None
)
