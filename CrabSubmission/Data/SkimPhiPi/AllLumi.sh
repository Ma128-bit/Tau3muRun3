#!/bin/sh
# Usage:
#    AllLumi.sh

for i in 2022_RunC 2022_RunD-v1 2022_RunD-v2 2022_RunE 2022_RunF 2022_RunG
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