#!/bin/python
import os
from PhysicsTools.NanoAODTools.LambPlot.plotConfiguration.WH_SS.Full2016nanov6.variables import variables
from PhysicsTools.NanoAODTools.LambPlot.plotConfiguration.WH_SS.Full2016nanov6.cuts import cuts

base=os.environ['NANOAODTOOLS_BASE']
back = [ 'Fake' , 'WZ' , 'VgS' ]
for iyear in ['2016','2017','2018']:
    if iyear != '2016' : continue
    for icut in cuts:
        if icut != 'SSmumu' : continue
        for ivar in variables:
            if ivar != 'MinMjjl' : continue
            os.system( 'python %s/python/LambPlot/scripts/whss.py -v %s -r %s -y %s -z %s -z %s -z %s' %( base , ivar , icut , iyear , back[0] , back[1] , back[2] ) )
