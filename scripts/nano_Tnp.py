#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.modules.analysis.TnP.addTnpTree import addTnpTree

Tnpler = lambda : addTnpTree( '2016' , 'Electron' )

p=PostProcessor( "." \
                 , [ "%s/test/WHWW.root" % os.environ['NANOAODTOOLS_BASE'] ] \
                 , "Electron_pt>15" \
                 , "%s/scripts/data/tnp.txt" % os.environ['NANOAODTOOLS_BASE'] \
                 , [ Tnpler() ] \
                 , provenance=True \
)

p.run()
