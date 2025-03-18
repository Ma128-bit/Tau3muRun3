import subprocess, json, time, os, argparse, time

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--year", required=True, type=str, help="Year of the dataset")
    argparser.add_argument("--era", type=str, default=None, help="Era of the dataset")
    argparser.add_argument("--MCera", type=str, default=None, help="Era of the dataset")
    args = argparser.parse_args()
    year = args.year
    era = args.era
    MCera = args.MCera
    if (MCera==None) and (era==None):
        print("Please specify either --era or --MCera")
        exit()
    with open("../Runs.json", "r") as file:
        data = json.load(file)[year]
    if era != None:
        era_index = data["Eras"].index(era) if era in data["Eras"] else None
        if era_index == None:
            print(f"WARNING: {era} is not in the list of eras. Please check.")
            exit()
        globaltag = data["GTs"][era_index]
        golden_json = data["golden_json"][era_index]

        with open(f"../datasets/datasets_{year}_{era}.txt", "r") as filetxt:
            righe = [riga.strip() for riga in filetxt]
        if len(righe) != 8:
            print(f"WARNING: {era} has more/less than 8 datasets. Please check.")
            time.sleep(3)

        command = f"""
        directory="$PWD";
        homedir=$(dirname "$(dirname "$directory")/CrabSubmission");
        pathtoskimfile="$homedir/SkimTools/test";
        mkdir -p "{year}_era{era}"; 
        echo "Data {year} - era {era} is selected"; 
        path="$directory/{year}_era{era}/PatAndTree_cfg.py";
        cp "$pathtoskimfile/run_Data2022_PatAndTree_cfg.py" "$path";
        sed -i "s#124X_dataRun3_PromptAnalysis_v1#{globaltag}#g" "{year}_era{era}/PatAndTree_cfg.py";
        cp templates/report.sh "{year}_era{era}/report.sh";
        cp templates/status.sh "{year}_era{era}/status.sh";
        cp templates/resubmit.sh "{year}_era{era}/resubmit.sh";
        cd "{year}_era{era}";
        sed -i "s#YEAR#{year}#g" *.sh;
        sed -i "s#ERANAME#{era}#g" *.sh;
        cd ..;
        cp templates/submit.sh "{year}_era{era}/submit.sh";
        """
        subprocess.run(command, shell=True, check=True)
        for i, dataset in enumerate(righe):
            command = f"""
            directory="$PWD";
            path="$directory/{year}_era{era}/PatAndTree_cfg.py";
            cp templates/CRAB_template.py "{year}_era{era}/CRAB_stream_{i}.py";
            sed -i "s#YEAR#{year}#g" "{year}_era{era}/CRAB_stream_{i}.py";
            sed -i "s#ERANAME#{era}#g" "{year}_era{era}/CRAB_stream_{i}.py";
            sed -i "s#NUMBER#{i}#g" "{year}_era{era}/CRAB_stream_{i}.py";
            sed -i "s#DATASET_NAME#{dataset}#g" "{year}_era{era}/CRAB_stream_{i}.py";
            sed -i "s#FILE_TO_SUBMIT_PATH#$path#g" "{year}_era{era}/CRAB_stream_{i}.py";
            sed -i "s#GOLDEN_JSON_PATH#{golden_json}#g" "{year}_era{era}/CRAB_stream_{i}.py";
            cd "{year}_era{era}";
            crab submit -c "CRAB_stream_{i}.py";
            cd ..;
            echo "Stream {i} submitted!";
            sleep 1;
            """
            subprocess.run(command, shell=True, check=True)
    elif MCera != None:
        era_index = data["MC_era"].index(MCera) if MCera in data["MC_era"] else None
        if era_index == None:
            print(f"WARNING: {MCera} is not in the list of MC_eras. Please check.")
            exit()
        MC_input_type = data["MC_input_type"][era_index]
        globaltag = data["MC_GTs"][era_index]
        MC_datsets = data["MC_datasets"][era_index]
        command = f"""
        directory="$PWD";
        homedir=$(dirname "$(dirname "$directory")/CrabSubmission");
        pathtoskimfile="$homedir/SkimTools/test";
        mkdir -p "{year}_{MCera}"; 
        echo "Data {year} - {MCera} is selected"; 
        path="$directory/{year}_{MCera}/PatAndTree_cfg.py";
        cp "$pathtoskimfile/run_MC2022_PatAndTree_cfg.py" "$path";
        sed -i "s#130X_mcRun3_2022_realistic_postEE_v6#{globaltag}#g" "{year}_{MCera}/PatAndTree_cfg.py";
        cp templates/CRAB_template_MC.py "{year}_{MCera}/CRAB_MC.py";
        sed -i "s#YEAR#{year}#g" "{year}_{MCera}/CRAB_MC.py";
        sed -i "s#ERANAME#{MCera}#g" "{year}_{MCera}/CRAB_MC.py";
        sed -i "s#DATASET_NAME#{MC_datsets}#g" "{year}_{MCera}/CRAB_MC.py";
        sed -i "s#FILE_TO_SUBMIT_PATH#$path#g" "{year}_{MCera}/CRAB_MC.py";
        sed -i "s#INPUT_TYPE#{MC_input_type}#g" "{year}_{MCera}/CRAB_MC.py";
        cd "{year}_{MCera}";
        crab submit -c "CRAB_MC.py";
        cd ..;
        echo "{MCera} submitted!";
        sleep 1;
        """
        subprocess.run(command, shell=True, check=True)







