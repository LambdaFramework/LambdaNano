#!/bin/python
import os
from PhysicsTools.NanoAODTools.LambPlot.plotConfiguration.WH_SS.Full2016nanov6.variables import variables
from PhysicsTools.NanoAODTools.LambPlot.plotConfiguration.WH_SS.Full2016nanov6.cuts import cuts

base=os.environ['NANOAODTOOLS_BASE']

iyear="2016"
ivar="nJet"
ir="dummy"

#test
os.system( 'python %s/python/LambPlot/scripts/whss.py -v %s -r %s -y %s -z "WZ" -z "VgS"' %( base , ivar , ir , iyear ) )
