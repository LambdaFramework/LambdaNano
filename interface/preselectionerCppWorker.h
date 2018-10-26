#ifndef PhysicsTools_NanoAODTools_preselectionerCppWorker_h
#define PhysicsTools_NanoAODTools_preselectionerCppWorker_h

#include <utility>
#include <algorithm>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <TMath.h>
#include <TLorentzVector.h>
#include <Python.h>
#include "TVector2.h"
#include "DataFormats/Math/interface/LorentzVector.h"

class preselectionerCppWorker {

public:

  preselectionerCppWorker(){}

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
  void setMHTju(TTreeReaderValue<float> *MHTju_pt_, TTreeReaderValue<float> *MHTju_phi_){
    MHTju_pt = MHTju_pt_; MHTju_phi = MHTju_phi_;
  }
  void setGen(TTreeReaderValue<unsigned> *nGenPart_, TTreeReaderArray<float> *GenPart_pt_, TTreeReaderArray<int> *GenPart_pdgId_){
    nGenPart = nGenPart_; GenPart_pt = GenPart_pt_; GenPart_pdgId = GenPart_pdgId_;
  }

  //Derived Variable Computation Function
  int countEvent();
  //ptZ dependent correction
  float ptZCorr();

private:
  //variable pointers
  TTreeReaderValue<float> *MHTju_pt = nullptr;
  TTreeReaderValue<float> *MHTju_phi = nullptr;
  TTreeReaderValue<unsigned> *nGenPart = nullptr;
  TTreeReaderArray<float> *GenPart_pt = nullptr;
  TTreeReaderArray<int> *GenPart_pdgId = nullptr;
};

#endif
