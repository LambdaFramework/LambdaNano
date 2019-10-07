# Lambda NanoAOD Tools (taken from cmsNanoaod tool)
Tools for working with NanoAOD (requiring only python + root, not CMSSW)

# UNDER DEVELOPMENT

## To-do list

  Rewritten lambdaframework, more consistent with postprocesser definition with plotter.

 - [x] Postprocesser interface (SiewYan)
 - [x] Chain of steps , specify which module is running (SiewYan+Matteo)
 - [x] Production, the correct ntuple use (SiewYan+Matteo)
 - [x] Collection of module:
    - [ ] Lepton maker (jet cleaning+WP compute) (SiewYan)
    - [ ] Muon maker (jet cleaning+WP compute) (Matteo)
    - [ ] Electron Maker (jet cleaning+WP compute) (SiewYan)
    - [ ] Jet maker (jet cleaning+WP compute) (Matteo)
    - [ ] MET maker (MET cleaner) (SiewYan)
    - [ ] Derived/analysis-specific Variable compute (need to declare in variables.py) (SiewYan + Matteo)
    - [ ] Trigger maker ? (SiewYan+Matteo)
 - [ ] Data folder hosting variable, SF, WP (SiewYan)
 - [x] Plotting (kinda taking care of...) (SiewYan)
    - [x] Augmenting to RDataFrame
 - [ ] Making datacard (Matteo)
 - [ ] Using combine limit (SiewYan)

## Checkout instructions: 
### standalone

You need to setup ```python 2.7``` and a recent ROOT version first.

    git clone git@github.com:LambdaFramework/LambdaNano.git NanoAODTools
    cd NanoAODTools
    bash standalone/env_standalone.sh build
    source standalone/env_standalone.sh

Repeat only the last command at the beginning of every session.

Please never commit neither the build directory, nor the empty init.py files created by the script.

### CMSSW env: CMSSW = ~~[ dev: CMSSW_10_2_13 ]~~ --> move to [ dev: CMSSW_9_4_13 ]

    cd $CMSSW_BASE/src
    git clone git@github.com:LambdaFramework/LambdaNano.git PhysicsTools/NanoAODTools
    cd PhysicsTools/NanoAODTools
    cmsenv
    scram b
    
### Checkout LambPlot package for plotting

    # Standalone
    cd NanoAODTools/python
    git clone git@github.com:LambdaFramework/LambPlot.git
    # or checkout dfdev to use RDataFrame, ITS FAST
    # git clone git@github.com:LambdaFramework/LambPlot.git -b dfdev
    
    # CMSSW
    cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools/python
    git clone git@github.com:LambdaFramework/LambPlot.git
    # or checkout dfdev to use RDataFrame, ITS FAST
    # git clone git@github.com:LambdaFramework/LambPlot.git -b dfdev
    
## General instructions to run the post-processing step

The postprocessing script sit in ``scripts`` folder, please consult the output by

    python scripts/postproc.py
