#include "../interface/lepSFProducerCpp.h"

//constructor
lepSFProducerCpp::lepSFProducerCpp( const char* year, const unsigned int nLeptons, std::string requested_SF, const unsigned int requested_lepton ){

  nLeptons_ = nLeptons;
  working_point_ = "TightObjWP";  // WP is hardcoded for now, thinking of passing it at run time for more flexibility
  year_ = year;
  requested_SF_ = requested_SF;
  requested_lepton_ = requested_lepton;

  std::cout<<std::endl;
  std::cout<<" worker::lepSFProducerCpp --> configuration" <<std::endl;
  std::cout<<" worker::lepSFProducerCpp::nLeptons_ : "<< nLeptons_ <<std::endl;
  std::cout<<" worker::lepSFProducerCpp::year_ : "<< year_ <<std::endl;
  std::cout<<" worker::lepSFProducerCpp::requested_SF_ : "<< requested_SF_ <<std::endl;
  std::cout<<" worker::lepSFProducerCpp::requested_lepton_ : "<< requested_lepton_ <<std::endl;
  std::cout<<std::endl;
  //
  nested_dict SF_files_map;
  std::string base = std::getenv("NANOAODTOOLS_BASE") ;

  // 2016
  SF_files_map["electron"]["TightObjWP"]["2016"]["wpSF"]= { base + "/python/postprocessing/data/latino/scale_factor/Full2016v7/egammaEffi_passingMVA80Xwp90Iso16.txt" };
  SF_files_map["electron"]["TightObjWP"]["2016"]["ttHMVA"]= { base + "/python/postprocessing/data/latino/scale_factor/Full2016v7/egammaEffi_TightHWW_ttHMVA_0p7_SFs_2016.txt" } ;
  SF_files_map["muon"]["TightObjWP"]["2016"]["idSF"] = { base + "/python/postprocessing/data/latino/scale_factor/Full2016v2/muonID_TH2_SFs_pt_eta.root" } ;
  SF_files_map["muon"]["TightObjWP"]["2016"]["isoSF"] = { base + "/python/postprocessing/data/latino/scale_factor/Full2016v2/muonISO_TH2_SFs_pt_eta.root" } ;
  SF_files_map["muon"]["ttHMVA0p8"]["2016"]["ttHMVA"] = { base + "/python/postprocessing/data/latino/scale_factor/ttH_SYS_SFs/ttHMVA0p8_TightHWWCut_SFs_2016.root" } ;
  SF_files_map["muon"]["ttHMVA0p8"]["2016"]["ttHMVA_SYS"] = { base + "/python/postprocessing/data/latino/scale_factor/ttH_SYS_SFs/ttHMVA0p8_TightHWWCut_SFs_SYS_2016.root" } ;

  // 2017
  SF_files_map["electron"]["TightObjWP"]["2017"]["wpSF"] = { base + "/python/postprocessing/data/latino/scale_factor/Full2017v7/egammaEffi_passingMVA102Xwp90isoHWWiso0p06_2017RunB.txt",
                                                             base + "/python/postprocessing/data/latino/scale_factor/Full2017v7/egammaEffi_passingMVA102Xwp90isoHWWiso0p06_2017RunCD.txt",
                                                             base + "/python/postprocessing/data/latino/scale_factor/Full2017v7/egammaEffi_passingMVA102Xwp90isoHWWiso0p06_2017RunE.txt",
                                                             base + "/python/postprocessing/data/latino/scale_factor/Full2017v7/egammaEffi_passingMVA102Xwp90isoHWWiso0p06_2017RunF.txt" } ;

  SF_files_map["electron"]["TightObjWP"]["2017"]["ttHMVA"] = { base + "/python/postprocessing/data/latino/scale_factor/Full2017v7/egammaEffi_TightHWW_ttHMVA_0p7_SFs_2017RunB.txt",
							       base + "/python/postprocessing/data/latino/scale_factor/Full2017v7/egammaEffi_TightHWW_ttHMVA_0p7_SFs_2017RunCD.txt",
							       base + "/python/postprocessing/data/latino/scale_factor/Full2017v7/egammaEffi_TightHWW_ttHMVA_0p7_SFs_2017RunE.txt",
							       base + "/python/postprocessing/data/latino/scale_factor/Full2017v7/egammaEffi_TightHWW_ttHMVA_0p7_SFs_2017RunF.txt",
  };

  SF_files_map["muon"]["TightObjWP"]["2017"]["idSF"] = { base + "/python/postprocessing/data/latino/scale_factor/Full2017/muonID_cut_Tight_HWW_combined.root" };
  SF_files_map["muon"]["TightObjWP"]["2017"]["isoSF"] = { base + "/python/postprocessing/data/latino/scale_factor/Full2017/muonISO_cut_Tight_HWW_combined.root" };
  SF_files_map["muon"]["ttHMVA0p8"]["2017"]["ttHMVA"] = { base + "/python/postprocessing/data/latino/scale_factor/ttH_SYS_SFs/ttHMVA0p8_TightHWWCut_SFs_2017.root" };
  SF_files_map["muon"]["ttHMVA0p8"]["2017"]["ttHMVA_SYS"] = { base + "/python/postprocessing/data/latino/scale_factor/ttH_SYS_SFs/ttHMVA0p8_TightHWWCut_SFs_SYS_2017.root" };

  // 2018
  SF_files_map["electron"]["TightObjWP"]["2018"]["wpSF"] = { base + "/python/postprocessing/data/latino/scale_factor/Full2018v7/egammaEffi_passingMVA102Xwp90isoHWWiso0p06_2018.txt" };
  SF_files_map["electron"]["TightObjWP"]["2018"]["ttHMVA"] = { base + "/python/postprocessing/data/latino/scale_factor/Full2018v7/egammaEffi_TightHWW_ttHMVA_0p7_SFs_2018.txt" };
  SF_files_map["muon"]["TightObjWP"]["2018"]["idSF"] = { base + "/python/postprocessing/data/latino/scale_factor/Full2018/ID_TH2_SFs_pt_eta.root" };
  SF_files_map["muon"]["TightObjWP"]["2018"]["isoSF"] = { base + "/python/postprocessing/data/latino/scale_factor/Full2018/ISO_TH2_SFs_pt_eta.root" };
  SF_files_map["muon"]["ttHMVA0p8"]["2018"]["ttHMVA"] = { base + "/python/postprocessing/data/latino/scale_factor/ttH_SYS_SFs/ttHMVA0p8_TightHWWCut_SFs_2018.root" };
  SF_files_map["muon"]["ttHMVA0p8"]["2018"]["ttHMVA_SYS"] = { base + "/python/postprocessing/data/latino/scale_factor/ttH_SYS_SFs/ttHMVA0p8_TightHWWCut_SFs_SYS_2018.root" };


  SF_files_map_ = SF_files_map;

  // electron
  std::vector<TH2D> h_SF_ele {};
  std::vector<TH2D> h_SF_ele_err {};
  std::vector<TH2D> h_SF_ele_sys {};
  std::vector<TH2D> h_SF_ele_ttHMVA {};
  std::vector<TH2D> h_SF_ele_ttHMVA_err {};
  std::vector<TH2D> h_SF_ele_ttHMVA_sys {};

  makeSF_ele( SF_files_map_["electron"][working_point_][year_]["wpSF"]  , h_SF_ele , h_SF_ele_err , h_SF_ele_sys );
  makeSF_ele( SF_files_map_["electron"][working_point_][year_]["ttHMVA"]  , h_SF_ele_ttHMVA , h_SF_ele_ttHMVA_err , h_SF_ele_ttHMVA_sys );

  h_SF_ele_ = h_SF_ele;
  h_SF_ele_err_ = h_SF_ele_err;
  h_SF_ele_sys_ = h_SF_ele_sys;
  h_SF_ele_ttHMVA_ = h_SF_ele_ttHMVA;
  h_SF_ele_ttHMVA_err_ = h_SF_ele_ttHMVA_err;
  h_SF_ele_ttHMVA_sys_ = h_SF_ele_ttHMVA_sys;

  //std::cout<<"len(h_SF_ele_): "<<h_SF_ele_.size()<<std::endl;
  // muon
  std::vector<TH2D> h_SF_mu_Id {};
  std::vector<TH2D> h_SF_mu_Id_err {};
  std::vector<TH2D> h_SF_mu_Id_sys {};
  std::vector<TH2D> h_SF_mu_Iso {};
  std::vector<TH2D> h_SF_mu_Iso_err {};
  std::vector<TH2D> h_SF_mu_Iso_sys {};
  std::vector<TH2D> h_SF_mu_ttHMVA {};
  std::vector<TH2D> h_SF_mu_ttHMVA_err {};
  std::vector<TH2D> h_SF_mu_ttHMVA_sys {};

  makeSF_muon( SF_files_map_["muon"][working_point_][year_]["idSF"]  , h_SF_mu_Id , h_SF_mu_Id_err , h_SF_mu_Id_sys , "Muon_idSF2D" ); //  IdSF
  makeSF_muon( SF_files_map_["muon"][working_point_][year_]["isoSF"]  , h_SF_mu_Iso , h_SF_mu_Iso_err , h_SF_mu_Iso_sys , "Muon_isoSF2D" ); // IsoSF
  std::pair< std::list<std::string> , std::list<std::string> > listPair;
  listPair = std::make_pair( SF_files_map_["muon"]["ttHMVA0p8"][year_]["ttHMVA"] , SF_files_map_["muon"]["ttHMVA0p8"][year_]["ttHMVA_SYS"] );
  makeSF_muon_tthMVA( listPair  , h_SF_mu_ttHMVA , h_SF_mu_ttHMVA_err , h_SF_mu_ttHMVA_sys , "ttHMVA0p8_TightHWWCut" );  // ttHMVA SF + SYST

  h_SF_mu_Id_ = h_SF_mu_Id;
  h_SF_mu_Id_err_ = h_SF_mu_Id_err;
  h_SF_mu_Id_sys_ = h_SF_mu_Id_sys;
  h_SF_mu_Iso_ = h_SF_mu_Iso;
  h_SF_mu_Iso_err_ = h_SF_mu_Iso_err;
  h_SF_mu_Iso_sys_ = h_SF_mu_Iso_sys;
  h_SF_mu_ttHMVA_ = h_SF_mu_ttHMVA;
  h_SF_mu_ttHMVA_err_ = h_SF_mu_ttHMVA_err;
  h_SF_mu_ttHMVA_sys_ = h_SF_mu_ttHMVA_sys;

}

