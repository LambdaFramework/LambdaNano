#include "../interface/producerCppWorker.h"
using namespace std;

int producerCppWorker::countEvent(){
  return 1;
}

float producerCppWorker::getHadronicMET(){

  //Hadronic Recoil
  //Correcting PFMET by subtracting the contribution of leptonic Pt in the event

  float METpt = (*MET_pt).Get()[0];
  float METphi = (*MET_phi).Get()[0];
  float METpx=METpt*TMath::Cos(METphi);
  float METpy=METpt*TMath::Sin(METphi);
  float px=0.;
  float py=0.;

  unsigned nEle =  (*nElectron).Get()[0];
  unsigned nMu =  (*nMuon).Get()[0];

  float leptonicpx=0.;
  float leptonicpy=0.;

  if (nEle>0){
    for (unsigned i=0; i<nEle; i++){
      leptonicpx+=((*Electron_pt)[i])*TMath::Cos((*Electron_eta)[i]);
      leptonicpy+=((*Electron_pt)[i])*TMath::Sin((*Electron_eta)[i]);
    }
  }  
  
  if (nMu>0){
    for (unsigned i=0; i<nMu; i++){
      leptonicpx+=((*Muon_pt)[i])*TMath::Cos((*Muon_eta)[i]);
      leptonicpy+=((*Muon_pt)[i])*TMath::Sin((*Muon_eta)[i]);
    }
  }

  px = METpx + leptonicpx;
  py = METpy + leptonicpy;

  return TMath::Sqrt(TMath::Power(px,2)+TMath::Power(py,2));

};

std::pair<float,float> producerCppWorker::getHT(){
    math::XYZTLorentzVectorF ht(0,0,0,0);
    unsigned n = (*nJet).Get()[0];
    for (unsigned i=0; i<n; i++){
      ht += math::PtEtaPhiMLorentzVectorF((*Jet_pt)[i],0,(*Jet_phi)[i],0);
    }
    return std::pair<float,float>(ht.Pt(),ht.Phi());
};

std::vector<double> producerCppWorker::getW(){

  //Transverse Mass
  //Compute the 4 vector transverse property of W boson mass

  unsigned nEle =  (*nElectron).Get()[0];
  unsigned nMu =  (*nMuon).Get()[0];
  //MET components
  float METpt = (*MET_pt).Get()[0];
  float METphi = (*MET_phi).Get()[0];
  //float METsumEt = (*MET_sumEt).Get()[0];
  //std::cout<<"nEle : "<<nEle<<" ; "<<"nMu : "<<nMu<<std::endl;

  std::vector<double> tmass;

  //compare the number of lepton
  if (nEle>=1 && nMu>=1){
    if ( (*Electron_pt)[0] > (*Muon_pt)[0] ){
      tmass.push_back( TMath::Sqrt( ( 2*(*Electron_pt)[0]*METpt )*( 1 - TMath::Cos( deltaPhi( (*Electron_phi)[0] , METphi ) ) ) ) );
    }
    else if ( (*Electron_pt)[0] < (*Muon_pt)[0] ){
      tmass.push_back( TMath::Sqrt( ( 2*(*Muon_pt)[0]*METpt )*( 1 - TMath::Cos( deltaPhi( (*Muon_phi)[0] , METphi ) ) ) ) );
    }
  }
  else if (nMu==0 && nEle>=1){
    tmass.push_back( TMath::Sqrt( ( 2*(*Electron_pt)[0]*METpt )*( 1 - TMath::Cos( deltaPhi( (*Electron_phi)[0] , METphi ) ) ) ) );
  }
  else if (nEle==0 && nMu>=1){
    tmass.push_back( TMath::Sqrt( ( 2*(*Muon_pt)[0]*METpt )*( 1 - TMath::Cos( deltaPhi( (*Muon_phi)[0] , METphi ) ) ) ) );
  }
  else if (nEle==0 && nMu==0){
    tmass.push_back(0.);
  }
  else{std::cout<<"WTF"<<std::endl;}

  return tmass;
};

