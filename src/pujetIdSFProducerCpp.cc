#include "../interface/pujetIdSFProducerCpp.h"

std::string pujetIdSFProducerCpp::year{""};
pujetIdSFProducerCpp::MapSets pujetIdSFProducerCpp::effMapSets{};
pujetIdSFProducerCpp::MapSets pujetIdSFProducerCpp::sfMapSets{};
std::array<float, pujetIdSFProducerCpp::nWPs> pujetIdSFProducerCpp::scalefactors{};

//constructor
pujetIdSFProducerCpp::pujetIdSFProducerCpp( char const* filename, char const* yr, char const* wp ) :
  filename_ {filename},
  wpStr_{wp}
{
  if (wpStr_ == "loose")
    wp_ = kLoose;
  else if (wpStr_ == "medium")
    wp_ = kMedium;
  else if (wpStr_ == "tight")
    wp_ = kTight;
  else
    throw std::runtime_error("unknown working point " + wpStr_);
  
  if (year.size() == 0)
    year = yr;
  else if (year != yr)
    throw std::runtime_error("PUJetIdEventSF already set up for " + year);
  
  std::cout<<std::endl;
  std::cout<<" worker::pujetIdSFProducerCpp --> configuration" <<std::endl;
  std::cout<<" worker::pujetIdSFProducerCpp::filename_ : "<< filename_ <<std::endl;
  std::cout<<" worker::pujetIdSFProducerCpp::year_ : "<< year <<std::endl;
  std::cout<<" worker::pujetIdSFProducerCpp::wp_ : "<< wp_ <<std::endl;
  std::cout<<std::endl;

  auto* source{TFile::Open(filename_.c_str())};

  // Same order of bit to check the Jetid 
  std::string wps[nWPs] = {"T", "M", "L"};
  for (unsigned iwp{0}; iwp != nWPs; ++iwp) {
    effMapSets[0][iwp].reset(static_cast<TH1*>(source->Get(("h2_eff_mc"+year +"_" + wps[iwp]).c_str())));
    effMapSets[1][iwp].reset(static_cast<TH1*>(source->Get(("h2_mistag_mc"+year +"_" + wps[iwp]).c_str())));
    effMapSets[0][iwp]->SetDirectory(nullptr);
    effMapSets[1][iwp]->SetDirectory(nullptr);
    sfMapSets[0][iwp].reset(static_cast<TH1*>(source->Get(("h2_eff_sf"+year +"_" + wps[iwp]).c_str())));
    sfMapSets[1][iwp].reset(static_cast<TH1*>(source->Get(("h2_mistag_sf"+year +"_" + wps[iwp]).c_str())));
    sfMapSets[0][iwp]->SetDirectory(nullptr);
    sfMapSets[1][iwp]->SetDirectory(nullptr);
  }
  
}

pujetIdSFProducerCpp::~pujetIdSFProducerCpp(){
  for (auto& sms : sfMapSets) {
    for (auto& sfMap : sms)
      sfMap.reset();
  }
  for (auto& sms : effMapSets) {
    for (auto& efMap : sms)
      efMap.reset();
  }
}

double pujetIdSFProducerCpp::evaluate() {

  std::fill_n(scalefactors.begin(), nWPs, 1.);

  unsigned nJ{*nJet->Get()};

  for (unsigned iJ{0}; iJ != nJ; ++iJ) {
    double pt{Jet_pt->At(iJ)};
    double eta{Jet_eta->At(iJ)};

    if (pt < 30. || pt > 50.|| std::abs(eta) > 4.7 || Jet_jetId->At(iJ)<2)
    // excluding also the jets with jetId < 2 since we are considering only these jets in the selection before PUid selection.
      continue;

    bool isLeptonMatched = false;
    for (unsigned int ilep = 0; ilep < *(nLepton->Get()); ilep++){
      float lepEta = Lepton_eta->At(ilep);
      float lepPhi = Lepton_phi->At(ilep);
      float jetEta = Jet_eta->At(iJ);
      float jetPhi = Jet_phi->At(iJ);
      float dPhi = abs(lepPhi - jetPhi);
      if (dPhi > TMath::Pi())  
        dPhi = 2*TMath::Pi() - dPhi;

      float dR2 = (lepEta - jetEta) * (lepEta - jetEta) + dPhi * dPhi;
      
      if (dR2 < 0.3*0.3)  isLeptonMatched =true;
    }
    if (isLeptonMatched) continue;

    unsigned mapType{};
    if (Jet_genJetIdx->At(iJ) != -1)
      mapType = 0;
    else
      mapType = 1;

    for (unsigned iWP{0}; iWP != nWPs; ++iWP) {
      // if mapTap = 0 efficiency h2 are used, if mapType = 1 mistag h2 are used
      auto& sf_map{sfMapSets[mapType][iWP]};
      auto& eff_map{effMapSets[mapType][iWP]};

      int iX{eff_map->GetXaxis()->FindFixBin(pt)};
      if (iX == 0)
        iX = 1;
      else if (iX > eff_map->GetNbinsX())
        iX = eff_map->GetNbinsX();

      int iY{eff_map->GetYaxis()->FindFixBin(eta)};
      if (iY == 0)
        iY = 1;
      else if (iY > eff_map->GetNbinsY())
        iY = eff_map->GetNbinsY();
      
      // iWP = 0 Tight, 1 Medium, 2 Loose 
      bool passId = ( Jet_puId->At(iJ) ) & ( 1 << iWP );
      if (passId)  scalefactors[iWP] *= (sf_map->GetBinContent(iX, iY));
      else         
	scalefactors[iWP] *= (1- sf_map->GetBinContent(iX, iY)*eff_map->GetBinContent(iX,iY)) / (1-eff_map->GetBinContent(iX,iY));
    }
  }
  //cout << "SF T-M-L: "<< scalefactors[0] << " "<<scalefactors[1] << " "<<scalefactors[2] << endl;

  return scalefactors[wp_];
}