void lepSFProducerCpp::makeSF_ele( std::list<std::string> SF_files_map_in , std::vector<TH2D> &sf_nom , std::vector<TH2D> &sf_stat , std::vector<TH2D> &sf_syst ) {

  int ele_nbins_eta = 10;
  int ele_nbins_pt = 7;

  float ele_eta_bins[] {-2.5, -2., -1.566, -1.444,  -0.8, 0., 0.8, 1.444, 1.566, 2.0, 2.5};
  float ele_pt_bins[] {10., 15., 20., 35., 50., 90., 150., 500.};

  // Loop on run periods
  for( auto f : SF_files_map_in ){

    TH2D h_SF = TH2D("", "", ele_nbins_eta, ele_eta_bins, ele_nbins_pt, ele_pt_bins);
    TH2D h_SF_err = TH2D("", "", ele_nbins_eta, ele_eta_bins, ele_nbins_pt, ele_pt_bins);
    TH2D h_SF_sys = TH2D("", "", ele_nbins_eta, ele_eta_bins, ele_nbins_pt, ele_pt_bins);

    for(int iBinX = 1; iBinX<=h_SF.GetNbinsX(); iBinX++){
      for(int iBinY = 1; iBinY<=h_SF.GetNbinsY(); iBinY++){

	double eta = h_SF.GetXaxis()->GetBinCenter(iBinX);
	double pt = h_SF.GetYaxis()->GetBinCenter(iBinY);

	if(f.find(".txt") != std::string::npos){
	  //Parsing the .txt file
	  std::string line;
	  std::istringstream strm;
	  double num;
	  std::ifstream ifs(f);

	  double lines[70][12];

	  int i=0;
	  int j=0;
	  while(getline(ifs, line)){
	    j=0;
	    std::istringstream strm(line);
	    while(strm >> num){
	      lines[i][j] = num;
	      j++;
	    }
	    i++;
	  }
	  //Looking for correct eta, pt bin
	  for(unsigned int i=0;i<70;i++){

	    if(eta>=lines[i][0] && eta<=lines[i][1] && pt>=lines[i][2] && pt<=lines[i][3]){

	      double data = lines[i][4];
	      double mc = lines[i][6];

	      double sigma_d = lines[i][5];
	      double sigma_m = lines[i][7];

	      h_SF.SetBinContent(iBinX, iBinY, data/mc);
	      h_SF_err.SetBinContent(iBinX, iBinY, TMath::Sqrt( TMath::Power(sigma_d/mc, 2) + TMath::Power(data/mc/mc*sigma_m, 2) ));
	      h_SF_sys.SetBinContent(iBinX, iBinY, TMath::Sqrt( TMath::Power(lines[i][8], 2) + TMath::Power(lines[i][9], 2) + TMath::Power(lines[i][10], 2) + TMath::Power(lines[i][11], 2) ) / mc);
	      break;
	    }
	  }
	}
	else{
	  //Not needed for now as all electron SF files are .txt
	  continue;
	}
      }
    }

    sf_nom.push_back(h_SF);
    sf_stat.push_back(h_SF_err);
    sf_syst.push_back(h_SF_sys);
  }
}

