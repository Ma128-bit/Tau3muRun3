import FWCore.ParameterSet.Config as cms

process = cms.Process('DsPhiPiSkim')

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
#process.load('DsPhiPiTreeMaker.DsPhiPiTreeMaker.DsPhiPiSkimAOD_cff')
#process.load('DsPhiPiTreeMaker.DsPhiPiTreeMaker.DsPhiPiMuMuPi_BParking_cff')
process.load('SkimTools.SkimPhiPi.DsPhiPiMuMuPi_miniAOD_cff')

#process.GlobalTag.globaltag = '124X_mcRun3_2022_realistic_v12' #MC2022
#process.GlobalTag.globaltag = '102X_upgrade2018_realistic_v21' #MC2018
process.GlobalTag.globaltag = '130X_mcRun3_2022_realistic_v5' #MC2022

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #Official MC DsPhiPi 2018 rereco --> /DsToPhiPi_ToMuMu_MuFilter_TuneCP5_13TeV-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM
            'store/user/caruta/Pythia8_DsPhiPi_MuMuPi_Run3_2022/124X_mcRun3_2022_realistic_v12_MINIAODSIM/221117_080521/0000/DsPhiPi_2022_step2_1.root',
            'store/user/caruta/Pythia8_DsPhiPi_MuMuPi_Run3_2022/124X_mcRun3_2022_realistic_v12_MINIAODSIM/221117_080521/0000/DsPhiPi_2022_step2_536.root',
            'store/user/caruta/Pythia8_DsPhiPi_MuMuPi_Run3_2022/124X_mcRun3_2022_realistic_v12_MINIAODSIM/221117_080521/0000/DsPhiPi_2022_step2_56.root',
            'store/user/caruta/Pythia8_DsPhiPi_MuMuPi_Run3_2022/124X_mcRun3_2022_realistic_v12_MINIAODSIM/221117_080521/0000/DsPhiPi_2022_step2_53.root',
            'store/user/caruta/Pythia8_DsPhiPi_MuMuPi_Run3_2022/124X_mcRun3_2022_realistic_v12_MINIAODSIM/221117_080521/0000/DsPhiPi_2022_step2_6.root',
            'store/user/caruta/Pythia8_DsPhiPi_MuMuPi_Run3_2022/124X_mcRun3_2022_realistic_v12_MINIAODSIM/221117_080521/0000/DsPhiPi_2022_step2_36.root'
	)
)


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("Tree_MCPhiPi.root"))



process.unpackedPatTrigger = cms.EDProducer("PATTriggerObjectStandAloneUnpacker",
    patTriggerObjectsStandAlone = cms.InputTag( 'slimmedPatTrigger' ),
    triggerResults              = cms.InputTag( 'TriggerResults::HLT' ),
    unpackFilterLabels = cms.bool(True)
)

process.Tree3Mu = cms.EDAnalyzer("DsPhiPiTreeMakerMINI",
                                 isMcLabel = cms.untracked.bool(True),
                                 isAnaLabel = cms.untracked.bool(True),
                                 is2016Label = cms.untracked.bool(True),
                                 is2017Label = cms.untracked.bool(True),
                                 is2018Label = cms.untracked.bool(True),
                                 isBParkingLabel = cms.untracked.bool(False),
                                 #is3MuLabel = cms.untracked.bool(False),
                                 muonLabel=cms.InputTag("looseMuons"),
                                 VertexLabel=cms.InputTag("offlineSlimmedPrimaryVertices"),
                                 TracksLabel=cms.InputTag("LooseTrack"),
                                 genParticleLabel=cms.InputTag("prunedGenParticles"),
                                 #Cand3MuLabel=cms.InputTag("ThreeMuonsVtxKalmanFit"),
                                 Cand2Mu1TrackLabel=cms.InputTag("TwoMuonsOneTrackKalmanVtxFit"),
                                 DiMuonLabel=cms.InputTag("DiMuonsVtxFit"),
                                 pileupSummary = cms.InputTag("slimmedAddPileupInfo"),
                                 triggerResults = cms.InputTag("TriggerResults", "", "HLT"),
                                 #triggerSummary = cms.InputTag("hltTriggerSummaryAOD", "", "HLT"),
                                 objects = cms.InputTag("unpackedPatTrigger"),
                                 AlgInputTag = cms.InputTag( "gtStage2Digis" ),
                                 algInputTag = cms.InputTag( "gtStage2Digis" ),
                                 extInputTag = cms.InputTag( "gtStage2Digis" )
)



process.DsPhiPiSkim = cms.Path( process.TwoMuOneTrackSelSeq*
                                process.unpackedPatTrigger* 
                                process.Tree3Mu
)



