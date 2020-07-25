import ROOT
import os
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class pujetIdSFProducerCpp(Module):
    def __init__(self , puidSFSource , year , wp ):
        if "/pujetIdSFProducerCpp_cc.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ pujetIdSFProducerCpp worker module"
            base = os.getenv("NANOAODTOOLS_BASE")
            if base:
                ROOT.gROOT.ProcessLine(".L %s/src/pujetIdSFProducerCpp.cc+O"%base)
            else:
                base = "%s/src/PhysicsTools/NanoAODTools"%os.getenv("CMSSW_BASE")
                ROOT.gSystem.Load("libPhysicsToolsNanoAODTools.so")
                ROOT.gROOT.ProcessLine(".L %s/interface/pujetIdSFProducerCpp.h"%base)
                
        # Initialization
        self.worker = ROOT.pujetIdSFProducerCpp( puidSFSource , year , wp )
        
        self.isMC = True
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.initReaders(inputTree) # initReaders must be called in beginFile
        self.out = wrappedOutputTree
        self.out.branch("PUJetIdSF",  "F");
        if any (x in inputFile.GetName() for x in ['SingleMuon','SingleElectron','DoubleMuon']):
            print "Looking at DATA"
            self.isMC = False
        pass
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def initReaders(self,tree): # this function gets the pointers to Value and ArrayReaders and sets them in the C++ worker class
        self.worker.setVals(
            tree.valueReader("nLepton"),
            tree.valueReader("nJet"),
            tree.arrayReader("Lepton_eta"),
            tree.arrayReader("Lepton_phi"),
            tree.arrayReader("Jet_pt"),
            tree.arrayReader("Jet_eta"),
            tree.arrayReader("Jet_phi"),
            tree.arrayReader("Jet_jetId"),
            tree.arrayReader("Jet_genJetIdx"),
            tree.arrayReader("Jet_puId")
        ) 
        self._ttreereaderversion = tree._ttreereaderversion # self._ttreereaderversion must be set AFTER all calls to tree.valueReader or tree.arrayReader

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if not self.isMC : return False
        if event._tree._ttreereaderversion > self._ttreereaderversion: # do this check at every event, as other modules might have read further branches
            self.initReaders(event._tree)
        # do NOT access other branches in python between the check/call to initReaders and the call to C++ worker code
        
        output = self.worker.evaluate()
        
        self.out.fillBranch("PUJetIdSF", output )
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

pujetIdSF = lambda : pujetIdSFProducerCpp(
    puidSFSource = '%s/python/postprocessing/data/latino/scale_factor/RunII_JetPUID/PUID_81XTraining_EffSFandUncties.root' %os.getenv("NANOAODTOOLS_BASE"),
    year = '2016' ,
    wp = 'loose',
)
