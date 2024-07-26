import FWCore.ParameterSet.Config as cms

import copy
from HLTrigger.HLTfilters.hltHighLevel_cfi import *
from PhysicsTools.PatAlgos.producersLayer1.genericParticleProducer_cfi import patGenericParticles
from PhysicsTools.PatAlgos.producersLayer1.muonProducer_cfi import patMuons
from PhysicsTools.PatAlgos.selectionLayer1.muonSelector_cfi import *
#from PhysicsTools.PatAlgos.triggerLayer1.triggerEventProducer_cfi import *
#from PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cfi import *
#from PhysicsTools.PatAlgos.tools.trigTools import *

Tau3MuHLTFilter = copy.deepcopy(hltHighLevel)
Tau3MuHLTFilter.throw = cms.bool(False)
Tau3MuHLTFilter.HLTPaths = ["HLT_DoubleMu3_Trk_Tau3mu*", "HLT_DoubleMu3_TkMu_DsTau3Mu_v*", "HLT_DoubleMu3_Trk_Tau3mu_NoL1Mass_v*"]
#list taken from https://github.com/cms-sw/cmssw/blob/CMSSW_9_2_X/HLTrigger/Configuration/tables/GRun.txt


PatMuons = patMuons.clone(
    src = cms.InputTag("muons"),
    useParticleFlow = cms.bool( False ),
    #embedHighLevelSelection = cms.bool(True),
    computeMiniIso = cms.bool(False), 
    computeMuonMVA= cms.bool(False),
    computeSoftMuonMVA = cms.bool(True),
    addTriggerMatching = cms.bool(True),
    addGenMatch   = cms.bool(False),
    embedGenMatch = cms.bool(False),
)


#selectedPatMuons.src = cms.InputTag("PatMuons")




#patTrigger.onlyStandAlone = cms.bool( True )
##patTrigger.addL1Algos =cms.bool( False )


"""
muonTriggerMatchHLTMuons = cms.EDProducer(
  # matching in DeltaR, sorting by best DeltaR
  "PATTriggerMatcherDRDPtLessByR"
  # matcher input collections
, src     = cms.InputTag( 'selectedPatMuons' )
, matched = cms.InputTag( 'patTrigger' )
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
                          src = cms.InputTag("PatMuons"),
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
InitialPlots = cms.EDAnalyzer('SimpleEventCounter',
                                   muonsInputTag = cms.InputTag("muons"),
                                   )

PlotsMatchedMuonsHLT = cms.EDAnalyzer('RecoMuonAnalyzer',
                                   muonsInputTag = cms.InputTag("PatMuons"),
                                   )

PlotsAfterTrigger = cms.EDAnalyzer('RecoMuonAnalyzer',
                                   muonsInputTag = cms.InputTag("PatMuons"),
                                   )

PlotsAfterLooseMuon = cms.EDAnalyzer('RecoMuonAnalyzer',
                                   muonsInputTag = cms.InputTag("looseMuons"),
                                   )

PlotsAfter3Muons = cms.EDAnalyzer('RecoMuonAnalyzer',
                                   muonsInputTag = cms.InputTag("looseMuons"),
                                   )

PlotsAfterTauCand = cms.EDAnalyzer('RecoMuonAnalyzer',
                                   muonsInputTag = cms.InputTag("looseMuons"),
                                   )





ThreeMuonSelSeq = cms.Sequence(InitialPlots *
                               Tau3MuHLTFilter *
                               PatMuons *
                               PlotsAfterTrigger *
                               #selectedPatMuons *
                               #patTrigger *
                               #muonTriggerMatchHLTMuons 
                               #patTriggerEvent
                               looseMuons *
                               PlotsAfterLooseMuon *
                               ThreeMuonsFilter *
                               PlotsAfter3Muons *
                               ThreeMuonsCand *
                               ThreeMuonsCandFilter *
                               ThreeMuonsVtxKinFit *
                               ThreeMuonsVtxKalmanFit *
                               PlotsAfterTauCand
                               )








