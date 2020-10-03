import ROOT
import os
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class eleFlipSFProducerCpp(Module):
    def __init__(self , year , wp ):
        self.wp = wp
        if "/eleFlipSFProducerCpp_cc.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ eleFlipSFProducerCpp worker module"
            base = os.getenv("NANOAODTOOLS_BASE")
            if base:
                ROOT.gROOT.ProcessLine(".L %s/src/eleFlipSFProducerCpp.cc+O"%base)
            else:
                base = "%s/src/PhysicsTools/NanoAODTools"%os.getenv("CMSSW_BASE")
                ROOT.gSystem.Load("libPhysicsToolsNanoAODTools.so")
                ROOT.gROOT.ProcessLine(".L %s/interface/eleFlipSFProducerCpp.h"%base)
                
        # Initialization
        self.worker = ROOT.eleFlipSFProducerCpp( year , wp )
        
        self.isMC = True
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.initReaders(inputTree) # initReaders must be called in beginFile
        self.out = wrappedOutputTree
        self.out.branch( "flip_ele_%s_2l" % self.wp   ,  "F" );
        #self.out.branch( "flip_ele_%s_SF_2l" % self.wp   ,  "F" );
        if any (x in inputFile.GetName() for x in [ 'SingleMuon' , 'SingleElectron' , 'DoubleMuon' , 'DoubleEG' , 'MuonEG' , 'EGamma' ]):
            self.isMC = False
        pass
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def initReaders(self,tree): # this function gets the pointers to Value and ArrayReaders and sets them in the C++ worker class
        self.worker.setVals(
            tree.valueReader("nLepton") ,
            tree.arrayReader("Lepton_pt") ,
            tree.arrayReader("Lepton_eta") ,
            tree.arrayReader("Lepton_phi") ,
            tree.arrayReader("Lepton_pdgId") ,
            tree.valueReader("nLeptonGen") ,
            tree.arrayReader("LeptonGen_pt") ,
            tree.arrayReader("LeptonGen_eta") ,
            tree.arrayReader("LeptonGen_phi") ,
            tree.arrayReader("LeptonGen_pdgId") ,

        ) 
        self._ttreereaderversion = tree._ttreereaderversion # self._ttreereaderversion must be set AFTER all calls to tree.valueReader or tree.arrayReader

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if not self.isMC : return False
        
        if event._tree._ttreereaderversion > self._ttreereaderversion: # do this check at every event, as other modules might have read further branches
            self.initReaders(event._tree)
        # do NOT access other branches in python between the check/call to initReaders and the call to C++ worker code
        
        totalFlip = self.worker.evaluate()
        
        self.out.fillBranch( "flip_ele_%s_2l" % self.wp      ,  totalFlip ) # total flip rate
        #self.out.fillBranch( "flip_ele_%s_SF_2l" % self.wp   ,  totalFlip[1] ) # scale factor

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

#lepSF = lambda : lepSFProducerCpp(
#    year = '2016' ,
#    nlep = 2 ,
#    sf = 'total_SF'
#)
