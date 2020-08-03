HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
YELLOW = '\033[33m'

#process color
scheme={
    #bkg
    'DYJetsToLL'    : { 'order' : 1  , 'fillcolor' : 418 , 'fillstyle' : 1001 , 'label' : 'Z(ll) + jets'                                     },
    'DYJetsToLL_HT' : { 'order' : 1  , 'fillcolor' : 418 , 'fillstyle' : 1001 , 'label' : 'Z(ll) + jets'                                     },
    'DYJetsToLL_Pt' : { 'order' : 2  , 'fillcolor' : 418 , 'fillstyle' : 1001 , 'label' : 'Z(ll) + jets'                                     },
    'WJetsToLNu'    : { 'order' : 3  , 'fillcolor' : 881 , 'fillstyle' : 1001 , 'label' : 'W(l#nu) + jets'                                   },
    'WJetsToLNu_HT' : { 'order' : 3  , 'fillcolor' : 881 , 'fillstyle' : 1001 , 'label' : 'W(l#nu) + jets'                                   },
    'TTbar'         : { 'order' : 4  , 'fillcolor' : 798 , 'fillstyle' : 1001 , 'label' : 't#bar{t}'                                         },
    'ST'      	    : { 'order' : 5  , 'fillcolor' : 801 , 'fillstyle' : 1001 , 'label' : 'ST'                                               },
    'VZ'      	    : { 'order' : 6  , 'fillcolor' : 602 , 'fillstyle' : 1001 , 'label' : 'VZ'                                               },
    'WW'      	    : { 'order' : 7  , 'fillcolor' : 41  , 'fillstyle' : 1001 , 'label' : 'WW'                                               },
    'Vg'      	    : { 'order' : 8  , 'fillcolor' : 42  , 'fillstyle' : 1001 , 'label' : 'Vg'                                               },
    'ttV'     	    : { 'order' : 9  , 'fillcolor' : 38  , 'fillstyle' : 1001 , 'label' : 'ttV'                                              },
    'VVV'     	    : { 'order' : 10 , 'fillcolor' : 46  , 'fillstyle' : 1001 , 'label' : 'VVV'                                              },
    'QCD'           : { 'order' : 11 , 'fillcolor' : 921 , 'fillstyle' : 1001 , 'label' : 'QCD'                                              },
    'tZq'           : { 'order' : 12 , 'fillcolor' : 30  , 'fillstyle' : 1001 , 'label' : 'tZq'                                              },
    'BkgSum'  	    : { 'order' : 0  , 'fillcolor' : 1   , 'fillstyle' : 1001 , 'label' : 'MC stat.'                                         },
    #signal
    'VH'            : { 'order' : 0  , 'fillcolor' : 3   , 'fillstyle' : 3003 , 'label' : 'VH'                                               },
    'WHWW'          : { 'order' : 0  , 'fillcolor' : 5   , 'fillstyle' : 3003 , 'label' : 'WHWW'                                             },
    'Whww'          : { 'order' : 0  , 'fillcolor' : 2   , 'fillstyle' : 3003 , 'label' : 'W^{#pm}H(l^{#pm}l^{#pm}#tilde{#nu}#tilde{#nu}jj)' },
    #data
    'data_obs'      : { 'order' : 0  , 'fillcolor' : 0   , 'fillstyle' : 1    , 'label' : 'Data'                                             },

}
