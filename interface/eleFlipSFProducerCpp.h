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
#include "Math/VectorUtil.h"
//#include "DataFormats/Math/interface/LorentzVector.h"

typedef std::map<std::string, std::map<std::string, std::map<std::string, std::map<std::string, std::list<std::string>>>>> nested_dict;

class eleFlipSFProducerCpp {

public:
  eleFlipSFProducerCpp( const char* year, const char* wp );
  std::pair<double,double> evaluate();
  
  void setVals(
	       TTreeReaderValue<unsigned> *nLepton_ ,
	       TTreeReaderArray<float> *Lepton_pt_ ,
	       TTreeReaderArray<float> *Lepton_eta_ ,
	       TTreeReaderArray<float> *Lepton_phi_ ,
	       TTreeReaderArray<int> *Lepton_pdgId_ ,
	       TTreeReaderValue<unsigned> *nLeptonGen_ ,
               TTreeReaderArray<float> *LeptonGen_pt_ ,
               TTreeReaderArray<float> *LeptonGen_eta_ ,
               TTreeReaderArray<float> *LeptonGen_phi_ ,
               TTreeReaderArray<int> *LeptonGen_pdgId_
	       ){
    nLepton = nLepton_; Lepton_pt = Lepton_pt_; Lepton_eta = Lepton_eta_; Lepton_phi = Lepton_phi_; Lepton_pdgId = Lepton_pdgId_;
    nLeptonGen = nLeptonGen_; LeptonGen_pt = LeptonGen_pt_; LeptonGen_eta = LeptonGen_eta_; LeptonGen_phi = LeptonGen_phi_; LeptonGen_pdgId = LeptonGen_pdgId_;
  };
  
 private:
  const char* working_point_;
  const char* year_;

  TTreeReaderValue<unsigned> *nLepton = nullptr;
  TTreeReaderArray<float> *Lepton_pt = nullptr;
  TTreeReaderArray<float> *Lepton_eta = nullptr;
  TTreeReaderArray<float> *Lepton_phi = nullptr;
  TTreeReaderArray<int>	*Lepton_pdgId = nullptr;
  TTreeReaderValue<unsigned> *nLeptonGen = nullptr;
  TTreeReaderArray<float> *LeptonGen_pt = nullptr;
  TTreeReaderArray<float> *LeptonGen_eta = nullptr;
  TTreeReaderArray<float> *LeptonGen_phi = nullptr;
  TTreeReaderArray<int> *LeptonGen_pdgId = nullptr;

  nested_dict SF_files_map_;
  std::map<const std::string,TH2D*> SFmap;

  void loadHist( std::list<std::string> SF_files_map_in );
  double GetSF( double pt , double eta );
  double chargeflip( double pt , double eta );

};
#endif
