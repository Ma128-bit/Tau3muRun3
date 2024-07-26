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

#rm -r JobAdd_perEra
mkdir JobAdd_perEra

for era in C D-v1 D-v2 E F G
do
	hadd JobAdd_perEra/Era_${era}_${ANALYSISTYPE}.root 2022${era}_*_${ANALYSISTYPE}_${OUT_NAME}/AnalysedTree_${DATATYPE}_2022${era}_*_${ANALYSISTYPE}*.root
done

hadd JobAdd_perEra/Era_D_${ANALYSISTYPE}.root JobAdd_perEra/Era_D-v*_${ANALYSISTYPE}.root
rm JobAdd_perEra/Era_D-v*_${ANALYSISTYPE}.root

if [ ${ANALYSISTYPE} == "tau3mu" ]
then
	for MC in B0_preE B0_postE Bp_preE Bp_postE DsPhiPi_postE DsPhiPi_preE Ds_preE Ds_postE
	do
	  	echo "Start MC_${MC}!"
	        hadd JobAdd_perEra/MC_${MC}.root ${MC}_tau3mu_${OUT_NAME}/AnalysedTree_MC_${MC}_tau3mu*.root
	done
fi
