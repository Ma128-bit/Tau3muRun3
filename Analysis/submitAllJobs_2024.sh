#!/bin/sh
# Usage:
#    submitAllJobs.sh <N_files> <AnalysisType>

helpstring="Usage:
submitAllJobs_2024.sh [N_files] [AnalysisType] [OutputName]

N_files: Number of ntuples to be used per job
AnalysisType: Choose between 'tau3mu' and 'control'
"

N_FILES=$1
ANALYSISTYPE=$2
OUT_NAME=$3


# Check inputs
if [ -z ${3+x} ]
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

for i in 2024B_0 2024B_1 2024B_2 2024B_3 2024B_4 2024B_5 2024B_6 2024B_7 2024C_0 2024C_1 2024C_2 2024C_3 2024C_4 2024C_5 2024C_6 2024C_7 2024D_0 2024D_1 2024D_2 2024D_3 2024D_4 2024D_5 2024D_6 2024D_7 2024E-v1_0 2024E-v1_1 2024E-v1_2 2024E-v1_3 2024E-v1_4 2024E-v1_5 2024E-v1_6 2024E-v1_7 2024E-v2_0 2024E-v2_1 2024E-v2_2 2024E-v2_3 2024E-v2_4 2024E-v2_5 2024E-v2_6 2024E-v2_7 2024F_0 2024F_1 2024F_2 2024F_3 2024F_4 2024F_5 2024F_6 2024F_7 #2024G_0 2024G_1 2024G_2 2024G_3 2024G_4 2024G_5 2024G_6 2024G_7 
do
    echo -e "\nData $i"
    echo -e "\npython createRunFile_new.py --run $i --n ${N_FILES} ${DATATYPE} ${ANALYSISTYPE} --outName ${OUT_NAME}"
    python createRunFile_new.py --run $i --n ${N_FILES} ${DATATYPE} ${ANALYSISTYPE} --outName ${OUT_NAME}
    sleep 1
    echo -e "\nsubmit_analysis_${i}_${ANALYSISTYPE}_${OUT_NAME}.sh"
    source submit_analysis_${i}_${ANALYSISTYPE}_${OUT_NAME}.sh
    cd ..
    sleep 1
done
