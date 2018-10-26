import ROOT
import os
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class mhtjuProducerCpp(Module): # MHT producer, unclean jets only (no lepton overlap cleaning, no jet selection)
    def __init__(self):
        if "/mhtjuProducerCppWorker_cc.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ mhtjuProducerCppWorker worker module"
            base = os.getenv("NANOAODTOOLS_BASE")
            if base:
                ROOT.gROOT.ProcessLine(".L %s/src/mhtjuProducerCppWorker.cc+O"%base)
            else:
                base = "%s/src/PhysicsTools/NanoAODTools"%os.getenv("CMSSW_BASE")
                ROOT.gSystem.Load("libPhysicsToolsNanoAODTools.so")
                ROOT.gROOT.ProcessLine(".L %s/interface/mhtjuProducerCppWorker.h"%base)
        self.worker = ROOT.mhtjuProducerCppWorker()
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.initReaders(inputTree) # initReaders must be called in beginFile
        self.out = wrappedOutputTree
        self.out.branch("MHTju_pt",  "F");
        self.out.branch("MHTju_phi", "F");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def initReaders(self,tree): # this function gets the pointers to Value and ArrayReaders and sets them in the C++ worker class
        #jettiness
        self.nJet = tree.valueReader("nJet")
        self.Jet_pt = tree.arrayReader("Jet_pt")
        self.Jet_phi = tree.arrayReader("Jet_phi")
        self.Jet_puId = tree.arrayReader("Jet_puId")
        #electron
        self.nElectron = tree.valueReader("nElectron")
        self.Electron_pt = tree.arrayReader("Electron_pt")
        self.Electron_phi = tree.arrayReader("Electron_phi")
        self.Electron_cutBased = tree.arrayReader("Electron_cutBased")
        #muon
        self.nMuon = tree.valueReader("nMuon")
        self.Muon_pt = tree.arrayReader("Muon_pt")
        self.Muon_phi = tree.arrayReader("Muon_phi")
        self.Muon_softId = tree.arrayReader("Muon_softId")
        self.Muon_mediumId = tree.arrayReader("Muon_mediumId")
        self.Muon_tightId = tree.arrayReader("Muon_tightId")
        #sending it worker
        self.worker.setJets(self.nJet,self.Jet_pt,self.Jet_phi,self.Jet_puId)
        self.worker.setElectron(self.nElectron,self.Electron_pt,self.Electron_phi,self.Electron_cutBased)
        self.worker.setMuon(self.nMuon,self.Muon_pt,self.Muon_phi,self.Muon_softId,self.Muon_mediumId,self.Muon_tightId)
        
        self._ttreereaderversion = tree._ttreereaderversion # self._ttreereaderversion must be set AFTER all calls to tree.valueReader or tree.arrayReader

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        if event._tree._ttreereaderversion > self._ttreereaderversion: # do this check at every event, as other modules might have read further branches
            self.initReaders(event._tree)
        # do NOT access other branches in python between the check/call to initReaders and the call to C++ worker code
        output = self.worker.getHT()

        self.out.fillBranch("MHTju_pt", output[0])
        self.out.fillBranch("MHTju_phi", -output[1]) # note the minus
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

mhtju = lambda : mhtjuProducerCpp()
