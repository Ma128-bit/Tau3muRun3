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

#process.GlobalTag.globaltag = '102X_dataRun2_v13' #data_rereco 2018 A-C 
#process.GlobalTag.globaltag = '124X_dataRun3_Prompt_v4' #data_reco 2022 B-D
#process.GlobalTag.globaltag = '124X_dataRun3_Prompt_v8' #data_reco 2022 E-F
process.GlobalTag.globaltag = '124X_dataRun3_Prompt_v10'

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #data2018A --> /DoubleMuonLowMass/Run2018A-17Sep2018-v1/MINIAOD
        'root://xrootd-cms.infn.it///store/data/Run2022G/ParkingDoubleMuonLowMass5/MINIAOD/PromptReco-v1/000/362/437/00000/645c4ac6-81f3-4c9d-9e29-21934c2ff83c.root'
	)
)


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("Tree_PhiPi.root"))



process.unpackedPatTrigger = cms.EDProducer("PATTriggerObjectStandAloneUnpacker",
    patTriggerObjectsStandAlone = cms.InputTag( 'slimmedPatTrigger' ),
    triggerResults              = cms.InputTag( 'TriggerResults::HLT' ),
    unpackFilterLabels = cms.bool(True)
)

process.Tree3Mu = cms.EDAnalyzer("DsPhiPiTreeMakerMINI",
                                 isMcLabel = cms.untracked.bool(False),
                                 isAnaLabel = cms.untracked.bool(True),
                                 is2016Label = cms.untracked.bool(False),
                                 is2017Label = cms.untracked.bool(False),
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