void lepSFProducerCpp::makeSF_muon( std::list<std::string> SF_files_map_in , std::vector<TH2D> &sf_nom , std::vector<TH2D> &sf_stat , std::vector<TH2D> &sf_syst , std::string histname ) {

  for( auto f : SF_files_map_in ){

    TFile rootfile(f.c_str());
    TH2D* htemp = (TH2D*)rootfile.Get(histname.c_str());

    int mu_nbins_eta = htemp->GetNbinsX(), mu_nbins_pt = htemp->GetNbinsY();
    double mu_eta_bins[mu_nbins_eta + 1], mu_pt_bins[mu_nbins_pt + 1];

    for(int k=0;k<=mu_nbins_eta;k++) { mu_eta_bins[k] = htemp->GetXaxis()->GetXbins()->At(k); }
    for(int k=0;k<=mu_nbins_pt;k++) { mu_pt_bins[k] = htemp->GetYaxis()->GetXbins()->At(k); }

    TH2D h_SF = TH2D("", "", mu_nbins_eta, mu_eta_bins, mu_nbins_pt, mu_pt_bins);
    TH2D h_SF_err = TH2D("", "", mu_nbins_eta, mu_eta_bins, mu_nbins_pt, mu_pt_bins);
    TH2D h_SF_sys = TH2D("", "", mu_nbins_eta, mu_eta_bins, mu_nbins_pt, mu_pt_bins);

    for(int i=1; i<=mu_nbins_eta;i++){
            for(int j=1; j<=mu_nbins_pt;j++){
	      h_SF.SetBinContent(i, j, htemp->GetBinContent(i, j));
	      h_SF_err.SetBinContent(i, j, htemp->GetBinError(i, j));
	      h_SF_sys.SetBinContent(i, j, 1.); // FIXME this is here as a placeholder: old SF files only have total error, in the new ones it is split
            }
        }

    sf_nom.push_back(h_SF);
    sf_stat.push_back(h_SF_err);
    sf_syst.push_back(h_SF_sys);
  }
}

