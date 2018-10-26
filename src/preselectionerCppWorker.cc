#include "../interface/preselectionerCppWorker.h"
using namespace std;

int preselectionerCppWorker::countEvent(){
  return 1;
}

float preselectionerCppWorker::ptZCorr(){
  float wgtZ = 1.;
  unsigned nGen = (*nGenPart).Get()[0];
  int nGenZ = 0;
  for( unsigned j = 0; j < nGen; j++)   {
    if (  (*GenPart_pdgId)[j] != 23 )    continue;
    nGenZ++;
    float ptZ =  (*GenPart_pt)[j];
    if( nGenZ > 1) continue;
    if ( ptZ < 20.                ) wgtZ = 1.2;
    if ( ptZ >= 20. && ptZ < 30.  ) wgtZ = 1.;
    if ( ptZ >= 30. && ptZ < 40.  ) wgtZ = 0.75;
    if ( ptZ >= 40. && ptZ < 50.  ) wgtZ = 0.65;
    if ( ptZ >= 50. && ptZ < 200. ) wgtZ = 0.65 - 0.00034*ptZ;
    if ( ptZ >= 200.              ) wgtZ = 0.6;
  }
  return wgtZ;
}
