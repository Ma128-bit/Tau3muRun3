import FWCore.ParameterSet.Config as cms

import copy
from HLTrigger.HLTfilters.hltHighLevel_cfi import *
from PhysicsTools.PatAlgos.producersLayer1.genericParticleProducer_cfi import patGenericParticles
from PhysicsTools.PatAlgos.producersLayer1.muonProducer_cfi import patMuons


Tau3MuHLTFilter = copy.deepcopy(hltHighLevel)
Tau3MuHLTFilter.throw = cms.bool(False)
Tau3MuHLTFilter.HLTPaths = ["HLT_DoubleMu3_Trk_Tau3mu*", "HLT_DoubleMu3_TkMu_DsTau3Mu_v*", "HLT_DoubleMu3_Trk_Tau3mu_NoL1Mass_v*"]
#list taken from https://github.com/cms-sw/cmssw/blob/CMSSW_9_2_X/HLTrigger/Configuration/tables/GRun.txt

"""
muonTriggerMatchHLTMuons = cms.EDProducer(
  # matching in DeltaR, sorting by best DeltaR
  "PATTriggerMatcherDRDPtLessByR"
  # matcher input collections
, src     = cms.InputTag( 'slimmedMuons' )
, matched = cms.InputTag( 'selectedPatTrigger' )
  # selections of trigger objects
, matchedCuts = cms.string( 'type( "TriggerMuon" ) && path("HLT_DoubleMu3_TkMu_DsTau3Mu_v*" )' )
  # selection of matches
, maxDPtRel   = cms.double( 0.5 ) 
, maxDeltaR   = cms.double( 0.5 )
, maxDeltaEta = cms.double( 0.2 ) # no effect here
  # definition of matcher output
, resolveAmbiguities    = cms.bool( False )
, resolveByMatchQuality = cms.bool( False )
)
"""

looseMuons = cms.EDFilter("PATMuonSelector",
                          src = cms.InputTag("slimmedMuons"),
                          #cut = cms.string('pt > 0.5 &&  abs(eta)<2.4 && (innerTrack().isNonnull) && (charge!=0) && (innerTrack().hitPattern().numberOfValidPixelHits()>0) && innerTrack.quality("highPurity")'), 
                          cut = cms.string('pt > 0.5 &&  abs(eta)<2.4 && (innerTrack().isNonnull) && (charge!=0) && (innerTrack().hitPattern().numberOfValidPixelHits()>0)'), 
                          filter = cms.bool(True)                                
)

ThreeMuonsFilter = cms.EDFilter("CandViewCountFilter",
                             src = cms.InputTag("looseMuons"),
                             minNumber = cms.uint32(3)
)


ThreeMuonsCand = cms.EDProducer("CandViewShallowCloneCombiner",
                         checkCharge = cms.bool(False),
                         #cut = cms.string('(mass < 10) && (mass >0.5)  && (abs(charge)=1) && (abs(daughter(0).vz - daughter(1).vz) < 1) && (abs(daughter(1).vz - daughter(2).vz) < 1) && (abs(daughter(0).vz - daughter(2).vz) < 1)'),
                         cut = cms.string('(mass < 10) && (mass >0.5)  && (abs(charge)=1)'),       
                         decay = cms.string("looseMuons looseMuons looseMuons")
) 

ThreeMuonsCandFilter = cms.EDFilter("CandViewCountFilter",
                             src = cms.InputTag("ThreeMuonsCand"),
                             minNumber = cms.uint32(1)
)

ThreeMuonsVtxKinFit = cms.EDProducer("KinematicVertexFitCompositeCandProducer",
                                     src = cms.InputTag("ThreeMuonsCand")
                                     )

ThreeMuonsVtxKalmanFit = cms.EDProducer("KalmanVertexFitCompositeCandProducer",
                                        src = cms.InputTag("ThreeMuonsCand")
                                        )


########################Define Histograms########################
InitialPlots = cms.EDAnalyzer('RecoMuonAnalyzer',
                                   muonsInputTag = cms.InputTag("slimmedMuons"),
                                   )

PlotsMatchedMuonsHLT = cms.EDAnalyzer('RecoMuonAnalyzer',
                                   muonsInputTag = cms.InputTag("slimmedMuons"),
                                   )

PlotsAfterTrigger = cms.EDAnalyzer('RecoMuonAnalyzer',
                                   muonsInputTag = cms.InputTag("slimmedMuons"),
                                   )

PlotsAfterLooseMuon = cms.EDAnalyzer('RecoMuonAnalyzer',
                                   muonsInputTag = cms.InputTag("slimmedMuons"),
                                   )

PlotsAfter3Muons = cms.EDAnalyzer('RecoMuonAnalyzer',
                                   muonsInputTag = cms.InputTag("slimmedMuons"),
                                   )

PlotsAfterTauCand = cms.EDAnalyzer('RecoMuonAnalyzer',
                                   muonsInputTag = cms.InputTag("slimmedMuons"),
                                   )





ThreeMuonSelSeq = cms.Sequence(InitialPlots *
                               Tau3MuHLTFilter *
                               PlotsAfterTrigger *
                               looseMuons *
                               #ConcreteLooseMuons *
                               PlotsAfterLooseMuon *
                               ThreeMuonsFilter *
                               PlotsAfter3Muons *
                               ThreeMuonsCand *
                               ThreeMuonsCandFilter *
                               PlotsAfterTauCand *
                               ThreeMuonsVtxKinFit *
                               ThreeMuonsVtxKalmanFit
                               )







