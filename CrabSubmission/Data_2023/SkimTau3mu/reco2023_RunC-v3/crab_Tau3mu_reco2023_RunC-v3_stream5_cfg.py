import sys
sys.path.append('../../..')
import config_info
 
from CRABClient.UserUtilities import config, getUsername
config = config()

config.General.requestName = 'SkimTau3mu_2023eraC-v3_stream5_Mini_v3'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'

config.JobType.psetName = config_info.cmssw_dir + 'src/SkimTools/SkimTau3Mu/test/run_Data2023C-v1-3_PatAndTree_cfg.py'

config.Data.inputDataset = '/ParkingDoubleMuonLowMass5/Run2023C-22Sep2023_v3-v1/MINIAOD'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 50
config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions23/Cert_Collisions2023_eraC_367095_368823_Golden.json'
#config.Data.runRange = '193093-193999' # '193093-194075'
#config.Data.publication = True
config.Data.outputDatasetTag = 'SkimTau3mu_2023eraC-v3_stream5_Mini_v3'
config.JobType.allowUndistributedCMSSW = True 
config.Site.storageSite = config_info.storageSite
config.Site.ignoreGlobalBlacklist  = True

