#ifndef PhysicsTools_NanoAODTools_producerCppWorker_h
#define PhysicsTools_NanoAODTools_producerCppWorker_h

#include <utility>
#include <algorithm>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <TMath.h>
#include <TLorentzVector.h>
#include <Python.h>
#include "TVector2.h"
#include "DataFormats/Math/interface/LorentzVector.h"

class producerCppWorker {

public:

  producerCppWorker(){}

  //Helper
  double deltaPhi(float v1, float v2)
  {
    float diff = fabs(v2 - v1);
    float corr = 2*acos(-1.) - diff;
    if (diff < acos(-1.))
      return diff;
    else
      return corr;
  }
  
  //Physics Objects Extraction Definition
  void setJets(TTreeReaderValue<unsigned> *nJet_, TTreeReaderArray<float> *Jet_pt_, TTreeReaderArray<float> *Jet_eta_, TTreeReaderArray<float> *Jet_phi_, TTreeReaderArray<float> *Jet_mass_){
    nJet = nJet_; Jet_pt = Jet_pt_; Jet_eta = Jet_eta_; Jet_phi = Jet_phi_; Jet_mass = Jet_mass_;
  }

  void setPFMET(TTreeReaderValue<float> *MET_phi_, TTreeReaderValue<float> *MET_pt_, TTreeReaderValue<float> *MET_sumEt_){
    MET_phi = MET_phi_; MET_pt = MET_pt_; MET_sumEt = MET_sumEt_;
  }

  void setCaloMET(TTreeReaderValue<float> *CaloMET_phi_, TTreeReaderValue<float> *CaloMET_pt_, TTreeReaderValue<float> *CaloMET_sumEt_ ){
    CaloMET_phi = CaloMET_phi_; CaloMET_pt = CaloMET_pt_; CaloMET_sumEt = CaloMET_sumEt_;
  }

  void setElectrons(TTreeReaderValue<unsigned> *nElectron_, TTreeReaderArray<float> *Electron_pt_, TTreeReaderArray<float> *Electron_eta_, TTreeReaderArray<float> *Electron_phi_, TTreeReaderArray<float> *Electron_mass_ ){
    nElectron = nElectron_; Electron_pt = Electron_pt_; Electron_eta = Electron_eta_; Electron_phi = Electron_phi_; Electron_mass = Electron_mass_;
  }

  void setMuons(TTreeReaderValue<unsigned> *nMuon_, TTreeReaderArray<float> *Muon_pt_, TTreeReaderArray<float> *Muon_eta_, TTreeReaderArray<float> *Muon_phi_, TTreeReaderArray<float> *Muon_mass_ ){
    nMuon = nMuon_; Muon_pt = Muon_pt_; Muon_eta = Muon_eta_; Muon_phi = Muon_phi_; Muon_mass = Muon_mass_; 
  }

  //Derived Variable Computation Function
  int countEvent();
  float getHadronicMET();
  std::pair<float,float> getHT();
  std::vector<double> getW();
  std::vector<double> getZ();
  std::vector<double> getJJ();
  std::vector<double> getJJL();
  float getDeltaPhiJetMET();

private:
  //variable pointers
  TTreeReaderValue<unsigned> *nJet = nullptr;
  TTreeReaderArray<float> *Jet_pt = nullptr;
  TTreeReaderArray<float> *Jet_eta = nullptr;
  TTreeReaderArray<float> *Jet_phi = nullptr;
  TTreeReaderArray<float> *Jet_mass = nullptr;

  TTreeReaderValue<float> *MET_phi = nullptr;
  TTreeReaderValue<float> *MET_pt = nullptr;
  TTreeReaderValue<float> *MET_sumEt = nullptr;

  TTreeReaderValue<float> *CaloMET_phi = nullptr;
  TTreeReaderValue<float> *CaloMET_pt = nullptr;
  TTreeReaderValue<float> *CaloMET_sumEt = nullptr;

  TTreeReaderValue<unsigned> *nElectron = nullptr;
  TTreeReaderArray<float> *Electron_pt = nullptr;
  TTreeReaderArray<float> *Electron_eta = nullptr;
  TTreeReaderArray<float> *Electron_phi = nullptr;
  TTreeReaderArray<float> *Electron_mass = nullptr;

  TTreeReaderValue<unsigned> *nMuon = nullptr;
  TTreeReaderArray<float> *Muon_pt = nullptr;
  TTreeReaderArray<float> *Muon_eta = nullptr;
  TTreeReaderArray<float> *Muon_phi = nullptr;
  TTreeReaderArray<float> *Muon_mass = nullptr;
};

#endif