void lepSFProducerCpp::makeSF_muon_tthMVA( std::pair< std::list<std::string> , std::list<std::string> > SF_files_map_in , std::vector<TH2D> &sf_nom , std::vector<TH2D> &sf_stat , std::vector<TH2D> &sf_syst , std::string histname ) {

  // NOM
  for( auto f : SF_files_map_in.first ){

    TFile rootfile(f.c_str());
    TH2D* htemp = (TH2D*)rootfile.Get(histname.c_str());

    int mu_nbins_eta = htemp->GetNbinsX(), mu_nbins_pt = htemp->GetNbinsY();
    double mu_eta_bins[mu_nbins_eta + 1], mu_pt_bins[mu_nbins_pt + 1];

    for(int k=0;k<=mu_nbins_eta;k++) { mu_eta_bins[k] = htemp->GetXaxis()->GetXbins()->At(k); }
    for(int k=0;k<=mu_nbins_pt;k++) { mu_pt_bins[k] = htemp->GetYaxis()->GetXbins()->At(k); }

    TH2D h_SF = TH2D("", "", mu_nbins_eta, mu_eta_bins, mu_nbins_pt, mu_pt_bins);
    TH2D h_SF_err = TH2D("", "", mu_nbins_eta, mu_eta_bins, mu_nbins_pt, mu_pt_bins);
    TH2D h_SF_sys = TH2D("", "", mu_nbins_eta, mu_eta_bins, mu_nbins_pt, mu_pt_bins);

    for(int i=1; i<=mu_nbins_eta;i++){
      for(int j=1; j<=mu_nbins_pt;j++){
	h_SF.SetBinContent(i, j, htemp->GetBinContent(i, j));
	h_SF_err.SetBinContent(i, j, htemp->GetBinError(i, j));
      }
    }

    sf_nom.push_back(h_SF);
    sf_stat.push_back(h_SF_err);
  }

  // SYS
  for( auto f : SF_files_map_in.second ){
    TFile rootfile(f.c_str());
    TH2D* htemp = (TH2D*)rootfile.Get(histname.c_str());

    int mu_nbins_eta = htemp->GetNbinsX(), mu_nbins_pt = htemp->GetNbinsY();
    double mu_eta_bins[mu_nbins_eta + 1], mu_pt_bins[mu_nbins_pt + 1];

    for(int k=0;k<=mu_nbins_eta;k++) { mu_eta_bins[k] = htemp->GetXaxis()->GetXbins()->At(k); }
    for(int k=0;k<=mu_nbins_pt;k++) { mu_pt_bins[k] = htemp->GetYaxis()->GetXbins()->At(k); }

    TH2D h_SF = TH2D("", "", mu_nbins_eta, mu_eta_bins, mu_nbins_pt, mu_pt_bins);
    TH2D h_SF_err = TH2D("", "", mu_nbins_eta, mu_eta_bins, mu_nbins_pt, mu_pt_bins);
    TH2D h_SF_sys = TH2D("", "", mu_nbins_eta, mu_eta_bins, mu_nbins_pt, mu_pt_bins);

    for(int i=1; i<=mu_nbins_eta;i++){
      for(int j=1; j<=mu_nbins_pt;j++){
	h_SF_sys.SetBinContent(i, j, htemp->GetBinError(i, j));
      }
    }
    sf_syst.push_back(h_SF_sys);
  }
}

