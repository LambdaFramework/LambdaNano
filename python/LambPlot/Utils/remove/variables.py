#!/bin/python
#import PhysicsTools.NanoAODTools.Config as cfg
from PhysicsTools.NanoAODTools.plotter.lambPlot import cfg
import importlib
import sys

#GEN
from PhysicsTools.NanoAODTools.postprocessing.analysis.Run2_16.NanoV4.genvariables import br_all as Genbr

var = importlib.import_module('PhysicsTools.NanoAODTools.postprocessing.analysis.'+cfg.era()+'.'+cfg.nanover()+'.variables')
br_all = var.br_all

var_template={}
variable={}
for ibranch in br_all+Genbr:
    var_template["%s[N]"%ibranch.name() if ibranch.dimen()==1 else "%s"%ibranch.name()] = {}
    var_template["%s[N]"%ibranch.name() if ibranch.dimen()==1 else "%s"%ibranch.name()]["title"] = ibranch.titleX()
    var_template["%s[N]"%ibranch.name() if ibranch.dimen()==1 else "%s"%ibranch.name()]["titleY"] = ibranch.titleY()
    var_template["%s[N]"%ibranch.name() if ibranch.dimen()==1 else "%s"%ibranch.name()]["nbins"] = ibranch.nbins()
    var_template["%s[N]"%ibranch.name() if ibranch.dimen()==1 else "%s"%ibranch.name()]["min"] = ibranch.mins()
    var_template["%s[N]"%ibranch.name() if ibranch.dimen()==1 else "%s"%ibranch.name()]["max"] = ibranch.maxs()
    var_template["%s[N]"%ibranch.name() if ibranch.dimen()==1 else "%s"%ibranch.name()]["log"] = ibranch.log()
    pass

################################################################################
##                              ADD-ON from MODULE
################################################################################
##Top up variables
#PV_npvs
var_template["PV_npvs"] = {}
var_template["PV_npvs"]["title"] = "Number of Reconstructed Primary Vertices"
var_template["PV_npvs"]["titleY"] = "Events / XXX"
var_template["PV_npvs"]["nbins"] = 100
var_template["PV_npvs"]["min"] = -0.5
var_template["PV_npvs"]["max"] = 99.5
var_template["PV_npvs"]["log"] = True

################################################################################
#                              COMPOSITE VARIABLE
################################################################################
#C_deltaRll
var_template["C_deltaRll"] = {}
var_template["C_deltaRll"]["title"] = "Reco #Delta R(Lep1,Lep2)"
var_template["C_deltaRll"]["titleY"] = "Events / XXX"
var_template["C_deltaRll"]["nbins"] = 30
var_template["C_deltaRll"]["min"] = 0.
var_template["C_deltaRll"]["max"] = 6
var_template["C_deltaRll"]["log"] = True

#C_deltaPhill
var_template["C_deltaPhill"] = {}
var_template["C_deltaPhill"]["title"] = "Reco #Delta #phi(Lep1,Lep2)"
var_template["C_deltaPhill"]["titleY"] = "Events / XXX"
var_template["C_deltaPhill"]["nbins"] = 32
var_template["C_deltaPhill"]["min"] = 0.
var_template["C_deltaPhill"]["max"] = 3.2
var_template["C_deltaPhill"]["log"] = True

#deltaEtall
var_template["C_deltaEtall"] = {}
var_template["C_deltaEtall"]["title"] = "Reco #Delta #eta(Lep1,Lep2)"
var_template["C_deltaEtall"]["titleY"] = "Events / XXX"
var_template["C_deltaEtall"]["nbins"] = 32
var_template["C_deltaEtall"]["min"] = 0.
var_template["C_deltaEtall"]["max"] = 3.2
var_template["C_deltaEtall"]["log"] = True

