import os

def addSampleWeight(sampleDic,key,Sample,Weight): #samples ; tag ; sample name ; additional weights
    ## discreetized additional weight management
    ## add new weight entry
    if not 'weights' in sampleDic[key] :
        sampleDic[key]['weights'] = {}
        ## evaluate how many species
        templist = map( lambda x : os.path.basename(x).split('_',1)[-1].replace('.root','').split('__part')[0] ,  sampleDic[key]['name'] )
        templist = list(set(templist))

        ## register weights for specific process
        for i,tag in enumerate(templist): sampleDic[key]['weights'][tag] = '(1.)'

    sampleDic[key]['weights'][Sample] = '%s*(%s)' %( sampleDic[key]['weights'][Sample] , Weight )
    pass

def nanoGetSampleFiles(inputDir , sample , isFake=False):

    if 'Run' not in sample:
        inputDir = inputDir+'/'+sample
    elif 'Run' in sample :
        inputDir = inputDir+'/Run2016_'+sample.split('_')[0] if not isFake else inputDir+'/Run2016_'+sample.split('_')[0]+'_fake/'
        
    return [ inputDir+'/'+x for x in os.listdir(inputDir) if 'nanoLatino_'+sample+'__' in x ]
