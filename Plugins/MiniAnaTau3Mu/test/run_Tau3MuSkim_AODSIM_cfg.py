import FWCore.ParameterSet.Config as cms

process = cms.Process('Tau3MuSkim')

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load("MiniAna2017.MiniAna2017Tree.Tau3MuSkimAOD_cff")

process.GlobalTag.globaltag = '94X_dataRun2_ReReco_EOY17_v6' #data2017
#process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_TrancheIV_v6' #mc2016
#process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_RealisticBS_25ns_13TeV2016_v1_mc' #mc2016 gives proper mass distr
#process.GlobalTag.globaltag = '94X_mc2017_realistic_v14'

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )


process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'root://xrootd-cms.infn.it///store/data/Run2017F/DoubleMuonLowMass/AOD/09May2018-v1/80000/AECC4C56-BAB0-E811-B92A-008CFA1979AC.root'
         #'file:/lustre/cms/store/user/fsimone/DsTau3Mu/crab_crab_DsTau3Mu__13TeV_MC2016_RECO/190120_140919/0001/custom_DsTau3Mu_13TeV_RECO_crab350_1008.root',
         #'file:/lustre/cms/store/user/fsimone/DsTau3Mu/crab_crab_DsTau3Mu__13TeV_MC2016_RECO/190120_140919/0001/custom_DsTau3Mu_13TeV_RECO_crab350_1007.root',  
         #'file:/lustre/cms/store/user/fsimone/DsTau3Mu/crab_crab_DsTau3Mu__13TeV_MC2016_RECO/190120_140919/0001/custom_DsTau3Mu_13TeV_RECO_crab350_1006.root',
         #'file:/lustre/cms/store/user/fsimone/DsTau3Mu/crab_crab_DsTau3Mu__13TeV_MC2016_RECO/190120_140919/0001/custom_DsTau3Mu_13TeV_RECO_crab350_1005.root',
         #'file:/lustre/cms/store/user/fsimone/DsTau3Mu/crab_crab_DsTau3Mu__13TeV_MC2016_RECO/190120_140919/0001/custom_DsTau3Mu_13TeV_RECO_crab350_1004.root',
         #'file:/lustre/cms/store/user/fsimone/DsTau3Mu/crab_crab_DsTau3Mu__13TeV_MC2016_RECO/190120_140919/0001/custom_DsTau3Mu_13TeV_RECO_crab350_1003.root',
         #'file:/lustre/cms/store/user/fsimone/DsTau3Mu/crab_crab_DsTau3Mu__13TeV_MC2016_RECO/190120_140919/0001/custom_DsTau3Mu_13TeV_RECO_crab350_1002.root',
         #'file:/lustre/cms/store/user/fsimone/DsTau3Mu/crab_crab_DsTau3Mu__13TeV_MC2016_RECO/190120_140919/0001/custom_DsTau3Mu_13TeV_RECO_crab350_1001.root',
         #'file:/lustre/cms/store/user/fsimone/DsTau3Mu/crab_crab_DsTau3Mu__13TeV_MC2016_RECO/190120_140919/0001/custom_DsTau3Mu_13TeV_RECO_crab350_1000.root',
         #'file:/lustre/cms/store/user/fsimone/DsTau3Mu/crab_crab_DsTau3Mu__13TeV_MC2016_RECO/190120_140919/0000/custom_DsTau3Mu_13TeV_RECO_crab350_999.root',
         #'file:/lustre/cms/store/user/fsimone/DsTau3Mu/crab_crab_DsTau3Mu__13TeV_MC2016_RECO/190120_140919/0000/custom_DsTau3Mu_13TeV_RECO_crab350_998.root',
         #'file:/lustre/cms/store/user/fsimone/DsTau3Mu/crab_crab_DsTau3Mu__13TeV_MC2016_RECO/190120_140919/0000/custom_DsTau3Mu_13TeV_RECO_crab350_997.root',
         #'file:/lustre/cms/store/user/fsimone/DsTau3Mu/crab_crab_DsTau3Mu__13TeV_MC2016_RECO/190120_140919/0000/custom_DsTau3Mu_13TeV_RECO_crab350_996.root',
         #'file:/lustre/cms/store/user/fsimone/DsTau3Mu/crab_crab_DsTau3Mu__13TeV_MC2016_RECO/190120_140919/0000/custom_DsTau3Mu_13TeV_RECO_crab350_995.root',
         #'file:/lustre/cms/store/user/fsimone/DsTau3Mu/crab_crab_DsTau3Mu__13TeV_MC2016_RECO/190120_140919/0000/custom_DsTau3Mu_13TeV_RECO_crab350_994.root',
         #'file:/lustre/cms/store/user/fsimone/DsTau3Mu/crab_crab_DsTau3Mu__13TeV_MC2016_RECO/190120_140919/0000/custom_DsTau3Mu_13TeV_RECO_crab350_993.root',
         #'file:/lustre/cms/store/user/fsimone/DsTau3Mu/crab_crab_DsTau3Mu__13TeV_MC2016_RECO/190120_140919/0000/custom_DsTau3Mu_13TeV_RECO_crab350_992.root',
         #'file:/lustre/cms/store/user/fsimone/DsTau3Mu/crab_crab_DsTau3Mu__13TeV_MC2016_RECO/190120_140919/0000/custom_DsTau3Mu_13TeV_RECO_crab350_991.root',

        #'file:./B0A2E5AE-60AF-E811-8BF5-0CC47A7E6A5C.root' #Run2017F AOD
        #'/store/mc/RunIISummer16MiniAODv2/DsToTau_To3Mu_MuFilter_TuneCUEP8M1_13TeV-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/ECAA9E63-C5FD-E711-9C1E-008CFAE451DC.root'
        #'root://xrootd-cms.infn.it//store/mc/RunIISummer16MiniAODv2/DsToTau_To3Mu_MuFilter_TuneCUEP8M1_13TeV-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/D699CEF5-E1FA-E711-A7EC-02163E013399.root'
        #'root://xrootd-cms.infn.it//store/data/Run2017F/DoubleMuonLowMass/MINIAOD/17Nov2017-v1/00000/129CB4BC-17FD-E711-8D49-FA163E838299.root'

    )
)


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("histoSkim.root"))


