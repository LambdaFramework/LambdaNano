#!/bin/bash

if [ $# -eq 0 ]
then
    echo "No arguments supplied"
    echo "please run with ./createFilelist.sh MC/DATA 2016/2017/2018"
    exit
fi

if [[ "$1" != "MC" ]] && [[ "$1" != "DATA" ]]
then
    echo specify DATA or MC
    exit
fi

if [[ "$2" != "2016" ]] && [[ "$2" != "2017" ]] && [[ "$2" != "2018" ]]
then
    echo specify 2016, 2017 or 2018
    exit
fi

#fix path
filelistpath="$PWD/../python/postprocessing/data/filelists/Legnaro_T2/"

############ from here

if [[ "$2" == "2016" ]]
then
    #2016
    mccampaign="PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6"
    Season="RunIISummer16NanoAODv4-"
    #Season="RunIISummer16NanoAOD-"

    if [[ "$1" != "DATA" ]];then
	dirname="Summer16"
    else
	dirname="Run2016"
    fi
elif [[ "$2" == "2017" ]];then
    #2017
    #mccampaign="PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6"
    mccampaign="PU2017_12Apr2018_94X_mc2017_realistic_v14"
    #Season="RunIIFall17NanoAODv4-"
    Season="RunIIFall17NanoAOD-"
    
    if [[ "$1" != "DATA" ]];then
	dirname="Fall17"
    else
	dirname="Run2017"
    fi	
elif [[ "$2" == "2018" ]];then
    #2018
    mccampaign="Nano14Dec2018_102X_upgrade2018_realistic_v16"
    Season="RunIIAutumn18NanoAODv4-"
    #Season="RunIIAutumn18NanoAOD-"

    if [[ "$1" != "DATA" ]];then
	dirname="Autumn18"
    else
	dirname="Run2018"
    fi
fi

# step 0: execute script with dataset (campaign) name
if [[ "$1" == "MC" ]]
then
    #Grab all
    #dataset=/*/*/MINIAODSIM
    echo "python2.6 get_ds_file_info.py -d \"/$name/${Season}${mccampaign}*/NANOAODSIM\" -s \"T2_IT_Legnaro\""
    python2.6 get_ds_file_info.py -d "/*/${Season}${mccampaign}*/NANOAODSIM" -s "T2_IT_Legnaro" > query.txt #append Summer16
else
    ### NOT LOOKING THIS AT THE MOMENT
    if  [[ "$3" == "A" ]] || [[ "$3" == "B" ]] || [[ "$3" == "C" ]] || [[ "$3" == "D" ]] || [[ "$3" == "E" ]] || [[ "$3" == "F" ]] || [[ "$3" == "G" ]] || [[ "$3" == "H" ]]
    then
	#Period dependent query
	echo "python2.6 get_ds_file_info.py -d \"/*/${dirname}$3*/NANOAOD\" -s \"T2_IT_Legnaro\""
        python2.6 get_ds_file_info.py -d "/*/${dirname}$3*/NANOAOD" -s "T2_IT_Legnaro" > query.txt   # for Data
    elif [ -z "$3" ];then
	#Grab all
	echo "python2.6 get_ds_file_info.py -d \"/*/${dirname}*/NANOAOD\" -s \"T2_IT_Legnaro\""
	python2.6 get_ds_file_info.py -d "/*/${dirname}*/NANOAOD" -s "T2_IT_Legnaro" > query.txt   # for Data
    fi
fi

# step 1: get name of the temporary file
tmpname=$(cat query.txt | awk '{print $4}' | sed -e 's/to//g')
#check availability
echo File to be read: $tmpname
if [[ "$1" == "MC" ]];then
    if [ -s $tmpname ];then
	echo -e "\e[92m /*/${Season}${mccampaign}*/NANOAODSIM exists in Legnaro \e[0m"
    else
	echo -e "\e[91m /*/${Season}${mccampaign}*/NANOAODSIM does not exists in Legnaro \e[0m"
    fi
elif [[ "$1" == "DATA" ]];then
    if [ -s $tmpname ];then
        echo -e "\e[92m /*/${dirname}$4*/NANOAOD exists in Legnaro \e[0m"
    else
        echo -e "\e[91m /*/${dirname}$4*/NANOAOD does not exists in Legnaro \e[0m"
    fi
fi

# # step 2: get list of the samples names (with postfix)
cat query.txt | grep NANOAOD | awk '{print $1}' | sed -e "s/\/${Season}${mccampaign}//g" | sed -e 's/\/NANOAODSIM//g' | sed -e 's/\/NANOAOD//g' | sed -e 's/\///g' > samplelist.txt

############ to where
if [ ! -e "$filelistpath" ];then
    mkdir -p $filelistpath
fi

if [ -e "$filelistpath" ];then
    #ensure everything is fine
    rm -rf $filelistpath/$dirname
    mkdir -p $filelistpath/$dirname
fi

# step 3: get filelist form the dump, filter it, and dump it into appropriate files
cat samplelist.txt | while read sample
do
    if [[ "$1" == "MC" ]]
    then
        checkthis=${mccampaign}
        
        if [[ $sample == *"_ext"* ]]
        then
            trimname=$(echo $sample | sed -e 's/_ext[0-9]-v[0-9]//g')
            versionname=""${sample: -8}""
        else
            trimname=$(echo $sample | sed -e 's/-v[0-9]//g')
            versionname=""${sample: -3}""
        fi

        #dirname="Summer16" # for MC
        recoversion=$trimname
    else
        checkthis=""

        #dirname="Run2016" # for Data
        #trimname=${sample%Run2016*} # for Data
	trimname=${sample%${dirname}*} # for Data
        recoversion=$(echo $sample | cut -d "-" -f2)
        versionname=${sample: -2} # for Data
    fi

    cat $tmpname | grep store | grep $trimname | grep $checkthis$versionname | grep $recoversion | sort > $filelistpath/$dirname/$sample.txt
    sed -i -e 's/^/dcap:\/\/t2-srm-02.lnl.infn.it\/pnfs\/lnl.infn.it\/data\/cms\//' $filelistpath/$dirname/$sample.txt
#    sed -i -e 's|^|root://xrootd-cms.infn.it/|' filelists/$dirname/$sample.txt

    echo $dirname/$sample.txt

done

# final step: clean up
rm query.txt
rm samplelist.txt
