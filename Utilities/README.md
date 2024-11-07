# Utilities
Plots for CC and other things done between ntuple/analysis and xgboost
Modify `file_locations.py` to specify the locations of your files

## Description of scripts
* `SelEffNtuple.py` or `SelEffAna.py`
  * Run as: `python3 SelEffNtuple.py` or `python3 SelEffAna.py`
  * Default: MC - Control channel. Pass `--tau3mu` and/or `--data`
  * Out: .csv file with number of events per era and per cut
  * Description: It is used to obtain the selection efficiencies starting from data after Ntuplizer/Analysis

* `Control_fits.py`
  * Run as: `python3 Control_fits.py --year 2022`
  * Options: `--year` : `2022` or `2023` 
  * Out: Mass_Fits directories with invariant mass fits and yield in csv

* `MC_yield.py`
  * Run as: `python3 MC_yield.py --year 2022`
  * Options: `--year` : `2022` or `2023` 
  * Out: Mass_Fits directories with invariant mass fits and yield in csv

* `PUreweight.py`
  * Run as: `python3 PUreweight.py --year 2022`
  * Options: `--year` : `2022` or `2023` 
  * Out: Compute the ratio of the PU distribution in data and MC (The first time you run it, remember to uncomment the first lines)

* `New_Ntuple.py`
  * Before running it: make sure you have set the correct values for the variables in `cpp_library.h`.
  * Run as: `python3 New_Ntuple.py --type X`
    * with `X` = `tau3mu2022`/`tau3mu2023` or `control2022`/`control2023`
  * Out: ROOTFiles directory with merged analysis files and weights 

* `MVA_predictions.py`
  * Run as: `python3 MVA_predictions.py --type X`
    * with `X` = `tau3mu` or `control`
  * Out: Takes the outputs of New_Ntuple.py, combines them, and includes the MVA score in a *plusMVA.root file

* `DsPhiPi_sPlot.cpp`
  * Run as: `root -l`, `.L DsPhiPi_sPlot.cpp` `DsPhiPi_sPlot(root_name, tree_name, isMC)`
    * with `isMC` = 0 or 5
    * example `DsPhiPi_sPlot("ROOTFiles/AllControl2022", "FinalTree", 0)`

* `Control_plots.py`
  * Run as: `python3 Control_plots.py --year 2022 --type diff --file ROOTFiles/AllControl2022.root`
  * Options: `--year` : `2022` or `2023`; `--type` : `sPlot` or `diff` 
  * Out: Control_Plots directories with plots
 
