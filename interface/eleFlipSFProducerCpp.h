#ifndef PhysicsTools_NanoAODTools_eleFlipSFProducerCpp_h
#define PhysicsTools_NanoAODTools_eleFlipSFProducerCpp_h

#include <utility>
#include <vector>
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include <iostream>
#include <TMath.h>
#include <TFile.h>
#include <TH2D.h>
#include <cstdlib>
#include <string>
#include <map>
#include <tuple>
#include <iterator>
#include <sstream>
#include <fstream>
#include <string.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
//#include "DataFormats/Math/interface/LorentzVector.h"

typedef std::map<std::string, std::map<std::string, std::map<std::string, std::map<std::string, std::list<std::string>>>>> nested_dict;

class eleFlipSFProducerCpp {

public:
  
  eleFlipSFProducerCpp(const char* year, const unsigned int nLeptons, std::string requested_SF, const unsigned int requested_lepton=0);
  double evaluate();
  
  void setVals(
	       TTreeReaderValue<unsigned> *nLepton_ ,
	       TTreeReaderArray<float> *Lepton_pt_ ,
	       TTreeReaderArray<float> *Lepton_eta_ ,
	       TTreeReaderArray<int> *Lepton_pdgId_
	       ){
    nLepton = nLepton_; Lepton_pt = Lepton_pt_; Lepton_eta = Lepton_eta_; Lepton_pdgId = Lepton_pdgId_;
  };
  
 private:
  unsigned int nLeptons_;
  const char* working_point_;
  const char* year_;
  std::string requested_SF_;
  unsigned int requested_lepton_;

  TTreeReaderValue<unsigned> *nLepton = nullptr;
  TTreeReaderArray<float> *Lepton_pt = nullptr;
  TTreeReaderArray<float> *Lepton_eta = nullptr;
  TTreeReaderArray<int>	*Lepton_pdgId = nullptr;

  nested_dict SF_files_map_;
  std::map<const std::string,TH2D*> SFmap;

  void loadHist( std::list<std::string> SF_files_map_in );
  double GetSF( double eta, double pt , std::string key );
  
  // store in memory
  //std::vector<TH2D> h_SF_ele_;
  
};
#endif
