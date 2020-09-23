import ROOT
import sys
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class alias_Producer(Module):
    def __init__(self):
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
        
        lepton_dz=[]; lepton_dxy=[]
        for ilep in leptons:
            lep_dz = electrons[ilep.electronIdx].dz if abs(ilep.pdgId)==11 else muons[ilep.muonIdx].dz
            lep_dxy = electrons[ilep.electronIdx].dxy if abs(ilep.pdgId)==11 else muons[ilep.muonIdx].dxy
            lepton_dz.append( lep_dz ) ; lepton_dxy.append( lep_dxy )

        monojet = ROOT.TLorentzVector() ; monojetlep1 = ROOT.TLorentzVector() ; monojetlep2 = ROOT.TLorentzVector()
        dijet = ROOT.TLorentzVector() ; dijetlep1 = ROOT.TLorentzVector() ; dijetlep2 = ROOT.TLorentzVector()
        
        ## mj1/2
        if event.nCleanJet==1 and event.nLepton!=0 :
            monojet = jets[cleanjets[0].jetIdx].p4()

            if event.nLepton>=1 :
                monojetlep1 = monojet + electrons[leptons[0].electronIdx].p4() if abs(leptons[0].pdgId)==11 else monojet + muons[leptons[0].muonIdx].p4()
            if event.nLepton>=2 :
                monojetlep2 = monojet + electrons[leptons[1].electronIdx].p4() if abs(leptons[1].pdgId)==11 else monojet + muons[leptons[1].muonIdx].p4()
        ## mjjl1/2
        elif event.nCleanJet>=2 and event.nLepton!=0 :
            dijet = jets[cleanjets[0].jetIdx].p4() + jets[cleanjets[1].jetIdx].p4()

            if event.nLepton>=1 :
                dijetlep1 = dijet + electrons[leptons[0].electronIdx].p4() if abs(leptons[0].pdgId)==11 else dijet + muons[leptons[0].muonIdx].p4()
            if event.nLepton>=2 :
                dijetlep2 = dijet + electrons[leptons[1].electronIdx].p4() if abs(leptons[1].pdgId)==11 else dijet + muons[leptons[1].muonIdx].p4()

        self.out.fillBranch( 'Lepton_dz'  , lepton_dz )
        self.out.fillBranch( 'Lepton_dxy' , lepton_dxy )
        self.out.fillBranch( 'mjL1'       , monojetlep1.M() if monojetlep1.M() != 0. else -9999. )
        self.out.fillBranch( 'mjL2'       , monojetlep2.M() if monojetlep2.M() != 0. else -9999. )
        self.out.fillBranch( 'mjjL1'      , dijetlep1.M() if dijetlep1.M() != 0. else -9999. )
        self.out.fillBranch( 'mjjL2'      , dijetlep2.M() if dijetlep2.M() != 0. else -9999. )

        # preselection
        #return True if nbveto == 0 else False;
        return True
    pass

alias = lambda : alias_Producer()
