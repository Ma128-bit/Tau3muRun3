# Ntuplizer for the Tau&rarr;3mu search at Run 3

## Make the ntuples
The ntuples useful for the analysis can be created both for the tau3mu and the control channel. This can be done by using the skims in the:
* `SkimTools/X` with `X` = `SkimTau3Mu, SkimPhiPi` \
which use the plugins in the directories `MiniAnaTau3Mu` and `DsPhiPiTreeMakerMINI`, respectively.

Example:
```
cmsRun SkimTools/SkimTau3Mu/test/run_MC2022_PatAndTree_cfg.py
```

To run the ntuple production on the grid, the crab configurations files for the submission of the jobs are in the `CrabSubmission` directory. Example:
```
crab submit -c crab_Tau3mu_reco2023_RunC-v1_stream0_cfg.py 
```

To submit all the jobs use:
```
source submitAllJobs.sh
```
<p>&nbsp;</p>

### Resubmit Failed Jobs
The script `resubmitFailedJobs.sh` allows for the resubmission of the failed jobs in all eras.

<p>&nbsp;</p>

## Measurement of luminosity
Run the script `reportAllJobs.sh`, this allows for the creation of the file `processedLumis.json` for each stream and era.\
On Lxplus run:
```
source /cvmfs/cms-bril.cern.ch/cms-lumi-pog/brilws-docker/brilws-env
```
to enable the BRIL Work Suite.\
Then use `AllLumi.sh` to measure the luminosity of each stream of a specific era.\
The mean value of these luminosities is the final luminosity of that era.

<p>&nbsp;</p>
