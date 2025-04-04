from CRABClient.UserUtilities import config, getUsername
config = config()

config.General.requestName = 'SkimDsPhiPi_YEAR_ERANAME_Mini_v4'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'

config.JobType.psetName = 'FILE_TO_SUBMIT_PATH'

config.Data.inputDataset = 'DATASET_NAME'
config.Data.allowNonValidInputDataset = True
config.Data.inputDBS = 'INPUT_TYPE'
config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 300
#config.Data.publication = True
config.Data.outputDatasetTag = 'SkimDsPhiPi_YEAR_ERANAME_Mini_v4'
config.JobType.allowUndistributedCMSSW = True 
config.Site.storageSite = 'T2_IT_Bari'
config.Site.ignoreGlobalBlacklist  = True
