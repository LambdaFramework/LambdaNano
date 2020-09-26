import ROOT
import sys
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.helpers.tools import *

class aliasProducer(Module):
    def __init__( self , year_ ):
        self.year = year_
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch( 'Lepton_dz' , 'F' , lenVar='nLepton' )
        self.out.branch( 'Lepton_dxy' , 'F' , lenVar='nLepton' )
        self.out.branch( 'mjL1' , 'F' )
        self.out.branch( 'mjL2' , 'F' )
        self.out.branch( 'mjjL1' , 'F' )
        self.out.branch( 'mjjL2' , 'F' )
        self.out.branch( 'dRjL1' , 'F' )
        self.out.branch( 'dRjL2' , 'F' )
        self.out.branch( 'dRjjL1' , 'F' )
        self.out.branch( 'dRjjL2' , 'F' )
        self.out.branch( 'Top_pTrw' , 'F' )

        if any (x in inputFile.GetName() for x in [ 'SingleMuon' , 'SingleElectron' , 'DoubleMuon' , 'DoubleEG' , 'MuonEG' , 'EGamma' ]):
            self.isMC = False
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        #if not self.isMC : return True

        ## impact parameters
        leptons = Collection(event, "Lepton")
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        cleanjets = Collection(event,"CleanJet")
        jets = Collection(event,"Jet")
        genparts = Collection(event,"GenPart")

        lepton_dz=[]; lepton_dxy=[]
        for ilep in leptons:
            lep_dz = electrons[ilep.electronIdx].dz if abs(ilep.pdgId)==11 else muons[ilep.muonIdx].dz
            lep_dxy = electrons[ilep.electronIdx].dxy if abs(ilep.pdgId)==11 else muons[ilep.muonIdx].dxy
            lepton_dz.append( lep_dz ) ; lepton_dxy.append( lep_dxy )

        monojetlep1 = ROOT.TLorentzVector() ; monojetlep2 = ROOT.TLorentzVector()
        dRjL1_ = 99999. ; dRjL2_ = 9999. ; dRjjL1_ = 9999. ; dRjjL2_ = 9999.
        dijetlep1 = ROOT.TLorentzVector() ; dijetlep2 = ROOT.TLorentzVector()

        monojet = ROOT.TLorentzVector() ; dijet = ROOT.TLorentzVector()
        lepton1 = ROOT.TLorentzVector() ; lepton2 = ROOT.TLorentzVector()

        ## mj1/2
        cleanjet30 = filter( lambda x : x.pt > 30 , cleanjets )

        if len(cleanjet30) == 1 and event.nLepton != 0 :
            monojet = jets[cleanjets[0].jetIdx].p4()
            lepton1 = electrons[leptons[0].electronIdx].p4() if abs(leptons[0].pdgId)==11 else muons[leptons[0].muonIdx].p4()

            monojetlep1 = monojet + lepton1
            dRjL1_ = deltaR( monojet.Eta() , monojet.Phi() , lepton1.Eta() , lepton1.Phi() )

            if event.nLepton > 1 :
                lepton2 = electrons[leptons[1].electronIdx].p4() if abs(leptons[1].pdgId)==11 else muons[leptons[1].muonIdx].p4()
                monojetlep2 = monojet + lepton2
                dRjL2_ = deltaR( monojet.Eta() , monojet.Phi() , lepton2.Eta() , lepton2.Phi() )

        ## mjjl1/2
        elif len(cleanjet30) > 1 and event.nLepton != 0 :
            dijet = jets[cleanjets[0].jetIdx].p4() + jets[cleanjets[1].jetIdx].p4()
            lepton1 = electrons[leptons[0].electronIdx].p4() if abs(leptons[0].pdgId)==11 else muons[leptons[0].muonIdx].p4()

            dijetlep1 = dijet + lepton1
            dRjjL1_ = deltaR( dijet.Eta() , dijet.Phi() , lepton1.Eta() , lepton1.Phi() )
            if event.nLepton > 1 :
                lepton2 = electrons[leptons[1].electronIdx].p4() if abs(leptons[1].pdgId)==11 else muons[leptons[1].muonIdx].p4()
                dijetlep2 = dijet + lepton2
                dRjjL2_ = deltaR( dijet.Eta() , dijet.Phi() , lepton2.Eta() , lepton2.Phi() )

        ## TopGEN for 2018
        if self.year == '2018':
            lastcopy = (1 << 13)
            topGenPtOTF = 0.
            antitopGenPtOTF = 0.
            Top_pTrw = -9999.
            TTbar = filter( lambda x : abs(x.pdgId) == 6 and ( ( x.statusFlags / (1 << 13) ) % 2 ) != 0 , genparts )
            top = filter( lambda x : x.pdgId == 6 and ( ( x.statusFlags / (1 << 13) ) % 2 ) != 0 , TTbar )
            antitop = filter( lambda x : x.pdgId == -6 and ( ( x.statusFlags / (1 << 13) ) % 2 ) != 0 , TTbar )
            if len(TTbar) == 2 :
                for itop in top : topGenPtOTF+=itop.pt
                for iantitop in antitop : antitopGenPtOTF+=iantitop.pt

                Top_pTrw = ROOT.TMath.Sqrt ( ROOT.TMath.Exp( 0.0615 - 0.0005 * topGenPtOTF ) * ROOT.TMath.Exp( 0.0615 - 0.0005 * antitopGenPtOTF ) )
            elif len(TTbar) == 1 :
                Top_pTrw = 1.


        #'(Sum(abs(GenPart_pdgId) == 6 && TMath::Odd(GenPart_statusFlags / (1 << 13))) == 2) * (TMath::Sqrt(TMath::Exp(0.0615 - 0.0005 * (Sum((GenPart_pdgId == 6 && TMath::Odd(GenPart_statusFlags / (1 << 13))) * GenPart_pt))) * TMath::Exp(0.0615 - 0.0005 * (Sum((GenPart_pdgId == -6 && TMath::Odd(GenPart_statusFlags / (1 << 13))) * GenPart_pt))))) + (Sum(abs(GenPart_pdgId) == 6 && TMath::Odd(GenPart_statusFlags / (1 << 13))) == 1)'

        self.out.fillBranch( 'Lepton_dz'  , lepton_dz )
        self.out.fillBranch( 'Lepton_dxy' , lepton_dxy )
        self.out.fillBranch( 'mjL1'       , monojetlep1.M() if monojetlep1.M() != 0. else 9999. )
        self.out.fillBranch( 'mjL2'       , monojetlep2.M() if monojetlep2.M() != 0. else 9999. )
        self.out.fillBranch( 'mjjL1'      , dijetlep1.M() if dijetlep1.M() != 0. else 9999. )
        self.out.fillBranch( 'mjjL2'      , dijetlep2.M() if dijetlep2.M() != 0. else 9999. )
        self.out.fillBranch( 'dRjL1'      , dRjL1_ )
	self.out.fillBranch( 'dRjL2'      , dRjL2_ )
        self.out.fillBranch( 'dRjjL1'     , dRjjL1_ )
        self.out.fillBranch( 'dRjjL2'     , dRjjL2_ )
        self.out.fillBranch( 'Top_pTrw'   , Top_pTrw )

        # preselection
        #return True if nbveto == 0 else False;
        return True
    pass

#alias = lambda : alias_Producer()
