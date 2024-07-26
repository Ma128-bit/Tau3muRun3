#!/bin/sh
# Usage:
#    resubmitFailedJobs.sh

for i in 2022_RunC 2022_RunD-v1 2022_RunD-v2 2022_RunE 2022_RunF 2022_RunG
do
    echo -e "\nData $i"
    cd reco${i}
    source resubmit.sh
    cd ..
    sleep 1
done
