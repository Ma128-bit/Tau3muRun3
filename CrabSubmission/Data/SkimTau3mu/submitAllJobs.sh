#!/bin/sh
# Usage:
#    submitAllJobs.sh

declare -a preE=("2022_RunC" "2022_RunD-v1" "2022_RunD-v2" "2022_RunE")
declare -a postE=("2022_RunF" "2022_RunG")

current_dir=$(pwd)

if [[ "$current_dir" == *"CMSSW_13_"* ]]; then
    era=("${postE[@]}")
else
    era=("${preE[@]}")
fi

for i in "${era[@]}"; do
    echo -e "\nData $i"
    cd reco${i}
    source submit.sh
    cd ..
    sleep 1
done
