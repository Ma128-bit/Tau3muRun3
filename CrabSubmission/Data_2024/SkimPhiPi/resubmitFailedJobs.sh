#!/bin/sh
# Usage:
#    resubmitFailedJobs.sh

for i in 2024_RunB 2024_RunC 2024_RunD 2024_RunE-v1 2024_RunE-v2 2024_RunF 2024_RunG
do
    echo -e "\nData $i"
    cd reco${i}
    source resubmit.sh
    cd ..
    sleep 1
done
