import sys
sys.path.append('../../..')
import config_info
 
from CRABClient.UserUtilities import config, getUsername
config = config()

config.General.requestName = 'SkimTau3mu_2022eraF_stream5_Mini_v3'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'

config.JobType.psetName = config_info.cmssw_dir + 'src/SkimTools/SkimTau3Mu/test/run_Data2022FG_PatAndTree_cfg.py'
config.Data.allowNonValidInputDataset = True
config.Data.inputDataset = '/ParkingDoubleMuonLowMass5/Run2022F-22Sep2023-v1/MINIAOD'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 50
config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions22/Cert_Collisions2022_eraF_360390_362167_Golden.json'
#config.Data.runRange = '193093-193999' # '193093-194075'
#config.Data.publication = True
config.Data.outputDatasetTag = 'SkimTau3mu_2022eraF_stream5_Mini_v3'
config.JobType.allowUndistributedCMSSW = True
config.Site.storageSite = config_info.storageSite
config.Site.ignoreGlobalBlacklist  = True

