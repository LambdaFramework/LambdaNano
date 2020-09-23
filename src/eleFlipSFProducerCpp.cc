#include "../interface/eleFlipSFProducerCpp.h"

//constructor
eleFlipSFProducerCpp::eleFlipSFProducerCpp( const char* year, const unsigned int nLeptons, std::string requested_SF, const unsigned int requested_lepton ){

  nLeptons_ = nLeptons;
  working_point_ = "TightObjWP";  // WP is hardcoded for now, thinking of passing it at run time for more flexibility
  year_ = year;
  requested_SF_ = requested_SF;
  requested_lepton_ = requested_lepton;

  std::cout<<std::endl;
  std::cout<<" worker::eleFlipSFProducerCpp --> configuration" <<std::endl;
  std::cout<<" worker::eleFlipSFProducerCpp::nLeptons_ : "<< nLeptons_ <<std::endl;
  std::cout<<" worker::eleFlipSFProducerCpp::year_ : "<< year_ <<std::endl;
  std::cout<<" worker::eleFlipSFProducerCpp::requested_SF_ : "<< requested_SF_ <<std::endl;
  std::cout<<" worker::eleFlipSFProducerCpp::requested_lepton_ : "<< requested_lepton_ <<std::endl;
  std::cout<<std::endl;
  //
  nested_dict SF_files_map;
  std::string base = std::getenv("NANOAODTOOLS_BASE") ;

  // 2016
  SF_files_map["electron"]["TightObjWP"]["2016"]["flipper"] = { base + "/python/postprocessing/data/latino/scale_factor/chargeFlip/Full2016/chargeFlip_nanov5_2016_SF.root" } ;
  SF_files_map["electron"]["TightObjWP"]["2017"]["flipper"] = { base + "/python/postprocessing/data/latino/scale_factor/chargeFlip/Full2017/chargeFlip_nanov5_2017_SF.root" } ;
  SF_files_map["electron"]["TightObjWP"]["2018"]["flipper"] = { base + "/python/postprocessing/data/latino/scale_factor/chargeFlip/Full2018/chargeFlip_nanov5_2018_SF.root" } ;
  
  SF_files_map_ = SF_files_map;

  // electron
  //std::vector<TH2D> h_SF_ele {};

  loadHist( SF_files_map_["electron"][working_point_][year_]["flipper"] );
}

void eleFlipSFProducerCpp::loadHist( std::list<std::string> SF_files_map_in ) {

  TFile f( SF_files_map_in.front().c_str() );

  TH2D *h_mc       = (TH2D*) f.Get("mc")->Clone();                                                                                                                                                               
  TH2D *h_mc_sys   = (TH2D*) f.Get("mc_sys")->Clone();                                                                                                                                                           
  TH2D *h_data     = (TH2D*) f.Get("data")->Clone();                                                                                                                                                             
  TH2D *h_data_sys = (TH2D*) f.Get("data_sys")->Clone();                                                                                                                                                         
  TH2D *h_sf       = (TH2D*) f.Get("sf")->Clone();                                                                                                                                                               
  TH2D *h_sf_sys   = (TH2D*) f.Get("sf_sys")->Clone();

  h_mc->SetDirectory(0); h_mc_sys->SetDirectory(0);                                                                                                                                                              
  h_data->SetDirectory(0); h_data_sys->SetDirectory(0);                                                                                                                                                          
  h_sf->SetDirectory(0); h_sf_sys->SetDirectory(0);

  SFmap.insert(std::make_pair( "mc"       , h_mc       ));                                                                                                                                                       
  SFmap.insert(std::make_pair( "mc_sys"   , h_mc_sys   ));                                                                                                                                                       
  SFmap.insert(std::make_pair( "data"     , h_data     ));                                                                                                                                                       
  SFmap.insert(std::make_pair( "data_sys" , h_data_sys ));                                                                                                                                                       
  SFmap.insert(std::make_pair( "sf"       , h_sf       ));                                                                                                                                                       
  SFmap.insert(std::make_pair( "sf_sys"   , h_sf_sys   ));                                                                                                                                                       
  
  std::cout<<"loaded 2D map : "<< SF_files_map_in.front() <<std::endl;
  
}

double eleFlipSFProducerCpp::GetSF( double eta, double pt, std::string key ){

  double eta_temp = eta;
  double pt_temp = pt;

  double SF = 1.; //, SF_err, SF_sys;

  double eta_max = 2.49;
  double eta_min = -2.5;
  double pt_max = 199.;
  double pt_min = 25.;
  
  if(eta_temp < eta_min){eta_temp = eta_min;}
  if(eta_temp > eta_max){eta_temp = eta_max;}
  if(pt_temp < pt_min){pt_temp = pt_min;}
  if(pt_temp > pt_max){pt_temp = pt_max;}
  
  SF = SFmap[key]->GetBinContent(SFmap[key]->FindBin( TMath::Abs(eta_temp) , pt_temp ) );

  return SF;
}

double eleFlipSFProducerCpp::evaluate(){
  
  std::vector<double> SF_vect {};
  
  for(unsigned i=0;i<nLeptons_;i++){
    if(TMath::Abs(Lepton_pdgId->At(i)) != 11) continue;
    double res = GetSF( Lepton_eta->At(i), Lepton_pt->At(i) , "sf" ); 
    SF_vect.push_back(res);    
  } // end of for loops
  double SF = 1.;
    
  // Calculate product of IsIso_SFs for all leptons in the event --> central value of SF to be returned
  for(auto x : SF_vect) SF *= x;

  if(requested_SF_.compare("total_SF") == 0) { return SF; }
  else{ std::cout << "invalid option: please choose from [total_SF, single_SF, single_SF_up, single_SF_down]" << std::endl; return 0; }

}
