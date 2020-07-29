import ROOT
import sys
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class bVeto_Producer(Module):
    def __init__( self, jetSelection ):
        self.jetSel  = jetSelection
        self.isMC = True
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch( "isbVeto" , "I" )
        self.out.branch( "vbVetoSF" , "F" )
        if any (x in inputFile.GetName() for x in ['SingleMuon','SingleElectron','DoubleMuon']):
            print "Looking at DATA"
            self.isMC = False    
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        #if not self.isMC : return True
        
        cleanjets = Collection(event, "CleanJet")
        
        #nbveto = len(filter( lambda y : event.Jet_btagDeepB[y.jetIdx] > 0.1522  , filter( self.jetSel , cleanjets )))
        nbveto=0
        #btagSF=1.
        for ijet in filter( self.jetSel , cleanjets) :
            jetIdx = ijet.jetIdx
            if jetIdx < 0 :
                print("ijet.jetIdx < 0")
                continue;
            if event.Jet_btagDeepB[jetIdx] > 0.1522: nbveto+=1
            #btagSF = ROOT.TMath.Log(event.Jet_btagSF_shape[jetIdx])
            
        btagSF = sum( map(lambda y : ROOT.TMath.Log(event.Jet_btagSF_shape[y.jetIdx]) , filter( self.jetSel , cleanjets )))
        
        
        self.out.fillBranch( "isbVeto" , 1 if nbveto == 0 else 0 )
        self.out.fillBranch( "vbVetoSF" , ROOT.TMath.Exp(btagSF) )

        # preselection
        #return True if nbveto == 0 else False;
        return True
    pass

bVetoer = lambda : bVeto_Producer(
    jetSelection = lambda x : x.pt > 20 and abs(x.eta) < 2.5
)