std::tuple<double, double, double> lepSFProducerCpp::GetSF(int flavor, double eta, double pt, int run_period, std::string type){

  double eta_temp = eta;
  double pt_temp = pt;

  double SF, SF_err, SF_sys;

  if((flavor==11) && (type == "ttHMVA")){

    double eta_max = 2.49;
    double eta_min = -2.5;
    double pt_max = 499.;
    double pt_min = 10.;

    if(eta_temp < eta_min){eta_temp = eta_min;}
    if(eta_temp > eta_max){eta_temp = eta_max;}
    if(pt_temp < pt_min){pt_temp = pt_min;}
    if(pt_temp > pt_max){pt_temp = pt_max;}

    SF = h_SF_ele_ttHMVA_[run_period].GetBinContent(h_SF_ele_ttHMVA_[run_period].FindBin(eta_temp, pt_temp));
    SF_err = h_SF_ele_ttHMVA_err_[run_period].GetBinContent(h_SF_ele_ttHMVA_err_[run_period].FindBin(eta_temp, pt_temp));
    SF_sys = h_SF_ele_ttHMVA_sys_[run_period].GetBinContent(h_SF_ele_ttHMVA_sys_[run_period].FindBin(eta_temp, pt_temp));

  }

  else if((flavor==11) && (type == "Id")){

    double eta_max = 2.49;
    double eta_min = -2.5;
    double pt_max = 499.;
    double pt_min = 10.;

    if(eta_temp < eta_min){eta_temp = eta_min;}
    if(eta_temp > eta_max){eta_temp = eta_max;}
    if(pt_temp < pt_min){pt_temp = pt_min;}
    if(pt_temp > pt_max){pt_temp = pt_max;}

    SF = h_SF_ele_[run_period].GetBinContent(h_SF_ele_[run_period].FindBin(eta_temp, pt_temp));
    SF_err = h_SF_ele_err_[run_period].GetBinContent(h_SF_ele_err_[run_period].FindBin(eta_temp, pt_temp));
    SF_sys = h_SF_ele_sys_[run_period].GetBinContent(h_SF_ele_sys_[run_period].FindBin(eta_temp, pt_temp));

  }

  else if((flavor == 13) && (type == "Id")){

    double eta_max = 2.39;
    double eta_min = -2.4;
    double pt_max = 199.;
    double pt_min = 10.;

    if(eta_temp < eta_min){eta_temp = eta_min;}
    if(eta_temp > eta_max){eta_temp = eta_max;}
    if(pt_temp < pt_min){pt_temp = pt_min;}
    if(pt_temp > pt_max){pt_temp = pt_max;}

    SF = h_SF_mu_Id_[run_period].GetBinContent(h_SF_mu_Id_[run_period].FindBin(eta_temp, pt_temp));
    SF_err = h_SF_mu_Id_err_[run_period].GetBinContent(h_SF_mu_Id_err_[run_period].FindBin(eta_temp, pt_temp));
    SF_sys = h_SF_mu_Id_sys_[run_period].GetBinContent(h_SF_mu_Id_sys_[run_period].FindBin(eta_temp, pt_temp));

  }

  else if((flavor == 13) && (type == "Iso")){

    double eta_max = 2.39;
    double eta_min = -2.4;
    double pt_max = 199.;
    double pt_min = 10.;

    if(eta_temp < eta_min){eta_temp = eta_min;}
    if(eta_temp > eta_max){eta_temp = eta_max;}
    if(pt_temp < pt_min){pt_temp = pt_min;}
    if(pt_temp > pt_max){pt_temp = pt_max;}

    SF = h_SF_mu_Iso_[run_period].GetBinContent(h_SF_mu_Iso_[run_period].FindBin(eta_temp, pt_temp));
    SF_err = h_SF_mu_Iso_err_[run_period].GetBinContent(h_SF_mu_Iso_err_[run_period].FindBin(eta_temp, pt_temp));
    SF_sys = h_SF_mu_Iso_sys_[run_period].GetBinContent(h_SF_mu_Iso_sys_[run_period].FindBin(eta_temp, pt_temp));

  }

  else if((flavor == 13) && (type == "ttHMVA")){

    double eta_max = 2.39;
    double eta_min = -2.4;
    double pt_max = 199.;
    double pt_min = 10.;

    if(eta_temp < eta_min){eta_temp = eta_min;}
    if(eta_temp > eta_max){eta_temp = eta_max;}
    if(pt_temp < pt_min){pt_temp = pt_min;}
    if(pt_temp > pt_max){pt_temp = pt_max;}

    SF = h_SF_mu_ttHMVA_[run_period].GetBinContent(h_SF_mu_ttHMVA_[run_period].FindBin(eta_temp, pt_temp));
    SF_err = h_SF_mu_ttHMVA_err_[run_period].GetBinContent(h_SF_mu_ttHMVA_err_[run_period].FindBin(eta_temp, pt_temp));
    SF_sys = h_SF_mu_ttHMVA_sys_[run_period].GetBinContent(h_SF_mu_ttHMVA_sys_[run_period].FindBin(eta_temp, pt_temp));

  }

  else {std::cout << "Invalid call to compute_SF::GetSF" << std::endl;}

  std::tuple<double, double, double> result = {SF, SF_err, SF_sys};

  return result;

}

