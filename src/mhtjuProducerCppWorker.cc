#include "../interface/mhtjuProducerCppWorker.h"

//Compute ht with the following criteries:
//Jet_puId[jet] > 4 AND ( either no good electrons (muons) with pT> 15 (5) GeV within a cone DR <0.4 around the jet ||

/*
std::pair<float,float> mhtjuProducerCppWorker::getHT(){

    math::XYZTLorentzVectorF ht(0,0,0,0);

    unsigned njet = (*nJet).Get()[0];
    unsigned nelectron = (*nElectron).Get()[0];
    unsigned nmuon = (*nMuon).Get()[0];

    for (unsigned i=0; i<njet; i++){

      //Number of associated muon in jets
      int jet_nMuons = (*Jet_nMuons)[i];
      int jet_nElectrons = (*Jet_nElectrons)[i];
      int passJetMuon=0;
      int passJetElectron=0;
      //Jet cleaning-Muon
      if ( (*Jet_puId)[i] > 4 ){
    
	//unsigned njetMuon=(*Jet_nMuons)[i];
	for (unsigned j=0; j<nmuon; j++){
	  int muonInJetIndex = (*Muon_jetIdx)[j];
	  if ( (*Muon_jetIdx)[j]>1 ){ // non-zero indicate its association to jet (not isolated)
	    if ( ( (*Muon_tightId)[j]!=1 && (*Muon_pt)[j]>5 ) || // the associated muon must not be tight 
		 ( ( ( (*Muon_tightId)[j]==1 && (*Muon_pt)[j]>5 ) &&  // if it is a tight muon
		     ( (*Jet_chHEF)[muonInJetIndex] > 0.1 || (*Jet_neHEF)[muonInJetIndex] > 0.2 ) ) ) ) // check on the charge and neutral hadronic energy fraction cut
	      {
		// Here we have Proven cleanjet
		passJetMuon+=1;
	      }
	  }
	}

	for (unsigned k=0; k<nelectron; k++){
          int electronInJetIndex = (*Electron_jetIdx)[k];
	  if ( (*Electron_jetIdx)[k]>1 ){
	    if ( ( (*Electron_cutBased)[k]!=4 && (*Electron_pt)[k]>15 ) ||
		 ( ( ( (*Electron_cutBased)[k]==4 && (*Electron_pt)[k]>15 ) &&
		     ( (*Jet_chHEF)[electronInJetIndex] > 0.1 || (*Jet_neHEF)[electronInJetIndex] > 0.2 ) ) ) ) 
	      {
		passJetElectron+=1;
	      }
	  }
	}
      }
      else{
	continue;
      }

      if ( jet_nMuons==passJetMuon && jet_nElectrons==passJetElectron )
	ht += math::PtEtaPhiMLorentzVectorF((*Jet_pt)[i],0,(*Jet_phi)[i],0);
    }
    return std::pair<float,float>(ht.Pt(),ht.Phi());
};
*/

