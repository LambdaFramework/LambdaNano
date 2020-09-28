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
        self.out.branch( "bVeto_v1" , "I" )
        self.out.branch( "bVeto_v2" , "I" )
        self.out.branch( "bVetoSF_v1" , "F" )
        self.out.branch( "bVetoSF_v2" , "F" )
        if any (x in inputFile.GetName() for x in [ 'SingleMuon' , 'SingleElectron' , 'DoubleMuon' , 'DoubleEG' , 'MuonEG' , 'EGamma' ]):
            self.isMC = False    
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        cleanjets = Collection(event, "CleanJet")

        # latino's
        # loose
        bWP_v1 = {
            '2016' : 0.1522 ,
            '2017' : 0.1522 ,
            '2018' : 0.1241
        }

        # alberto's
        # https://github.com/zucchett/NanoSkim/blob/master/Skimmer/samesign.py#L118-L135
        # medium
        bWP_v2 = {
            '2016' : 0.6321 ,
            '2017' : 0.4941 ,
            '2018' : 0.4184
        }

        bJet20 = filter( self.jetSel , cleanjets )
        bJet30 = filter( lambda x : x.pt > 30 and abs(x.eta) < 2.5 , cleanjets )

        nbjet_v1 = 0 ; btagSF_v1 = 1. ; bReqSF_v1 = 1.
        nbjet_v2 = 0 ; btagSF_v2 = 1. ; bReqSF_v2 = 1.

        # v1
        for ijet in bJet20 :
            jetIdx = ijet.jetIdx
            if jetIdx < 0 : continue;
            if event.Jet_btagDeepB[jetIdx] > bWP_v1[self.year]: nbjet_v1+=1
            
        btagSF_v1 = sum( map(lambda y : ROOT.TMath.Log(event.Jet_btagSF_shape[y.jetIdx]) , bJet20 ) ) if self.isMC else 1.
        
        # v2
        for ijet in bJet30 :
            jetIdx = ijet.jetIdx
            if jetIdx < 0 : continue;
            if event.Jet_btagDeepB[jetIdx] >= bWP_v2[self.year]: nbjet_v2+=1
            
        btagSF_v2 = sum( map(lambda y : ROOT.TMath.Log(event.Jet_btagSF_shape[y.jetIdx]) , bJet30 ) ) if self.isMC else	1.
        
        self.out.fillBranch( "bVeto_v1" , 1 if nbjet_v1 == 0 else 0 )
        self.out.fillBranch( "bVeto_v2" , 1 if nbjet_v2 == 0 else 0 )
        self.out.fillBranch( "bVetoSF_v1" , ROOT.TMath.Exp(btagSF_v1) )
        self.out.fillBranch( "bVetoSF_v2" , ROOT.TMath.Exp(btagSF_v2) )

        # 2017 missing some
        #https://github.com/latinos/PlotsConfigurations/blob/master/Configurations/WH_SS/Full2017nanov6/aliases.py#L146-L149

        return True
    pass

#bVetoer = lambda : bVetoProducer(
#    year = None ,
#    jetSelection = lambda x : x.pt > 20 and abs(x.eta) < 2.5
#)
