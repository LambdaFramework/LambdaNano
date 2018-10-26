import ROOT
import os
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class ProducerCpp(Module): # MHT producer, unclean jets only (no lepton overlap cleaning, no jet selection)
    def __init__(self):
        if "/producerCppWorker_cc.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ producerCppWorker worker module"
            base = os.getenv("NANOAODTOOLS_BASE")
            if base:
                ROOT.gROOT.ProcessLine(".L %s/src/producerCppWorker.cc+O"%base)
            else:
                base = "%s/src/PhysicsTools/NanoAODTools"%os.getenv("CMSSW_BASE")
                ROOT.gSystem.Load("libPhysicsToolsNanoAODTools.so")
                ROOT.gROOT.ProcessLine(".L %s/interface/producerCppWorker.h"%base)
        self.worker = ROOT.producerCppWorker()
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.initReaders(inputTree) # initReaders must be called in beginFile
        self.out = wrappedOutputTree
        #Book histogram
        self.out.branch("nnEvents", "I")
        self.out.branch("hadronicRecoil",  "F");
        self.out.branch("TMW",  "F");
        self.out.branch("Z_pt",  "F");
        self.out.branch("Z_eta",  "F");
        self.out.branch("Z_phi",  "F");
        self.out.branch("Z_mass",  "F");
        self.out.branch("JJ_pt",  "F");
        self.out.branch("JJ_eta",  "F");
        self.out.branch("JJ_phi",  "F");
        self.out.branch("JJ_mass",  "F");
        self.out.branch("JJL_pt",  "F");
        self.out.branch("JJL_eta",  "F");
        self.out.branch("JJL_phi",  "F");
        self.out.branch("JJL_mass",  "F");
        self.out.branch("DeltaPhiJetMET",  "F");

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def initReaders(self,tree): # this function gets the pointers to Value and ArrayReaders and sets them in the C++ worker class
        #assign/extract pointers to Value and Array
        #Jet
        self.nJet = tree.valueReader("nJet")
        self.Jet_pt = tree.arrayReader("Jet_pt")
        self.Jet_eta = tree.arrayReader("Jet_eta")
        self.Jet_phi = tree.arrayReader("Jet_phi")
        self.Jet_mass = tree.arrayReader("Jet_mass")
        #PFMET
        self.MET_phi = tree.valueReader("MET_phi")
        self.MET_pt = tree.valueReader("MET_pt")
        self.MET_sumEt = tree.valueReader("MET_sumEt")
        #CaloMET
        self.CaloMET_phi = tree.valueReader("CaloMET_phi")
        self.CaloMET_pt = tree.valueReader("CaloMET_pt")
        self.CaloMET_sumEt = tree.valueReader("CaloMET_sumEt")
        #Electron
        self.nElectron = tree.valueReader("nElectron")
        self.Electron_pt = tree.arrayReader("Electron_pt")
        self.Electron_eta = tree.arrayReader("Electron_eta")
        self.Electron_phi = tree.arrayReader("Electron_phi")
        self.Electron_mass = tree.arrayReader("Electron_mass")
        #self.Electron_charge = tree.arrayReader("Electron_charge")
        #self.Electron_cutBased = tree.arrayReader("Electron_cutBased")
        #self.Electron_genPartFlav = tree.arrayReader("Electron_genPartFlav")
        #self.Electron_pdgId = tree.arrayReader("Electron_pdgId")
        #self.Electron_pfRelIso03_all = tree.arrayReader("Electron_pfRelIso03_all")
        #self.Electron_pfRelIso03_chg = tree.arrayReader("Electron_pfRelIso03_chg")
        #Muon                                            
        self.nMuon = tree.valueReader("nMuon")
        self.Muon_pt = tree.arrayReader("Muon_pt")
        self.Muon_eta = tree.arrayReader("Muon_eta")
        self.Muon_phi = tree.arrayReader("Muon_phi")
        self.Muon_mass = tree.arrayReader("Muon_mass") 
        #self.Muon_charge = tree.arrayReader("Muon_charge")
        #self.Muon_genPartFlav = tree.arrayReader("Muon_genPartFlav")
        #self.Muon_pdgId = tree.arrayReader("Muon_pdgId")
        #self.Muon_pfRelIso03_all = tree.arrayReader("Muon_pfRelIso03_all")
        #self.Muon_pfRelIso03_chg = tree.arrayReader("Muon_pfRelIso03_chg")
        #self.Muon_pfRelIso04_all = tree.arrayReader("Muon_pfRelIso04_all")
        #self.Muon_softId = tree.arrayReader("Muon_softId")
        #self.Muon_tightCharge = tree.arrayReader("Muon_tightCharge")
        #self.Muon_tightId = tree.arrayReader("Muon_tightId")

        #set in C++ worker class
        self.worker.setJets(self.nJet,self.Jet_pt,self.Jet_eta,self.Jet_phi,self.Jet_mass)
        self.worker.setPFMET(self.MET_phi,self.MET_pt,self.MET_sumEt)
        self.worker.setCaloMET(self.CaloMET_phi,self.CaloMET_pt,self.CaloMET_sumEt)
        self.worker.setElectrons(self.nElectron,self.Electron_pt,self.Electron_eta,self.Electron_phi,self.Electron_mass)
        self.worker.setMuons(self.nMuon,self.Muon_pt,self.Muon_eta,self.Muon_phi,self.Muon_mass)

        self._ttreereaderversion = tree._ttreereaderversion # self._ttreereaderversion must be set AFTER all calls to tree.valueReader or tree.arrayReader

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        if event._tree._ttreereaderversion > self._ttreereaderversion: # do this check at every event, as other modules might have read further branches
            self.initReaders(event._tree)
        # do NOT access other branches in python between the check/call to initReaders and the call to C++ worker code
        #invoke function from C++ to compute, return 4/3-vectors per each physics quantities
        #output = self.worker.getHT()
        counter = self.worker.countEvent()
        hadronicMET = self.worker.getHadronicMET()
        #Woutput = self.worker.getW()
        Zoutput = self.worker.getZ()
        JJoutput = self.worker.getJJ()
        JJLoutput = self.worker.getJJL()
        dphiJMoutput = self.worker.getDeltaPhiJetMET()
        
        #store
        self.out.fillBranch("nnEvents", counter);
        self.out.fillBranch("hadronicRecoil", hadronicMET);
        #self.out.fillBranch("TMW",  Woutput[0]);
        self.out.fillBranch("Z_pt",  Zoutput[0]);
        self.out.fillBranch("Z_eta",  Zoutput[1]);
        self.out.fillBranch("Z_phi",  Zoutput[2]);
        self.out.fillBranch("Z_mass",  Zoutput[3]);
        self.out.fillBranch("JJ_pt",  JJoutput[0]);
        self.out.fillBranch("JJ_eta",  JJoutput[1]);
        self.out.fillBranch("JJ_phi",  JJoutput[2]);
        self.out.fillBranch("JJ_mass",  JJoutput[3]);
        self.out.fillBranch("JJL_pt",  JJLoutput[0]);
        self.out.fillBranch("JJL_eta",  JJLoutput[1]);
        self.out.fillBranch("JJL_phi",  JJLoutput[2]);
        self.out.fillBranch("JJL_mass",  JJLoutput[3]);
        self.out.fillBranch("DeltaPhiJetMET", dphiJMoutput);
      
        #self.out.fillBranch("MHTju_pt", output[0])
        #self.out.fillBranch("MHTju_phi", -output[1]) # note the minus
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

producer = lambda : ProducerCpp()