process.Tau3MuSkim = cms.Path(process.ThreeMuonSelSeq 
                     )


process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string("file_AODSIM.root"),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('Tau3MuSkim')),
                               outputCommands = cms.untracked.vstring(
        'drop *',
        'keep *_looseMuons_*_Tau3MuSkim',
        'keep recoVertexCompositeCandidates_*_*_Tau3MuSkim',
        'keep recoCompositeCandidates_*_*_Tau3MuSkim',
        'keep *_offlinePrimaryVertices_*_*',
        'keep *_generator_*_*',
        'keep *_offlineBeamSpot_*_*',
        'keep recoMuon_muons_*_*',
        'keep *_TriggerResults_*_*',
        'keep *_gtStage2Digis_*_*',
        'keep *_gmtStage2Digis_Muon_*',
        'keep *_scalersRawToDigi_*_*',
        'keep *_Trigger_*_*',
        'keep *_PileupInfo_*_*',
        'keep *_genParticles_*_*',
        'keep recoVertex_offlinePrimaryVertices_*_*',
        'keep *_generalTracks_*_RECO',
        'keep *_g4SimHits_*_*'
        #'keep recoTracks_generalTracks_*_*',

        )
)

#type_label_instance_process
process.outpath = cms.EndPath(process.out) 



"""
from PhysicsTools.PatAlgos.triggerLayer1.triggerEventProducer_cfi import *
from PhysicsTools.PatAlgos.tools.trigTools import *
patTriggerEvent.patTriggerMatches  = cms.VInputTag( "muonTriggerMatchHLTMuons" )
switchOnTrigger( process )
switchOnTriggerMatching( process, triggerMatchers = [ 'muonTriggerMatchHLTMuons' ] )
"""