double lepSFProducerCpp::evaluate(){

  std::vector<double> SF_vect {};
  std::vector<double> SF_err_vect {};
  std::vector<double> SF_up {};
  std::vector<double> SF_do {};

  for(unsigned i=0;i<nLeptons_;i++){

    if(TMath::Abs(Lepton_pdgId->At(i)) == 11){

      std::list<std::string> SF_path = SF_files_map_["electron"][working_point_][year_]["wpSF"];
      std::list<std::string> SF_path_ttHMVA = SF_files_map_["electron"][working_point_][year_]["ttHMVA"];

      std::tuple<double, double, double> res = GetSF(11, Lepton_eta->At(i), Lepton_pt->At(i), SF_path.size()==1 ? 0 : *run_period->Get() - 1, "Id");
      std::tuple<double, double, double> res_ttHMVA = GetSF(11, Lepton_eta->At(i), Lepton_pt->At(i), SF_path_ttHMVA.size()==1 ? 0 : *run_period->Get() - 1, "ttHMVA");

      SF_vect.push_back(std::get<0>(res)*std::get<0>(res_ttHMVA));
      SF_err_vect.push_back(TMath::Sqrt(TMath::Power(std::get<1>(res), 2) + TMath::Power(std::get<2>(res), 2)
					+ TMath::Power(std::get<1>(res_ttHMVA), 2) + TMath::Power(std::get<2>(res_ttHMVA), 2) ));

    }

    else if(TMath::Abs(Lepton_pdgId->At(i)) == 13){

      std::list<std::string> SF_path_id = SF_files_map_["muon"][working_point_][year_]["idSF"];
      std::list<std::string> SF_path_iso = SF_files_map_["muon"][working_point_][year_]["isoSF"];

      std::tuple<double, double, double> res_id = GetSF(13, Lepton_eta->At(i), Lepton_pt->At(i), SF_path_id.size()==1 ? 0 : *run_period->Get() - 1, "Id");
      std::tuple<double, double, double> res_iso = GetSF(13, Lepton_eta->At(i), Lepton_pt->At(i), SF_path_iso.size()==1 ? 0 : *run_period->Get() - 1, "Iso");
      std::tuple<double, double, double> res_ttHMVA = GetSF(13, Lepton_eta->At(i), Lepton_pt->At(i), SF_path_iso.size()==1 ? 0 : *run_period->Get() - 1, "ttHMVA");

      double SF_id = std::get<0>(res_id);
      double SF_iso = std::get<0>(res_iso);
      double SF_ttHMVA = std::get<0>(res_ttHMVA);

      SF_vect.push_back(SF_id * SF_iso * SF_ttHMVA);
      // SF_err_vect.push_back((SF_id * SF_iso) * TMath::Sqrt( TMath::Power(std::get<1>(res_id)/SF_id, 2) + TMath::Power(std::get<1>(res_iso)/SF_iso, 2) )); // Old formula for debugging
      SF_err_vect.push_back(
			    (SF_id * SF_iso * SF_ttHMVA) * TMath::Sqrt(
								       TMath::Power(std::get<1>(res_id)/SF_id, 2)
								       + TMath::Power(std::get<1>(res_iso)/SF_iso, 2)
								       + (TMath::Power(std::get<1>(res_ttHMVA), 2) + TMath::Power(std::get<2>(res_ttHMVA), 2))/SF_ttHMVA/SF_ttHMVA )
			    );
    }

  }

  double SF = 1.;
  double SF_err = 0.;

  // Calculate product of IsIso_SFs for all leptons in the event --> central value of SF to be returned
  for(auto x : SF_vect) SF *= x;

  // Now for the variations, these also have to account for the recoSF
  for(unsigned int i=0;i<nLeptons_;i++){
    SF_up.push_back( ((SF_vect[i] * Lepton_RecoSF->At(i)) + TMath::Sqrt(TMath::Power(SF_err_vect[i], 2) + TMath::Power(Lepton_RecoSF_Up->At(i) - Lepton_RecoSF->At(i), 2) ))/(SF_vect[i] * Lepton_RecoSF->At(i)) );
    SF_do.push_back( ((SF_vect[i] * Lepton_RecoSF->At(i)) - TMath::Sqrt(TMath::Power(SF_err_vect[i], 2) + TMath::Power(Lepton_RecoSF_Down->At(i) - Lepton_RecoSF->At(i), 2) ))/(SF_vect[i] * Lepton_RecoSF->At(i)) );
  }

  if(requested_SF_.compare("total_SF") == 0) { return SF; }
  else if(requested_SF_.compare("single_SF_up") == 0) { return requested_lepton_<SF_vect.size() ? SF_up[requested_lepton_] : 1.; }
  else if(requested_SF_.compare("single_SF_down") == 0) { return requested_lepton_<SF_vect.size() ? SF_do[requested_lepton_] : 1.; }
  else if(requested_SF_.compare("single_SF") == 0) { return requested_lepton_<SF_vect.size() ? SF_vect[requested_lepton_] : 1.; }
  else{ std::cout << "invalid option: please choose from [total_SF, single_SF, single_SF_up, single_SF_down]" << std::endl; return 0; }

}
