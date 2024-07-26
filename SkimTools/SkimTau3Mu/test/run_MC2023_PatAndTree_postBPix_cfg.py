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

process.GlobalTag.globaltag = '130X_mcRun3_2023_realistic_postBPix_v2' #MC2023

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )


process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
      #'root://xrootd-cms.infn.it//'
      '/store/user/caruta/Pythia8_DsTau3mu_Run3_2022/124X_mcRun3_2022_realistic_v12_MINIAODSIM/221120_083655/0000/DsTau3mu_2022_step2_1.root'
     #'/store/user/caruta/Pythia8_DsTau3mu_Run3_2022/124X_mcRun3_2022_realistic_v12_GEN-SIM/221118_095107/0000/DsTau3mu_2022_step0_963.root'
      #'/store/user/caruta/Pythia8_DsToTauTo3Mu_Run3_2022_GEN-SIM/MCRun3_ToTauTo3Mu_MINIAODSIM/220913_053056/0000/DsTau3mu_2022_step2_10.root', '/store/user/caruta/Pythia8_DsToTauTo3Mu_Run3_2022_GEN-SIM/MCRun3_ToTauTo3Mu_MINIAODSIM/220913_053056/0000/DsTau3mu_2022_step2_100.root', '/store/user/caruta/Pythia8_DsToTauTo3Mu_Run3_2022_GEN-SIM/MCRun3_ToTauTo3Mu_MINIAODSIM/220913_053056/0000/DsTau3mu_2022_step2_101.root', '/store/user/caruta/Pythia8_DsToTauTo3Mu_Run3_2022_GEN-SIM/MCRun3_ToTauTo3Mu_MINIAODSIM/220913_053056/0000/DsTau3mu_2022_step2_102.root', '/store/user/caruta/Pythia8_DsToTauTo3Mu_Run3_2022_GEN-SIM/MCRun3_ToTauTo3Mu_MINIAODSIM/220913_053056/0000/DsTau3mu_2022_step2_103.root', '/store/user/caruta/Pythia8_DsToTauTo3Mu_Run3_2022_GEN-SIM/MCRun3_ToTauTo3Mu_MINIAODSIM/220913_053056/0000/DsTau3mu_2022_step2_104.root', '/store/user/caruta/Pythia8_DsToTauTo3Mu_Run3_2022_GEN-SIM/MCRun3_ToTauTo3Mu_MINIAODSIM/220913_053056/0000/DsTau3mu_2022_step2_105.root', '/store/user/caruta/Pythia8_DsToTauTo3Mu_Run3_2022_GEN-SIM/MCRun3_ToTauTo3Mu_MINIAODSIM/220913_053056/0000/DsTau3mu_2022_step2_106.root', '/store/user/caruta/Pythia8_DsToTauTo3Mu_Run3_2022_GEN-SIM/MCRun3_ToTauTo3Mu_MINIAODSIM/220913_053056/0000/DsTau3mu_2022_step2_107.root', '/store/user/caruta/Pythia8_DsToTauTo3Mu_Run3_2022_GEN-SIM/MCRun3_ToTauTo3Mu_MINIAODSIM/220913_053056/0000/DsTau3mu_2022_step2_108.root', '/store/user/caruta/Pythia8_DsToTauTo3Mu_Run3_2022_GEN-SIM/MCRun3_ToTauTo3Mu_MINIAODSIM/220913_053056/0000/DsTau3mu_2022_step2_109.root', '/store/user/caruta/Pythia8_DsToTauTo3Mu_Run3_2022_GEN-SIM/MCRun3_ToTauTo3Mu_MINIAODSIM/220913_053056/0000/DsTau3mu_2022_step2_11.root', '/store/user/caruta/Pythia8_DsToTauTo3Mu_Run3_2022_GEN-SIM/MCRun3_ToTauTo3Mu_MINIAODSIM/220913_053056/0000/DsTau3mu_2022_step2_110.root', '/store/user/caruta/Pythia8_DsToTauTo3Mu_Run3_2022_GEN-SIM/MCRun3_ToTauTo3Mu_MINIAODSIM/220913_053056/0000/DsTau3mu_2022_step2_111.root', '/store/user/caruta/Pythia8_DsToTauTo3Mu_Run3_2022_GEN-SIM/MCRun3_ToTauTo3Mu_MINIAODSIM/220913_053056/0000/DsTau3mu_2022_step2_112.root', '/store/user/caruta/Pythia8_DsToTauTo3Mu_Run3_2022_GEN-SIM/MCRun3_ToTauTo3Mu_MINIAODSIM/220913_053056/0000/DsTau3mu_2022_step2_113.root', '/store/user/caruta/Pythia8_DsToTauTo3Mu_Run3_2022_GEN-SIM/MCRun3_ToTauTo3Mu_MINIAODSIM/220913_053056/0000/DsTau3mu_2022_step2_114.root', '/store/user/caruta/Pythia8_DsToTauTo3Mu_Run3_2022_GEN-SIM/MCRun3_ToTauTo3Mu_MINIAODSIM/220913_053056/0000/DsTau3mu_2022_step2_115.root'
    ),
            #eventsToProcess = cms.untracked.VEventRange('320012:56448719')
)


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("TreeMC.root"))




process.unpackedPatTrigger = cms.EDProducer("PATTriggerObjectStandAloneUnpacker",
    patTriggerObjectsStandAlone = cms.InputTag( 'slimmedPatTrigger' ),
    triggerResults              = cms.InputTag( 'TriggerResults::HLT' ),
    unpackFilterLabels = cms.bool(True)
)

process.TreeMakerBkg = cms.EDAnalyzer("MiniAnaTau3Mu",
                                      isMcLabel = cms.untracked.bool(True),
                                      isAnaLabel = cms.untracked.bool(True),
                                      is2016Label = cms.untracked.bool(True),
                                      is2017Label = cms.untracked.bool(True),
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





