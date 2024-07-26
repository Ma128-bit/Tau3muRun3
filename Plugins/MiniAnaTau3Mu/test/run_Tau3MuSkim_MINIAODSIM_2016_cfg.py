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
process.load("MiniAna2017.MiniAna2017Tree.Tau3MuSkim_cff")

#process.GlobalTag.globaltag = '94X_dataRun2_ReReco_EOY17_v6' #data2017
#process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_TrancheIV_v6' #mc2016
process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_RealisticBS_25ns_13TeV2016_v1_mc' #mc2017
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )


process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #'file:./B0A2E5AE-60AF-E811-8BF5-0CC47A7E6A5C.root'
        '/store/mc/RunIISummer16MiniAODv2/DsToTau_To3Mu_MuFilter_TuneCUEP8M1_13TeV-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/ECAA9E63-C5FD-E711-9C1E-008CFAE451DC.root'
        #'root://xrootd-cms.infn.it//store/mc/RunIISummer16MiniAODv2/DsToTau_To3Mu_MuFilter_TuneCUEP8M1_13TeV-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/D699CEF5-E1FA-E711-A7EC-02163E013399.root'
        #'root://xrootd-cms.infn.it//store/data/Run2017F/DoubleMuonLowMass/MINIAOD/17Nov2017-v1/00000/129CB4BC-17FD-E711-8D49-FA163E838299.root'

    )
)

#process.demo = cms.EDAnalyzer("MiniAna2017Tree",
#                              isMcLabel = cms.untracked.bool(True),
#                              muonLabel=cms.InputTag("slimmedMuons"),
#                              VertexLabel=cms.InputTag("offlineSlimmedPrimaryVertices"),
#                              genParticleLabel=cms.InputTag("packedGenParticles") 
#)


#process.options = cms.untracked.PSet(
#  SkipEvent = cms.untracked.vstring( "Error: uninitialized ProxyBase used" ),
  #IgnoreCompletely = cms.untracked.vstring( "ProductNotFound" )
#)

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("histoSkimMiniAOD.root"))


process.Tau3MuSkim = cms.Path(process.ThreeMuonSelSeq 
                     )

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string("fileMINIADOSIM.root"),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('Tau3MuSkim')),
                               outputCommands = cms.untracked.vstring(
        'drop *',
        'keep *_*_*_Tau3MuSkim', 
        'keep *_offlineSlimmedPrimaryVertices_*_*',
        'keep *_generator_*_*',
        'keep *_offlineBeamSpot_*_*',
        'keep *_slimmedMuons_*_*',
        'keep *_TriggerResults_*_*',
        'keep *_gtStage2Digis_*_*',
        'keep *_gmtStage2Digis_*_*',
        'keep *_scalersRawToDigi_*_*',
        'keep *_offlineSlimmedPrimaryVertices_*_*',
        'keep *_patTrigger_*_*',
        'keep *_slimmedAddPileupInfo_*_*',
        'keep *_slimmedMETs_*_*',
        'keep *_slimmedMETsNoHF_*_*',
        'keep *_slimmedMETsPuppi_*_*',
        'keep *_packedGenParticles_*_*',
        'keep *_selectedPatTrigger_*_*',
        'keep *_offlineSlimmedPrimaryVertices_*_*',
        'keep *_slimmedSecondaryVertices_*_*',
        'keep *_bunchSpacingProducer_*_*',
        )
)


process.outpath = cms.EndPath(process.out) 




