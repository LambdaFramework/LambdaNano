void functions() {
  //gSystem->Load("libMathMore");
  cout<<"  C++ functions loaded"<<endl;
}

float deltaPhi(float phi1, float phi2) {
  float PHI = fabs(phi1-phi2);
  if (PHI<=3.14159265)
    return PHI;
  else
    return 2*3.14159265-PHI;
}

float deltaR(float phi1, float eta1, float phi2, float eta2) {
  //return sqrt((eta2-eta1)**2+deltaPhi(phi1,phi2)**2);
  return sqrt( pow((eta2-eta1),2) + pow(deltaPhi(phi1,phi2),2) );
}

float deltaEta(float eta1, float eta2) {
  return fabs(eta1 - eta2);
}


//float vectorSumPhi(float px1, float py1, float px2, float py2){
//  float phi = atan((py1+py2)/(px1+px2));
//  if ((px1+px2)>0) return phi;
//  else if ((py1+py2)>0) return phi + 3.14159265;
//  else return phi - 3.14159265;
//}


//float vectorSumPt(float pt1, float phi1, float pt2, float phi2){
//  return sqrt( pow(pt1*cos(phi1) + pt2*cos(phi2),2) +
//	       pow(pt1*sin(phi1) + pt2*sin(phi2),2) );
//}

//float vectorSum3Pt(float pt1, float phi1, float pt2, float phi2,float pt3, float phi3){
//  return sqrt( pow(pt1*cos(phi1) + pt2*cos(phi2) + pt3*cos(phi3),2) +
//	       pow(pt1*sin(phi1) + pt2*sin(phi2) + pt3*sin(phi3),2) );
//}

//float vectorSumMass(float px1, float py1, float pz1, float px2, float py2, float pz2) {
//  double E1 = sqrt(px1**2 + py1**2 + pz1**2);
//  double E2 = sqrt(px2**2 + py2**2 + pz2**2);
//  double cosTheta = (px1*px2 + py1*py2 + pz1*pz2)/ (E1*E2);
//  return sqrt(2*E1*E2*(1-cosTheta));
//}

float transverseMass(float lepPt, float lepPhi, float met,  float metPhi) {
  double cosDPhi = cos(deltaPhi(lepPhi,metPhi));
  return sqrt(2*lepPt*met*(1-cosDPhi));
}

float invariantMass(float p1_pt, float p1_eta, float p1_phi, float p1_mass, float p2_pt, float p2_eta, float p2_phi, float p2_mass) {
  if(p1_pt<0. || p2_pt<0.) return -1.;
  TLorentzVector p1;
  TLorentzVector p2;
  p1.SetPtEtaPhiM(p1_pt, p1_eta, p1_phi, p1_mass);
  p2.SetPtEtaPhiM(p2_pt, p2_eta, p2_phi, p2_mass);
  return (p1+p2).M();
}

float invariantMassPt(float p1_pt, float p1_eta, float p1_phi, float p1_mass, float p2_pt, float p2_eta, float p2_phi, float p2_mass) {
  if(p1_pt<0. || p2_pt<0.) return -1.;
  TLorentzVector p1;
  TLorentzVector p2;
  p1.SetPtEtaPhiM(p1_pt, p1_eta, p1_phi, p1_mass);
  p2.SetPtEtaPhiM(p2_pt, p2_eta, p2_phi, p2_mass);
  return (p1+p2).Pt();
}

float invariantDoubleMass(float Z_pt, float Z_eta, float Z_phi, float jet1_pt, float jet1_eta, float jet1_phi, float jet2_pt, float jet2_eta, float jet2_phi) {
  if(jet1_pt<0. || jet2_pt<0.) return -1.;
  TLorentzVector j1;
  TLorentzVector j2;
  TLorentzVector Z;
  Z.SetPtEtaPhiM(Z_pt, Z_eta, Z_phi, 91.);
  j1.SetPtEtaPhiM(jet1_pt, jet1_eta, jet1_phi, 5.);
  j2.SetPtEtaPhiM(jet2_pt, jet2_eta, jet2_phi, 5.);
  return (j1+j2+Z).M();
}
//float caloMet1l(float pt, float phi, float met, float metPhi){
//  return sqrt( pow(pt*cos(phi) + met*cos(metPhi),2) +
//	       pow(pt*sin(phi) + met*sin(metPhi),2));
//}

//float caloMet2l(float pt1, float phi1, float pt2, float phi2, float met, float metPhi){
//  return sqrt( pow(pt1*cos(phi1) + pt2*cos(phi2) + met*cos(metPhi),2) +
//	       pow(pt1*sin(phi1) + pt2*sin(phi2) + met*sin(metPhi),2));
//}

//float A_tmass(float met_pt, float met_phi, float j_pt, float j_eta, float j_phi, float j_mass) {
//  TLorentzVector h, Z;
//  h.SetPtEtaPhiM(j_pt, j_eta, j_phi, j_mass);
//  Z.SetPtEtaPhiM(met_pt, 0., met_phi, 0.);
//  return TMath::Sqrt( 2.*h.Energy()*met_pt*(1.-TMath::Cos( h.DeltaPhi(Z) )) );
//}

//float A_cmass(float met_pt, float met_phi, float j_pt, float j_eta, float j_phi, float j_mass) {
//  TLorentzVector h, Z;
//  h.SetPtEtaPhiM(j_pt, j_eta, j_phi, j_mass);
//  Z.SetPtEtaPhiM(met_pt, -j_eta, met_phi, 91.18);
//  //Z.SetPz(-h.Pz());
//  return (h+Z).M();
//}

