#!/bin/sh
# Usage:
#    submitAllJobs.sh <N_files> <AnalysisType>

helpstring="Usage:
submitAllJobs.sh [N_files] [AnalysisType] [OutputName]

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


for i in 2022C_0 2022C_1 2022C_2 2022C_3 2022C_4 2022C_5 2022C_6 2022C_7 2022D-v1_0 2022D-v1_1 2022D-v1_2 2022D-v1_3 2022D-v1_4 2022D-v1_5 2022D-v1_6 2022D-v1_7 2022D-v2_0 2022D-v2_1 2022D-v2_2 2022D-v2_3 2022D-v2_4 2022D-v2_5 2022D-v2_6 2022D-v2_7 2022E_0 2022E_1 2022E_2 2022E_3 2022E_4 2022E_5 2022E_6 2022E_7 2022F_0 2022F_1 2022F_2 2022F_3 2022F_4 2022F_5 2022F_6 2022F_7 2022G_0 2022G_1 2022G_2 2022G_3 2022G_4 2022G_5 2022G_6 2022G_7
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
