#!/bin/sh
# Usage:
#    submitAllJobs.sh

crab submit -c crab_MCRun3_BdTau3mu_postE_cfg.py
sleep 5
crab submit -c crab_MCRun3_BdTau3mu_preE_cfg.py
sleep 5
crab submit -c crab_MCRun3_BuTau3mu_preE_cfg.py
sleep 5
crab submit -c crab_MCRun3_DsTau3mu_preE_cfg.py
sleep 5
crab submit -c crab_MCRun3_BuTau3mu_postE_cfg.py
sleep 5
crab submit -c crab_MCRun3_DsTau3mu_postE_cfg.py
