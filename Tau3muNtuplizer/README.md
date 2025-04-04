# Ntuplizer code for the τ&rarr;3mu search at Run 3

## Instructions
The main informations on data and MC samples are stored in the `Runs.json` file and in files in the `datasets` folder.
### How to add new years (or modify existing ones)
1. Apply your changes in `Runs.json`;
2. If your changes affect data (not required if changes are only in MC), run `getDatset.py` to download information from DAS (as in the example below);
    - `voms-proxy-init -voms cms -rfc`
    - `python3 getDatset.py --year 2022` 

<p>&nbsp;</p>

### Submit all era in a year:
```
submitAllJobs.sh [Year] [MCflag]
```
* `[year]` = `2022`,  `2023` or `2024`: `[MCflag]` = `true or false`

### Run ntuplizer on a full dataset:
```
cd CrabSubmission
source submit_CRAB.sh [era] [year] 
```
**For DATA:**

* `[year]` = `2022` : `[era]` = `C, D-v1, D-v2, E, F, G`
* `[year]` = `2023` : `[era]` = `C-v1, C-v2, C-v3, C-v4, D-v1, D-v2`
* `[year]` = `2024` : `[era]` = `?`

**For MC:**

* `[year]` = `2022` or  `2023`: `[era]` = `MC_Bd_pre, MC_Bu_pre, MC_Ds_pre, MC_Bd_post, MC_Bu_post, MC_Ds_post`
* `[year]` = `2024` : `[era]` = `MC_Bd, MC_Bu, MC_Ds`

<p>&nbsp;</p>

### Run ntuplizer on few root files:

`cd SkimTools/test`

For data: `cmsRun run_Data2022_PatAndTree_cfg.py`

For MC: `cmsRun run_MC2022_PatAndTree_cfg.py`

<p>&nbsp;</p>
