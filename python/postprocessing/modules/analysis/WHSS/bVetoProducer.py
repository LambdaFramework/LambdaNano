import ROOT
import sys
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class bVetoProducer(Module):
    def __init__( self , year , jetSelection = lambda x : x.pt > 20 and abs(x.eta) < 2.5 ):
        self.year = year
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
        if any (x in inputFile.GetName() for x in [ 'SingleMuon' , 'SingleElectron' , 'DoubleMuon' , 'DoubleEG' , 'MuonEG' , 'EGamma' ]):
            self.isMC = False    
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        cleanjets = Collection(event, "CleanJet")

        bWP={
            '2016' : 0.1522 ,
            '2017' : 0.1522 ,
            '2018' : 0.1241
        }

        bJet_cands = filter( self.jetSel , cleanjets)
        nbveto=0 ; btagSF=1. ; bReqSF=1.
        zerojet = True
        if len(bJet_cands)!=0 :
            zerojet = True if list(bJet_cands)[0].pt < 30. else False
        
        for ijet in bJet_cands :
            jetIdx = ijet.jetIdx
            if jetIdx < 0 :
                print("ijet.jetIdx < 0")
                continue;
            if event.Jet_btagDeepB[jetIdx] > bWP[self.year]: nbveto+=1

        btagSF = sum( map(lambda y : ROOT.TMath.Log(event.Jet_btagSF_shape[y.jetIdx]) , bJet_cands ) ) if self.isMC else 1.

        #if self.year=='2017':
        #    bjcands = filter( lambda x : x.pt > 30 and abs(x.eta)<2.5 , cleanjets )
        #    bReqSF = sum( map(lambda y : ROOT.TMath.Log(event.Jet_btagSF_shape[y.jetIdx]) , bjcands ) ) if self.isMC else 1.
        
        self.out.fillBranch( "isbVeto" , 1 if nbveto == 0 else 0 )
        self.out.fillBranch( "vbVetoSF" , ROOT.TMath.Exp(btagSF) )

        return True
    pass

#bVetoer = lambda : bVetoProducer(
#    year = None ,
#    jetSelection = lambda x : x.pt > 20 and abs(x.eta) < 2.5
#)
