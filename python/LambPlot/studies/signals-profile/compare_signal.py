#!/bin/python
import os

base=os.environ['NANOAODTOOLS_BASE']

for iyear in ['2016','2017','2018']:
    if iyear != '2016': continue
    for icut in [ 'Signal_incl_2j' , 'Signal_incl_1j' ] :
        for ivar in [ "mlljj20_whss" , "mlljj20_whss_bin3" , "MinMjjl" , "MinMjl" , "MindRjjl" , "MindRjl" ] :
            if ivar != 'mlljj20_whss': continue
            os.system( 'python %s/python/LambPlot/scripts/whss.py -o %s -v %s -r %s -y %s -s' %( base , icut , ivar , icut , iyear ) )