std::vector<double> producerCppWorker::getZ(){

  //Z boson reconstruction
  //Taking the sum of 4 vector of leading and sub-leading lepton pt of same flavor.

  unsigned nEle =  (*nElectron).Get()[0];
  unsigned nMu =  (*nMuon).Get()[0];

  TLorentzVector V(0,0,0,0);
  TLorentzVector V1(0,0,0,0);
  TLorentzVector V2(0,0,0,0);

  //std::cout<<"nEle : "<<nEle<<" ; "<<"nMu : "<<nMu<<std::endl; 
  //std::cout<<"(*Muon_pt)[0] = "<<(*Muon_pt)[0]<<" , (*Muon_eta)[0] = "<<(*Muon_eta)[0]<<" , (*Muon_phi)[0] = "<<(*Muon_phi)[0]<<" , (*Muon_mass)[0] = "<<(*Muon_mass)[0]<<std::endl;
  //std::cout<<"(*Electron_pt)[0] = "<<(*Electron_pt)[0]<<" , (*Electron_eta)[0] = "<<(*Electron_eta)[0]<<" , (*Electron_phi)[0] = "<<(*Electron_phi)[0]<<" , (*Electron_mass)[0] = "<<(*Electron_mass)[0]<<std::endl;

  if (nEle>1 && nMu>1){
    //lepton pt determine    
    if ( (*Electron_pt)[0] > (*Muon_pt)[0] )
      {
	V1.SetPtEtaPhiM( (*Electron_pt)[0], (*Electron_eta)[0], (*Electron_phi)[0], (*Electron_mass)[0] );
	V2.SetPtEtaPhiM( (*Electron_pt)[1], (*Electron_eta)[1], (*Electron_phi)[1], (*Electron_mass)[1] );
	V=V1+V2;
      }
    else if ( (*Electron_pt)[0] < (*Muon_pt)[0] )
      {
	V1.SetPtEtaPhiM( (*Muon_pt)[0], (*Muon_eta)[0], (*Muon_phi)[0], (*Muon_mass)[0] );
	V2.SetPtEtaPhiM( (*Muon_pt)[1], (*Muon_eta)[1], (*Muon_phi)[1], (*Muon_mass)[1] );
	V=V1+V2;
      }
  }
  else if (nEle>1 && nMu==0){
    V1.SetPtEtaPhiM( (*Electron_pt)[0], (*Electron_eta)[0], (*Electron_phi)[0], (*Electron_mass)[0] );
    V2.SetPtEtaPhiM( (*Electron_pt)[1], (*Electron_eta)[1], (*Electron_phi)[1], (*Electron_mass)[1] );
    V=V1+V2;
  }
  else if (nEle==0 && nMu>1){
    V1.SetPtEtaPhiM( (*Muon_pt)[0], (*Muon_eta)[0], (*Muon_phi)[0], (*Muon_mass)[0] );
    V2.SetPtEtaPhiM( (*Muon_pt)[1], (*Muon_eta)[1], (*Muon_phi)[1], (*Muon_mass)[1] );
    V=V1+V2;
  }

  //std::cout<<"V.Pt() = "<<V.Pt()<<" , V.Eta() = "<<V.Eta()<<" , V.Phi() = "<<V.Phi()<<" , V.M() = "<<V.M()<<std::endl;
  
  return std::vector<double>{V.Pt(),V.Eta(),V.Phi(),V.M()};
};

std::vector<double> producerCppWorker::getJJ(){

  //Reconstructed dijet system
  //Taking the 4 vector of leading and sub-leading jet pt
  
  unsigned nJets =  (*nJet).Get()[0];
  
  TLorentzVector V(0,0,0,0);
  TLorentzVector V1(0,0,0,0);
  TLorentzVector V2(0,0,0,0);

  if (nJets>1){
    V1.SetPtEtaPhiM( (*Jet_pt)[0], (*Jet_eta)[0], (*Jet_phi)[0], (*Jet_mass)[0] );
    V2.SetPtEtaPhiM( (*Jet_pt)[1], (*Jet_eta)[1], (*Jet_phi)[1], (*Jet_mass)[1] );
    V=V1+V2;
  }

  return std::vector<double>{V.Pt(),V.Eta(),V.Phi(),V.M()};
  
};

std::vector<double> producerCppWorker::getJJL(){

  //Reconstructed dijet and a lepton system
  //Taking the 4 vector sum of dijet system and a leading lepton

  unsigned nJets =  (*nJet).Get()[0];
  unsigned nEle =  (*nElectron).Get()[0];
  unsigned nMu =  (*nMuon).Get()[0];

  TLorentzVector V(0,0,0,0);
  TLorentzVector V1(0,0,0,0);
  TLorentzVector V2(0,0,0,0);
  TLorentzVector V3(0,0,0,0);

  if ( nJets>1 && (nEle>=1 || nMu>=1) ){

    V1.SetPtEtaPhiM( (*Jet_pt)[0], (*Jet_eta)[0], (*Jet_phi)[0], (*Jet_mass)[0] );
    V2.SetPtEtaPhiM( (*Jet_pt)[1], (*Jet_eta)[1], (*Jet_phi)[1], (*Jet_mass)[1] );
    
    if (nEle>=1 && nMu>=1){
      if ( (*Electron_pt)[0] > (*Muon_pt)[0] ){
	V3.SetPtEtaPhiM( (*Electron_pt)[0], (*Electron_eta)[0], (*Electron_phi)[0], (*Electron_mass)[0] );
      }
      else if ( (*Electron_pt)[0] < (*Muon_pt)[0] ){
	V3.SetPtEtaPhiM( (*Muon_pt)[0], (*Muon_eta)[0], (*Muon_phi)[0], (*Muon_mass)[0] );
      }
    }
    else if (nEle>=1 && nMu==0){
      V3.SetPtEtaPhiM( (*Electron_pt)[0], (*Electron_eta)[0], (*Electron_phi)[0], (*Electron_mass)[0] );
    }
    else if (nEle==0 && nMu>=1){
      V3.SetPtEtaPhiM( (*Muon_pt)[0], (*Muon_eta)[0], (*Muon_phi)[0], (*Muon_mass)[0] );
    }
  }

  V=V1+V2+V3;
  
  return std::vector<double>{V.Pt(),V.Eta(),V.Phi(),V.M()};

};

float producerCppWorker::getDeltaPhiJetMET(){

  //DeltaPhiJetMET

  unsigned nJets=(*nJet).Get()[0];
  float METpt = (*MET_pt).Get()[0];
  float METphi = (*MET_phi).Get()[0];
  float dphijetmet=999.;
  TLorentzVector V(0,0,0,0);
  TLorentzVector METV(METpt, 0., METphi, 0.);

  for (unsigned i=0; i<nJets; i++){
    V.SetPtEtaPhiM( (*Jet_pt)[i], (*Jet_eta)[i], (*Jet_phi)[i], (*Jet_mass)[i] );
    dphijetmet = std::min( fabs( V.DeltaPhi(METV) ), (double)dphijetmet );
    V.SetPtEtaPhiM( 0., 0., 0., 0. );
  }

  return dphijetmet;

};

