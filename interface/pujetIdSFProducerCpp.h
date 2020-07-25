#ifndef PhysicsTools_NanoAODTools_pujetIdSFProducerCpp_h
#define PhysicsTools_NanoAODTools_pujetIdSFProducerCpp_h

/*
  Temporary on-the-fly PU JetId SF calculator. Returns the product of SFs for all jets with pt > 30. && |eta| < 4.7
  taken from Davide
*/

#include "TSystem.h"
#include "TFile.h"
#include "TMath.h"
#include "TH1.h"

#include <string>
#include <unordered_map>
#include <iostream>
#include <vector>
#include <array>
#include <string>

#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>

class pujetIdSFProducerCpp {

public:
  
  pujetIdSFProducerCpp( char const* filename, char const* yr, char const* wp );
  ~pujetIdSFProducerCpp();
  double evaluate();
  
  void setVals(
	       TTreeReaderValue<unsigned> *nLepton_ ,
	       TTreeReaderValue<unsigned> *nJet_ ,
	       TTreeReaderArray<float> *Lepton_eta_ ,
	       TTreeReaderArray<float> *Lepton_phi_ ,
	       TTreeReaderArray<float> *Jet_pt_ ,
	       TTreeReaderArray<float> *Jet_eta_ ,
	       TTreeReaderArray<float> *Jet_phi_ ,
	       TTreeReaderArray<int> *Jet_jetId_ ,
	       TTreeReaderArray<int> *Jet_genJetIdx_ ,
               TTreeReaderArray<int> *Jet_puId_
	       ){
    nLepton = nLepton_ ; nJet = nJet_ ;
    Lepton_eta = Lepton_eta_ ; Lepton_phi = Lepton_phi_ ;
    Jet_pt = Jet_pt_ ; Jet_eta = Jet_eta_ ; Jet_phi = Jet_phi_ ;
    Jet_jetId = Jet_jetId_ ; Jet_genJetIdx = Jet_genJetIdx_ ; Jet_puId = Jet_puId_ ;
  };
  
 private:
  enum WP {
    kTight,
    kMedium,
    kLoose,
    nWPs
  };
  
  std::string filename_{};
  std::string wpStr_{};
  static std::string year;
  WP wp_{nWPs};
  
  TTreeReaderValue<unsigned> *nLepton = nullptr;
  TTreeReaderValue<unsigned> *nJet = nullptr;
  TTreeReaderArray<float> *Lepton_eta = nullptr;
  TTreeReaderArray<float> *Lepton_phi = nullptr;
  TTreeReaderArray<float> *Jet_pt = nullptr;
  TTreeReaderArray<float> *Jet_eta = nullptr;
  TTreeReaderArray<float> *Jet_phi = nullptr;
  TTreeReaderArray<int> *Jet_jetId = nullptr;
  TTreeReaderArray<int> *Jet_genJetIdx = nullptr;
  TTreeReaderArray<int> *Jet_puId = nullptr;

  typedef std::array<std::unique_ptr<TH1>, nWPs> MapSet;
  typedef std::array<MapSet, 2> MapSets;

  static MapSets sfMapSets;
  static MapSets effMapSets;
  
  static std::array<float, nWPs> scalefactors;  
};
#endif
