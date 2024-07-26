#!/bin/sh
# Usage:
#    AllLumi.sh

for i in 2023_RunB 2023_RunC-v1 2023_RunC-v2 2023_RunC-v3 2023_RunC-v4 2023_RunD-v1 2023_RunD-v2
do
    echo -e "\nData $i"
    cd reco${i}
    cd crab_projects
    for j in 0 1 2 3 4 5 6 7
    do
        cd crab_SkimDsPhiPi_${i}_stream${j}_Mini_v3
        cd results
        brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_BRIL.json -u /fb -i processedLumis.json --hltpath "HLT_DoubleMu3_Trk_Tau3mu_v*"
        cd ..
        cd ..
        sleep 1
    done
    cd ..
    cd ..
    sleep 1
done