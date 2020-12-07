#include "../interface/eleFlipSFProducerCpp.h"

//constructor
eleFlipSFProducerCpp::eleFlipSFProducerCpp( const char* year, const char* wp ){

  working_point_ = wp ;
  year_ = year;

  std::cout<<std::endl;
  std::cout<<" worker::eleFlipSFProducerCpp --> configuration" <<std::endl;
  std::cout<<" worker::eleFlipSFProducerCpp::year_ : "<< year_ <<std::endl;
  std::cout<<" worker::eleFlipSFProducerCpp::working_point_ : "<< working_point_ <<std::endl;
  std::cout<<std::endl;
  //
  nested_dict SF_files_map;
  std::string base = std::getenv("NANOAODTOOLS_BASE") ;

  // HWW_WP
  SF_files_map["electron"]["HWW_WP"]["2016"]["flipper"] = { base + "/python/postprocessing/data/scale_factor/chargeFlip/HWW_WP/chargeFlip_nanov5_2016_SF.root" } ;
  SF_files_map["electron"]["HWW_WP"]["2017"]["flipper"] = { base + "/python/postprocessing/data/scale_factor/chargeFlip/HWW_WP/chargeFlip_nanov5_2017_SF.root" } ;
  SF_files_map["electron"]["HWW_WP"]["2018"]["flipper"] = { base + "/python/postprocessing/data/scale_factor/chargeFlip/HWW_WP/chargeFlip_nanov5_2018_SF.root" } ;

  // HWW_tthMVA_WP
  SF_files_map["electron"]["HWW_tthMVA_WP"]["2016"]["flipper"] = { base + "/python/postprocessing/data/scale_factor/chargeFlip/HWW_tthMVA_WP/chargeFlip_nanov5_2016_SF.root" } ;
  SF_files_map["electron"]["HWW_tthMVA_WP"]["2017"]["flipper"] = { base + "/python/postprocessing/data/scale_factor/chargeFlip/HWW_tthMVA_WP/chargeFlip_nanov5_2017_SF.root" } ;
  SF_files_map["electron"]["HWW_tthMVA_WP"]["2018"]["flipper"] = { base + "/python/postprocessing/data/scale_factor/chargeFlip/HWW_tthMVA_WP/chargeFlip_nanov5_2018_SF.root" } ;
  
  SF_files_map_ = SF_files_map;

  loadHist( SF_files_map_["electron"][working_point_][year_]["flipper"] );
}

void eleFlipSFProducerCpp::loadHist( std::list<std::string> SF_files_map_in ) {

  TFile f( SF_files_map_in.front().c_str() );

  //TH2D *h_mc       = (TH2D*) f.Get("mc")->Clone();
  //TH2D *h_mc_sys   = (TH2D*) f.Get("mc_sys")->Clone();
  TH2D *h_data     = (TH2D*) f.Get("data")->Clone();                                                                                                                                                             
  //TH2D *h_data_sys = (TH2D*) f.Get("data_sys")->Clone();
  TH2D *h_sf       = (TH2D*) f.Get("sf")->Clone(); 
  //TH2D *h_sf_sys   = (TH2D*) f.Get("sf_sys")->Clone();

  //h_mc->SetDirectory(0); h_mc_sys->SetDirectory(0);
  h_data->SetDirectory(0); //h_data_sys->SetDirectory(0);
  h_sf->SetDirectory(0); //h_sf_sys->SetDirectory(0);

  //SFmap.insert(std::make_pair( "mc"       , h_mc       )); 
  //SFmap.insert(std::make_pair( "mc_sys"   , h_mc_sys   ));
  SFmap.insert(std::make_pair( "data"     , h_data     ));                                                                                                                                                       
  //SFmap.insert(std::make_pair( "data_sys" , h_data_sys ));
  SFmap.insert(std::make_pair( "sf"       , h_sf       ));                                                                                                                                                       
  //SFmap.insert(std::make_pair( "sf_sys"   , h_sf_sys   ));
  
  std::cout<<"loaded 2D map : "<< SF_files_map_in.front() <<std::endl;
  
}

double eleFlipSFProducerCpp::GetSF( double pt , double eta ){

  double eta_temp = eta;
  double pt_temp = pt;
  
  double eta_max = 2.49;
  double eta_min = -2.5;
  double pt_max = 199.;
  double pt_min = 25.;
  
  double SF = 1.;

  if(eta_temp < eta_min){eta_temp = eta_min;}
  if(eta_temp > eta_max){eta_temp = eta_max;}
  if(pt_temp < pt_min){pt_temp = pt_min;}
  if(pt_temp > pt_max){pt_temp = pt_max;}
  
  SF = SFmap["sf"]->GetBinContent(SFmap["sf"]->FindBin( TMath::Abs(eta_temp) , pt_temp ) );

  return SF;
}

double eleFlipSFProducerCpp::chargeflip( double pt , double eta ){

  double eta_temp = eta;
  double pt_temp = pt;
  
  double eta_max = 2.49;
  double eta_min = -2.5;
  double pt_max = 199.;
  double pt_min = 25.;

  double frate = 0.;
  
  if(eta_temp < eta_min){eta_temp = eta_min;}
  if(eta_temp > eta_max){eta_temp = eta_max;}
  if(pt_temp < pt_min){pt_temp = pt_min;}
  if(pt_temp > pt_max){pt_temp = pt_max;}

  frate = SFmap["data"]->GetBinContent(SFmap["data"]->FindBin( TMath::Abs(eta_temp) , pt_temp ) );

  return frate;
}

std::pair<double,double> eleFlipSFProducerCpp::evaluate(){
  
  double epsilon1 = 0.; double epsilon2 = 0.; double sf1 = 1. ; double sf2 = 1.;
  unsigned nlepton = (*nLepton).Get()[0]; //unsigned nGenLepton = (*nLeptonGen).Get()[0];
  
  // return 1
  if ( nlepton < 2 ) return std::make_pair( 0. , 0. );
  
  if (TMath::Abs(Lepton_pdgId->At(0)) == 11) {
    epsilon1 = chargeflip( Lepton_pt->At(0) , Lepton_eta->At(0) );
    sf1 = GetSF( Lepton_pt->At(0) , Lepton_eta->At(0) );
  }
  if (TMath::Abs(Lepton_pdgId->At(1)) == 11) {
    epsilon2 = chargeflip( Lepton_pt->At(1) , Lepton_eta->At(1) );
    sf2 = GetSF( Lepton_pt->At(1) , Lepton_eta->At(1) );
  }

  double CommonW = epsilon1 * ( 1. - epsilon2 ) + ( 1. - epsilon1 ) * epsilon2;
  double sf = sf1 * sf2;
  
  return std::make_pair( CommonW , sf );
}

