import sys
sys.path.append('../..')
import config_info

from CRABClient.UserUtilities import config, getUsername
config = config()

config.General.requestName = 'SkimPhiPi_MC_23_Run3_Mini_preBPix'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'


config.JobType.psetName = config_info.cmssw_dir + 'src/SkimTools/SkimPhiPi/test/run_MC2023_DsPhiPiSkimAndTree_cfg.py'
config.Data.inputDataset = '/DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/Run3Summer23MiniAODv4-130X_mcRun3_2023_realistic_v14-v2/MINIAODSIM'
config.Data.allowNonValidInputDataset = True
config.Data.inputDBS = 'global'
#config.Data.splitting = 'LumiBased'
config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 2500
config.Data.outLFNDirBase = config_info.store
#config.Data.publication = True
config.Data.outputDatasetTag = 'SkimPhiPi_MC_23_Run3_Mini_preBPix'
config.JobType.allowUndistributedCMSSW = True 
config.Site.storageSite = config_info.storageSite
config.Site.ignoreGlobalBlacklist  = True

