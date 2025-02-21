# XGBoost

## Run the script
BDT_optimal_cut.py for select best cuts on bdt_score: 
```
python3 BDT_optimal_cut.py --config ../../../xgboost/CMSSW_13_0_13/src/xgboost/results/BDT/20231111-232226/Run2022_config.json
```

Add_BDT_prediction.py for adding the bdtcv branch to an external file (e.g. control channel)
```
python3 Add_BDT_prediction.py --inputfile ../ROOTFiles/AllControl2023_new_plusMVA.root --config ./BDT_results/xgb_tau3mu_20250214-154330/config.json 
```
