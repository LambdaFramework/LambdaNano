#include "PhysicsTools/NanoAODTools/interface/WeightCalculatorFromHistogram.h"
#include "PhysicsTools/NanoAODTools/interface/ReduceMantissa.h"
#include "PhysicsTools/NanoAODTools/interface/LeptonEfficiencyCorrectorCppWorker.h"

WeightCalculatorFromHistogram wcalc;
ReduceMantissaToNbitsRounding red(12);
LeptonEfficiencyCorrectorCppWorker lepSF;
