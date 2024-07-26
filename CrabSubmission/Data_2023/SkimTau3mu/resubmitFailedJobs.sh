#!/bin/sh
# Usage:
#    reportAllJobs.sh

for i in 2023_RunB 2023_RunC-v1 2023_RunC-v2 2023_RunC-v3 2023_RunC-v4 2023_RunD-v1 2023_RunD-v2
do
    echo -e "\nData $i"
    cd reco${i}
    source resubmit.sh
    cd ..
    sleep 1
done
