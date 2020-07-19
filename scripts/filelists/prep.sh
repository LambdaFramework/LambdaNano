#!/bin/bash

set -e

samples="
DYJetsToLL_M-50-LO_ext2
DYJetsToLL_M-10to50-LO
TTTo2L2Nu
ST_s-channel
ST_t-channel_antitop
ST_t-channel_top
ST_tW_antitop
ST_tW_top
WWTo2L2Nu
WpWmJJ_EWK_noTop
GluGluWWTo2L2Nu_MCFM
Wg_MADGRAPHMLM
Zg
WZTo3LNu_mllmin01
WZTo2L2Q
ZZTo2L2Nu
ZZTo2L2Q
ZZTo4L
ZZZ
WZZ
WWZ
WWW
GluGluHToWWTo2L2NuPowheg_M125
VBFHToWWTo2L2Nu_M125
HZJ_HToWW_M125
ggZH_HToWW_M125
HWplusJ_HToWW_M125
HWminusJ_HToWW_M125
GluGluHToTauTau_M125
VBFHToTauTau_M125
HZJ_HToTauTau_M125
HWplusJ_HToTauTau_M125
HWminusJ_HToTauTau_M125
"

for sample in ${samples}
do
    #ls /media/shoh/02A1ACF427292FC0/nanov5/Summer16_102X_nAODv5_Full2016v6/MCl1loose2016v6__MCCorr2016v6__l2loose__l2tightOR2016v6/nanoLatino_${sample}__* > ${sample}.txt
    echo "\"${sample}\","
done