//float topMass(float pt1, float eta1, float phi1, float mass1, float csv1, float pt2, float eta2, float phi2, float mass2, float csv2, float pt3, float eta3, float phi3, float mass3, float csv3, float pt4, float eta4, float phi4, float mass4, float csv4) {
//  TLorentzVector jet1, jet2, jet3, jet4, bjet1, bjet2, ljet1, ljet2;
//  jet1.SetPtEtaPhiM(pt1, eta1, phi1, mass1);
//  jet2.SetPtEtaPhiM(pt2, eta2, phi2, mass2);
//  jet3.SetPtEtaPhiM(pt3, eta3, phi3, mass3);
//  jet4.SetPtEtaPhiM(pt4, eta4, phi4, mass4);
//  
//  std::vector<std::pair<float, TLorentzVector> > jets;
//  jets.push_back(std::make_pair<float, TLorentzVector>(csv1, jet1));
//  jets.push_back(std::make_pair<float, TLorentzVector>(csv2, jet2));
//  jets.push_back(std::make_pair<float, TLorentzVector>(csv3, jet3));
//  jets.push_back(std::make_pair<float, TLorentzVector>(csv4, jet4));
//  std::sort(jets.begin(), jets.end());
//  
//  bjet1 = jets[0].second();
//  bjet2 = jets[1].second();
//  ljet1 = jets[2].second();
//  ljet2 = jets[3].second();
//  
//  TLorentzVector W = ljet1 + ljet2;
//  
//  TLorentzVector t1 = W + bjet1;
//  TLorentzVector t2 = W + bjet2;
//  
//  if(t1.Mass()-175 < t2.Mass()-175) {return t1.Mass();}
//  else {return t2.Mass();}
//  
//}

float W(float lepton_pt, float lepton_eta, float lepton_phi, float lepton_mass, float met_pt, float met_phi) {
  TLorentzVector lepton;
  TLorentzVector met;
  TLorentzVector neutrino;

  lepton.SetPtEtaPhiM(lepton_pt, lepton_eta, lepton_phi, lepton_mass);
  met.SetPtEtaPhiM(met_pt, 0, met_phi, 0);
  
  float pz = 0.;
  float a = 80.4*80.4 - lepton.M()*lepton.M() + 2.*lepton.Px()*met.Px() + 2.*lepton.Py()*met.Py();
  float A = 4*( lepton.E()*lepton.E() - lepton.Pz()*lepton.Pz() );
  float B = -4*a*lepton.Pz();
  float C = 4*lepton.E()*lepton.E() * (met.Px()*met.Px()  + met.Py()*met.Px()) - a*a;
  float D = B*B - 4*A*C;
  if(D>0) {
    float s1 = (-B+sqrt(D))/(2*A);
    float s2 = (-B-sqrt(D))/(2*A);
    if(abs(s1) < abs(s2)) {
      pz = s1;
    }
    else {
      pz = s2;
    }
  }
  else {
    pz = -B/(2*A);
  }
  neutrino.SetPxPyPzE(met.Px(), met.Py(), pz, sqrt(met.Px()*met.Px() + met.Py()*met.Py() + pz*pz));
  
  TLorentzVector X;
  X = lepton + neutrino;
  return X.M();
}

float XWh(float lepton_pt, float lepton_eta, float lepton_phi, float met_pt, float met_phi, float jet_pt, float jet_eta, float jet_phi, float jet_mass) {
  TLorentzVector lepton;
  TLorentzVector met;
  TLorentzVector jet;
  TLorentzVector neutrino;

  lepton.SetPtEtaPhiM(lepton_pt, lepton_eta, lepton_phi, 0);
  met.SetPtEtaPhiM(met_pt, 0, met_phi, 0);
  jet.SetPtEtaPhiM(jet_pt, jet_eta, jet_phi, jet_mass);
  
  float pz = 0.;
  float a = 80.4*80.4 - lepton.M()*lepton.M() + 2.*lepton.Px()*met.Px() + 2.*lepton.Py()*met.Py();
  float A = 4*( lepton.E()*lepton.E() - lepton.Pz()*lepton.Pz() );
  float B = -4*a*lepton.Pz();
  float C = 4*lepton.E()*lepton.E() * (met.Px()*met.Px()  + met.Py()*met.Px()) - a*a;
  float D = B*B - 4*A*C;
  if(D>0) {
    float s1 = (-B+sqrt(D))/(2*A);
    float s2 = (-B-sqrt(D))/(2*A);
    if(abs(s1) < abs(s2)) {
      pz = s1;
    }
    else {
      pz = s2;
    }
  }
  else {
    pz = -B/(2*A);
  }
  neutrino.SetPxPyPzE(met.Px(), met.Py(), pz, sqrt(met.Pt()*met.Pt() + pz*pz));
  
  TLorentzVector X;
  X = neutrino + lepton + jet;
  met.SetPz(lepton.Pz());
  X = met + lepton + jet;
  return X.M();
}

/*
float HTpt(int njet, float* jet_pt, float* jet_phi){

  TLorentzVector ht;
  TLorentzVector HT;
  for (unsigned i=0; i<njet; i++){
    ht.SetPtEtaPhiE(0,0,0,0);
    ht.SetPtEtaPhiE(jet_pt[i],0,jet_phi[i],0);
    HT += ht;
  }
  return HT.Pt();
}
*/
