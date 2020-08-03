# Lambda
Nanoaod Plotter

DEVELOPING, DO NOT USE IT 

## Setup With NanoAODTools tools
```
git clone https://github.com/LambdaFramework/nanoAOD-tools.git NanoAODTools
cd NanoAODTools
bash standalone/env_standalone.sh build
source standalone/env_standalone.sh
cd python
git clone https://github.com/LambdaFramework/LambPlot.git -b V3
```

## Setup standalone
```
git clone https://github.com/LambdaFramework/LambPlot.git -b V3
```

## Plotting on background with selection:
```
python lambPlot.py -v Vmass -c OSmumu
```

## Plotting on signal process:
```
python lambPlot.py -v S_RecoL1L2DeltaR -c Reco-mumu -s
```
