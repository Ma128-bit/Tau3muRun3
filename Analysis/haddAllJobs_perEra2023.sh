#!/bin/sh
# Usage:
#    haddAllJobs_perEra2023.sh <AnalysisType> <OutputName>

helpstring="Usage:
haddAllJobs_perEra2023.sh [AnalysisType] [OutputName]
"

ANALYSISTYPE=$1
OUT_NAME=$2


# Check inputs
if [ -z ${2+x} ]
then
echo ${helpstring}
return
fi

# Control channel
if [ ${ANALYSISTYPE} == "control" ]
then
    echo -e "\nDsPhiPi analysis"
    DATATYPE='data_control'
elif [ ${ANALYSISTYPE} == "tau3mu" ]
then
    echo -e "\nTau3mu analysis"
    DATATYPE='data'
fi

#rm -r JobAdd_perEra_2023
mkdir JobAdd_perEra_2023

for era in B C-v1 C-v2 C-v3 C-v4 D-v1 D-v2
do
	hadd JobAdd_perEra_2023/Era_${era}_${ANALYSISTYPE}.root 2023${era}_*_${ANALYSISTYPE}_${OUT_NAME}/AnalysedTree_${DATATYPE}_2023${era}_*_${ANALYSISTYPE}*.root
done

hadd JobAdd_perEra_2023/Era_C_${ANALYSISTYPE}.root JobAdd_perEra_2023/Era_C-v*_${ANALYSISTYPE}.root
hadd JobAdd_perEra_2023/Era_D_${ANALYSISTYPE}.root JobAdd_perEra_2023/Era_D-v*_${ANALYSISTYPE}.root
rm JobAdd_perEra_2023/Era_C-v*_${ANALYSISTYPE}.root
rm JobAdd_perEra_2023/Era_D-v*_${ANALYSISTYPE}.root

if [ ${ANALYSISTYPE} == "tau3mu" ]
then
	for MC in B0_preBPix B0_postBPix Bp_preBPix Bp_postBPix DsPhiPi_postBPix DsPhiPi_preBPix Ds_preBPix Ds_postBPix
	do
	  	echo "Start MC_${MC}!"
	        hadd JobAdd_perEra_2023/MC_${MC}.root ${MC}_tau3mu_${OUT_NAME}/AnalysedTree_MC_${MC}_tau3mu*.root
	done
fi

