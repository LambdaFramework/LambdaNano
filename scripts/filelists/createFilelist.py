#!/bin/python

import os, sys
from collections import OrderedDict

base="/media/shoh/02A1ACF427292FC0/nanov5"

if os.getcwd().split('/')[1] == 'lustre' : base="/lustre/cmswork/hoh/Homebrew_latino/data"

dirlist=OrderedDict({
    '2016' : {
        'MCdir' : base + "/Summer16_102X_nAODv5_Full2016v6/MCl1loose2016v6__MCCorr2016v6__l2loose__l2tightOR2016v6" ,
        'DATAdir' : base + "/Run2016_102X_nAODv5_Full2016v6/DATAl1loose2016v6__l2loose__l2tightOR2016v6" ,
        'FAKEdir' : base + "/Run2016_102X_nAODv5_Full2016v6_ForNewWPs/DATAl1loose2016v6__l2loose__fakeW"
    },
    '2017' : {
        'MCdir'	: base + "/Fall2017_102X_nAODv5_Full2017v6/MCl1loose2017v6__MCCorr2017v6__l2loose__l2tightOR2017v6" ,
        'DATAdir' : base + "/Run2017_102X_nAODv5_Full2017v6/DATAl1loose2017v6__l2loose__l2tightOR2017v6" ,
        'FAKEdir' : base + "/Run2017_102X_nAODv5_Full2017v6_ForNewWPs/DATAl1loose2017v6__l2loose__fakeW"
    },
    '2018' : {
        'MCdir' : base + "/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6" ,
        'DATAdir' : base + "/Run2018_102X_nAODv6_Full2018v6/DATAl1loose2018v6__l2loose__l2tightOR2018v6" ,
        'FAKEdir' : base + "/Run2018_102X_nAODv6_Full2018v6_ForNewWPs/DATAl1loose2018v6__l2loose__fakeW"
    }
})

for ilist in dirlist:
    year=ilist ; MCdir=dirlist[ilist]['MCdir'] ; DATAdir=dirlist[ilist]['DATAdir'] ; FAKEdir=dirlist[ilist]['FAKEdir']
    
    if os.path.isdir('%s/%s' %( os.getcwd() , year ) ):
        os.system('rm -r %s/%s' %( os.getcwd() , year ))
    
    os.mkdir('%s/%s' %( os.getcwd() , year ) )

    MClist   = list( dict.fromkeys([ x.replace('nanoLatino_','').split('__')[0] for x in os.listdir(MCdir) ]) )
    DATAlist = list( dict.fromkeys([ x.replace('nanoLatino_','').split('__')[0].split('_')[0] for x in os.listdir(DATAdir) ]) )
    FAKElist = map( lambda x: "%s_fake" %x , list(dict.fromkeys([ x.replace('nanoLatino_','').split('__')[0].split('_')[0] for x in os.listdir(FAKEdir) ])) )

    for i, ilist in enumerate([ MClist , DATAlist , FAKElist ]) :
        if i == 0 : directory=MCdir
        if i == 1 : directory=DATAdir
        if i == 2 : directory=FAKEdir
        for iprocess in ilist:
            print('creating filelist for process %s for year %s ' %(iprocess,year) )
            if i == 0:
                os.system('ls %s/*_%s__* > %s/%s.txt' %( directory , iprocess if i !=2 else iprocess.split('_')[0] , year , iprocess  ) )
            else:
                os.system('ls %s/*%s* > %s/%s.txt' %( directory , iprocess if i !=2 else iprocess.split('_')[0] , year , iprocess  ) )
