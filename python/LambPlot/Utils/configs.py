from PhysicsTools.NanoAODTools.LambPlot.Utils.color import *

import os
import importlib

class Config(object):

    def __init__(self,era):

        #Analysis parameters
        self._era = era
        self._year = era.split('_')[-1]
        self.modules={}
        if self._year == '2016' : self._lumi = 35800. #pb-1
        if self._year == '2017' : self._lumi = 41500. #pb-1
        if self._year == '2018' : self._lumi = 68000. #pb-1
        self._groupPlot = {}

        # import the module
        basePath   = 'PhysicsTools.NanoAODTools.LambPlot.plotConfiguration.WH_SS.Full%snanov6' %self._year
        samples_   = importlib.import_module('%s.samples' %basePath )
        cuts_      = importlib.import_module('%s.cuts' %basePath )
        aliases_   = importlib.import_module('%s.aliases' %basePath )
        variables_ = importlib.import_module('%s.variables' %basePath )
        plot_      = importlib.import_module('%s.plot' %basePath )

        self.modules['samples'] = samples_.samples
        self.modules['selection'] = cuts_.cuts
        self.modules['aliases'] = aliases_.aliases
        self.modules['variables'] = variables_.variables
        self.modules['groupPlot'] = plot_.groupPlot
        self.ntuple = samples_.mcDirectory

    def getModule(self, name):
        return self.modules[name]

    def register(self, samples_ ):
        groupPlot = self.modules['groupPlot']
        # build group list structure
        for i, igroup in enumerate(samples_):
            if igroup == 'DATA': continue
            species = groupPlot[igroup]['isSignal']
            self._groupPlot[igroup]              = {}            
            self._groupPlot[igroup]['order']     = i
            self._groupPlot[igroup]['samples']   = groupPlot[igroup]['samples']
            self._groupPlot[igroup]['fillcolor'] = groupPlot[igroup]['color'] if species == 0 else 8
            self._groupPlot[igroup]['fillstyle'] = 1001 if species == 0 else 3003
            self._groupPlot[igroup]['linecolor'] = 1 #groupPlot[igroup]['color']
            self._groupPlot[igroup]['linewidth'] = 2
            self._groupPlot[igroup]['linestyle'] = 1
            self._groupPlot[igroup]['label']     = groupPlot[igroup]['nameHR']
            self._groupPlot[igroup]['weight']    = 1.
            self._groupPlot[igroup]['plot']      = True

        #DATA
        if 'DATA' in samples_:
            self._groupPlot['DATA'] ={}
            self._groupPlot['DATA']['order']     = 0
            self._groupPlot['DATA']['samples']   = groupPlot['DATA']['samples']
	    self._groupPlot['DATA']['fillcolor'] = groupPlot['DATA']['color']
            self._groupPlot['DATA']['fillstyle'] = 1
            self._groupPlot['DATA']['linecolor'] = 1
            self._groupPlot['DATA']['linewidth'] = 2
            self._groupPlot['DATA']['linestyle'] = 1
            self._groupPlot['DATA']['label']     = groupPlot['DATA']['nameHR']
            self._groupPlot['DATA']['weight']    = 1.
            self._groupPlot['DATA']['plot']      = True

        
        #BKGSUM
        self._groupPlot['BkgSum'] ={}
        self._groupPlot['BkgSum']['order']     = 0
        self._groupPlot['BkgSum']['samples']   = []
        self._groupPlot['BkgSum']['fillcolor'] = 1
        self._groupPlot['BkgSum']['fillstyle'] = 1001
        self._groupPlot['BkgSum']['linecolor'] = 1
        self._groupPlot['BkgSum']['linewidth'] = 2
        self._groupPlot['BkgSum']['linestyle'] = 1
        self._groupPlot['BkgSum']['label']     = 'MC. stat.'
        self._groupPlot['BkgSum']['weight']    = 1.
        self._groupPlot['BkgSum']['plot']      = True
        

    def era(self):
        return self._era
    def lumi(self):
        return self._lumi
    def getGroupPlot(self):
        return self._groupPlot

    def summary(self):

        print "-"*80
        print YELLOW+"Era configured : "+ENDC, OKGREEN+ self._year +ENDC
        print YELLOW+"Integrated luminosity configured : "+ENDC, OKGREEN+str( self._lumi ), " pb/-1"+ENDC
        print YELLOW+"NTUPLE configured : "+ENDC, OKGREEN+ self.ntuple +ENDC
        print YELLOW+"Imported Modules configured : "+ENDC, self.modules.keys()
        print "-"*80