void mhtjuProducerCppWorker::reportHT(){

  unsigned njet = (*nJet).Get()[0];
  unsigned nelectron = (*nElectron).Get()[0];
  unsigned nmuon = (*nMuon).Get()[0];

  std::cout<<"== PROCESSING Event =="<<std::endl;
  std::cout<<"EVENT: Number of Jet = "<<njet<<std::endl;
  std::cout<<"EVENT: Number of Electron = "<<nelectron<<std::endl;
  std::cout<<"EVENT: Number of Muon = "<<nmuon<<std::endl;
  std::cout<<std::endl;

  for (unsigned i=0; i<njet; i++){

    //Number of associated lepton in jet
    unsigned jet_nMuons = (*Jet_nMuons)[i];
    unsigned jet_nElectrons = (*Jet_nElectrons)[i];
    float jet_chHEF = (*Jet_chHEF)[i];
    float jet_neHEF = (*Jet_neHEF)[i];

    std::cout<<"== PROCESSING Physics Object-Jet =="<<std::endl;
    std::cout<<"JET-"<<i<<"th: Number of Muon = "<<jet_nMuons<<std::endl;
    std::cout<<"JET-"<<i<<"th: Number of Electron = "<<jet_nElectrons<<std::endl;
    std::cout<<"JET-"<<i<<"th: Jet_puId of Jet = "<<(*Jet_puId)[i]<<std::endl;
    std::cout<<"JET-"<<i<<"th: jet_chHEF = "<<jet_chHEF<<std::endl;
    std::cout<<"JET-"<<i<<"th: jet_neHEF = "<<jet_neHEF<<std::endl;
    std::cout<<std::endl;

    //index lepton associated to jet 
    for (unsigned j=0; j<jet_nMuons; j++){
      //int indexM2J = (*Muon_jetIdx)[j];
      int indexJ2M1 = (*Jet_muonIdx1)[j];
      int indexJ2M2 = (*Jet_muonIdx2)[j];
      //if (indexJ2M1<0 || indexJ2M2<0) continue; // if null ref, meaning no leading lepton pt associated with jet

      std::cout<<"== PROCESSING Physics Object-Jet-Muon =="<<std::endl;
      //std::cout<<"JET-MUON-"<<j<<"th: Jet index associated to Muon = "<<indexM2J<<std::endl;
      std::cout<<"JET-MUON-"<<j<<"th: Muon (1) index associated to Jet = "<<indexJ2M1<<std::endl;
      std::cout<<"JET-MUON-"<<j<<"th: Muon (2) index associated to Jet = "<<indexJ2M2<<std::endl;
      if(indexJ2M1<0) continue;
      else{
	std::cout<<"JET-MUON-"<<j<<"th: pointing --> Muon_pt[indexJ2M1] = "<< (*Muon_pt)[indexJ2M1] <<std::endl;
	std::cout<<"JET-MUON-"<<j<<"th: pointing --> Muon_mediumId[indexJ2M1] = "<< (*Muon_mediumId)[indexJ2M1] <<std::endl;
      }
      if(indexJ2M2<0) continue;
      else{
	std::cout<<"JET-MUON-"<<j<<"th: pointing --> Muon_pt[indexJ2M2] = "<< (*Muon_pt)[indexJ2M2] <<std::endl;
	std::cout<<"JET-MUON-"<<j<<"th: pointing --> Muon_mediumId[indexJ2M2] = "<< (*Muon_mediumId)[indexJ2M2] <<std::endl;
      }
      std::cout<<std::endl;
    }

    //index lepton associated to jet 
    for (unsigned k=0; k<jet_nElectrons; k++){                                                                                                                     
      //int indexE2J = (*Electron_jetIdx)[k];
      int indexJ2E1 = (*Jet_electronIdx1)[k];
      int indexJ2E2 = (*Jet_electronIdx2)[k];
      //if (indexJ2E1<0 || indexJ2E2<0) continue;

      std::cout<<"== PROCESSING Physics Object-Jet-Electron =="<<std::endl;
      //std::cout<<"JET-Electron-"<<k<<"th: Jet index associated to Electron = "<<indexE2J<<std::endl;
      std::cout<<"JET-Electron-"<<k<<"th: Electron (1) index associated to Jet = "<<indexJ2E1<<std::endl;
      std::cout<<"JET-Electron-"<<k<<"th: Electron (2) index associated to Jet = "<<indexJ2E2<<std::endl;
      if (indexJ2E1<0) continue;
      else{
	std::cout<<"JET-Electron-"<<k<<"th: pointing --> Electron_pt[indexJ2E1] = "<<(*Electron_pt)[indexJ2E1]<<std::endl;
	std::cout<<"JET-Electron-"<<k<<"th: pointing --> Electron_cutBased[indexJ2E1] = "<<(*Electron_cutBased)[indexJ2E1]<<std::endl;
	}
      if (indexJ2E2<0) continue;
      else{
	std::cout<<"JET-Electron-"<<k<<"th: pointing --> Electron_pt[indexJ2E2] = "<<(*Electron_pt)[indexJ2E2]<<std::endl;
	std::cout<<"JET-Electron-"<<k<<"th: pointing --> Electron_cutBased[indexJ2E2] = "<<(*Electron_cutBased)[indexJ2E2]<<std::endl;
      }
      std::cout<<std::endl;
    }
  }

  std::cout<<"== END Event =="<<std::endl;
  return;
}

