#ifndef PhysicsTools_NanoAODTools_lepSFProducerCpp_h
#define PhysicsTools_NanoAODTools_lepSFProducerCpp_h

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

class lepSFProducerCpp {

public:
  
  lepSFProducerCpp(const char* year, const unsigned int nLeptons, std::string requested_SF, const bool ele_SS , const unsigned int requested_lepton=0);
  double evaluate();
  
  void setVals(
	       TTreeReaderValue<unsigned> *nLepton_ ,
	       TTreeReaderArray<float> *Lepton_pt_ ,
	       TTreeReaderArray<float> *Lepton_eta_ ,
	       TTreeReaderArray<int> *Lepton_pdgId_ ,
	       TTreeReaderValue<int>	*run_period_ ,
	       TTreeReaderArray<float> *Lepton_RecoSF_ ,
	       TTreeReaderArray<float> *Lepton_RecoSF_Up_ ,
	       TTreeReaderArray<float> *Lepton_RecoSF_Down_
	       ){
    nLepton = nLepton_; Lepton_pt = Lepton_pt_; Lepton_eta = Lepton_eta_; Lepton_pdgId = Lepton_pdgId_; run_period = run_period_;
    Lepton_RecoSF = Lepton_RecoSF_; Lepton_RecoSF_Up = Lepton_RecoSF_Up_; Lepton_RecoSF_Down = Lepton_RecoSF_Down_;
  };
  
 private:
  unsigned int nLeptons_;
  const char* working_point_;
  const char* working_point_ele_;
  const char* year_;
  std::string requested_SF_;
  unsigned int requested_lepton_;

  TTreeReaderValue<unsigned> *nLepton = nullptr;
  TTreeReaderArray<float> *Lepton_pt = nullptr;
  TTreeReaderArray<float> *Lepton_eta = nullptr;
  TTreeReaderArray<int>	*Lepton_pdgId = nullptr;
  TTreeReaderValue<int> *run_period = nullptr;
  TTreeReaderArray<float> *Lepton_RecoSF = nullptr;
  TTreeReaderArray<float> *Lepton_RecoSF_Up = nullptr;
  TTreeReaderArray<float> *Lepton_RecoSF_Down = nullptr;

  nested_dict SF_files_map_;
  
  void makeSF_ele ( std::list<std::string> SF_files_map_in , std::vector<TH2D> &sf_nom , std::vector<TH2D> &sf_stat , std::vector<TH2D> &sf_syst );
  void makeSF_muon( std::list<std::string> SF_files_map_in , std::vector<TH2D> &sf_nom , std::vector<TH2D> &sf_stat , std::vector<TH2D> &sf_syst , std::string histname );
  void makeSF_muon_tthMVA( std::pair< std::list<std::string> , std::list<std::string> > SF_files_map_in , std::vector<TH2D> &sf_nom , std::vector<TH2D> &sf_stat , std::vector<TH2D> &sf_syst , std::string histname );  
  std::tuple<double, double, double> GetSF(int flavor, double eta, double pt, int run_period=0, std::string type = "");
  
  // store in memory
  std::vector<TH2D> h_SF_ele_;
  std::vector<TH2D> h_SF_ele_err_;
  std::vector<TH2D> h_SF_ele_sys_;
  std::vector<TH2D> h_SF_ele_ttHMVA_;
  std::vector<TH2D> h_SF_ele_ttHMVA_err_;
  std::vector<TH2D> h_SF_ele_ttHMVA_sys_;
  std::vector<TH2D> h_SF_mu_Id_;
  std::vector<TH2D> h_SF_mu_Id_err_;
  std::vector<TH2D> h_SF_mu_Id_sys_;
  std::vector<TH2D> h_SF_mu_Iso_;
  std::vector<TH2D> h_SF_mu_Iso_err_;
  std::vector<TH2D> h_SF_mu_Iso_sys_;
  std::vector<TH2D> h_SF_mu_ttHMVA_;
  std::vector<TH2D> h_SF_mu_ttHMVA_err_;
  std::vector<TH2D> h_SF_mu_ttHMVA_sys_;

  // SS electron
  //std::vector<TH2D> h_SF_ele_SS_;
  //std::vector<TH2D> h_SF_ele_SS_err_;
  //std::vector<TH2D> h_SF_ele_SS_sys_;
  //std::vector<TH2D> h_SF_ele_ttHMVA_SS_;
  //std::vector<TH2D> h_SF_ele_ttHMVA_SS_err_;
  //std::vector<TH2D> h_SF_ele_ttHMVA_SS_sys_;
  
};
#endif
