import os
import json
from pprint import pprint
import time
import datetime
import urllib
#import urllib2
import subprocess

########## OPTIONS ##########

import optparse
usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-n', '--requestNumber',action='store', type='string', dest='requestNumber', default='')
parser.add_option('-f', '--fileName',     action='store', type='string', dest='fileName',      default='')
parser.add_option('-d', '--datasetName',  action='store', type='string', dest='datasetName',   default='')
parser.add_option('-q', '--queryDAS',     action='store_true',           dest='queryDAS',      default=False)
parser.add_option('-s', '--siteName',     action='store', type='string', dest='siteName',      default='')

(options, args) = parser.parse_args()


def get_dataset_info(url):

    res=urllib.urlopen(url)
    data = json.load(res)

    for i in range(0, len(data["phedex"]["dataset"])):
        if ('subscription' in data["phedex"]["dataset"][i]): 
            #print i
            #print  "dataset name = ", data["phedex"]["dataset"][i]["name"]
            #print data["phedex"]["dataset"][i]["files"]
            #print data["phedex"]["dataset"][i]["is_open"]
            #print  "percentage transferred files", data["phedex"]["dataset"][i]["subscription"][0]["percent_files"]
            #print  "request_id", data["phedex"]["dataset"][i]["subscription"][0]["request"]
            ds_name=data["phedex"]["dataset"][i]["name"]
            perc_tranf_files=data["phedex"]["dataset"][i]["subscription"][0]["percent_files"]
            request_id=data["phedex"]["dataset"][i]["subscription"][0]["request"]

            transf_list.append({'ds_name':str(ds_name),'perc_tranf_files':perc_tranf_files,'request_id':request_id})
        else: continue

    print '%-60s  %-18s  %8s'% ('dataset_name', 'trasferred_files(%)', 'request_id') 
    for i in range(0, len(transf_list)):
        print '%-60s  %-18s  %8d'% (transf_list[i]['ds_name'], transf_list[i]['perc_tranf_files'], transf_list[i]['request_id']) 
    return transf_list


def get_transf_files(transf_list):
    print "#############################"
    # print "find all files, regardless of the site"
    tt=time.strftime("%d%m%Y_%H%M%S")
    f=open('/tmp/dataset_files_'+tt, 'a')
    for i in range(0, len(transf_list)):
        ds_name=transf_list[i]['ds_name']
        f.write('datasetname = '+ds_name+'\n')
        url_repl='https://cmsweb.cern.ch/phedex/datasvc/json/prod/filereplicas?dataset='+ds_name
        res_repl=urllib.urlopen(url_repl)
        data_repl=json.load(res_repl)
        for i in range(0, len(data_repl["phedex"]["block"])):
            for j in range (0, len(data_repl["phedex"]["block"][i]["file"])): 
                file_name=data_repl["phedex"]["block"][i]["file"][j]["name"]
                f.write(file_name+'\n')
        
        if options.queryDAS:
            proc = subprocess.Popen('python batch/das_client.py --query=\"dataset dataset=%s | grep dataset.nevents\" --limit=0'%ds_name, stdout=subprocess.PIPE, shell=True)
            (nevents, err) = proc.communicate()
            f.write(nevents+'\n')
            
        f.write('\n')
    pass

    f.close()
    print "filelist saved in ",'/tmp/dataset_files_'+tt


def main():
    
    if options.queryDAS:
        os.system('voms-proxy-init --voms cms')
    
    if options.requestNumber != '':
        request=str(options.requestNumber)
        #print request
        url='https://cmsweb.cern.ch/phedex/datasvc/json/prod/subscriptions?request='+request
        transf_list=get_dataset_info(url)
        get_transf_files(transf_list)

    if options.datasetName != '':
        ds=str(options.datasetName)
        #print ds
        lookforsite=''
        if (options.siteName!=''):
          lookforsite = '&node='+options.siteName
        url='https://cmsweb.cern.ch/phedex/datasvc/json/prod/subscriptions?dataset='+ds+lookforsite
        transf_list=get_dataset_info(url)
        get_transf_files(transf_list)
        
    if options.fileName != '':
        if not os.path.exists(os.path.expandvars(options.fileName)):
            print '--- ERROR ---'
            print '  \''+options.fileName+'\' path not found'
            print '  please point to the correct path to the file' 
            print 
            exit()
        file=open(os.path.expandvars(options.fileName),'r')
        for ds in file.readlines():
            print ds
            url='https://cmsweb.cern.ch/phedex/datasvc/json/prod/subscriptions?dataset='+ds
            transf_list=get_dataset_info(url)
        get_transf_files(transf_list)

    #ds_name=['/*DY*/*/MINIAODSIM']
    #for ds in ds_name:
       #print ds
       #url='https://cmsweb.cern.ch/phedex/datasvc/json/prod/subscriptions?dataset='+ds
       #transf_list=get_dataset_info(url)

    #get_transf_files(transf_list)

if __name__ == '__main__':
    transf_list=[]
    main()
