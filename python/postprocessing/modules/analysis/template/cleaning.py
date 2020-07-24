import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import sys
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
#from PhysicsTools.NanoAODTools.postprocessing.helper.anaFunc import *
from PhysicsTools.NanoAODTools.postprocessing.helpers.tools import deltaPhi, deltaR, closest
from math import fabs

class Cleaning(Module):
    def __init__(self, jetSelection, muonSelection, electronSelection, tauselection, debug=False):
        self.jetSel = jetSelection
        self.muSel = muonSelection
        self.elSel = electronSelection
        self.tauSel = tauselection
        self.DEBUG = debug
        self.nevent = 0
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Jet_isClean", "I", lenVar="nJet")
        self.out.branch("Muon_isClean", "I", lenVar="nMuon")
        self.out.branch("Electron_isClean", "I", lenVar="nElectron")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        self.nevent+=1
        njet=-999.
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        tau = Collection(event, "Tau")
        jets = Collection(event, "Jet")
        #vector must be same length with n(Objects)
        goodjet = [ 1 for i in xrange(event.nJet) ]
        goodmuon = [ 1 for i in xrange(event.nMuon) ]
        goodelectron = [ 1 for i in xrange(event.nElectron) ]

        #JetList  = map(lambda ev: ev, jets) #self.jetSel
        #MuonList = map(lambda ev: ev, muons)
        #ElecList = map(lambda ev: ev, electrons)

        JetList  = filter(self.jetSel, jets)
        MuonList = filter(self.muSel, muons)
        ElecList = filter(self.elSel, electrons)

        for ilep in  MuonList+ElecList:
            for ijet in JetList:
                if deltaR(ijet,ilep)<0.4:
                    if ilep._prefix.split('_')[0]=="Muon":
                        if self.muSel(ilep):
                            if ijet.chHEF>0.1 or ijet.neHEF>0.2:
                                goodmuon[ilep._index]=0
                                break
                            else:
                                goodjet[ijet._index] = 0
                        elif not self.muSel(ilep):
                            goodjet[ijet._index] = 0
                    elif ilep._prefix.split('_')[0]=="Electron":
                        if self.elSel(ilep):
                            if ijet.chHEF>0.1 or ijet.neHEF>0.2:
                                goodelectron[ilep._index]=0
                                break
                            else:
                                 goodjet[ijet._index] = 0
                        elif not self.elSel(ilep):
                            goodjet[ijet._index] = 0

        '''
        for ilep in MuonList+ElecList:
            for ijet in JetList:
                ## MATCHED with Lepton
                if deltaR(ijet,ilep)<0.4:
                    #MUON
                    if ilep._prefix.split('_')[0]=="Muon":
                        if not self.muSel(ilep):
                            goodmuon[ilep._index]=0                     # NO GOOD MUON INSIDE JET ; ACCEPT JET
                        elif self.muSel(ilep):
                            if ijet.chHEF>0.1 or ijet.neHEF>0.2:
                                goodmuon[ilep._index]=0                 # GOOD MUON INSIDE JET ; within acceptable Energy Fraction ; ACCEPT JET
                            else:
                                goodjet[ijet._index] = 0                # GOOD MUON INSIDE JET ; REJECT JET
                    #ELECTRON
                    elif ilep._prefix.split('_')[0]=="Electron":
                        if not self.elSel(ilep):
                            goodelectron[ilep._index]=0                 # NO GOOD ELECTRON INSIDE JET ; ACCEPT JET
                        elif self.elSel(ilep):
                            if ijet.chHEF>0.1 or ijet.neHEF>0.2:
                                goodelectron[ilep._index]=0             # GOOD ELECTRON INSIDE JET ; within acceptable Energy Fraction ; ACCEPT JET
                            else:
                                goodjet[ijet._index] = 0                # GOOD ELECTRON INSIDE JET; REJECT JET
                                '''
        if self.DEBUG:
            print "================== EVENT ", self.nevent, " =================="
            print "================== NEW Clean Flag =================="
            print " goodjet  : ", goodjet
            print " goodmuon : ", goodmuon
            print " goodelec : ", goodelectron
            print "================== END EVENT ==================="
            print ""

        ## Fill ##
        self.out.fillBranch("Jet_isClean", goodjet)
        self.out.fillBranch("Muon_isClean", goodmuon)
        self.out.fillBranch("Electron_isClean", goodelectron)
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
cleaning = lambda : Cleaning(
    #JET SELECTED FOR MHT COMPUTATION , je.jetId>0
    jetSelection      = lambda je : je.pt>30 and fabs(je.eta)<2.5 and je.puId>4 and je.jetId>0,
    #GOOD MUON DEFINITION
    muonSelection     = lambda mu : mu.pt>5  and fabs(mu.eta)<2.4 and mu.mediumId > 0,
    #GOOD ELECTRON DEFINITION
    electronSelection = lambda el : el.pt>15 and fabs(el.eta)<2.4 and el.cutBased > 0,
    tauselection      = lambda tau : tau,
    debug             = False,
    )

##puId
#https://twiki.cern.ch/twiki/bin/viewauth/CMS/PileupJetID?rev=37
#https://gitlab.cern.ch/shoh/reference/blob/master/definitions/Moriond17.md#24-jet

##JetId
# Jet ID flags bit1 is loose, bit2 is tight

##Recommendation of jet
#https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVRun2016

###NOTE
#Preliminarly, some (loose) quality requirements on the nanoAOD objects are defined:
#
#- all muons satisfy the quality criterium on the nanoAOD variable:
#
#   Muon_mediumId[jmu] > 0
#
#- all electrons satisfy the quality criterium on the nanoAOD variable:
#
#   Electron_cutBased[jele] > 0
#
#- "clean" jets will be used (WARNING: in the current nanoAOD implementation, essentially all the high pT
#muons and/or electrons appear also in the jet list...these must be skipped, for instance, in
#the HT computation).  "Clean jets" are defined requiring:
#
# - Jet_puId[jet] > 4 AND
#
#    - either no good electrons (muons) with pT> 15 (5) GeV within a cone DR <0.4 around the jet
#
#      OR
#
#    - if a good electron/muon (passing the quality criterium stated above) near the jet is found:
#         -  Jet_chHEF[jet] > 0.1 OR  Jet_neHEF[jet] > 0.2
#
#
#- HT is computed summing up the pT of all "clean" jets with pT>30, |eta|< 2.5