#C_deltaRjj
var_template["C_deltaRjj"] = {}
var_template["C_deltaRjj"]["title"] = "Reco #Delta R(j1,j2)"
var_template["C_deltaRjj"]["titleY"] = "Events / XXX"
var_template["C_deltaRjj"]["nbins"] = 30
var_template["C_deltaRjj"]["min"] = 0.
var_template["C_deltaRjj"]["max"] = 6
var_template["C_deltaRjj"]["log"] = True

#C_deltaPhijj
var_template["C_deltaPhijj"] = {}
var_template["C_deltaPhijj"]["title"] = "Reco #Delta #phi(j1,j2)"
var_template["C_deltaPhijj"]["titleY"] = "Events / XXX"
var_template["C_deltaPhijj"]["nbins"] = 32
var_template["C_deltaPhijj"]["min"] = 0.
var_template["C_deltaPhijj"]["max"] = 3.2
var_template["C_deltaPhijj"]["log"] = True

#deltajj
var_template["C_deltaEtajj"] = {}
var_template["C_deltaEtajj"]["title"] = "Reco #Delta #eta(j1,j2)"
var_template["C_deltaEtajj"]["titleY"] = "Events / XXX"
var_template["C_deltaEtajj"]["nbins"] = 32
var_template["C_deltaEtajj"]["min"] = 0.
var_template["C_deltaEtajj"]["max"] = 3.2
var_template["C_deltaEtajj"]["log"] = True

############################################
############################################
#Vllmass
var_template["C_Vllmass"] = {}
var_template["C_Vllmass"]["title"] = "Vllmass [GeV/c^{2}]"
var_template["C_Vllmass"]["titleY"] = "Events / XXX GeV/c^{2}"
var_template["C_Vllmass"]["nbins"] = 100
var_template["C_Vllmass"]["min"] = 0.
var_template["C_Vllmass"]["max"] = 200.
var_template["C_Vllmass"]["log"] = True

#Vjjmass
var_template["C_Vjjmass"] = {}
var_template["C_Vjjmass"]["title"] = "Vjjmass [GeV/c^{2}]"
var_template["C_Vjjmass"]["titleY"] = "Events / XXX GeV/c^{2}"
var_template["C_Vjjmass"]["nbins"] = 100
var_template["C_Vjjmass"]["min"] = 0.
var_template["C_Vjjmass"]["max"] = 200.
var_template["C_Vjjmass"]["log"] = True

#Vllpt
var_template["C_Vllpt"] = {}
var_template["C_Vllpt"]["title"] = "Vllpt [GeV]"
var_template["C_Vllpt"]["titleY"] = "Events / XXX GeV"
var_template["C_Vllpt"]["nbins"] = 100
var_template["C_Vllpt"]["min"] = 0.
var_template["C_Vllpt"]["max"] = 200.
var_template["C_Vllpt"]["log"] = True

#Vjjpt
var_template["C_Vjjpt"] = {}
var_template["C_Vjjpt"]["title"] = "Vjjpt [GeV]"
var_template["C_Vjjpt"]["titleY"] = "Events / XXX GeV"
var_template["C_Vjjpt"]["nbins"] = 100
var_template["C_Vjjpt"]["min"] = 0.
var_template["C_Vjjpt"]["max"] = 500.
var_template["C_Vjjpt"]["log"] = True

################################################################################
################################################################################

for n, v in var_template.iteritems():
    if '[N]' in n:
        for i in range(0, 4):
            ni = n.replace('[N]', "[%d]" % i)
            variable[ni] = v.copy()
            variable[ni]['title'] = variable[ni]['title'].replace('[N]', "%d" % i)
            variable[ni]['titleY'] = variable[ni]['titleY'].replace('XXX', "%s" % ( (variable[ni]['max'] - variable[ni]['min'])/variable[ni]['nbins'] ) )
    else:
        variable[n] = v.copy()
        variable[n]['titleY'] = variable[n]['titleY'].replace('XXX', "%s" % ( (variable[n]['max'] - variable[n]['min'])/variable[n]['nbins'] ) )
