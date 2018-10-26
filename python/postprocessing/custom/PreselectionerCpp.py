import ROOT
import os
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class PreselectionerCpp(Module): # MHT producer, unclean jets only (no lepton overlap cleaning, no jet selection)
    def __init__(self):
        if "/preselectionerCppWorker_cc.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ preselectionerCppWorker worker module"
            base = os.getenv("NANOAODTOOLS_BASE")
            if base:
                ROOT.gROOT.ProcessLine(".L %s/src/preselectionerCppWorker.cc+O"%base)
            else:
                base = "%s/src/PhysicsTools/NanoAODTools"%os.getenv("CMSSW_BASE")
                ROOT.gSystem.Load("libPhysicsToolsNanoAODTools.so")
                ROOT.gROOT.ProcessLine(".L %s/interface/preselectionerCppWorker.h"%base)
        self.worker = ROOT.preselectionerCppWorker()
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.initReaders(inputTree) # initReaders must be called in beginFile
        self.out = wrappedOutputTree
        #Book histogram
        self.out.branch("MHTju_pt_counter", "I")
        #self.out.branch("ZPtCorr","F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def initReaders(self,tree): # this function gets the pointers to Value and ArrayReaders and sets them in the C++ worker class
        #assign/extract pointers to Value and Array
        self.MHTju_pt = tree.valueReader("MHTju_pt")
        self.MHTju_phi = tree.valueReader("MHTju_phi")
        #self.nGenPart = tree.valueReader("nGenPart")
        #self.GenPart_pdgId = tree.arrayReader("GenPart_pdgId")
        #self.GenPart_pt = tree.arrayReader("GenPart_pt")

        #set in C++ worker class
        self.worker.setMHTju(self.MHTju_pt,self.MHTju_phi)
        #self.worker.setGen(self.nGenPart,self.GenPart_pt,self.GenPart_pdgId)

        self._ttreereaderversion = tree._ttreereaderversion # self._ttreereaderversion must be set AFTER all calls to tree.valueReader or tree.arrayReader

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        if event._tree._ttreereaderversion > self._ttreereaderversion: # do this check at every event, as other modules might have read further branches
            self.initReaders(event._tree)
        # do NOT access other branches in python between the check/call to initReaders and the call to C++ worker code
        #invoke function from C++ to compute, return 4/3-vectors per each physics quantities
        counter = self.worker.countEvent()
        #ptcorrection = self.worker.ptZCorr()

        #store
        self.out.fillBranch("MHTju_pt_counter", counter);
        #self.out.fillBranch("ZPtCorr", ptcorrection);
        
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

preselection = lambda : PreselectionerCpp()
