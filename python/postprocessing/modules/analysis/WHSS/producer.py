import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class whssProducer(Module):
    def __init__( self, jetSelection , eleSelection , muonSelection ):
        self.jetSel  = jetSelection
        self.eleSel  = eleSelection
	self.muonSel = muonSelection
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("EventMass",  "F");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        eventSum = ROOT.TLorentzVector()
        
        for lep in muons :
            eventSum += lep.p4()
        for lep in electrons :
            eventSum += lep.p4()
        for j in filter(self.jetSel,jets):
            eventSum += j.p4()
        self.out.fillBranch("EventMass",eventSum.M())
        return True

whssConstr = lambda : whssProducer(
    jetSelection = lambda j : j.pt > 30,
    eleSelection = lambda e : e.pt > 10,
    muonSelection = lambda u : u.pt > 10
)
