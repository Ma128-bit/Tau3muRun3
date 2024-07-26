#!/bin/sh
# Usage:
#    submitAllJobs.sh

crab submit -c crab_MCRun3_BdTau3mu_postBPix_cfg.py
sleep 5
crab submit -c crab_MCRun3_BdTau3mu_preBPix_cfg.py
sleep 5
crab submit -c crab_MCRun3_BuTau3mu_preBPix_cfg.py
sleep 5
crab submit -c crab_MCRun3_DsTau3mu_preBPix_cfg.py
sleep 5
crab submit -c crab_MCRun3_BuTau3mu_postBPix_cfg.py
sleep 5
crab submit -c crab_MCRun3_DsTau3mu_postBPix_cfg.py