std::pair<float,float> mhtjuProducerCppWorker::getHT(){

  math::XYZTLorentzVectorF ht(0,0,0,0);

  unsigned njet = (*nJet).Get()[0];
  //unsigned nelectron = (*nElectron).Get()[0];
  //unsigned nmuon = (*nMuon).Get()[0];

  //slimmedJets, i.e. ak4 PFJets CHS with JECs applied, after basic selection (pt > 15)
  for (unsigned i=0; i<njet; i++){

    //Number of associated lepton in jet
    unsigned jet_nMuons = (*Jet_nMuons)[i];
    unsigned jet_nElectrons = (*Jet_nElectrons)[i];
    //Jet kinematics
    float jet_pt = (*Jet_pt)[i];
    float jet_eta = fabs((*Jet_eta)[i]);
    float jet_phi = (*Jet_phi)[i];
    float jet_chHEF = (*Jet_chHEF)[i];
    float jet_neHEF = (*Jet_neHEF)[i];
    int jetpuID = (*Jet_puId)[i];

    if (jetpuID<4) continue;

    if (jet_nMuons>0 || jet_nElectrons>0){

      //We have only two pointer to the muon
      //index point to muon from jet
      int indexJ2M1 = (*Jet_muonIdx1)[i];
      int indexJ2M2 = (*Jet_muonIdx2)[i];
      //index point to electron from jet
      int indexJ2E1 = (*Jet_electronIdx1)[i];
      int indexJ2E2 = (*Jet_electronIdx2)[i];

      if ( indexJ2M1>=0 )
	if (  ( ( (*Muon_pt)[indexJ2M1]>5 && (*Muon_mediumId)[indexJ2M1] == 1) ) || ( ( (*Muon_mediumId)[indexJ2M1] == 1) && ( jet_chHEF < 0.1 || jet_neHEF<0.2 ) )  ) continue;
      if ( indexJ2M2>=0 )
	if (  ( ( (*Muon_pt)[indexJ2M2]>5 && (*Muon_mediumId)[indexJ2M2] == 1) ) || ( ( (*Muon_mediumId)[indexJ2M2] == 1) && ( jet_chHEF < 0.1 || jet_neHEF<0.2 ) )  ) continue;

      if ( indexJ2E1>=0 )
	if (  ( ( (*Electron_pt)[indexJ2E1]>15 && (*Electron_cutBased)[indexJ2E1] >= 1) ) || ( ( (*Electron_cutBased)[indexJ2E1] >= 1) && ( jet_chHEF < 0.1 || jet_neHEF<0.2 ) )  ) continue;
      if ( indexJ2E2>=0)
	if (  ( ( (*Electron_pt)[indexJ2E2]>15 && (*Electron_cutBased)[indexJ2E2] >= 1) ) || ( ( (*Electron_cutBased)[indexJ2E2] >= 1) && ( jet_chHEF < 0.1 || jet_neHEF<0.2 ) )  ) continue;
    }
    
    if (jet_pt<30 && jet_eta>2.5) continue;
    
    ht += math::PtEtaPhiMLorentzVectorF(jet_pt,0,jet_phi,0);
  }
  
  return std::pair<float,float>(ht.Pt(),ht.Phi()); 
}

std::pair<float,float> mhtjuProducerCppWorker::getHTv1(){

  int Jet_clean[100];
  unsigned njet = (*nJet).Get()[0];
  unsigned nmuon = (*nMuon).Get()[0];
  unsigned nelectron = (*nElectron).Get()[0];

  for( unsigned jet = 0; jet < njet; jet++)   {
    Jet_clean[jet] = 1;      // default value: jet is supposed to be a good one
    if( fabs((*Jet_eta)[jet]) > 2.5 )  continue;
    
    // check nearest mu
    float DRmin = 999.;
    for( unsigned jmu = 0; jmu < nmuon; jmu++)   {
      if( (*Muon_mediumId)[jmu] == 0 ) continue; // only good muons
      if( (*Muon_pt)[jmu] < 5. )       continue;
      float deta =  (*Jet_eta)[jet] - (*Muon_eta)[jmu];
      float dphi =  fabs( (*Jet_phi)[jet] - (*Muon_phi)[jmu]);
      if(dphi > 3.1416 ) dphi = 6.2832 - dphi;
      float DR = sqrt(deta*deta + dphi*dphi);
      if( DR < DRmin ) DRmin = DR;
    } // next muon                                                                                                                                       

    // check nearest electron
    for( unsigned je = 0; je < nelectron; je++)   {
      if( (*Electron_cutBased)[je] == 0 )  continue; // only good electron
      if( (*Electron_pt)[je] < 15. )       continue;
      float deta =  (*Jet_eta)[jet] - (*Electron_eta)[je];
      float dphi =  fabs( (*Jet_phi)[jet] - (*Electron_phi)[je]);
      if(dphi > 3.1416 ) dphi = 6.2832 - dphi;
      float DR = sqrt(deta*deta + dphi*dphi);
      if( DR < DRmin ) DRmin = DR;
    } // next electron
    if( DRmin > 0.4 ) continue; // no near lepton; jet is clean
    // check energy fractions
    Jet_clean[jet] = 0;
    if( (*Jet_chHEF)[jet] > 0.1 )                         Jet_clean[jet] = 1;
    if( (*Jet_chHEF)[jet] < 0.1 && (*Jet_neHEF)[jet] > 0.2 ) Jet_clean[jet] = 1;
  } // next jet     

  // HT computation -------------------- 
  math::XYZTLorentzVectorF ht(0,0,0,0);
  for( unsigned jet = 0; jet < njet; jet++)   { // loop on jets ----------
    if( (*Jet_pt)[jet] < 30.)    continue;
    if( (*Jet_puId)[jet]  == 4 ) continue;  // jet cleaning...                                                                                           
    if( Jet_clean[jet] == 0 ) continue;
    if( fabs((*Jet_eta)[jet]) > 2.5  ) continue;
    ht += math::PtEtaPhiMLorentzVectorF((*Jet_pt)[jet],0,(*Jet_phi)[jet],0);
  }   // next jet ---------------------------------

  return std::pair<float,float>(ht.Pt(),ht.Phi());
}
