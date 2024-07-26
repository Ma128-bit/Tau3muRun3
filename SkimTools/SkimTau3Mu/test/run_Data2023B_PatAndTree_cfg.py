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
process.load("SkimTools.SkimTau3Mu.Tau3MuSkim_miniAOD_cff")
#process.load("SkimTools.SkimTau3Mu.Tau3MuSkim_miniAOD_noHLT_cff")

process.GlobalTag.globaltag = '130X_dataRun3_PromptAnalysis_v1' #2023

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

#Begin processing the 25271st record. Run 320012, Event 56448719, LumiSection 36 on stream 0 at 20-Apr-2020 18:53:30.862 CEST
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #'root://xrootd-cms.infn.it///store/data/Run2022C/ParkingDoubleMuonLowMass0/MINIAOD/PromptReco-v1/000/355/863/00000/389f9ca1-f590-4691-b7f2-41e0146a8a79.root',
	#'root://xrootd-cms.infn.it///store/data/Run2022C/ParkingDoubleMuonLowMass0/MINIAOD/10Dec2022-v2/2540000/10ea983f-969f-4ed5-9b97-bc6f66e8e5e6.root',
	#'root://xrootd-cms.infn.it///store/data/Run2022C/ParkingDoubleMuonLowMass0/MINIAOD/10Dec2022-v2/2540000/084379cc-875d-44ef-b533-28c0a9a52786.root',
	#'root://xrootd-cms.infn.it///store/data/Run2022C/ParkingDoubleMuonLowMass0/MINIAOD/10Dec2022-v2/2540000/0e9f3095-009a-48c0-9817-a3ebefa4997e.root',
	#'root://xrootd-cms.infn.it///store/data/Run2022C/ParkingDoubleMuonLowMass0/MINIAOD/10Dec2022-v2/2540000/11a2b182-9e14-4195-8ad0-2f93dfc21ae1.root',
	#'root://xrootd-cms.infn.it///store/data/Run2022C/ParkingDoubleMuonLowMass0/MINIAOD/10Dec2022-v2/2540000/00ff4dbc-2204-48f1-aa40-e13b6b18c6cd.root',
	#'root://xrootd-cms.infn.it///store/data/Run2022C/ParkingDoubleMuonLowMass0/MINIAOD/10Dec2022-v2/2540000/058e2de8-ef0e-4ce2-b3c5-d03218896697.root',
	#'root://xrootd-cms.infn.it///store/data/Run2022C/ParkingDoubleMuonLowMass0/MINIAOD/10Dec2022-v2/2540000/09641b36-730b-4d5c-a3ce-962b839f49d0.root',
	#'root://xrootd-cms.infn.it///store/data/Run2022G/ParkingDoubleMuonLowMass5/MINIAOD/PromptReco-v1/000/362/437/00000/645c4ac6-81f3-4c9d-9e29-21934c2ff83c.root',
	#'root://xrootd-cms.infn.it///store/data/Run2022C/ParkingDoubleMuonLowMass1/MINIAOD/10Dec2022-v3/2540000/3a0e798e-8aef-4809-9e11-f22d18cec45f.root',
	'root://xrootd-cms.infn.it///store/data/Run2023B/ParkingDoubleMuonLowMass0/MINIAOD/PromptReco-v1/000/366/442/00000/77993198-8548-4532-83b-762a8863c9b9.root'
    ),
            #eventsToProcess = cms.untracked.VEventRange('320012:56448719')
)


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("TreeData.root"))


process.unpackedPatTrigger = cms.EDProducer("PATTriggerObjectStandAloneUnpacker",
    patTriggerObjectsStandAlone = cms.InputTag( 'slimmedPatTrigger' ),
    triggerResults              = cms.InputTag( 'TriggerResults::HLT' ),
    unpackFilterLabels = cms.bool(True)
)

process.TreeMakerBkg = cms.EDAnalyzer("MiniAnaTau3Mu",
                                      isMcLabel = cms.untracked.bool(False),
                                      isAnaLabel = cms.untracked.bool(True),
                                      is2016Label = cms.untracked.bool(False),
                                      is2017Label = cms.untracked.bool(False),
                                      is2018Label = cms.untracked.bool(True),
                                      isBParkingLabel = cms.untracked.bool(False),
                                      muonLabel=cms.InputTag("looseMuons"),
                                      photonLabel=cms.InputTag("slimmedPhotons"),
                                      VertexLabel=cms.InputTag("offlineSlimmedPrimaryVertices"),
                                      genParticleLabel=cms.InputTag("prunedGenParticles"),
                                      pileupSummary = cms.InputTag("slimmedAddPileupInfo"),
                                      Cand3MuLabel=cms.InputTag("ThreeMuonsVtxKalmanFit"),
                                      triggerResults = cms.InputTag("TriggerResults", "", "HLT"),
                                      objects = cms.InputTag("unpackedPatTrigger"),
                                      AlgInputTag = cms.InputTag( "gtStage2Digis" ),
                                      algInputTag = cms.InputTag( "gtStage2Digis" ),
                                      extInputTag = cms.InputTag( "gtStage2Digis" )
                                      
)




process.Tau3MuSkim = cms.Path(process.ThreeMuonSelSeq*
                              process.unpackedPatTrigger*
                              process.TreeMakerBkg
                     )





