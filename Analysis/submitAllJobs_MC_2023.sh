#!/bin/sh
# Usage:
#    submitAllJobs.sh <N_files> <OutputName>

helpstring="Usage:
submitAllJobs.sh [N_files] [OutputName]

N_files: Number of ntuples to be used per job
AnalysisType: Choose between 'tau3mu' and 'control'
"

N_FILES=$1
OUT_NAME=$2
ANALYSISTYPE="tau3mu"

# Check inputs
if [ -z ${2+x} ]
then
  echo ${helpstring}
  return
fi


if [ ${ANALYSISTYPE} == "tau3mu" ]
then
    echo -e "\n2023 MC analysis"
    DATATYPE='data'
fi

if [ ${ANALYSISTYPE} == "tau3mu" ]
then
	for i in Ds_preBPix Ds_postBPix B0_preBPix B0_postBPix Bp_preBPix Bp_postBPix DsPhiPi_preBPix DsPhiPi_postBPix
	do
	    echo -e "\nMC dataset $i"
	    echo -e "\npython createRunFile_new.py MC ${ANALYSISTYPE} --n ${N_FILES} --MCprocess $i --outName ${OUT_NAME}"
	    python createRunFile_new.py MC ${ANALYSISTYPE} --n ${N_FILES} --MCprocess $i --outName ${OUT_NAME}
	    sleep 1
	    echo -e "\nsubmit_analysis_${i}_${ANALYSISTYPE}_${OUT_NAME}.sh"
	    source submit_analysis_${i}_${ANALYSISTYPE}_${OUT_NAME}.sh
	    cd ..
	    sleep 1
	done
fi
