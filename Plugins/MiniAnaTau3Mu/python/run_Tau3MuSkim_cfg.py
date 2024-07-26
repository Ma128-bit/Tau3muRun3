import FWCore.ParameterSet.Config as cms

process = cms.Process('Tau3MuSkim')

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
#process.load("Configuration.Geometry.GeometryIdeal_cff")
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

#process.GlobalTag.globaltag = '94X_dataRun2_ReReco_EOY17_v6'
process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_TrancheIV_v6'
#process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_RealisticBS_25ns_13TeV2016_v1_mc'
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )


process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #'/store/cmst3/user/gpetrucc/miniAOD/v1/TT_Tune4C_13TeV-pythia8-tauola_PU_S14_PAT.root'
        #'/store/mc/RunIIFall17MiniAODv2/ZToMuMu_NNPDF31_13TeV-powheg_M_50_120/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/90000/FEFE887F-E944-E811-ADCB-A0369FE2C14A.root'
        #'/store/mc/RunIISummer16MiniAODv2/DsToTau_To3Mu_MuFilter_TuneCUEP8M1_13TeV-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/ECAA9E63-C5FD-E711-9C1E-008CFAE451DC.root'
        'root://xrootd-cms.infn.it//store/mc/RunIISummer16MiniAODv2/DsToTau_To3Mu_MuFilter_TuneCUEP8M1_13TeV-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/D699CEF5-E1FA-E711-A7EC-02163E013399.root'
        #'root://xrootd-cms.infn.it//store/data/Run2017F/DoubleMuonLowMass/MINIAOD/17Nov2017-v1/00000/129CB4BC-17FD-E711-8D49-FA163E838299.root'

    )
)

#process.demo = cms.EDAnalyzer("MiniAna2017Tree",
#                              isMcLabel = cms.untracked.bool(True),
#                              muonLabel=cms.InputTag("slimmedMuons"),
#                              VertexLabel=cms.InputTag("offlineSlimmedPrimaryVertices"),
#                              genParticleLabel=cms.InputTag("packedGenParticles") 
#)


process.options = cms.untracked.PSet(
  SkipEvent = cms.untracked.vstring( "Error: uninitialized ProxyBase used" ),
  #IgnoreCompletely = cms.untracked.vstring( "ProductNotFound" )
)

#process.TFileService = cms.Service("TFileService",
#                                   fileName = cms.string("histoMuon.root")
#)

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string("test.root"),
                               outputCommands = cms.untracked.vstring(
        'keep *',
        )
)

process.p = cms.Path(process.ThreeMuonSelSeq)

process.outpath = cms.EndPath(process.out)
