/*
 
 Description: [one line class summary]
 
 Implementation:
 [Notes on implementation]
 */
//
// Original Author:  Federica Simone
//
//


// system include files
#include <memory>
#include <algorithm>
// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/EDGetToken.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include <DataFormats/MuonReco/interface/MuonFwd.h>
#include <DataFormats/MuonReco/interface/Muon.h>
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "TFile.h"
#include "TH1.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TH2.h"
#include "TTree.h"
#include "TLorentzVector.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"
#include "RecoBTag/SecondaryVertex/interface/SecondaryVertex.h"
#include "RecoVertex/AdaptiveVertexFit/interface/AdaptiveVertexFitter.h"


#include "RecoVertex/KinematicFit/interface/KinematicParticleVertexFitter.h"
#include "RecoVertex/KinematicFitPrimitives/interface/KinematicParticleFactoryFromTransientTrack.h"
#include "RecoVertex/KinematicFit/interface/MassKinematicConstraint.h"
#include "RecoVertex/KinematicFit/interface/KinematicParticleFitter.h"
#include "RecoVertex/KinematicFitPrimitives/interface/MultiTrackKinematicConstraint.h"
#include "RecoVertex/KinematicFit/interface/KinematicConstrainedVertexFitter.h"
#include "RecoVertex/KinematicFit/interface/TwoTrackMassKinematicConstraint.h"
#include "RecoVertex/KinematicFitPrimitives/interface/KinematicParticle.h"
#include "RecoVertex/KinematicFitPrimitives/interface/RefCountedKinematicParticle.h"
#include "RecoVertex/KinematicFitPrimitives/interface/TransientTrackKinematicParticle.h"
#include "RecoVertex/KinematicFitPrimitives/interface/KinematicTree.h"


#include "RecoVertex/KinematicFit/interface/KinematicParticleVertexFitter.h"
#include "RecoVertex/KinematicFit/interface/KinematicParticleFitter.h"
#include "RecoVertex/KinematicFit/interface/MassKinematicConstraint.h"
#include "RecoVertex/KinematicFitPrimitives/interface/KinematicParticle.h"
#include "RecoVertex/KinematicFitPrimitives/interface/RefCountedKinematicParticle.h"
#include "RecoVertex/KinematicFitPrimitives/interface/TransientTrackKinematicParticle.h"
#include "RecoVertex/KinematicFitPrimitives/interface/TransientTrackKinematicParticle.h"
#include "RecoVertex/KinematicFitPrimitives/interface/KinematicParticleFactoryFromTransientTrack.h"
#include "RecoVertex/AdaptiveVertexFit/interface/AdaptiveVertexFitter.h"


#include "TrackingTools/Records/interface/TrackingComponentsRecord.h"

#include "TrackingTools/TransientTrack/interface/TransientTrackFromFTSFactory.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/PatternTools/interface/ClosestApproachInRPhi.h"

#include "DataFormats/Candidate/interface/VertexCompositeCandidateFwd.h"
#include "DataFormats/Candidate/interface/CompositeCandidate.h"

#include "RecoVertex/VertexPrimitives/interface/ConvertToFromReco.h"
#include "DataFormats/TrackReco/interface/TrackBase.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "SimDataFormats/Vertex/interface/SimVertex.h"
#include "SimDataFormats/Vertex/interface/SimVertexContainer.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Common/interface/TriggerResultsByName.h"

#include "PhysicsTools/PatUtils/interface/TriggerHelper.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "DataFormats/PatCandidates/interface/TriggerFilter.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "DataFormats/Candidate/interface/OverlapChecker.h"
#include "TrackingTools/IPTools/interface/IPTools.h"

#include "DataFormats/L1Trigger/interface/Muon.h"
#include "CondFormats/L1TObjects/interface/L1GtTriggerMenu.h"
#include "CondFormats/DataRecord/interface/L1GtTriggerMenuRcd.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutRecord.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/L1TGlobal/interface/GlobalAlgBlk.h"
#include "L1Trigger/L1TGlobal/interface/L1TGlobalUtil.h"
#include "CondFormats/DataRecord/interface/L1TUtmTriggerMenuRcd.h"
#include "CondFormats/L1TObjects/interface/L1TUtmTriggerMenu.h"
#include "CondFormats/DataRecord/interface/L1TGlobalPrescalesVetosRcd.h"
#include "CondFormats/L1TObjects/interface/L1TGlobalPrescalesVetos.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"
#include "DataFormats/TrackReco/interface/TrackToTrackMap.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
OverlapChecker overlap;

typedef pair<const reco::MuonChamberMatch*, const reco::MuonSegmentMatch*> MatchPair;


////
class DsPhiPiTreeMakerMINI : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
public:
    explicit DsPhiPiTreeMakerMINI(const edm::ParameterSet&);
    ~DsPhiPiTreeMakerMINI();
    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
    float dR(float eta1, float eta2, float phi1, float phi2);
    float dRtriggerMatch(pat::Muon m, std::vector<pat::TriggerObjectStandAlone> triggerObjects);
    float dRtriggerMatchTrk(reco::Track Trk, std::vector<pat::TriggerObjectStandAlone> triggerObjects);
    void beginRun(edm::Run const &, edm::EventSetup const&, edm::Event const&);
    void fillMatchInfo(const pat::Muon&);
    
    
private:
    virtual void beginJob() override;
    virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
    // virtual void beginRun(edm::Run const &, edm::EventSetup const&) override;
    virtual void endJob() override;
    edm::EDGetTokenT<edm::View<pat::Muon> > muons_;
    edm::EDGetTokenT<edm::View<reco::Vertex> > vertex_;
    //edm::EDGetTokenT<edm::View<reco::Track> > trackToken_;
    //edm::EDGetTokenT<std::vector<pat::PackedCandidate> > trackToken_;
    edm::EDGetTokenT<edm::View<pat::PackedCandidate> > trackToken_;
    //edm::EDGetTokenT<edm::View<reco::CompositeCandidate> > Cand3Mu_;
    edm::EDGetTokenT<edm::View<reco::CompositeCandidate> > Cand2Mu1Track_;
    edm::EDGetTokenT<edm::View<reco::CompositeCandidate> > DiMuon_;
    edm::EDGetTokenT<edm::View<reco::GenParticle> > genParticles_;
    edm::EDGetTokenT<std::vector<PileupSummaryInfo> > puToken_ ;
    edm::EDGetTokenT<edm::TriggerResults> triggerToken_;
    edm::EDGetTokenT<BXVector<l1t::Muon> > l1muonsToken_;
    edm::EDGetTokenT<reco::BeamSpot> token_BeamSpot;
    //edm::EDGetTokenT<trigger::TriggerEvent> trigeventToken_;
    edm::EDGetToken algToken_;
    edm::EDGetToken algTok_;
    edm::ESGetToken<TransientTrackBuilder, TransientTrackRecord> theTransientTrackBuilder_;
    //edm::ESGetToken<L1TUtmTriggerMenu,L1TUtmTriggerMenuRcd> theL1TUtmTriggerMenu_;
    edm::EDGetTokenT<std::vector<pat::PackedCandidate> >srcCands_;
    edm::EDGetTokenT<std::vector<pat::TriggerObjectStandAlone> > triggerObjects_;
    bool is3Mu;
    bool isMc;
    bool isAna;
    bool is2016;
    bool is2017;
    bool is2018;
    bool isBParking;
    //edm::EDGetTokenT<edm::TriggerResults> trigResultsToken;
    //edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> trigObjCollToken;
    //const TransientTrackBuilder* theTransientTrackBuilder_;
    HLTConfigProvider hltConfig;
    //TPMERegexp* _re;
    
    edm::Service<TFileService> fs;
    l1t::L1TGlobalUtil* gtUtil_; 
    TH1F *hEvents;
    TH1F *hEventsAfterGoodCand;
    
    edm::EDGetToken algInputTag_;
    //edm::EDGetToken algTag_, extTag_;
    const edm::InputTag algTag_, extTag_;
    
    /*
    TH1F *hEvents_3Mu, *hEvents_MuFilter, *hEvents_DiMuonDz, *hEvent_TauCharge, *hEvent_3MuonVtx, *hEvent_3MuonMass, *hEvent_Valid3MuonVtx; 
    TH1F *hGenMuonPt; TH1F *hGenMuonEta;
    TH1F *hMuonPt; TH1F *hMuonP; TH1F *hMuonEta, *hGlobalMuonEta, *hTrackerMuonEta, *hLooseMuonEta, *hSoftMuonEta;
    TH1F *hGlobalMuonPt, *hSoftMuonPt, *hLooseMuonPt, *hTrackerMuonPt;
    TH1F *hMuonNumberOfValidHits;
    TH1F *hMuonDB; TH1F *hMuonTime; TH1F *hMuonTimeErr;
    TH1F *hGenTauPt, *hDiMuonDz, *hDiMuonDR, *hGoodMuSize, *hMuonSize_GoodDiMu;
    TH1F *hThreeMuonInvMass, *hThreeMuonCharge, *hVtxSize, *hTau_vFit_chi2, *h3MuonMassVtxFit;
    TH2F *hMuonTimeVsP;
    */

    /////tree
    TTree*      tree_;
    std::vector<float>  MuonPt, MuonEta, MuonPhi;
    std::vector<double> MuonEnergy,  MuonCharge;
    std::vector<int> GenParticle_PdgId, GenParticle_MotherPdgId, GenParticle_isDs_mother, GenParticle_isDs_daughters;
    std::vector<int> evt_isPrompt;
    std::vector<double> GenParticle_Pt, GenParticle_Eta, GenParticle_Phi;
    
    //Vtx position
    std::vector<double> Muon_vx, Muon_vy, Muon_vz;
    
    //MuonID
    std::vector<double> Muon_isGlobal, Muon_isTracker, Muon_isSoft, Muon_isLoose, Muon_isMedium, Muon_isPF, Muon_isRPCMuon, Muon_isStandAloneMuon, Muon_isTrackerMuon, Muon_isCaloMuon, Muon_isQualityValid, Muon_isTimeValid, Muon_isIsolationValid, Muon_numberOfMatchedStations, Muon_numberOfMatches;
    
    //MuonTime
    std::vector<double>  Muon_timeAtIpInOut, Muon_timeAtIpInOutErr;
    
    //Muon inner + outer track
    std::vector<double>  Muon_GLnormChi2, Muon_GLhitPattern_numberOfValidMuonHits, Muon_trackerLayersWithMeasurement, Muon_Numberofvalidpixelhits, Muon_outerTrack_p, Muon_outerTrack_eta, Muon_outerTrack_phi, Muon_outerTrack_normalizedChi2, Muon_outerTrack_muonStationsWithValidHits, Muon_innerTrack_p, Muon_innerTrack_eta, Muon_innerTrack_phi, Muon_innerTrack_normalizedChi2, Muon_QInnerOuter;
    
    std::vector<double>   Muon_combinedQuality_updatedSta, Muon_combinedQuality_trkKink, Muon_combinedQuality_glbKink, Muon_combinedQuality_trkRelChi2, Muon_combinedQuality_staRelChi2, Muon_combinedQuality_chi2LocalPosition, Muon_combinedQuality_chi2LocalMomentum, Muon_combinedQuality_localDistance, Muon_combinedQuality_globalDeltaEtaPhi, Muon_combinedQuality_tightMatch, Muon_combinedQuality_glbTrackProbability, Muon_calEnergy_em, Muon_calEnergy_emS9, Muon_calEnergy_emS25, Muon_calEnergy_had, Muon_calEnergy_hadS9, Muon_segmentCompatibility, Muon_caloCompatibility, Muon_ptErrOverPt, Muon_BestTrackPt, Muon_BestTrackPtErr, Muon_BestTrackEta, Muon_BestTrackEtaErr, Muon_BestTrackPhi, Muon_BestTrackPhiErr;

    std::vector<double> Muon_combinedQuality_match1_dX, Muon_combinedQuality_match1_pullX, Muon_combinedQuality_match1_pullDxDz, Muon_combinedQuality_match1_dY, Muon_combinedQuality_match1_pullY, Muon_combinedQuality_match1_pullDyDz, Muon_combinedQuality_match2_dX, Muon_combinedQuality_match2_pullX, Muon_combinedQuality_match2_pullDxDz, Muon_combinedQuality_match2_dY, Muon_combinedQuality_match2_pullY, Muon_combinedQuality_match2_pullDyDz;

    std::vector<int>  Muon_PdgId, Muon_MotherPdgId, Muon_simFlavour;
    
    std::vector<double>  Mu01_Pt, Mu01_Eta, Mu01_Phi, Mu02_Pt, Mu02_Eta, Mu02_Phi, GenMatchMu01_SimPt, GenMatchMu02_SimPt, GenMatchMu01_SimEta, GenMatchMu02_SimEta, GenMatchMu01_SimPhi, GenMatchMu02_SimPhi, GenMatchMu01_Pt, GenMatchMu02_Pt, GenMatchMu01_Eta, GenMatchMu02_Eta, GenMatchMu01_Phi, GenMatchMu02_Phi, GenMatchMu03_Phi;
    
    std::vector<float> Mu01_dRtriggerMatch, Mu02_dRtriggerMatch, Tr_dRtriggerMatch;
    std::vector<float> Mu1_dRtriggerMatch_Mu7, Mu2_dRtriggerMatch_Mu7, Mu3_dRtriggerMatch_Mu7;
    std::vector<float> Mu1_dRtriggerMatch_Mu8, Mu2_dRtriggerMatch_Mu8, Mu3_dRtriggerMatch_Mu8;
    std::vector<float> Mu1_dRtriggerMatch_Mu8_IP5, Mu1_dRtriggerMatch_Mu8_IP6, Mu1_dRtriggerMatch_Mu9_IP0, Mu1_dRtriggerMatch_Mu9_IP3, Mu1_dRtriggerMatch_Mu9_IP4, Mu1_dRtriggerMatch_Mu9_IP5, Mu1_dRtriggerMatch_Mu9_IP6, Mu1_dRtriggerMatch_Mu12_IP6;
    std::vector<double> Mu1_dRtriggerMatch_2017, Mu2_dRtriggerMatch_2017, Mu3_dRtriggerMatch_2017;
    std::vector<double> Mu1_dRtriggerMatch, Mu2_dRtriggerMatch, Mu3_dRtriggerMatch;
    
    std::vector<double> Muon_emEt03, Muon_hadEt03, Muon_nJets03, Muon_nTracks03, Muon_sumPt03, Muon_emEt05, Muon_hadEt05, Muon_nJets05, Muon_nTracks05, Muon_sumPt05,
    Muon_hadVetoEt03,Muon_emVetoEt03, Muon_trackerVetoPt03, Muon_hadVetoEt05, Muon_emVetoEt05, Muon_trackerVetoPt05;
    
    std::vector<double> Triplet_mindca_iso, Triplet_relativeiso, Triplet_relativeiso2;
    std::vector<int>  Mu01_TripletIndex, Mu02_TripletIndex, Tr_TripletIndex, selectedTripletsIndex;
    std::vector<double>  Mu1_NTracks03iso, Mu2_NTracks03iso, Mu3_NTracks03iso;
    
    int TripletCollectionSize, TripletCollectionSize2, PVCollection_Size, MuonCollectionSize, SelectedTripletsSize;

    std::vector<double>  TripletVtx2_x, TripletVtx2_y, TripletVtx2_z, TripletVtx2_Chi2, TripletVtx2_NDOF, Triplet2_Mass, Triplet2_Pt, Triplet2_Eta, Triplet2_Phi, Triplet2_Charge;
    
    std::vector<double>  dxy_mu1,  dxy_mu2,  dxy_mu3,  dxyErr_mu1,  dxyErr_mu2,  dxyErr_mu3;
    
    std::vector<double>  RefittedPV2_x;
    std::vector<double>  RefittedPV2_y;
    std::vector<double>  RefittedPV2_z;
    std::vector<double>  RefittedPV2_NTracks;
    std::vector<int>     RefittedPV2_isValid;
    std::vector<double>  RefittedPV_Chi2, RefittedPV_nDOF;
    std::vector<double>  PV_bis_Chi2, PV_bis_nDOF;
    
    //RefittedPV_Chi2.push_back(PVertex.);
    
    std::vector<double>  FlightDistPVSV2;
    std::vector<double>  FlightDistPVSV2_Err;
    std::vector<double>  FlightDistPVSV2_Significance;
    std::vector<double>  FlightDistPVSV2_chi2;

    std::vector<double>  Track_pt, Track_eta, Track_phi, Track_charge, Track_normalizedChi2, Track_numberOfValidHits, Track_dxy, Track_dxyError, Track_dz, Track_dzError, Track_vx, Track_vy, Track_vz;
    std::vector<double>  Tr_Pt, Tr_Phi, Tr_Eta;
    std::vector<int>  Track_pdgId;
   
    std::vector<double> RefTrack1_Pt, RefTrack1_Eta, RefTrack1_Phi, RefTrack1_TripletIndex;
    std::vector<double> RefTrack2_Pt, RefTrack2_Eta, RefTrack2_Phi, RefTrack2_TripletIndex;
    std::vector<double> RefTrack3_Pt, RefTrack3_Eta, RefTrack3_Phi, RefTrack3_TripletIndex;

    std::vector<double> RefittedSV_Chi2, RefittedSV_nDOF, RefittedSV_Mass;

    std::vector<double> IsoTrackMu1_Pt, IsoTrackMu1_Eta, IsoTrackMu1_Phi;
    std::vector<double> IsoTrackMu2_Pt, IsoTrackMu2_Eta, IsoTrackMu2_Phi;
    std::vector<double> IsoTrackMu3_Pt, IsoTrackMu3_Eta, IsoTrackMu3_Phi;
 
    std::vector<double> PV_x,  PV_y,  PV_z,  PV_NTracks;
    std::vector<double> BS_x,  BS_y,  BS_z;
    std::vector<double> Vtx12_x, Vtx23_x, Vtx13_x, Vtx12_y, Vtx23_y, Vtx13_y, Vtx12_z, Vtx23_z, Vtx13_z, Vtx12_Chi2, Vtx23_Chi2, Vtx13_Chi2, Vtx12_nDOF, Vtx23_nDOF, Vtx13_nDOF;
    
    std::vector<int> NGoodTriplets;
    uint  evt, run, lumi, puN;
    std::vector<string>  Trigger_l1name;
    std::vector<int> Trigger_l1decision;
    std::vector<int> Trigger_l1prescale;
    
    std::vector<string>  Trigger_hltname;
    std::vector<int> Trigger_hltdecision;
    
    std::vector<double> MuonPt_HLT,  MuonEta_HLT,  MuonPhi_HLT;
    std::vector<double> MuonPt_HLT2017, MuonEta_HLT2017, MuonPhi_HLT2017, MuonPt_HLT_BPMu7, MuonEta_HLT_BPMu7, MuonPhi_HLT_BPMu7, MuonPt_HLT_BPMu8, MuonEta_HLT_BPMu8, MuonPhi_HLT_BPMu8, MuonPt_HLT_BPMu8_IP6,  MuonEta_HLT_BPMu8_IP6, MuonPhi_HLT_BPMu8_IP6, MuonPt_HLT_BPMu8_IP5, MuonEta_HLT_BPMu8_IP5, MuonPhi_HLT_BPMu8_IP5,   MuonPt_HLT_BPMu9_IP0, MuonEta_HLT_BPMu9_IP0, MuonPhi_HLT_BPMu9_IP0, MuonPt_HLT_BPMu9_IP3, MuonEta_HLT_BPMu9_IP3, MuonPhi_HLT_BPMu9_IP3, MuonPt_HLT_BPMu9_IP4,MuonEta_HLT_BPMu9_IP4,MuonPhi_HLT_BPMu9_IP4,MuonPt_HLT_BPMu9_IP5, MuonEta_HLT_BPMu9_IP5,MuonPhi_HLT_BPMu9_IP5,MuonPt_HLT_BPMu9_IP6,MuonEta_HLT_BPMu9_IP6,MuonPhi_HLT_BPMu9_IP6,MuonPt_HLT_BPMu12_IP6,MuonEta_HLT_BPMu12_IP6,MuonPhi_HLT_BPMu12_IP6;
    std::vector<double> MuonPt_HLT_DiMu_Incl, MuonEta_HLT_DiMu_Incl, MuonPhi_HLT_DiMu_Incl;
    std::vector<double> MuonPt_HLT_DiMu_Incl_displ, MuonEta_HLT_DiMu_Incl_displ, MuonPhi_HLT_DiMu_Incl_displ;
    std::vector<double> MuonPt_HLT_Dimuon, MuonEta_HLT_Dimuon, MuonPhi_HLT_Dimuon;
 
    std::vector<double> Muon_innerTrack_ValidFraction, Muon_innerTrack_highPurity, Muon_Numberofvalidtrackerhits, Muon_MVA, Muon_SoftMVA_Val,Muon_validMuonHitComb;
    
    std::vector<double>  DistXY_PVSV,  DistXY_significance_PVSV;
    std::vector<double>  Triplet_IsoMu3, Triplet_IsoMu2, Triplet_IsoMu1;
    std::vector<double>  FlightDistBS_SV,  FlightDistBS_SV_Err,  FlightDistBS_SV_Significance;
    
    std::vector<double> L1Muon_Pt, L1Muon_Eta, L1Muon_Phi, L1Muon_EtaAtVtx, L1Muon_PhiAtVtx, L1Muon_BX, L1Muon_Quality, L1Muon_Charge, L1Muon_ChargeValid, L1Muon_TfMuonIndex, L1Muon_dPhi, L1Muon_dEta, L1Muon_rank, L1Muon_isoSum;
   
    /////SyncTree
    /*
    TTree*      SyncTree_;
    std::vector<float>  allmuons_pt, leadmuon_pt, leadmuon_phi, leadmuon_eta;
    std::vector<float>  alltracks_pt, leadtrack_pt,  leadtrack_eta,  leadtrack_phi;
    uint nprimevtxs, nmuons, evt, run, lumi;
    */
};

    
DsPhiPiTreeMakerMINI::DsPhiPiTreeMakerMINI(const edm::ParameterSet& iConfig){
    //edm::InputTag algInputTag_;
    isMc = iConfig.getUntrackedParameter<bool>("isMcLabel");
    isAna = iConfig.getUntrackedParameter<bool>("isAnaLabel");
    is2016 = iConfig.getUntrackedParameter<bool>("is2016Label");
    is2017= iConfig.getUntrackedParameter<bool>("is2017Label");
    is2018= iConfig.getUntrackedParameter<bool>("is2018Label");
    isBParking= iConfig.getUntrackedParameter<bool>("isBParkingLabel");
    //is3Mu = iConfig.getUntrackedParameter<bool>("is3MuLabel");
    muons_ = consumes<edm::View<pat::Muon> >  (iConfig.getParameter<edm::InputTag>("muonLabel"));
    vertex_ = consumes<edm::View<reco::Vertex> > (iConfig.getParameter<edm::InputTag>("VertexLabel"));
    //trackToken_ = consumes<edm::View<reco::Track> > (iConfig.getParameter<edm::InputTag>("TracksLabel"));
    //trackToken_ = consumes<std::vector<pat::PackedCandidate> > (iConfig.getParameter<edm::InputTag>("TracksLabel"));
    trackToken_ = consumes<edm::View<pat::PackedCandidate> > (iConfig.getParameter<edm::InputTag>("TracksLabel"));
    genParticles_ = consumes<edm::View<reco::GenParticle>  > (iConfig.getParameter<edm::InputTag>("genParticleLabel"));
    srcCands_ = consumes<std::vector<pat::PackedCandidate> >(edm::InputTag("packedPFCandidates"));
    //Cand3Mu_ = consumes<edm::View<reco::CompositeCandidate> > (iConfig.getParameter<edm::InputTag>("Cand3MuLabel"));
    Cand2Mu1Track_ = consumes<edm::View<reco::CompositeCandidate> > (iConfig.getParameter<edm::InputTag>("Cand2Mu1TrackLabel"));
    DiMuon_ = consumes<edm::View<reco::CompositeCandidate> > (iConfig.getParameter<edm::InputTag>("DiMuonLabel"));
    puToken_ =   consumes<std::vector<PileupSummaryInfo> >(iConfig.getParameter<edm::InputTag>("pileupSummary"));
    triggerToken_ = consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("triggerResults"));
    //trigeventToken_ = consumes<trigger::TriggerEvent>(iConfig.getParameter<edm::InputTag>("triggerSummary"));
    algToken_ = consumes<BXVector<GlobalAlgBlk>>(iConfig.getParameter<edm::InputTag>("AlgInputTag"));
    algInputTag_ = consumes<BXVector<GlobalAlgBlk>>(iConfig.getParameter<edm::InputTag>("AlgInputTag"));
    //theL1TUtmTriggerMenu_ = esConsumes<L1TUtmTriggerMenu,L1TUtmTriggerMenuRcd>(edm::ESInputTag("", "TheL1TUtmTriggerMenu"));
    //gtUtil_ = new l1t::L1TGlobalUtil(iConfig, consumesCollector(), *this, algInputTag_, algInputTag_);
    algTok_ = consumes<BXVector<GlobalAlgBlk>>(iConfig.getParameter<edm::InputTag>("algInputTag"));
    //extTag_ = consumes<BXVector<GlobalAlgBlk>>(iConfig.getParameter<edm::InputTag>("extInputTag"));
    //edm::InputTag algTag = iConfig.getParameter<edm::InputTag>("algInputTag");
    //edm::InputTag extTag = iConfig.getParameter<edm::InputTag>("extInputTag");
    gtUtil_ = new l1t::L1TGlobalUtil(iConfig, consumesCollector(), *this, algTag_, extTag_, l1t::UseEventSetupIn::Event);
    token_BeamSpot = consumes<reco::BeamSpot>(edm::InputTag("offlineBeamSpot"));
    l1muonsToken_ = consumes<BXVector<l1t::Muon>>(edm::InputTag("gmtStage2Digis", "Muon"  , "RECO"));
    theTransientTrackBuilder_ = esConsumes<TransientTrackBuilder, TransientTrackRecord>(edm::ESInputTag("", "TransientTrackBuilder"));
    triggerObjects_ = consumes<std::vector<pat::TriggerObjectStandAlone> >(iConfig.getParameter<edm::InputTag>("objects"));
    //tauToken_(consumes(iConfig.getParameter("taus"))),
    //metToken_(consumes(iConfig.getParameter("mets")))
    //tree_(0);
    //MuonPt(0);
}


DsPhiPiTreeMakerMINI::~DsPhiPiTreeMakerMINI()
{
    // do anything here that needs to be done at desctruction time
    // (e.g. close files, deallocate resources etc.)
}

float DsPhiPiTreeMakerMINI::dR(float eta1, float eta2, float phi1, float phi2){
    float dphi=(phi1-phi2);
    float deta=(eta1-eta2);
    float deltaR= TMath::Sqrt(dphi*dphi + deta*deta);
    return deltaR;
}

float DsPhiPiTreeMakerMINI::dRtriggerMatch(pat::Muon m, vector<pat::TriggerObjectStandAlone> triggerObjects) {
    float dRmin = 1.;
    for (unsigned int i = 0 ; i < triggerObjects.size() ; i++) {
        float deltaR = sqrt( reco::deltaR2(triggerObjects[i].eta(), triggerObjects[i].phi(), m.eta(), m.phi()));
        //float deltaR = sqrt( pow(triggerObjects[i].eta() - m.eta(), 2) + pow(acos(cos(triggerObjects[i].phi() - m.phi())), 2));
        if (deltaR < dRmin) dRmin = deltaR;
    }
    return dRmin;
}
    
float DsPhiPiTreeMakerMINI::dRtriggerMatchTrk(reco::Track Trk, vector<pat::TriggerObjectStandAlone> triggerObjects) {
    float dRmin = 1.;
    for (unsigned int i = 0 ; i < triggerObjects.size() ; i++) {
        float deltaR = sqrt( reco::deltaR2(triggerObjects[i].eta(), triggerObjects[i].phi(), Trk.eta(), Trk.phi()));
        //float deltaR = sqrt( pow(triggerObjects[i].eta() - m.eta(), 2) + pow(acos(cos(triggerObjects[i].phi() - m.phi())), 2));
        if (deltaR < dRmin) dRmin = deltaR;
    }
    return dRmin;
}
    
bool isGoodTrack(const reco::Track &track) {
    if(track.pt()>1){
        if(std::fabs(track.eta())<2.4){
            if(track.hitPattern().trackerLayersWithMeasurement()>5){
                if(track.hitPattern().pixelLayersWithMeasurement()>1) return true;
            }
        }
    }
    return false;
}
    
typedef std::map<const reco::Track*, reco::TransientTrack> TransientTrackMap;
// auxiliary function to exclude tracks associated to tau lepton decay "leg"
// from primary event vertex refit
bool tracksMatchByDeltaR(const reco::Track* trk1, const reco::Track* trk2)
{
    if ( reco::deltaR(*trk1, *trk2) < 1.e-2 && trk1->charge() == trk2->charge() ) return true;
    else return false;
}
    
void removeTracks(TransientTrackMap& pvTracks_toRefit, const std::vector<reco::Track*> svTracks)
{
    for ( std::vector<reco::Track*>::const_iterator svTrack = svTracks.begin(); svTrack != svTracks.end(); ++svTrack ){
        //--- remove track from list of tracks included in primary event vertex refit
        //    if track matches by reference or in eta-phi
        //    any of the tracks associated to tau lepton decay "leg"
        for ( TransientTrackMap::iterator pvTrack = pvTracks_toRefit.begin(); pvTrack != pvTracks_toRefit.end(); ++pvTrack ) {
            if ( tracksMatchByDeltaR(pvTrack->first, *svTrack) ) {
                pvTracks_toRefit.erase(pvTrack);
                break;
            }
        }
    }
}
    
bool tracksMatchByDeltaR2(const reco::TransientTrack trk1, const reco::Track* trk2)
{
    //cout<<" pv_t eta="<<trk1.track().eta()<<" sv_t eta="<<trk2->eta()<<" deltaR(tk1, tk2)="<<reco::deltaR(trk1.track(), *trk2)<<endl;                 
    if ( reco::deltaR(trk1.track(), *trk2) < 1.e-2 && trk1.track().charge() == trk2->charge() ) return true;
    else return false;
}


    
void removeTracks3(vector<reco::TransientTrack> &pvTracks, const std::vector<reco::Track*> svTracks)
{
    // cout<<"Inside Remove Tracks: pvtracks="<<pvTracks.size()<<endl;                                                                                  
    for ( std::vector<reco::Track*>::const_iterator svTrack = svTracks.begin(); svTrack != svTracks.end(); ++svTrack ){
        for(uint f=0;f<pvTracks.size(); f++){
            if ( tracksMatchByDeltaR2(pvTracks.at(f), *svTrack) ) {
                //cout<<" track to be erased position: "<<f<<" eta="<<pvTracks.at(f).track().eta()<<endl;                                               
                pvTracks.erase(pvTracks.begin()+f);
                break;
            }
        }
    }
}

//mathing muon track and segment
//taken from Bmm5 code https://github.com/drkovalskyi/Bmm5/blob/master/NanoAOD/plugins/BmmMuonIdProducer.cc

const MatchPair&
getBetterMatch(const MatchPair& match1, const MatchPair& match2){

  // Prefer DT over CSC simply because it's closer to IP
  // and will have less multiple scattering (at least for
  // RB1 vs ME1/3 case). RB1 & ME1/2 overlap is tiny
  if (match2.first->detector() == MuonSubdetId::DT and
      match1.first->detector() != MuonSubdetId::DT)
    return match2;

  // For the rest compare local x match. We expect that
  // segments belong to the muon, so the difference in
  // local x is a reflection on how well we can measure it
  if ( abs(match1.first->x - match1.second->x) >
       abs(match2.first->x - match2.second->x) )
    return match2;
    
  return match1;
}

float dX(const MatchPair& match){
  if (match.first and match.second->hasPhi())
    return (match.first->x - match.second->x);
  else
    return -99;
}

float pullX(const MatchPair& match){
  if (match.first and match.second->hasPhi())
    return dX(match) /
      sqrt(pow(match.first->xErr, 2) + pow(match.second->xErr, 2));
  else
    return -99;
}

float pullDxDz(const MatchPair& match){
  if (match.first and match.second->hasPhi())
    return (match.first->dXdZ - match.second->dXdZ) /
           sqrt(pow(match.first->dXdZErr, 2) + pow(match.second->dXdZErr, 2));
  else
    return -99;
}
float dY(const MatchPair& match){
  if (match.first and match.second->hasZed())
    return (match.first->y - match.second->y);
  else
    return -99;
}

float pullY(const MatchPair& match){
  if (match.first and match.second->hasZed())
    return dY(match) /
      sqrt(pow(match.first->yErr, 2) + pow(match.second->yErr, 2));
  else
    return -99;
}

float pullDyDz(const MatchPair& match){
  if (match.first and match.second->hasZed())
    return (match.first->dYdZ - match.second->dYdZ) /
           sqrt(pow(match.first->dYdZErr, 2) + pow(match.second->dYdZErr, 2));
  else
    return -99;
}

void DsPhiPiTreeMakerMINI::fillMatchInfo(const pat::Muon& muon){
	// Initiate containter for results
        const int n_stations = 2;
        std::vector<MatchPair> matches;
        for (unsigned int i=0; i < n_stations; ++i)
            matches.push_back(std::pair(nullptr, nullptr));
        
        for (auto& chamberMatch : muon.matches()){
            unsigned int station = chamberMatch.station() - 1;
            if (station >= n_stations) continue;
        
            for (auto& segmentMatch : chamberMatch.segmentMatches){
              if ( not segmentMatch.isMask(reco::MuonSegmentMatch::BestInStationByDR) ||
               not segmentMatch.isMask(reco::MuonSegmentMatch::BelongsToTrackByDR) )
            continue;
        
        
            auto match_pair = MatchPair(&chamberMatch, &segmentMatch);
              
            if (matches[station].first)
                matches[station] = getBetterMatch(matches[station], match_pair);
            else
                matches[station] = match_pair;
            }
        }
        
        
        Muon_combinedQuality_match1_dX.push_back(dX(matches[0]));
        Muon_combinedQuality_match1_pullX.push_back(pullX(matches[0]));
        Muon_combinedQuality_match1_pullDxDz.push_back(pullDxDz(matches[0]));
        Muon_combinedQuality_match1_dY.push_back(dY(matches[0]));
        Muon_combinedQuality_match1_pullY.push_back(pullY(matches[0]));
        Muon_combinedQuality_match1_pullDyDz.push_back(pullDyDz(matches[0]));
        
        Muon_combinedQuality_match2_dX.push_back(dX(matches[1]));
        Muon_combinedQuality_match2_pullX.push_back(pullX(matches[1]));
        Muon_combinedQuality_match2_pullDxDz.push_back(pullDxDz(matches[1]));
        Muon_combinedQuality_match2_dY.push_back(dY(matches[1]));
        Muon_combinedQuality_match2_pullY.push_back(pullY(matches[1]));
        Muon_combinedQuality_match2_pullDyDz.push_back(pullDyDz(matches[1]));
}

void DsPhiPiTreeMakerMINI::beginRun(edm::Run const& iRun, edm::EventSetup const& iSetup, const edm::Event& iEvent) {
    //edm::Handle<edm::TriggerResults> trigResults; //our trigger result object
    //edm::InputTag trigResultsTag("TriggerResults"," ","HLT"); //make sure have correct process on MC
    //iEvent.getByLabel(trigResultsTag,trigResults);
    /*
    bool changed = true;
    if (hltConfig.init(iRun, iSetup, trigResultsTag.process(), changed)) {
        // if init returns TRUE, initialisation has succeeded!
        std::cout << "HLT config with process name "<< trigResultsTag.process() << " successfully extracted"<<std::endl;
    }
    else {
        // if init returns FALSE, initialisation has NOT succeeded, which indicates a problem
        // with the file and/or code and needs to be investigated!
        std::cout << "Error! HLT config extraction with process name " << trigResultsTag.process() << " failed"<<std::endl;
        // In this case, all access methods will return empty values!
    }
   */
}
    
    
    
void
DsPhiPiTreeMakerMINI::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;
    using namespace std;
    using namespace reco;
    using std::vector;
    
    edm::Handle< edm::View<reco::Vertex> >vertices;
    iEvent.getByToken(vertex_, vertices);
    if (vertices->empty()) return; // skip the event if no PV found
    const reco::Vertex &PV = vertices->front();
    
    edm::Handle< edm::View<pat::Muon> > muons;
    iEvent.getByToken(muons_, muons);

    /*
    edm::Handle<edm::View<reco::CompositeCandidate> > Cand3Mu;
    iEvent.getByToken(Cand3Mu_, Cand3Mu);
    */
    edm::Handle<edm::View<reco::CompositeCandidate> > Cand2Mu1Track;
    iEvent.getByToken(Cand2Mu1Track_, Cand2Mu1Track);

    edm::Handle<edm::View<reco::CompositeCandidate> > DiMuon;
    iEvent.getByToken(DiMuon_, DiMuon);

    edm::Handle< edm::View<reco::GenParticle> > genParticles;
    iEvent.getByToken(genParticles_, genParticles);

    //edm::Handle<edm::View<reco::Track> > trackCollection;
    edm::Handle<edm::View<pat::PackedCandidate> > trackCollection;
    //iEvent.getByToken(trackToken_, trackCollection);
    iEvent.getByToken(trackToken_,trackCollection);

    Handle<TriggerResults> triggerResults;
    iEvent.getByToken(triggerToken_, triggerResults);

    //Handle<trigger::TriggerEvent> triggerSummary;
    //iEvent.getByToken(trigeventToken_, triggerSummary);

    Handle<std::vector<pat::TriggerObjectStandAlone> > triggerObjects;
    iEvent.getByToken(triggerObjects_, triggerObjects);
    
    Handle<BXVector<l1t::Muon> > gmuons;
    iEvent.getByToken(l1muonsToken_, gmuons);

    edm::Handle<std::vector<pat::PackedCandidate> > PFCands;
    iEvent.getByToken(srcCands_,PFCands);
    
    reco::BeamSpot beamSpot;
    edm::Handle<reco::BeamSpot> beamSpotHandle;
    iEvent.getByToken(token_BeamSpot, beamSpotHandle);
    const reco::BeamSpot& beamspot = *beamSpotHandle.product();
    
    double x_bs = 0.0;
    double y_bs = 0.0;
    double z_bs = 0.0;
    if ( beamSpotHandle.isValid() ) {
        beamSpot = *beamSpotHandle;
        x_bs = beamSpot.x0();
        y_bs = beamSpot.y0();
        z_bs = beamSpot.z0();
    }else{
        cout << "No beam spot available from EventSetup \n" << endl;
    }

    Handle<BXVector<GlobalAlgBlk>> alg;
    iEvent.getByToken(algToken_,alg);

    edm::ESHandle<TransientTrackBuilder> theTransientTrackBuilder = iSetup.getHandle(theTransientTrackBuilder_);
    //edm::ESHandle<L1TUtmTriggerMenu> theL1TUtmTriggerMenu = iSetup.getHandle(theL1TUtmTriggerMenu_);
    //edm::ESHandle<TransientTrackBuilder> theTransientTrackBuilder;
    //iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",theTransientTrackBuilder);
    //theTransientTrackBuilder_ = theTransientTrackBuilder.product();
    
    for (int ibx = gmuons->getFirstBX(); ibx <= gmuons->getLastBX(); ++ibx) {
              for (auto itr = gmuons->begin(ibx); itr != gmuons->end(ibx); ++itr) {
                L1Muon_Pt.push_back(itr->pt());
                L1Muon_Eta.push_back(itr->eta());
                L1Muon_Phi.push_back(itr->phi());
                L1Muon_EtaAtVtx.push_back(itr->etaAtVtx());
                L1Muon_PhiAtVtx.push_back(itr->phiAtVtx());
                L1Muon_BX.push_back(ibx);
                L1Muon_Quality.push_back(itr->hwQual());
                L1Muon_Charge.push_back(itr->charge());
                L1Muon_ChargeValid.push_back(itr->hwChargeValid());
                L1Muon_TfMuonIndex.push_back(itr->tfMuonIndex());
                //L1Muon_dPhi.push_back(itr->dPhi());
                //L1Muon_dEta.push_back(itr->dEta());
                L1Muon_rank.push_back(itr->hwRank());
                L1Muon_isoSum.push_back(itr->hwIso());
                //cout << "Muon : " << " BX=" << ibx << " ipt=" << itr->pt() << " eta=" << itr->eta() << " phi=" << itr->phi() << " hweta="<< itr->hwEta()<<" charge="<<itr->charge()<< "rank="<<itr->hwRank()<<std::endl;
              }
            }

    hEvents->Fill(1);

    ///////////////Fill Trigger Vars, L1 and HLT///////////////
    cout << "I'm here !!! " << endl;

    gtUtil_->retrieveL1(iEvent, iSetup, algTok_);
    //theL1TUtmTriggerMenu_->retrieveL1(iEvent, iSetup, algToken_);
    const vector<pair<string, bool> > initialDecisions = gtUtil_->decisionsInitial();
    //const vector<pair<string, bool> > initialDecisions = theL1TUtmTriggerMenu_->decisionsInitial();
    cout << "Fill trigger Var" << endl;
    if (!iEvent.isRealData()) {
        for (size_t i_l1t = 0; i_l1t < initialDecisions.size(); i_l1t++) {
            string l1tName = (initialDecisions.at(i_l1t)).first;
            if(l1tName.find("DoubleMu") != string::npos || l1tName.find("TripleMu") != string::npos ||  l1tName.find("SingleMu")!= string::npos){
                Trigger_l1name.push_back( l1tName );
                Trigger_l1decision.push_back( initialDecisions.at(i_l1t).second );
                Trigger_l1prescale.push_back( 1 );
            }
        }
    }else{
        //ESHandle<L1TGlobalPrescalesVetos> psAndVetos;
        //auto psRcd = iSetup.tryToGet<L1TGlobalPrescalesVetosRcd>();
        //if(psRcd) psRcd->get(psAndVetos);
        //int columnN= gtUtil_->prescaleColumn();
        //int columnN= theL1TUtmTriggerMenu_->prescaleColumn();
        for (size_t i_l1t = 0; i_l1t < initialDecisions.size(); i_l1t++) {
        string l1tName = (initialDecisions.at(i_l1t)).first;
            if(l1tName.find("DoubleMu") != string::npos || l1tName.find("TripleMu") != string::npos ||  l1tName.find("SingleMu")!= string::npos){
                //cout<<"L1Seed="<<l1tName<<" decision="<<initialDecisions.at(i_l1t).second<<" prescale="<<(psAndVetos->prescale_table_)[columnN][i_l1t]<<endl;
                Trigger_l1name.push_back( l1tName );
                Trigger_l1decision.push_back( initialDecisions.at(i_l1t).second );
                //Trigger_l1prescale.push_back( (psAndVetos->prescale_table_)[columnN][i_l1t]);
            }
        }
    }
    const TriggerNames &triggerNames = iEvent.triggerNames( *triggerResults );
    for (size_t i_hlt = 0; i_hlt != triggerResults->size(); ++i_hlt){
        string hltName = triggerNames.triggerName(i_hlt);
        if(hltName.find("HLT_DoubleMu") != string::npos || hltName.find("HLT_Dimuon") != string::npos || hltName.find("HLT_Mu8_IP") != string::npos || hltName.find("HLT_Mu7_IP") != string::npos || (hltName.find("HLT_Mu9_IP") != string::npos) || (hltName.find("HLT_Mu12_IP") != string::npos)){
            //cout<<" HLTPath="<<hltName<<" isPassed="<<triggerResults->accept(i_hlt )<<endl;
            Trigger_hltname.push_back(hltName);
            Trigger_hltdecision.push_back(triggerResults->accept(i_hlt ));
        }
    }
    
    vector<pat::TriggerObjectStandAlone> TriggerObj_DsTau3Mu,  TriggerObj_DsTau3Mu2017, TriggerObj_Dimuon, TriggerObj_DimuonIncl, TriggerObj_DimuonIncl_displ;
    vector<pat::TriggerObjectStandAlone> MuonsObjects_BPMu7, MuonsObjects_BPMu12_IP6, MuonsObjects_BPMu8, MuonsObjects_BPMu8_IP6,MuonsObjects_BPMu8_IP5,MuonsObjects_BPMu9_IP0, MuonsObjects_BPMu9_IP3, MuonsObjects_BPMu9_IP4, MuonsObjects_BPMu9_IP5, MuonsObjects_BPMu9_IP6;
 
    for (pat::TriggerObjectStandAlone obj : *triggerObjects) { // note: not "const &" since we want to call unpackPathNames
        obj.unpackPathNames(triggerNames);
        for (unsigned h = 0; h < obj.filterLabels().size(); ++h) {
            if(obj.filterLabels()[h]=="hltdstau3muDisplaced3muFltr"){
            //std::cout << " Filter: " << obj.filterLabels()[h]<<endl;
            TriggerObj_DsTau3Mu.push_back(obj);
            }  
            if(obj.filterLabels()[h]=="hltTau3muTkVertexFilter"){
                TriggerObj_DsTau3Mu2017.push_back(obj);
            }
            // Inclusive dimu triggers
            if(obj.filterLabels()[h]=="hltDisplacedmumuFilterDoubleMu43LowMass"){
                TriggerObj_DimuonIncl.push_back(obj);
            }
            if(obj.filterLabels()[h]=="hltDisplacedmumuFilterDoubleMu4LowMassDisplaced"){
                TriggerObj_DimuonIncl_displ.push_back(obj);
            }

            if(obj.filterLabels()[h]=="hltDisplacedmumuFilterDimuon0LowMassL1s0er1p5R" || 
               obj.filterLabels()[h]=="hltDisplacedmumuFilterDimuon0LowMassL1s0er1p5" || 
               obj.filterLabels()[h]=="hltDisplacedmumuFilterDimuon0LowMass" || 
               obj.filterLabels()[h]=="hltDisplacedmumuFilterDimuon0LowMassL1s4" || 
               obj.filterLabels()[h]=="hltDisplacedmumuFilterDimuon0LowMassL1s4R" || 
               obj.filterLabels()[h]=="hltDisplacedmumuFilterDimuon0LowMassL1sTM530"){
                TriggerObj_Dimuon.push_back(obj);
            }
           
            if(isBParking){
                if(obj.filterLabels()[h]=="hltL3fL1sMu22OrParkL1f0L2f10QL3Filtered8Q"){
                  MuonsObjects_BPMu8.push_back(obj);
                }
                if(obj.filterLabels()[h]=="hltL3fL1sMu22OrParkL1f0L2f10QL3Filtered7IP4Q"){
                  MuonsObjects_BPMu7.push_back(obj);
                }
                if(obj.filterLabels()[h]=="hltL3fL1sMu22OrParkL1f0L2f10QL3Filtered8IP6Q"){
                  MuonsObjects_BPMu8_IP6.push_back(obj);
                }
                if(obj.filterLabels()[h]=="hltL3fL1sMu22OrParkL1f0L2f10QL3Filtered8IP5Q"){
                  MuonsObjects_BPMu8_IP5.push_back(obj);
                }
                if(obj.filterLabels()[h]=="hltL3fL1sMu22OrParkL1f0L2f10QL3Filtered9IP0Q"){
                  MuonsObjects_BPMu9_IP0.push_back(obj);
                }
                if(obj.filterLabels()[h]=="hltL3fL1sMu22OrParkL1f0L2f10QL3Filtered9IP3Q"){
                  MuonsObjects_BPMu9_IP3.push_back(obj);}
                if(obj.filterLabels()[h]=="hltL3fL1sMu22OrParkL1f0L2f10QL3Filtered9IP4Q"){
                  MuonsObjects_BPMu9_IP4.push_back(obj);
                }
                if(obj.filterLabels()[h]=="hltL3fL1sMu22OrParkL1f0L2f10QL3Filtered9IP5Q"){
                  MuonsObjects_BPMu9_IP5.push_back(obj);
                }
                if(obj.filterLabels()[h]=="hltL3fL1sMu22OrParkL1f0L2f10QL3Filtered9Q"){
                  MuonsObjects_BPMu9_IP6.push_back(obj);
                }
                if(obj.filterLabels()[h]=="hltL3fL1sMu22OrParkL1f0L2f10QL3Filtered12Q"){
                  MuonsObjects_BPMu12_IP6.push_back(obj);
                }
            }//isBParking
            std::vector pathNamesAll = obj.pathNames(false);
            std::vector pathNamesLast = obj.pathNames(true);
        }//loop filterLabels
    }//loop triggerObjects

    //cout<<"TriggerObj_DsTau3Mu.size()="<<TriggerObj_DsTau3Mu.size()<<endl;
    for(uint t=0; t<TriggerObj_DsTau3Mu.size();t++){
        //cout<<" trig obj pt="<<TriggerObj_DsTau3Mu.at(t).pt()<<endl;
        MuonPt_HLT.push_back(TriggerObj_DsTau3Mu.at(t).pt());
        MuonEta_HLT.push_back(TriggerObj_DsTau3Mu.at(t).eta());
        MuonPhi_HLT.push_back(TriggerObj_DsTau3Mu.at(t).phi());
    }
    for(uint t=0; t<TriggerObj_DsTau3Mu2017.size();t++){
        MuonPt_HLT2017.push_back(TriggerObj_DsTau3Mu2017.at(t).pt());
        MuonEta_HLT2017.push_back(TriggerObj_DsTau3Mu2017.at(t).eta());
        MuonPhi_HLT2017.push_back(TriggerObj_DsTau3Mu2017.at(t).phi());
    }
    for(uint t=0; t<TriggerObj_Dimuon.size();t++){
        MuonPt_HLT_Dimuon.push_back(TriggerObj_Dimuon.at(t).pt());
        MuonEta_HLT_Dimuon.push_back(TriggerObj_Dimuon.at(t).eta());
        MuonPhi_HLT_Dimuon.push_back(TriggerObj_Dimuon.at(t).phi());
    }
    // Trigger matching inclusive dimu triggers
    for(uint t=0; t<TriggerObj_DimuonIncl.size();t++){
        MuonPt_HLT_DiMu_Incl.push_back(TriggerObj_DimuonIncl.at(t).pt());
        MuonEta_HLT_DiMu_Incl.push_back(TriggerObj_DimuonIncl.at(t).eta());
        MuonPhi_HLT_DiMu_Incl.push_back(TriggerObj_DimuonIncl.at(t).phi());
    }
    for(uint t=0; t<TriggerObj_DimuonIncl_displ.size();t++){
        MuonPt_HLT_DiMu_Incl_displ.push_back(TriggerObj_DimuonIncl_displ.at(t).pt());
        MuonEta_HLT_DiMu_Incl_displ.push_back(TriggerObj_DimuonIncl_displ.at(t).eta());
        MuonPhi_HLT_DiMu_Incl_displ.push_back(TriggerObj_DimuonIncl_displ.at(t).phi());
    }
    //
    
    for(uint t=0; t<MuonsObjects_BPMu7.size();t++){
        MuonPt_HLT_BPMu7.push_back(MuonsObjects_BPMu7.at(t).pt());
        MuonEta_HLT_BPMu7.push_back(MuonsObjects_BPMu7.at(t).eta());
        MuonPhi_HLT_BPMu7.push_back(MuonsObjects_BPMu7.at(t).phi());
    }
    
    if(isBParking){
        for(uint t=0; t<MuonsObjects_BPMu8.size();t++){
            MuonPt_HLT_BPMu8.push_back(MuonsObjects_BPMu8.at(t).pt());
            MuonEta_HLT_BPMu8.push_back(MuonsObjects_BPMu8.at(t).eta());
            MuonPhi_HLT_BPMu8.push_back(MuonsObjects_BPMu8.at(t).phi());
        }
        for(uint t=0; t<MuonsObjects_BPMu8_IP6.size();t++){
            MuonPt_HLT_BPMu8_IP6.push_back(MuonsObjects_BPMu8_IP6.at(t).pt());
            MuonEta_HLT_BPMu8_IP6.push_back(MuonsObjects_BPMu8_IP6.at(t).eta());
            MuonPhi_HLT_BPMu8_IP6.push_back(MuonsObjects_BPMu8_IP6.at(t).phi());
        }
        for(uint t=0; t<MuonsObjects_BPMu8_IP5.size();t++){
            MuonPt_HLT_BPMu8_IP5.push_back(MuonsObjects_BPMu8_IP5.at(t).pt());
            MuonEta_HLT_BPMu8_IP5.push_back(MuonsObjects_BPMu8_IP5.at(t).eta());
            MuonPhi_HLT_BPMu8_IP5.push_back(MuonsObjects_BPMu8_IP5.at(t).phi());
        }
        for(uint t=0; t<MuonsObjects_BPMu9_IP0.size();t++){
            MuonPt_HLT_BPMu9_IP0.push_back(MuonsObjects_BPMu9_IP0.at(t).pt());
            MuonEta_HLT_BPMu9_IP0.push_back(MuonsObjects_BPMu9_IP0.at(t).eta());
            MuonPhi_HLT_BPMu9_IP0.push_back(MuonsObjects_BPMu9_IP0.at(t).phi());
        }
        for(uint t=0; t< MuonsObjects_BPMu9_IP3.size();t++){
            MuonPt_HLT_BPMu9_IP3.push_back(MuonsObjects_BPMu9_IP3.at(t).pt());
            MuonEta_HLT_BPMu9_IP3.push_back(MuonsObjects_BPMu9_IP3.at(t).eta());
            MuonPhi_HLT_BPMu9_IP3.push_back(MuonsObjects_BPMu9_IP3.at(t).phi());
        }
        for(uint t=0; t< MuonsObjects_BPMu9_IP4.size();t++){
            MuonPt_HLT_BPMu9_IP4.push_back(MuonsObjects_BPMu9_IP4.at(t).pt());
            MuonEta_HLT_BPMu9_IP4.push_back(MuonsObjects_BPMu9_IP4.at(t).eta());
            MuonPhi_HLT_BPMu9_IP4.push_back(MuonsObjects_BPMu9_IP4.at(t).phi());
        }
        for(uint t=0; t< MuonsObjects_BPMu9_IP5.size();t++){
            MuonPt_HLT_BPMu9_IP5.push_back(MuonsObjects_BPMu9_IP5.at(t).pt());
            MuonEta_HLT_BPMu9_IP5.push_back(MuonsObjects_BPMu9_IP5.at(t).eta());
            MuonPhi_HLT_BPMu9_IP5.push_back(MuonsObjects_BPMu9_IP5.at(t).phi());
        }
        for(uint t=0; t< MuonsObjects_BPMu9_IP6.size();t++){
            MuonPt_HLT_BPMu9_IP6.push_back(MuonsObjects_BPMu9_IP6.at(t).pt());
            MuonEta_HLT_BPMu9_IP6.push_back(MuonsObjects_BPMu9_IP6.at(t).eta());
            MuonPhi_HLT_BPMu9_IP6.push_back(MuonsObjects_BPMu9_IP6.at(t).phi());
        }
        for(uint t=0; t< MuonsObjects_BPMu12_IP6.size();t++){
            MuonPt_HLT_BPMu12_IP6.push_back(MuonsObjects_BPMu12_IP6.at(t).pt());
            MuonEta_HLT_BPMu12_IP6.push_back(MuonsObjects_BPMu12_IP6.at(t).eta());
            MuonPhi_HLT_BPMu12_IP6.push_back(MuonsObjects_BPMu12_IP6.at(t).phi());
        }
    }//isBParking

    ///////////////Fill GEN particles///////////////
    if(isMc){
        uint j=0;
        uint ngenP=genParticles->size();
        //cout<<"****************GenLevel Info Begin********************"<<endl;
        uint isPrompt=-1; //0 is prompt; 1 is not prompt
        int isDs_daughters = -1; //-1:not Ds //1:isDs->phi(mumu)pi
        int isDs_mother = -1; //-1:not Ds //1:is prompt pp->Ds//2:is D from B decays
        int phi_index;
        for(edm::View<reco::GenParticle>::const_iterator gp=genParticles->begin(); gp!=genParticles->end(), j<ngenP; ++gp , ++j){
            //if(fabs(gp->pdgId())==15) tauRaw = j;
            int isPhi = -1; //-1: notPhi; 0: isPhi but not ->2mu ;1: phi->2mu
            bool isPi = false;
            phi_index = -1;
            if ( fabs(gp->pdgId()) == 431 ) { //Ds
            isPi = false;
               //cout<<"D_s meson"<<endl;
               //se ha 2 figlie
               if(gp->numberOfDaughters()>=2){
                //if one is a phi
                //I save the index of the phi
                for(uint l=0; l<gp->numberOfDaughters(); l++) {
                if (fabs(gp->daughter(l)->pdgId())==333){
                    phi_index = l;
                    isPhi = 0;
                    cout<<"isPhi"<<endl;
                    if (gp->daughter(phi_index)->numberOfDaughters()>=2){
                    int n_muons = 0;
                    for(uint t=0; t<gp->daughter(phi_index)->numberOfDaughters(); t++) {
                        if (fabs(gp->daughter(phi_index)->daughter(t)->pdgId())==13){
                                n_muons++;
                            }
                    }
                    if (n_muons>=2) isPhi=+1;
                }
                }
                else{
                    if (fabs(gp->daughter(l)->pdgId())==211){
                        isPi = true;
                }
                }
                }
                if (isPi&&isPhi==+1){
                    isDs_daughters = +1;
                }
                //if the phi decays into two muons
                //ci può essere anche un fotone emesso insieme ai due muoni
                // loop sulle figlie
                //se le figlie sono phi->2mu e pi
                }//end if sulle due figlie
                // vediamo se si tratta di un decay prompt (isDs = 2) o non-prompt (isDs = 3)
               //loop sulle madri
               for(uint w=0; w<gp->numberOfMothers(); w++) {
                   //cout<<"  gp->mother("<<t<<")->pdgId() = "<<gp->mother(t)->pdgId()<<endl;
                   if( fabs(gp->mother(w)->pdgId()) == 433 || fabs(gp->mother(w)->pdgId()) == 435 || fabs(gp->mother(w)->pdgId()) == 10431 ) { //D*
                       for(uint i=0; i<gp->mother(w)->numberOfMothers(); i++) {
                           //cout<<"    gp->mother("<<t<<")->mother("<<i<<")->pdgId() = "<<gp->mother(t)->mother(i)->pdgId()<<endl;
                        if(fabs(gp->mother(w)->mother(i)->pdgId())==2212 || (fabs(gp->mother(w)->mother(i)->pdgId())>=1&&fabs(gp->mother(w)->mother(i)->pdgId())<9)||fabs(gp->mother(w)->mother(i)->pdgId())==21||fabs(gp->mother(w)->mother(i)->pdgId())==2101||fabs(gp->mother(w)->mother(i)->pdgId())==2103||fabs(gp->mother(w)->mother(i)->pdgId())==2203) { //p or (udscbt or g) quarks hadronization                             cout<<"    prompt"<<endl;
                             isDs_mother=1;
                           }else{
                             if(fabs(gp->mother(w)->mother(i)->pdgId())==521 || fabs(gp->mother(w)->mother(i)->pdgId())==511 || fabs(gp->mother(w)->mother(i)->pdgId())==531 || fabs(gp->mother(w)->mother(i)->pdgId())==5122 || fabs(gp->mother(w)->mother(i)->pdgId())==5132 || fabs(gp->mother(w)->mother(i)->pdgId())==5232) {
                                cout<<"    from B decay"<<endl;
                                isDs_mother=2;
                             }
                          }
                       }
                   }else{
                      if(fabs(gp->mother(w)->pdgId())==2212 || (fabs(gp->mother(w)->pdgId())>=1&&fabs(gp->mother(w)->pdgId())<9)||fabs(gp->mother(w)->pdgId())==21||fabs(gp->mother(w)->pdgId())==2101||fabs(gp->mother(w)->pdgId())==2103||fabs(gp->mother(w)->pdgId())==2203) { //p or (udsc) quarks hadronization
                         cout<<"    prompt"<<endl;
                         isDs_mother=1;
                      }else{
                         if(fabs(gp->mother(w)->pdgId())==521 || fabs(gp->mother(w)->pdgId())==511 || fabs(gp->mother(w)->pdgId())==531 || fabs(gp->mother(w)->pdgId())==5122 || fabs(gp->mother(w)->pdgId())==5132 || fabs(gp->mother(w)->pdgId())==5232){
                            cout<<"    from B decay"<<endl;
                            isDs_mother=2;
                         }
                      }
                   }
               }//loop sulle madri

            }//if Ds
            if (isDs_daughters == +1 && isDs_mother == +1) isPrompt = 0;
            if (isDs_daughters == +1 && isDs_mother == +2) isPrompt = +1;
            if(fabs(gp->pdgId())==13 || fabs(gp->pdgId())==15  || fabs(gp->pdgId())==11 || fabs(gp->pdgId())==211 || fabs(gp->pdgId())==321 ||  fabs(gp->pdgId())==12  || fabs(gp->pdgId())==14 || fabs(gp->pdgId())==16 || fabs(gp->pdgId())==431 || fabs(gp->pdgId())==333 || fabs(gp->pdgId())==511 || fabs(gp->pdgId())==521) {
                GenParticle_PdgId.push_back(gp->pdgId());
                GenParticle_Pt.push_back(gp->pt());
                GenParticle_Eta.push_back(gp->eta());
                GenParticle_Phi.push_back(gp->phi());
                GenParticle_isDs_daughters.push_back(isDs_daughters);
                GenParticle_isDs_mother.push_back(isDs_mother);

                //if(fabs(gp->pdgId())==13 && gp->numberOfMothers() && fabs(gp->mother(0)->pdgId()) ==333 ){
                //    cout<<"Mu from phi pt="<<gp->pt()<<" vz="<<gp->vz()<<endl;
                //}
                if (gp->numberOfMothers()) {GenParticle_MotherPdgId.push_back(gp->mother(0)->pdgId());
                }else{ GenParticle_MotherPdgId.push_back(-99); }
            }
        }//loop genParticle
    evt_isPrompt.push_back(isPrompt);
    }//isMC

    PVCollection_Size = vertices->size();
    uint kk=0;
    std::vector<uint> VtxIdV;
    cout<<"Number of PFCands="<<PFCands->size()<<endl;
    std::vector<uint> SelectedCandIdx;
    vector<pat::PackedCandidate> MyPFCands;
    for (std::vector<pat::PackedCandidate>::const_iterator cand = PFCands->begin(); cand != PFCands->end(), kk!= PFCands->size(); ++cand, ++kk) {
        if (cand->charge()==0) continue;
        if (cand->vertexRef().isNull()) continue;
        if (!(cand->hasTrackDetails()) ) continue;

       int key = cand->vertexRef().key();
       int quality = cand->pvAssociationQuality();
       if(cand->fromPV(cand->vertexRef().key())<2) continue;
       if( cand->fromPV(cand->vertexRef().key())==2 && quality != pat::PackedCandidate::UsedInFitLoose  ) continue;
       VtxIdV.push_back(key);
       SelectedCandIdx.push_back(kk);
       MyPFCands.push_back(*cand);
    }// loop over the PFCandidates

    //cout<<" vtx id size="<<VtxIdV.size()<<endl;
    sort( VtxIdV.begin(), VtxIdV.end() );
    VtxIdV.erase( unique(VtxIdV.begin(), VtxIdV.end() ),VtxIdV.end() );

    typedef vector<double> MyPt;
    vector<MyPt> AssoPtToVtx;
    vector<pat::PackedCandidate> SelPFCands;
    vector<vector<pat::PackedCandidate>> AssoCandToVtx;

    for(uint i=0; i<VtxIdV.size();i++){
          vector<double> tmp_pt;
          vector<pat::PackedCandidate> tmp_cand;
          for (vector<pat::PackedCandidate>::const_iterator myc = MyPFCands.begin(); myc != MyPFCands.end(); ++myc) {
              //cout<<"cand vtx="<<myc->vertexRef().key()<<" cand pt="<<myc->pt()<<endl;
              if(myc->vertexRef().key()==VtxIdV.at(i)) {
                  tmp_pt.push_back(myc->pt());
                  tmp_cand.push_back(*myc);
              }
          }
          AssoPtToVtx.push_back(tmp_pt);
          AssoCandToVtx.push_back(tmp_cand);
    }
    //cout<<" AssoCandToVtx.size()="<<AssoCandToVtx.size()<<endl;
    
    vector<vector<reco::TransientTrack>> transTracksAssoToVtx;
    for(uint i=0; i<AssoCandToVtx.size();i++){
        //cout<<i<<" vertex ID="<<VtxIdV.at(i)<<" with trk ass. n="<<AssoCandToVtx.at(i).size()<<endl;
        std::auto_ptr<reco::TrackCollection> newTrackCollection = std::auto_ptr<reco::TrackCollection>(new TrackCollection);
        std::vector<reco::TransientTrack> transTracks2;
        
        for(vector<pat::PackedCandidate>::const_iterator c = AssoCandToVtx.at(i).begin(); c != AssoCandToVtx.at(i).end(); ++c) {
            reco::Track myTrack = c->pseudoTrack();
            reco::TransientTrack mytt = theTransientTrackBuilder->build(myTrack);
            if(mytt.isValid()){
                transTracks2.push_back(mytt);
            }
        }
        transTracksAssoToVtx.push_back(transTracks2);
        //cout<<" trans Tracks size="<<transTracksAssoToVtx.at(i).size()<<endl;
    }

    std::vector<int> NTripl;
    bool is2Mu=true;

    if(is2Mu) {
        //Triplets  Loop
        cout<<"Number Of Triplets="<<Cand2Mu1Track->size()<<endl;
        TripletCollectionSize2 = Cand2Mu1Track->size();
        //int TripletIndex2 =-99;
        uint trIn2=0;
        //vector<int> selectedTriplets;
        cout << "Cand2Mu1Track->size(): " << Cand2Mu1Track->size() << endl;
        
        for(edm::View<reco::CompositeCandidate>::const_iterator PhiIt=Cand2Mu1Track->begin(); PhiIt!=Cand2Mu1Track->end(), trIn2<Cand2Mu1Track->size(); ++PhiIt, ++trIn2){
          
            //Daughter Kinematics at reco+gen level
            const Candidate * c1 = PhiIt->daughter(0)->masterClone().get();
            const pat::Muon *mu1 = dynamic_cast<const pat::Muon *>(c1);
          
            const Candidate * c2 = PhiIt->daughter(1)->masterClone().get();
            const pat::Muon *mu2 = dynamic_cast<const pat::Muon *>(c2);
          
            const Candidate * c3 = PhiIt->daughter(2)->masterClone().get();
            const reco::Track *Track3 = c3->bestTrack();
            
            const reco::TransientTrack transientTrack3=theTransientTrackBuilder->build( Track3 );
            //cout << "transientTrack3.isValid(): " << transientTrack3.isValid() << endl;
            if( !(transientTrack3.isValid()) ) continue;
            
            //check overlap among the legs of the triplet
            double dR_13 = sqrt( reco::deltaR2(mu1->eta(), mu1->phi(), c3->eta(), c3->phi()) );
            double dR_23 = sqrt( reco::deltaR2(mu2->eta(), mu2->phi(), c3->eta(), c3->phi()) );
            if(dR_13<0.01 || dR_23<0.01) continue;
            if(!(fabs(c1->eta()- c3->eta())>  1.e-6)) continue;
            if(!(fabs(c2->eta()- c3->eta())>  1.e-6)) continue;
            if(!(PhiIt->vertexChi2()>0)) continue;

            /////////////////VertexFit///////////////////////////////////
            TrackRef trk1, trk2;
            trk1 = mu1->innerTrack();
            trk2 = mu2->innerTrack();
            //if (mu1->isGlobalMuon()) { trk1 = mu1->get<TrackRef,reco::CombinedMuonTag>();}
            //else { trk1 = mu1->get<TrackRef>();}
            //if (mu2->isGlobalMuon()) { trk2 = mu2->get<TrackRef,reco::CombinedMuonTag>();}
            //else{ trk2 = mu2->get<TrackRef>();}
            //cout<<" trk1 id="<<trk1.id()<<" tr2:"<<trk2.id()<<endl;
            //const reco::TransientTrack transientTrack1=theTransientTrackBuilder_->build( trk1 );
            //const reco::TransientTrack transientTrack2=theTransientTrackBuilder_->build( trk2 );
            const reco::TransientTrack transientTrack1=theTransientTrackBuilder->build( trk1 );
            const reco::TransientTrack transientTrack2=theTransientTrackBuilder->build( trk2 );
            reco::Track Track1 =transientTrack1.track();
            reco::Track Track2 =transientTrack2.track();
            reco::Track Track_3 =transientTrack3.track();
            reco::Track* TrackRef1=&Track1;
            reco::Track* TrackRef2=&Track2;
            reco::Track* TrackRef3=&Track_3;
            vector<reco::Track*> SVTrackRef;
            SVTrackRef.push_back(TrackRef1);
            SVTrackRef.push_back(TrackRef2);
            SVTrackRef.push_back(TrackRef3); //da sistemare con kin fit phi->2mu

            ///////////////PV taken as closest to candidate
            reco::Vertex TripletVtx = reco::Vertex(PhiIt->vertex(), PhiIt->vertexCovariance(), PhiIt->vertexChi2(), PhiIt->vertexNdof(), PhiIt->numberOfDaughters() );
            double dphi_pv = -1.0;
            uint primaryvertex_index=0;
            uint selVtxId = 0;

            TLorentzVector ThreeCandidate;
            ThreeCandidate.SetPtEtaPhiM(PhiIt->pt(), PhiIt->eta(), PhiIt->phi(), PhiIt->mass());

            //cout << "PV choice! " << endl;
            //cout << "VtxIdV.size(): " << VtxIdV.size() << endl;
            //cout << "vertices->size(): " << vertices->size() << endl;
                
            if(VtxIdV.size()>0 && vertices->size()>0) {
                for(uint VtxIt =0;VtxIt<vertices->size();VtxIt++ ){
                    for(uint k=0;k<VtxIdV.size();k++){
                        if(VtxIdV[k]==VtxIt){
                            TVector3 Dv3D_reco(TripletVtx.x() - (*vertices)[VtxIt].x(), TripletVtx.y() - (*vertices)[VtxIt].y(), TripletVtx.z() - (*vertices)[VtxIt].z());
                            double Cosdphi_3D = Dv3D_reco.Dot(ThreeCandidate.Vect())/(Dv3D_reco.Mag()*ThreeCandidate.Vect().Mag());
                            //cout<<"cosDPhi3D="<<Cosdphi_3D<<endl;
                            if(Cosdphi_3D>dphi_pv){
                                dphi_pv = Cosdphi_3D;
                                primaryvertex_index=VtxIt;
                                selVtxId=k;
                            }
                        }
                    }
                }
                //cout<<" trans trk coll before ref="<<transTracksAssoToVtx.at(selVtxId).size()<<endl;
                //for(uint t=0; t<transTracksAssoToVtx.at(selVtxId).size(); t++){
                //    cout<<"pv track eta="<<transTracksAssoToVtx.at(selVtxId).at(t).track().eta()<<endl;}

                std::vector<reco::TransientTrack> pvTracks_original;
                TransientTrackMap pvTrackMap_refit;
                //cout << "transTracksAssoToVtx.at(selVtxId).size() before: " << transTracksAssoToVtx.at(selVtxId).size() << endl;
                
                ///// PV before removing SV tracks
                TransientVertex PVertex_bis;
                bool PVertex_bis_fit;
                if(transTracksAssoToVtx.at(selVtxId).size() >1){
                    PVertex_bis_fit = true;
                    KalmanVertexFitter PV_fitter_bis (true);
                    PVertex_bis = PV_fitter_bis.vertex(transTracksAssoToVtx.at(selVtxId));
                }
                else PVertex_bis_fit = false;
                    
                vector<reco::TransientTrack> transTracksAssoToVtx_copy;
                for(std::vector<reco::TransientTrack>::const_iterator transTrack_it = transTracksAssoToVtx.at(selVtxId).begin(); transTrack_it != transTracksAssoToVtx.at(selVtxId).end(); ++transTrack_it){
                    transTracksAssoToVtx_copy.push_back(*transTrack_it);
                }
                    
                removeTracks3(transTracksAssoToVtx_copy,  SVTrackRef);
                //cout << "transTracksAssoToVtx_copy.size() after: " << transTracksAssoToVtx_copy.size() << endl;

                if(transTracksAssoToVtx_copy.size()>1){
                    RefittedPV2_NTracks.push_back(transTracksAssoToVtx_copy.size());

                    /////////////PV Refit//////////////////////////////
                    KalmanVertexFitter PV_fitter (true);
                    TransientVertex PVertex = PV_fitter.vertex(transTracksAssoToVtx_copy);
                    RefittedPV2_isValid.push_back(PVertex.isValid());
                    RefittedPV_Chi2.push_back(PVertex.totalChiSquared());
                    RefittedPV_nDOF.push_back(PVertex.degreesOfFreedom());
                    
                    if(PVertex_bis_fit && PVertex_bis.isValid()){
                        PV_bis_Chi2.push_back(PVertex_bis.totalChiSquared());
                        cout << "PV_bis_Chi2: " << PVertex_bis.totalChiSquared() << endl;
                        PV_bis_nDOF.push_back(PVertex_bis.degreesOfFreedom());
                    }
                    else{
                        cout << "No Valid PV_bis" << endl;
                        PV_bis_Chi2.push_back(-99);
                        PV_bis_nDOF.push_back(-99);
                    }

                    if(PVertex.isValid() && PhiIt->vertexChi2()>0){
                        NTripl.push_back(1);
                        selectedTripletsIndex.push_back(trIn2);

                        Mu01_Pt.push_back(mu1->pt());
                        Mu01_Eta.push_back(mu1->eta());
                        Mu01_Phi.push_back(mu1->phi());
                        Mu01_TripletIndex.push_back(trIn2);
                        
                        Mu02_Pt.push_back(mu2->pt());
                        Mu02_Eta.push_back(mu2->eta());
                        Mu02_Phi.push_back(mu2->phi());
                        Mu02_TripletIndex.push_back(trIn2);
                        
                        Tr_Pt.push_back(Track3->pt());
                        Tr_Eta.push_back(Track3->eta());
                        Tr_Phi.push_back(Track3->phi());
                        Tr_TripletIndex.push_back(trIn2);

                        //Refitted vars related to SV
                        std::vector<reco::TransientTrack> Ttracks;
                        Ttracks.push_back(transientTrack1);
                        Ttracks.push_back(transientTrack2);
                        Ttracks.push_back(transientTrack3);
                        KalmanVertexFitter SVfitter (true);
                        TransientVertex SVertex_ref = SVfitter.vertex(Ttracks);
                        vector < TransientTrack > ttrks = SVertex_ref.refittedTracks();
                        //cout<<"ttrks.size() :"<<ttrks.size()<<endl;

                        TLorentzVector LV_Ds;
                        LV_Ds.SetPxPyPzE(0, 0, 0, 0);

                        if(SVertex_ref.isValid() && SVertex_ref.hasRefittedTracks() && ttrks.size()>2){
                            //cout<<"VALID ref SV chi2="<<SVertex_ref.totalChiSquared()<<" NDF="<<SVertex_ref.degreesOfFreedom()<<endl;
                            reco::Track SVTrack1 =ttrks.at(0).track();
                            reco::Track SVTrack2 =ttrks.at(1).track();
                            reco::Track SVTrack3 =ttrks.at(2).track();

                            TLorentzVector LV1, LV2, LV3;
                            LV1.SetPxPyPzE(SVTrack1.px(), SVTrack1.py(), SVTrack1.pz(), sqrt(pow(SVTrack1.p(), 2.0) + pow(0.10565, 2.0)));
                            LV2.SetPxPyPzE(SVTrack2.px(), SVTrack2.py(), SVTrack2.pz(), sqrt(pow(SVTrack2.p(), 2.0) + pow(0.10565, 2.0)));
                            LV3.SetPxPyPzE(SVTrack3.px(), SVTrack3.py(), SVTrack3.pz(), sqrt(pow(SVTrack3.p(), 2.0) + pow(0.13957018, 2.0)));
                            LV_Ds = LV1 + LV2 + LV3;

                            //cout<<"SVTrack1.pt() "<<SVTrack1.pt()<<" SVTrack1.eta() "<<SVTrack1.eta()<<" SVTrack1.phi() "<<SVTrack1.phi()<<endl;
                            //cout<<"Track1.pt() "<<Track1.pt()<<" Track1.eta() "<<Track1.eta()<<" Track1.phi() "<<Track1.phi()<<endl;
                            //cout<<"SVTrack2.pt() "<<SVTrack2.pt()<<" SVTrack2.eta() "<<SVTrack2.eta()<<" SVTrack2.phi() "<<SVTrack2.phi()<<endl;
                            //cout<<"Track2.pt() "<<Track2.pt()<<" Track2.eta() "<<Track2.eta()<<" Track2.phi() "<<Track2.phi()<<endl;
                            //cout<<"SVTrack3.pt() "<<SVTrack3.pt()<<" SVTrack3.eta() "<<SVTrack3.eta()<<" SVTrack3.phi() "<<SVTrack3.phi()<<endl;
                            //cout<<"Track3.pt() "<<Track3.pt()<<" Track3.eta() "<<Track3.eta()<<" Track3.phi() "<<Track3.phi()<<endl;
                            //cout<<"mu1->pt() "<<mu1->pt()<<" mu2->pt() "<<mu2->pt()<<" mu3->pt() "<<mu3->pt()<<endl;

                            RefTrack1_Pt.push_back(SVTrack1.pt()); RefTrack1_Eta.push_back(SVTrack1.eta()); RefTrack1_Phi.push_back(SVTrack1.phi()); RefTrack1_TripletIndex.push_back(trIn2);
                            RefTrack2_Pt.push_back(SVTrack2.pt()); RefTrack2_Eta.push_back(SVTrack2.eta()); RefTrack2_Phi.push_back(SVTrack2.phi()); RefTrack2_TripletIndex.push_back(trIn2);
                            RefTrack3_Pt.push_back(SVTrack3.pt()); RefTrack3_Eta.push_back(SVTrack3.eta()); RefTrack3_Phi.push_back(SVTrack3.phi()); RefTrack3_TripletIndex.push_back(trIn2);

                            RefittedSV_Chi2.push_back(SVertex_ref.totalChiSquared());
                            RefittedSV_nDOF.push_back(SVertex_ref.degreesOfFreedom());
                            RefittedSV_Mass.push_back(LV_Ds.M());
                            cout<<"Bebug mass LV_Ds.M()="<<LV_Ds.M()<<endl;
                        } else {
                            RefTrack1_Pt.push_back(-99); RefTrack1_Eta.push_back(-99); RefTrack1_Phi.push_back(-99); RefTrack1_TripletIndex.push_back(trIn2);
                            RefTrack2_Pt.push_back(-99); RefTrack2_Eta.push_back(-99); RefTrack2_Phi.push_back(-99); RefTrack2_TripletIndex.push_back(trIn2);
                            RefTrack3_Pt.push_back(-99); RefTrack3_Eta.push_back(-99); RefTrack3_Phi.push_back(-99); RefTrack3_TripletIndex.push_back(trIn2);

                            RefittedSV_Chi2.push_back(-99);
                            RefittedSV_nDOF.push_back(-99);
                            RefittedSV_Mass.push_back(-99);
                        }

                        ///////////////Check Trigger Matching///////////////
                        float dR1 = 999., dR2 = 999., dR3 = 999.;
                        float dR1_Mu7=999.,dR2_Mu7 = 999., dR3_Mu7 = 999.;
                        float dR1_Mu8=999.,dR2_Mu8 = 999., dR3_Mu8 = 999.;
                        float dR1_Mu8_IP6=999., dR1_Mu12_IP6=999, dR1_Mu8_IP5=999.;
                        float dR1_Mu9_IP0=999., dR1_Mu9_IP3=999.,  dR1_Mu9_IP4=999.,  dR1_Mu9_IP5=999., dR1_Mu9_IP6=999.;
                        float dR1_2017 = 999., dR2_2017 = 999., dR3_2017 = 999.;

                        dR1_2017 = DsPhiPiTreeMakerMINI::dRtriggerMatch(*mu1, TriggerObj_DsTau3Mu2017);
                        dR2_2017 = DsPhiPiTreeMakerMINI::dRtriggerMatch(*mu2, TriggerObj_DsTau3Mu2017);
                        dR3_2017 = DsPhiPiTreeMakerMINI::dRtriggerMatchTrk(*Track3, TriggerObj_DsTau3Mu2017);
                        Mu1_dRtriggerMatch_2017.push_back(dR1_2017);
                        Mu2_dRtriggerMatch_2017.push_back(dR2_2017);
                        Mu3_dRtriggerMatch_2017.push_back(dR3_2017);

                        dR1 = DsPhiPiTreeMakerMINI::dRtriggerMatch(*mu1, TriggerObj_DsTau3Mu);
                        dR2 = DsPhiPiTreeMakerMINI::dRtriggerMatch(*mu2, TriggerObj_DsTau3Mu);
                        dR3 = DsPhiPiTreeMakerMINI::dRtriggerMatchTrk(*Track3, TriggerObj_DsTau3Mu);
                        //cout<<"Trigger Matching: dR1="<<dR1<<" dR2="<<dR2<<" dR3="<<dR3<<endl;
                        Mu01_dRtriggerMatch.push_back(dR1);
                        Mu02_dRtriggerMatch.push_back(dR2);
                        Tr_dRtriggerMatch.push_back(dR3);

                        if(isBParking){
                            dR1_Mu8 = DsPhiPiTreeMakerMINI::dRtriggerMatch(*mu1, MuonsObjects_BPMu8);
                            dR2_Mu8 = DsPhiPiTreeMakerMINI::dRtriggerMatch(*mu2, MuonsObjects_BPMu8);
                            dR3_Mu8 = DsPhiPiTreeMakerMINI::dRtriggerMatchTrk(*Track3, MuonsObjects_BPMu8);
                            Mu1_dRtriggerMatch_Mu8.push_back(dR1_Mu8);
                            Mu2_dRtriggerMatch_Mu8.push_back(dR2_Mu8);
                            Mu3_dRtriggerMatch_Mu8.push_back(dR3_Mu8);

                            dR1_Mu7 = DsPhiPiTreeMakerMINI::dRtriggerMatch(*mu1, MuonsObjects_BPMu7);
                            dR2_Mu7 = DsPhiPiTreeMakerMINI::dRtriggerMatch(*mu2, MuonsObjects_BPMu7);
                            dR3_Mu7 = DsPhiPiTreeMakerMINI::dRtriggerMatchTrk(*Track3, MuonsObjects_BPMu7);

                            Mu1_dRtriggerMatch_Mu7.push_back(dR1_Mu7);
                            Mu2_dRtriggerMatch_Mu7.push_back(dR2_Mu7);
                            Mu3_dRtriggerMatch_Mu7.push_back(dR3_Mu7);

                            dR1_Mu8_IP5 = DsPhiPiTreeMakerMINI::dRtriggerMatch(*mu1, MuonsObjects_BPMu8_IP5);
                            Mu1_dRtriggerMatch_Mu8_IP5.push_back(dR1_Mu8_IP5);

                            dR1_Mu8_IP6 = DsPhiPiTreeMakerMINI::dRtriggerMatch(*mu1, MuonsObjects_BPMu8_IP6);
                            Mu1_dRtriggerMatch_Mu8_IP6.push_back(dR1_Mu8_IP6);

                            dR1_Mu9_IP0 = DsPhiPiTreeMakerMINI::dRtriggerMatch(*mu1, MuonsObjects_BPMu9_IP0);
                            Mu1_dRtriggerMatch_Mu9_IP0.push_back(dR1_Mu9_IP0);

                            dR1_Mu9_IP3 = DsPhiPiTreeMakerMINI::dRtriggerMatch(*mu1, MuonsObjects_BPMu9_IP3);
                            Mu1_dRtriggerMatch_Mu9_IP3.push_back(dR1_Mu9_IP3);

                            dR1_Mu9_IP4 = DsPhiPiTreeMakerMINI::dRtriggerMatch(*mu1, MuonsObjects_BPMu9_IP4);
                            Mu1_dRtriggerMatch_Mu9_IP4.push_back(dR1_Mu9_IP4);

                            dR1_Mu9_IP5 = DsPhiPiTreeMakerMINI::dRtriggerMatch(*mu1, MuonsObjects_BPMu9_IP5);
                            Mu1_dRtriggerMatch_Mu9_IP5.push_back(dR1_Mu9_IP5);

                            dR1_Mu9_IP6 = DsPhiPiTreeMakerMINI::dRtriggerMatch(*mu1, MuonsObjects_BPMu9_IP6);
                            Mu1_dRtriggerMatch_Mu9_IP6.push_back(dR1_Mu9_IP6);

                            dR1_Mu12_IP6 = DsPhiPiTreeMakerMINI::dRtriggerMatch(*mu1, MuonsObjects_BPMu12_IP6);
                            Mu1_dRtriggerMatch_Mu12_IP6.push_back(dR1_Mu12_IP6);
                        }//isBParking
                        
                        if(isMc){ //if is TauPhiPi Monte Carlo
                            bool isMatch1=false; bool isMatch2=false; //bool isMatch3=false;
                            if( (mu1->simType() == reco::MatchedMuonFromLightFlavour) && (fabs(mu1->simMotherPdgId()) == 333) ){ //chiedi mu 13 e richiesta su mother 333
                                isMatch1=true;
                            }
                            if( (mu2->simType() == reco::MatchedMuonFromLightFlavour) && (fabs(mu2->simMotherPdgId()) == 333) ){
                                isMatch2=true;
                            }
                            if( isMatch1 && isMatch2) {
                                //cout<<" Matched Di-muon mass="<<PhiIt->mass()<<endl;
                                GenMatchMu01_SimPt.push_back(mu1->simPt());
                                GenMatchMu02_SimPt.push_back(mu2->simPt());
                  
                                GenMatchMu01_SimEta.push_back(mu1->simEta());
                                GenMatchMu02_SimEta.push_back(mu2->simEta());
                  
                                GenMatchMu01_SimPhi.push_back(mu1->simPhi());
                                GenMatchMu02_SimPhi.push_back(mu2->simPhi());
                  
                                GenMatchMu01_Pt.push_back(mu1->pt());
                                GenMatchMu02_Pt.push_back(mu2->pt());
                  
                                GenMatchMu01_Eta.push_back(mu1->eta());
                                GenMatchMu02_Eta.push_back(mu2->eta());
                  
                                GenMatchMu01_Phi.push_back(mu1->phi());
                                GenMatchMu02_Phi.push_back(mu2->phi());
                            }
                        }//isMC
                        //GenVtx vars to be added

                        ////Triplets Vars
                        TripletVtx2_x.push_back(PhiIt->vx());
                        TripletVtx2_y.push_back(PhiIt->vy());
                        TripletVtx2_z.push_back(PhiIt->vz());
                      
                        TripletVtx2_Chi2.push_back(PhiIt->vertexChi2());
                        TripletVtx2_NDOF.push_back(PhiIt->vertexNdof());
                      
                        Triplet2_Mass.push_back(PhiIt->mass());
                        Triplet2_Pt.push_back(PhiIt->pt());
                        Triplet2_Eta.push_back(PhiIt->eta());
                        Triplet2_Phi.push_back(PhiIt->phi());
                        Triplet2_Charge.push_back(PhiIt->charge());
                        //Matrix covariance to be added!!!
                            
                        ////////////////////  Dimu vertices  ////////////////////
                        std::vector<reco::TransientTrack> SVTracks12_Vtx, SVTracks23_Vtx, SVTracks13_Vtx;
                        
                        SVTracks12_Vtx.push_back(transientTrack1);
                        SVTracks12_Vtx.push_back(transientTrack2);
                        SVTracks23_Vtx.push_back(transientTrack2);
                        SVTracks23_Vtx.push_back(transientTrack3);
                        SVTracks13_Vtx.push_back(transientTrack1);
                        SVTracks13_Vtx.push_back(transientTrack3);
                        
                        KalmanVertexFitter DiMu12_fitter (true);
                        TransientVertex DiMu12Vtx = DiMu12_fitter.vertex(SVTracks12_Vtx);
                        if(DiMu12Vtx.isValid()){
                            Vtx12_Chi2.push_back(DiMu12Vtx.totalChiSquared());
                            cout << "Vtx12_Chi2: " << DiMu12Vtx.totalChiSquared() << endl;
                            Vtx12_nDOF.push_back(DiMu12Vtx.degreesOfFreedom());
                            
                            GlobalPoint DiMu12Pos (DiMu12Vtx.position());
                            Vtx12_x.push_back(DiMu12Pos.x());
                            cout <<"Vtx12_x: " <<DiMu12Pos.x() << endl;
                            Vtx12_y.push_back(DiMu12Pos.y());
                            Vtx12_z.push_back(DiMu12Pos.z());
                        }
                        else{
                            Vtx12_Chi2.push_back(-99);
                            Vtx12_nDOF.push_back(-99);
                            Vtx12_x.push_back(-99);
                            Vtx12_y.push_back(-99);
                            Vtx12_z.push_back(-99);
                        }
                        KalmanVertexFitter DiMu23_fitter (true);
                        TransientVertex DiMu23Vtx = DiMu23_fitter.vertex(SVTracks23_Vtx);
                        if(DiMu23Vtx.isValid()){
                            Vtx23_Chi2.push_back(DiMu23Vtx.totalChiSquared());
                            cout << "Vtx23_Chi2: " << DiMu23Vtx.totalChiSquared() << endl;
                            Vtx23_nDOF.push_back(DiMu23Vtx.degreesOfFreedom());
                            
                            GlobalPoint DiMu23Pos (DiMu23Vtx.position());
                            Vtx23_x.push_back(DiMu23Pos.x());
                            cout <<"Vtx23_x: " <<DiMu23Pos.x() << endl;
                            Vtx23_y.push_back(DiMu23Pos.y());
                            Vtx23_z.push_back(DiMu23Pos.z());
                        }
                        else{
                            Vtx23_Chi2.push_back(-99);
                            Vtx23_nDOF.push_back(-99);
                            Vtx23_x.push_back(-99);
                            Vtx23_y.push_back(-99);
                            Vtx23_z.push_back(-99);
                        }
                        
                        KalmanVertexFitter DiMu13_fitter (true);
                        TransientVertex DiMu13Vtx = DiMu13_fitter.vertex(SVTracks13_Vtx);
                        if(DiMu13Vtx.isValid()){
                            Vtx13_Chi2.push_back(DiMu13Vtx.totalChiSquared());
                            cout << "Vtx13_Chi2: " << DiMu13Vtx.totalChiSquared() << endl;
                            Vtx13_nDOF.push_back(DiMu13Vtx.degreesOfFreedom());
                            
                            GlobalPoint DiMu13Pos (DiMu13Vtx.position());
                            Vtx13_x.push_back(DiMu13Pos.x());
                            cout <<"Vtx13_x: " <<DiMu13Pos.x() << endl;
                            Vtx13_y.push_back(DiMu13Pos.y());
                            Vtx13_z.push_back(DiMu13Pos.z());
                        }
                        else{
                            Vtx13_Chi2.push_back(-99);
                            Vtx13_nDOF.push_back(-99);
                            Vtx13_x.push_back(-99);
                            Vtx13_y.push_back(-99);
                            Vtx13_z.push_back(-99);
                        }

                        //Refitted Vars
                        //vector < TransientTrack > ttrks = TripletVtx.refittedTracks();
                            
                        ////Defining ISO VAR related to the triplet
                        math::XYZPoint SVertexPoint = math::XYZPoint(TripletVtx.x(), TripletVtx.y(), TripletVtx.z());
                        TLorentzVector LV1=TLorentzVector( mu1->px(), mu1->py(), mu1->pz(), mu1->energy() );
                        TLorentzVector LV2=TLorentzVector( mu2->px(), mu2->py(), mu2->pz(), mu2->energy() );
                        TLorentzVector LV3=TLorentzVector( c3->px(), c3->py(), c3->pz(), c3->energy() );
                        TLorentzVector LVDs = LV1 + LV2 + LV3;

                        int nTracks03_mu1=0, nTracks03_mu2=0, nTracks03_trk3=0;
                        double mindist=9999;
                        double sumPtTrack1=0, sumPtTrack2=0, sumPtTrack3=0, maxSumPtTracks=0;
                        //int nTracks03_mu1=0, nTracks03_mu2=0, nTracks03_mu3=0;

                        for (std::vector<pat::PackedCandidate>::const_iterator cand = PFCands->begin(); cand != PFCands->end();++cand) {
                            if(  (cand->pt()>1) && (fabs(cand->eta())<2.4) && (cand->trackerLayersWithMeasurement()>5) && (cand->pixelLayersWithMeasurement()>1)  ){
                                double dR1 = sqrt( reco::deltaR2(Track1.eta(), Track1.phi(), cand->eta(), cand->phi()) );
                                double dR2 = sqrt( reco::deltaR2(Track2.eta(), Track2.phi(), cand->eta(), cand->phi()) );
                                double dR3 = sqrt( reco::deltaR2(Track3->eta(), Track3->phi(), cand->eta(), cand->phi()) );

                                if (dR1 < 0.01 || dR2 < 0.01 || dR3 < 0.01) continue;
                                double dz = abs(cand->dz(SVertexPoint));
                                double dxy = abs(cand->dxy(SVertexPoint));
                                double dca_fv = sqrt(dz*dz+dxy*dxy);
                                if(dca_fv<mindist && dca_fv>0) {
                                    //cout<<"dca_fv"<<dca_fv<<endl;
                                    mindist = dca_fv;
                                }
                                //for eack track having pt>1, excluded the muon tracks,
                                //for each muon in the triplet, if deltaR<0.3 and the DCA is smaller than 1 mm
                                //the pt of the track is added -> I will take the largest total pt from the three muons
                                if (dca_fv < 0.1) {
                                   if (dR1<0.3) {
                                      sumPtTrack1+=cand->pt();
                                      nTracks03_mu1++;
                                   }
                                   if (dR2<0.3) {
                                      sumPtTrack2+=cand->pt();
                                      nTracks03_mu2++;
                                   }
                                   if (dR3<0.3) {
                                      sumPtTrack3+=cand->pt();
                                      nTracks03_trk3++;
                                   }
                                }
                            }
                        }//endl loop on tracks

                        Triplet_mindca_iso.push_back(mindist);
                        maxSumPtTracks = std::max(sumPtTrack1, std::max(sumPtTrack2,sumPtTrack3));
                        //cout<<TripletIndex<<" TauMass "<<TauIt->mass()<<" SumPt Tracks in cone="<<maxSumPtTracks<<" TauPt="<<TauIt->pt()<<endl;
                        double relativeiso = maxSumPtTracks/LVDs.Pt();
                        Triplet_relativeiso.push_back(relativeiso);

                        Mu1_NTracks03iso.push_back(nTracks03_mu1);
                        Mu2_NTracks03iso.push_back(nTracks03_mu2);
                        Mu3_NTracks03iso.push_back(nTracks03_trk3);

                        double sumPtTrackRel1=0, sumPtTrackRel2=0, sumPtTrackRel3=0, maxSumPtRelTracks =0;
                        sumPtTrackRel1=sumPtTrack1/LV1.Pt();
                        sumPtTrackRel2=sumPtTrack2/LV2.Pt();
                        sumPtTrackRel3=sumPtTrack3/LV3.Pt();
                        maxSumPtRelTracks = std::max(sumPtTrackRel1, std::max(sumPtTrackRel2,sumPtTrackRel3));
                        Triplet_relativeiso2.push_back(maxSumPtRelTracks);
                        Triplet_IsoMu1.push_back(sumPtTrack1);
                        Triplet_IsoMu2.push_back(sumPtTrack2);
                        Triplet_IsoMu3.push_back(sumPtTrack3);

                        //CachingVertex<5> fittedVertex = vertexFitter.vertex(tracksToVertex);
                        GlobalPoint PVertexPos  (PVertex.position());
                        GlobalPoint SVertexPos  (TripletVtx.x(), TripletVtx.y(), TripletVtx.z());
                        math::XYZPoint PVertexPoint = math::XYZPoint(PVertexPos.x(), PVertexPos.y(), PVertexPos.z());

                        //cout<<" PV Coord after refit="<<PVertexPos.x()<<" y="<<PVertexPos.y()<<" z="<<PVertexPos.z()<<endl;
                        //double FlightDist = TMath::Sqrt( pow(( PVertexPos.x() -SVertexPos.x()),2)+ pow(( PVertexPos.y() -SVertexPos.y()),2) + pow(( PVertexPos.z() -SVertexPos.z()),2));
                         
                        VertexDistance3D vertTool;
                        VertexState PVstate(PVertex.position(),PVertex.positionError());
                        //VertexState SVstate(SVertexPos,TripletVtx.position());
                        double distance = vertTool.distance(PVstate, TripletVtx).value();
                        double dist_err = vertTool.distance(PVstate, TripletVtx).error();
                        double dist_sign =vertTool.distance(PVstate, TripletVtx).significance();
                        //double chi2 = vertTool.compatibility(PVstate, TripletVtx);
                        VertexDistanceXY vdistXY;
                        Measurement1D distXY = vdistXY.distance(TripletVtx, PVertex);
                        DistXY_PVSV.push_back(distXY.value());
                        DistXY_significance_PVSV.push_back(distXY.significance());

                        PV_x.push_back( (*vertices)[primaryvertex_index].x());
                        PV_y.push_back( (*vertices)[primaryvertex_index].y());
                        PV_z.push_back( (*vertices)[primaryvertex_index].z());
                        PV_NTracks.push_back(pvTracks_original.size());
                        
                        RefittedPV2_x.push_back(PVertexPos.x());
                        RefittedPV2_y.push_back(PVertexPos.y());
                        RefittedPV2_z.push_back(PVertexPos.z());
                        //RefittedPV_Chi2.push_back(PVertex.);

                        reco::Vertex::Point NewBSPos(beamSpot.x(PVertexPos.z()), beamSpot.y(PVertexPos.z()), beamSpot.z0());
                        BeamSpot beamSpot_new(NewBSPos, beamSpot.sigmaZ(), beamSpot.dxdz(), beamSpot.dydz(), beamSpot.BeamWidthX(), beamSpot.covariance(), beamSpot.type());
                        VertexState BSstate(beamSpot_new);

                        VertexDistanceXY vertTool2D;
                        double BSdistance2D = vertTool2D.distance(BSstate, TripletVtx).value();
                        double BSdist_err2D = vertTool2D.distance(BSstate, TripletVtx).error();
                        double BSdist_sign2D =vertTool2D.distance(BSstate, TripletVtx).significance();
                        
 
                        FlightDistPVSV2.push_back(distance);
                        FlightDistPVSV2_Err.push_back(dist_err);
                        FlightDistPVSV2_Significance.push_back(dist_sign);
                        //FlightDistPVSV2_chi2.push_back(chi2);
                        FlightDistBS_SV.push_back(BSdistance2D);
                        FlightDistBS_SV_Err.push_back(BSdist_err2D);
                        FlightDistBS_SV_Significance.push_back(BSdist_sign2D);

                        x_bs = beamSpot_new.x0();
                        y_bs = beamSpot_new.y0();
                        z_bs = beamSpot_new.z0();

                        cout<<"Old BS: "<<beamSpot.x0()<<" "<<beamSpot.y0()<<" "<<beamSpot.z0()<<endl;
                        cout<<"New BS: "<<beamSpot_new.x0()<<" "<<beamSpot_new.y0()<<" "<<beamSpot_new.z0()<<endl;
                        //Beam spot coordinates
                        BS_x.push_back(x_bs);
                        BS_y.push_back(y_bs);
                        BS_z.push_back(z_bs);

                        /////Add dxy info
                        GlobalVector dir1(mu1->px(), mu1->py(),  mu1->pz()); //To compute sign of IP
                        GlobalVector dir2(mu2->px(), mu2->py(),  mu2->pz()); //To compute sign of IP
                        GlobalVector dir3(Track3->px(),  Track3->py(),    Track3->pz()); //To compute sign of IP
                        std::pair<bool,Measurement1D> signed_IP2D_mu1 = IPTools::signedTransverseImpactParameter(transientTrack1, dir1, PVertex);
                        std::pair<bool,Measurement1D> signed_IP2D_mu2 = IPTools::signedTransverseImpactParameter(transientTrack2, dir2, PVertex);
                        std::pair<bool,Measurement1D> signed_IP2D_mu3 = IPTools::signedTransverseImpactParameter(transientTrack3, dir3, PVertex);
                        //cout<<" IP mu1="<<signed_IP2D_mu1.second.value()<<" IP mu2="<<signed_IP2D_mu2.second.value()<<" IP mu3="<<signed_IP2D_mu3.second.value()<<endl;
                        dxy_mu1.push_back(signed_IP2D_mu1.second.value());
                        dxy_mu2.push_back(signed_IP2D_mu2.second.value());
                        dxy_mu3.push_back(signed_IP2D_mu3.second.value());
                        
                        dxyErr_mu1.push_back(signed_IP2D_mu1.second.error());
                        dxyErr_mu2.push_back(signed_IP2D_mu2.second.error());
                        dxyErr_mu3.push_back(signed_IP2D_mu3.second.error());
                       
                        /////////////////Study on phi->KK and K*->Kpi decays//////////////////////
                        /////min mu+track vtx chi2
                        double mu1_minvtxchi2 = 9999., mu2_minvtxchi2 = 9999., mu3_minvtxchi2 = 9999.;
                        double IsoTrack1_Pt  = -99, IsoTrack1_Eta = -99, IsoTrack1_Phi = -99;
                        double IsoTrack2_Pt  = -99, IsoTrack2_Eta = -99, IsoTrack2_Phi = -99;
                        double IsoTrack3_Pt  = -99, IsoTrack3_Eta = -99, IsoTrack3_Phi = -99;
                        for (std::vector<pat::PackedCandidate>::const_iterator cand = PFCands->begin(); cand != PFCands->end(); ++cand) {
                            if(! ((cand->pt()>0.4) && (fabs(cand->eta())<2.4) && (cand->trackerLayersWithMeasurement()>5) && (cand->pixelLayersWithMeasurement()>1) && (cand->trackHighPurity())) ) continue;
                            //track-PV dz<0.5
                            double dz = abs(cand->dz(PVertexPoint));
                            if(dz>=0.5) continue;

                            reco::Track add_track = *(cand->bestTrack());
                            //track-triplet collimation
                            double dR = sqrt( reco::deltaR2(PhiIt->eta(), PhiIt->phi(), add_track.eta(), add_track.phi()) );
                            if(dR>1) continue; //loose cut on track+tau collimation

                            //skip track matching with mu2 and mu3
                            double dR1 = sqrt( reco::deltaR2(Track1.eta(), Track1.phi(), add_track.eta(), add_track.phi()) );
                            double dR2 = sqrt( reco::deltaR2(Track2.eta(), Track2.phi(), add_track.eta(), add_track.phi()) );
                            double dR3 = sqrt( reco::deltaR2(Track_3.eta(), Track_3.phi(), add_track.eta(), add_track.phi()) );
                            if(dR1<0.01 || dR2<0.01 || dR3<0.01) continue;

                            reco::TransientTrack add_ttrack = theTransientTrackBuilder->build(*(cand->bestTrack()));
                            //mu1
                            if (cand->charge()*Track1.charge() < 0) { //OS
                                //build mu1-track vertex
                                std::vector<reco::TransientTrack> mu1_track;
                                mu1_track.push_back(transientTrack1);
                                mu1_track.push_back(add_ttrack);
                                //vertex fit
                                KalmanVertexFitter mu1_track_fitter (true);
                                TransientVertex mu1_track_vtx = mu1_track_fitter.vertex(mu1_track);
                                if(!mu1_track_vtx.isValid()) continue;

                                double vtxchi2 = mu1_track_vtx.totalChiSquared();
                                if (vtxchi2 < mu1_minvtxchi2) {mu1_minvtxchi2 = vtxchi2; IsoTrack1_Pt = add_track.pt(); IsoTrack1_Eta = add_track.eta(); IsoTrack1_Phi = add_track.phi();}
                            }//mu1
                            //mu2
                            if (cand->charge()*Track2.charge() < 0) { //OS
                                //build mu2-track vertex
                                std::vector<reco::TransientTrack> mu2_track;
                                mu2_track.push_back(transientTrack2);
                                mu2_track.push_back(add_ttrack);
                                //vertex fit
                                KalmanVertexFitter mu2_track_fitter (true);
                                TransientVertex mu2_track_vtx = mu2_track_fitter.vertex(mu2_track);
                                if(!mu2_track_vtx.isValid()) continue;

                                double vtxchi2 = mu2_track_vtx.totalChiSquared();
                                if (vtxchi2 < mu2_minvtxchi2) {mu2_minvtxchi2 = vtxchi2; IsoTrack2_Pt = add_track.pt(); IsoTrack2_Eta = add_track.eta(); IsoTrack2_Phi = add_track.phi();}
                            }//mu2
                            //mu3
                            if (cand->charge()*Track_3.charge() < 0) { //OS
                                //build mu1-track vertex
                                std::vector<reco::TransientTrack> mu3_track;
                                mu3_track.push_back(transientTrack3);
                                mu3_track.push_back(add_ttrack);
                                //vertex fit
                                KalmanVertexFitter mu3_track_fitter (true);
                                TransientVertex mu3_track_vtx = mu3_track_fitter.vertex(mu3_track);
                                if(!mu3_track_vtx.isValid()) continue;

                                double vtxchi2 = mu3_track_vtx.totalChiSquared();
                                if (vtxchi2 < mu3_minvtxchi2) {mu3_minvtxchi2 = vtxchi2; IsoTrack3_Pt = add_track.pt(); IsoTrack3_Eta = add_track.eta(); IsoTrack3_Phi = add_track.phi();}
                            }//mu3
                        }//loop on tracks
                        cout<<"min mu1+track vtx chi2="<<mu1_minvtxchi2<<" iso track pt="<<IsoTrack1_Pt<<" eta="<<IsoTrack1_Eta<<" phi="<<IsoTrack1_Phi<<endl;
                        cout<<"  collimation dR="<<sqrt( reco::deltaR2(Track1.eta(), Track1.phi(), IsoTrack1_Eta, IsoTrack1_Phi) )<<endl;
                        cout<<"min mu2+track vtx chi2="<<mu2_minvtxchi2<<" iso track pt="<<IsoTrack2_Pt<<" eta="<<IsoTrack2_Eta<<" phi="<<IsoTrack2_Phi<<endl;
                        cout<<"  collimation dR="<<sqrt( reco::deltaR2(Track2.eta(), Track2.phi(), IsoTrack2_Eta, IsoTrack2_Phi) )<<endl;
                        cout<<"min mu3+track vtx chi2="<<mu3_minvtxchi2<<" iso track pt="<<IsoTrack3_Pt<<" eta="<<IsoTrack3_Eta<<" phi="<<IsoTrack3_Phi<<endl;
                        cout<<"  collimation dR="<<sqrt( reco::deltaR2(Track_3.eta(), Track_3.phi(), IsoTrack3_Eta, IsoTrack3_Phi) )<<endl;
                        IsoTrackMu1_Pt.push_back(IsoTrack1_Pt); IsoTrackMu1_Eta.push_back(IsoTrack1_Eta); IsoTrackMu1_Phi.push_back(IsoTrack1_Phi);
                        IsoTrackMu2_Pt.push_back(IsoTrack2_Pt); IsoTrackMu2_Eta.push_back(IsoTrack2_Eta); IsoTrackMu2_Phi.push_back(IsoTrack2_Phi);
                        IsoTrackMu3_Pt.push_back(IsoTrack3_Pt); IsoTrackMu3_Eta.push_back(IsoTrack3_Eta); IsoTrackMu3_Phi.push_back(IsoTrack3_Phi);
   
                    }else{ //PVertex.isValid() && PhiIt->vertexChi2()>0
                        Mu01_Pt.push_back(-99);
                        Mu01_Eta.push_back(-99);
                        Mu01_Phi.push_back(-99);
                        Mu01_TripletIndex.push_back(-99);
                        
                        Mu02_Pt.push_back(-99);
                        Mu02_Eta.push_back(-99);
                        Mu02_Phi.push_back(-99);
                        Mu02_TripletIndex.push_back(-99);
                        
                        Tr_Pt.push_back(-99);
                        Tr_Eta.push_back(-99);
                        Tr_Phi.push_back(-99);
                        Tr_TripletIndex.push_back(-99);
                        
                        TripletVtx2_x.push_back(-99);
                        TripletVtx2_y.push_back(-99);
                        TripletVtx2_z.push_back(-99);
                        
                        TripletVtx2_Chi2.push_back(-99);
                        TripletVtx2_NDOF.push_back(-99);
                        
                        Triplet2_Mass.push_back(-99);
                        Triplet2_Pt.push_back(-99);
                        Triplet2_Eta.push_back(-99);
                        Triplet2_Phi.push_back(-99);
                        Triplet2_Charge.push_back(-99);
                        
                        Triplet_mindca_iso.push_back(-99);
                        Triplet_relativeiso.push_back(-99);
                        
                        Mu1_NTracks03iso.push_back(-99);
                        Mu2_NTracks03iso.push_back(-99);
                        Mu3_NTracks03iso.push_back(-99);
                        PV_x.push_back(-99);
                        PV_y.push_back(-99);
                        PV_z.push_back(-99);
                        PV_NTracks.push_back(-99);
                        RefittedPV2_x.push_back(-99);
                        RefittedPV2_y.push_back(-99);
                        RefittedPV2_z.push_back(-99);

                        BS_x.push_back(-99);
                        BS_y.push_back(-99);
                        BS_z.push_back(-99);

                        //RefittedPV2_Chi2.push_back(PVertex.);
                        Vtx12_Chi2.push_back(-99);
                        Vtx12_nDOF.push_back(-99);
                        Vtx12_x.push_back(-99);
                        Vtx12_y.push_back(-99);
                        Vtx12_z.push_back(-99);
                        Vtx23_Chi2.push_back(-99);
                        Vtx23_nDOF.push_back(-99);
                        Vtx23_x.push_back(-99);
                        Vtx23_y.push_back(-99);
                        Vtx23_z.push_back(-99);
                        Vtx13_Chi2.push_back(-99);
                        Vtx13_nDOF.push_back(-99);
                        Vtx13_x.push_back(-99);
                        Vtx13_y.push_back(-99);
                        Vtx13_z.push_back(-99);

                        RefTrack1_Pt.push_back(-99); RefTrack1_Eta.push_back(-99); RefTrack1_Phi.push_back(-99); RefTrack1_TripletIndex.push_back(-99);
                        RefTrack2_Pt.push_back(-99); RefTrack2_Eta.push_back(-99); RefTrack2_Phi.push_back(-99); RefTrack2_TripletIndex.push_back(-99);
                        RefTrack3_Pt.push_back(-99); RefTrack3_Eta.push_back(-99); RefTrack3_Phi.push_back(-99); RefTrack3_TripletIndex.push_back(-99);
                        RefittedSV_Chi2.push_back(-99);
                        RefittedSV_nDOF.push_back(-99);
                        RefittedSV_Mass.push_back(-99); 

                        IsoTrackMu1_Pt.push_back(-99); IsoTrackMu1_Eta.push_back(-99); IsoTrackMu1_Phi.push_back(-99);
                        IsoTrackMu2_Pt.push_back(-99); IsoTrackMu2_Eta.push_back(-99); IsoTrackMu2_Phi.push_back(-99);
                        IsoTrackMu3_Pt.push_back(-99); IsoTrackMu3_Eta.push_back(-99); IsoTrackMu3_Phi.push_back(-99);

                        Mu01_dRtriggerMatch.push_back(-99);
                        Mu02_dRtriggerMatch.push_back(-99);
                        Tr_dRtriggerMatch.push_back(-99);
                        
                        Mu1_dRtriggerMatch_Mu7.push_back(-99);
                        Mu2_dRtriggerMatch_Mu7.push_back(-99);
                        Mu3_dRtriggerMatch_Mu7.push_back(-99);
                        
                        Mu1_dRtriggerMatch_Mu8.push_back(-99);
                        Mu2_dRtriggerMatch_Mu8.push_back(-99);
                        Mu3_dRtriggerMatch_Mu8.push_back(-99);
                        
                        Mu1_dRtriggerMatch_Mu8_IP5.push_back(-99);
                        Mu1_dRtriggerMatch_Mu8_IP6.push_back(-99);
                        Mu1_dRtriggerMatch_Mu9_IP0.push_back(-99);
                        Mu1_dRtriggerMatch_Mu9_IP3.push_back(-99);
                        Mu1_dRtriggerMatch_Mu9_IP4.push_back(-99);
                        Mu1_dRtriggerMatch_Mu9_IP5.push_back(-99);
                        Mu1_dRtriggerMatch_Mu9_IP6.push_back(-99);
                        Mu1_dRtriggerMatch_Mu12_IP6.push_back(-99);
                        
                        Mu1_dRtriggerMatch_2017.push_back(-99);
                        Mu2_dRtriggerMatch_2017.push_back(-99);
                        Mu3_dRtriggerMatch_2017.push_back(-99);
                        
                        FlightDistPVSV2.push_back(-99);
                        FlightDistPVSV2_Err.push_back(-99);
                        FlightDistPVSV2_Significance.push_back(-99);
                        //FlightDistPVSV2_chi2.push_back(-99);
                        dxy_mu1.push_back(-99);
                        dxy_mu2.push_back(-99);
                        dxy_mu3.push_back(-99);
                        dxyErr_mu1.push_back(-99);
                        dxyErr_mu2.push_back(-99);
                        dxyErr_mu3.push_back(-99);
                        
                        GenMatchMu01_SimPt.push_back(-99);
                        GenMatchMu02_SimPt.push_back(-99);
                        GenMatchMu01_SimEta.push_back(-99);
                        GenMatchMu02_SimEta.push_back(-99);
                        GenMatchMu01_SimPhi.push_back(-99);
                        GenMatchMu02_SimPhi.push_back(-99);
                        
                        GenMatchMu01_Pt.push_back(-99);
                        GenMatchMu02_Pt.push_back(-99);
                        GenMatchMu01_Eta.push_back(-99);
                        GenMatchMu02_Eta.push_back(-99);
                        GenMatchMu01_Phi.push_back(-99);
                        GenMatchMu02_Phi.push_back(-99);
                        
                        Triplet_relativeiso2.push_back(-99);
                        
                        DistXY_PVSV.push_back(-99);
                        DistXY_significance_PVSV.push_back(-99);
                        Triplet_IsoMu1.push_back(-99);
                        Triplet_IsoMu2.push_back(-99);
                        Triplet_IsoMu3.push_back(-99);
                        
                        FlightDistBS_SV.push_back(-99);
                        FlightDistBS_SV_Err.push_back(-99);
                        FlightDistBS_SV_Significance.push_back(-99);

                        selectedTripletsIndex.push_back(-99);
                    }//!(PVertex.isValid() && PhiIt->vertexChi2()>0) 
                }//transTracksAssoToVtx_copy.size()>1
            }//VtxIdV.size()>0 && vertices->size()>0
        }//loop Cand2Mu1Track
    }//is2Mu
    
    NGoodTriplets.push_back(NTripl.size());
    if(NTripl.size()>0) hEventsAfterGoodCand->Fill(1);
    TripletCollectionSize2 = Cand2Mu1Track->size();
    SelectedTripletsSize = selectedTripletsIndex.size();
    //cout<<"***Number of triplets before selection="<<TripletCollectionSize2<<" after sel="<<SelectedTripletsSize<<endl;
    //cout<<"***Number of Muons="<<muons->size()<<endl;

    uint k=0;
    std::vector<int> MuFilter;
    vector<pat::Muon> MyMu, MyMu2, SyncMu;
    //double AllMuPt =0;
    MuonCollectionSize = muons->size();
    
    for(edm::View<pat::Muon>::const_iterator mu=muons->begin(); mu!=muons->end(), k<muons->size(); ++mu, ++k){
        
        MuFilter.push_back(1);
        MyMu.push_back(*mu);
        
        //Basic Kinematics
        MuonPt.push_back(mu->pt());
        MuonEta.push_back(mu->eta());
        MuonPhi.push_back(mu->phi());
        MuonEnergy.push_back(mu->energy());
        MuonCharge.push_back(mu->charge());
        
        Muon_PdgId.push_back(mu->simPdgId());
        Muon_MotherPdgId.push_back(mu->simMotherPdgId());
        Muon_simFlavour.push_back(mu->simFlavour());
        //Vtx position
        Muon_vx.push_back(mu->vx());
        Muon_vy.push_back(mu->vy());
        Muon_vz.push_back(mu->vz());
        
        //MuonID
        Muon_isGlobal.push_back(mu->isGlobalMuon());
        //Muon_isTracker.push_back(mu->isTrackerMuon());
        Muon_isSoft.push_back(mu->isSoftMuon(PV));
        Muon_isLoose.push_back(mu->isLooseMuon());
        Muon_isMedium.push_back(mu->isMediumMuon());
        Muon_isPF.push_back(mu->isPFMuon());
        Muon_isRPCMuon.push_back(mu->isRPCMuon());
        Muon_isStandAloneMuon.push_back(mu->isStandAloneMuon());
        Muon_isTrackerMuon.push_back(mu->isTrackerMuon());
        Muon_isCaloMuon.push_back(mu->isCaloMuon());
        Muon_isQualityValid.push_back(mu->isQualityValid());
        Muon_isTimeValid.push_back(mu->isTimeValid());
        Muon_isIsolationValid.push_back(mu->isIsolationValid());
        Muon_numberOfMatchedStations.push_back(mu->numberOfMatchedStations());
        Muon_numberOfMatches.push_back(mu->numberOfMatches(reco::Muon::SegmentArbitration));
        Muon_SoftMVA_Val.push_back(mu->softMvaValue());
        Muon_MVA.push_back(mu->mvaIDValue());
        Muon_timeAtIpInOut.push_back(mu->time().timeAtIpInOut);
        Muon_timeAtIpInOutErr.push_back(mu->time().timeAtIpInOutErr);
        
        std::vector<int> fvDThits{0, 0, 0, 0};
        std::vector<int> fvRPChits{0, 0, 0, 0};
        std::vector<int> fvCSChits{0, 0, 0, 0};

        float kVMuonHitComb = 0;
        if (mu->isGlobalMuon()) {
            reco::TrackRef gTrack = mu->globalTrack();
            const reco::HitPattern& gMpattern = gTrack->hitPattern();
            for (int i = 0; i < gMpattern.numberOfAllHits(reco::HitPattern::TRACK_HITS); i++) {
                uint32_t hit = gMpattern.getHitPattern(reco::HitPattern::TRACK_HITS, i);
                if (!gMpattern.validHitFilter(hit)) continue;
                int muStation0 = gMpattern.getMuonStation(hit) - 1;
                if (muStation0 >= 0 && muStation0 < 4) {
                    if(gMpattern.muonDTHitFilter(hit)) fvDThits[muStation0]++;
                    if(gMpattern.muonRPCHitFilter(hit)) fvRPChits[muStation0]++;
                    if(gMpattern.muonCSCHitFilter(hit)) fvCSChits[muStation0]++;
                }
            }

            for (unsigned int station = 0; station < 4; ++station) {
                kVMuonHitComb += (fvDThits[station]) / 2.;
                kVMuonHitComb += fvRPChits[station];
                if (fvCSChits[station] > 6) {
                    kVMuonHitComb += 6;
                }else{ kVMuonHitComb += fvCSChits[station]; }
            }
            Muon_validMuonHitComb.push_back(kVMuonHitComb);
        }else{ Muon_validMuonHitComb.push_back(-99); }

        if (mu->isGlobalMuon()) {
            Muon_GLnormChi2.push_back(mu->globalTrack()->normalizedChi2());
            Muon_GLhitPattern_numberOfValidMuonHits.push_back(mu->globalTrack()->hitPattern().numberOfValidMuonHits());
        }else{
            Muon_GLnormChi2.push_back(-999);
            Muon_GLhitPattern_numberOfValidMuonHits.push_back(-999);
        }
        
        if (mu->innerTrack().isNonnull()){
            Muon_trackerLayersWithMeasurement.push_back(mu->innerTrack()->hitPattern().trackerLayersWithMeasurement());
            bool ishighq = mu->innerTrack()->quality(reco::Track::highPurity);
            Muon_innerTrack_highPurity.push_back(ishighq);
            Muon_Numberofvalidpixelhits.push_back(mu->innerTrack()->hitPattern().numberOfValidPixelHits());
            Muon_innerTrack_ValidFraction.push_back( mu->innerTrack()->validFraction() );
            Muon_Numberofvalidtrackerhits.push_back(mu->innerTrack()->hitPattern().numberOfValidTrackerHits());
            Muon_innerTrack_p.push_back(mu->innerTrack()->p());
            Muon_innerTrack_eta.push_back(mu->innerTrack()->eta());
            Muon_innerTrack_phi.push_back(mu->innerTrack()->phi());
            Muon_innerTrack_normalizedChi2.push_back(mu->innerTrack()->normalizedChi2());
        }else{
            Muon_innerTrack_ValidFraction.push_back( -99);
            Muon_innerTrack_highPurity.push_back( -99);
            Muon_trackerLayersWithMeasurement.push_back(-999);
            Muon_Numberofvalidpixelhits.push_back(-999);
            Muon_Numberofvalidtrackerhits.push_back(-999);
            Muon_trackerLayersWithMeasurement.push_back(-999);
            Muon_innerTrack_p.push_back(-999);
            Muon_innerTrack_eta.push_back(-999);
            Muon_innerTrack_phi.push_back(-999);
            Muon_innerTrack_normalizedChi2.push_back(-999);
        }
        if (mu->outerTrack().isNonnull()){
            Muon_outerTrack_p.push_back(mu->outerTrack()->p());
            Muon_outerTrack_eta.push_back(mu->outerTrack()->eta());
            Muon_outerTrack_phi.push_back(mu->outerTrack()->phi());
            Muon_outerTrack_normalizedChi2.push_back(mu->outerTrack()->normalizedChi2());
            Muon_outerTrack_muonStationsWithValidHits.push_back(mu->outerTrack()->hitPattern().muonStationsWithValidHits());
        }else{
            Muon_outerTrack_p.push_back(-999);
            Muon_outerTrack_eta.push_back(-999);
            Muon_outerTrack_phi.push_back(-999);
            Muon_outerTrack_normalizedChi2.push_back(-999);
            Muon_outerTrack_muonStationsWithValidHits.push_back(-999);
        }
        if (mu->innerTrack().isNonnull() && mu->outerTrack().isNonnull()){
            Muon_QInnerOuter.push_back(mu->outerTrack()->charge()*mu->innerTrack()->charge());
        }else{ Muon_QInnerOuter.push_back(-999); }
        
        Muon_combinedQuality_updatedSta.push_back(mu->combinedQuality().updatedSta);
        Muon_combinedQuality_trkKink.push_back(mu->combinedQuality().trkKink);
        Muon_combinedQuality_glbKink.push_back(mu->combinedQuality().glbKink);
        Muon_combinedQuality_trkRelChi2.push_back(mu->combinedQuality().trkRelChi2);
        Muon_combinedQuality_staRelChi2.push_back(mu->combinedQuality().staRelChi2);
        Muon_combinedQuality_chi2LocalPosition.push_back(mu->combinedQuality().chi2LocalPosition);
        Muon_combinedQuality_chi2LocalMomentum.push_back(mu->combinedQuality().chi2LocalMomentum);
        Muon_combinedQuality_localDistance.push_back(mu->combinedQuality().localDistance);
        Muon_combinedQuality_globalDeltaEtaPhi.push_back(mu->combinedQuality().globalDeltaEtaPhi);
        Muon_combinedQuality_tightMatch.push_back(mu->combinedQuality().tightMatch);
        Muon_combinedQuality_glbTrackProbability.push_back(mu->combinedQuality().glbTrackProbability);

        //muon-segment matching variables
        DsPhiPiTreeMakerMINI::fillMatchInfo(*mu);

        Muon_calEnergy_em.push_back(mu->calEnergy().em);
        Muon_calEnergy_emS9.push_back(mu->calEnergy().emS9);
        Muon_calEnergy_emS25.push_back(mu->calEnergy().emS25);
        Muon_calEnergy_had.push_back(mu->calEnergy().had);
        Muon_calEnergy_hadS9.push_back(mu->calEnergy().hadS9);
        
        Muon_segmentCompatibility.push_back(muon::segmentCompatibility(*mu));
        Muon_caloCompatibility.push_back(muon::caloCompatibility(*mu));
        
        Muon_ptErrOverPt.push_back( (mu->muonBestTrack()->ptError()/mu->muonBestTrack()->pt()) );
        Muon_BestTrackPt.push_back( mu->muonBestTrack()->pt() );
        Muon_BestTrackPtErr.push_back( mu->muonBestTrack()->ptError() );
        
        Muon_BestTrackEta.push_back( mu->muonBestTrack()->eta() );
        Muon_BestTrackEtaErr.push_back( mu->muonBestTrack()->etaError() );
        
        Muon_BestTrackPhi.push_back( mu->muonBestTrack()->phi() );
        Muon_BestTrackPhiErr.push_back( mu->muonBestTrack()->phiError() );
        
        const reco::MuonIsolation Iso03 = mu->isolationR03();
        const reco::MuonIsolation Iso05 = mu->isolationR05();
        if (mu->isIsolationValid()) {
            Muon_emEt03.push_back(Iso03.emEt);
            Muon_hadEt03.push_back(Iso03.hadEt);
            Muon_nJets03.push_back(Iso03.nJets);
            Muon_nTracks03.push_back(Iso03.nTracks);
            Muon_sumPt03.push_back(Iso03.sumPt);
            Muon_emVetoEt03.push_back(Iso03.emVetoEt);
            Muon_hadVetoEt03.push_back(Iso03.hadVetoEt);
            Muon_trackerVetoPt03.push_back(Iso03.trackerVetoPt);
            
            Muon_emEt05.push_back(Iso05.emEt);
            Muon_hadEt05.push_back(Iso05.hadEt);
            Muon_nJets05.push_back(Iso05.nJets);
            Muon_nTracks05.push_back(Iso05.nTracks);
            Muon_sumPt05.push_back(Iso05.sumPt);
            Muon_hadVetoEt05.push_back(Iso05.hadVetoEt);
            Muon_trackerVetoPt05.push_back(Iso05.trackerVetoPt);
            Muon_emVetoEt05.push_back(Iso05.emVetoEt);
            
        } else { // if isolation is not valid use -1 as default
            Muon_emEt03.push_back(-1);
            Muon_hadEt03.push_back(-1);
            Muon_nJets03.push_back(-1);
            Muon_nTracks03.push_back(-1);
            Muon_sumPt03.push_back(-1);
            
            Muon_hadVetoEt03.push_back(-1);
            Muon_emVetoEt03.push_back(-1);
            Muon_trackerVetoPt03.push_back(-1);
            
            Muon_emEt05.push_back(-1);
            Muon_hadEt05.push_back(-1);
            Muon_nJets05.push_back(-1);
            Muon_nTracks05.push_back(-1);
            Muon_sumPt05.push_back(-1);
            
            Muon_emVetoEt05.push_back(-1);
            Muon_trackerVetoPt05.push_back(-1);
            Muon_hadVetoEt05.push_back(-1);
        }
    }
    
    // Loop on tracks
    edm::View<pat::PackedCandidate>::const_iterator trIt = trackCollection->begin();
    edm::View<pat::PackedCandidate>::const_iterator trEnd = trackCollection->end();
    
    for (; trIt != trEnd; ++trIt){
        if( trIt->pt() <= 2 || abs(trIt->eta())>=2.4 || trIt->charge()==0 || trIt->trackerLayersWithMeasurement()<=5 || trIt->pixelLayersWithMeasurement()<1 || (!(trIt->hasTrackDetails())) ) continue;
        const reco::Track track = ( *(trIt->bestTrack()) );
    
        Track_pt.push_back(track.pt());
        Track_eta.push_back(track.eta());
        Track_phi.push_back(track.phi());
        Track_normalizedChi2.push_back(track.normalizedChi2());
        Track_numberOfValidHits.push_back(track.numberOfValidHits());
        Track_charge.push_back(track.charge());
        Track_dxy.push_back(track.dxy());
        Track_dxyError.push_back(track.dxyError());
        Track_dz.push_back(track.dz());
        Track_dzError.push_back(track.dzError());
        Track_vx.push_back(track.vx());
        Track_vy.push_back(track.vy());
        Track_vz.push_back(track.vz());
    }

    if (!iEvent.isRealData()){
        Handle<vector<PileupSummaryInfo> >  PupInfo;
        iEvent.getByToken(puToken_, PupInfo);
        puN = PupInfo->begin()->getTrueNumInteractions();
    }
  
    ////Synch Tree//////
    /*
    double maxPt =0; double maxPhi=0, maxEta=0; vector<pat::Muon> SyncSortedMu ;
    double maxTrPt =0; double maxTrPhi=0, maxTrEta=0; vector<reco::Track> SyncSortedTr ;
    for(uint i=0; i<SyncMu.size();i++){
        if(SyncMu.at(i).pt() > maxPt){
            maxPt  = SyncMu.at(i).pt();
            maxPhi = SyncMu.at(i).phi();
            maxEta = SyncMu.at(i).eta();
            SyncSortedMu.push_back(SyncMu.at(i));
        }
    }
    
    allmuons_pt.push_back(AllMuPt);
    
    leadmuon_pt.push_back(maxPt);
    leadmuon_eta.push_back(maxEta);
    leadmuon_phi.push_back(maxPhi);
    nmuons = SyncMu.size();
    nprimevtxs =vertices->size();
    
    edm::View<reco::Track>::const_iterator trIt  = trackCollection->begin();
    edm::View<reco::Track>::const_iterator trEnd = trackCollection->end();
    
    double AllTrPt=0;
    for (; trIt != trEnd; ++trIt){
        const reco::Track track = (*trIt);
        if(  (track.pt()>1) && (fabs(track.eta())<2.4) && (track.hitPattern().trackerLayersWithMeasurement()>5) && (track.hitPattern().pixelLayersWithMeasurement()>1)  ){
            AllTrPt +=trIt->pt();
            if(track.pt() > maxTrPt){
                maxTrPt = track.pt();
                maxTrEta = track.eta();
                maxTrPhi= track.phi();
            }
        }
    }
    
    alltracks_pt.push_back(AllTrPt);
    leadtrack_pt.push_back(maxTrPt);
    leadtrack_eta.push_back(maxTrEta);
    leadtrack_phi.push_back(maxTrPhi);
    */
    ///////SyncTree
    
    evt   = iEvent.id().event();
    run = iEvent.id().run();
    lumi = iEvent.luminosityBlock();
    
    //  SyncTree_->Fill();
    tree_->Fill();
    
    /*
    allmuons_pt.clear();
    alltracks_pt.clear();
    leadmuon_pt.clear();
    leadmuon_phi.clear();
    leadmuon_eta.clear();
    allmuons_pt.clear();
    leadtrack_pt.clear();
    leadtrack_eta.clear();
    leadtrack_phi.clear();
    nmuons = -999;
    */
    run= -999;
    evt= -999;
    lumi= -999;
    puN= -999;
    
    NGoodTriplets.clear();
    GenParticle_PdgId.clear();
    GenParticle_Pt.clear();
    GenParticle_Eta.clear();
    GenParticle_Phi.clear();
    GenParticle_isDs_mother.clear();
    GenParticle_isDs_daughters.clear();
    GenParticle_MotherPdgId.clear();
    evt_isPrompt.clear();
    
    MuonCollectionSize =0;
    MuonPt.clear();
    MuonEta.clear();
    MuonPhi.clear();
    
    Muon_PdgId.clear();
    Muon_MotherPdgId.clear();
    Muon_simFlavour.clear();
    MuonEnergy.clear();
    MuonCharge.clear();
    
    //Vtx position
    Muon_vx.clear();
    Muon_vy.clear();
    Muon_vz.clear();
    
    //MuonID
    Muon_isGlobal.clear();
    Muon_isSoft.clear();
    Muon_isLoose.clear();
    Muon_isMedium.clear();
    Muon_isPF.clear();
    Muon_isRPCMuon.clear();
    Muon_isStandAloneMuon.clear();
    Muon_isTrackerMuon.clear();
    Muon_isCaloMuon.clear();
    Muon_isQualityValid.clear();
    Muon_isTimeValid.clear();
    Muon_isIsolationValid.clear();
    Muon_numberOfMatchedStations.clear();
    Muon_numberOfMatches.clear();
    Muon_SoftMVA_Val.clear();
    Muon_MVA.clear();

    //MuonTime
    Muon_timeAtIpInOut.clear();
    Muon_timeAtIpInOutErr.clear();
    
    //Muon inner + outer track
    Muon_GLnormChi2.clear();
    Muon_GLhitPattern_numberOfValidMuonHits.clear();
    
    Muon_trackerLayersWithMeasurement.clear();
    Muon_Numberofvalidpixelhits.clear();
    
    Muon_validMuonHitComb.clear();
    Muon_innerTrack_ValidFraction.clear();
    Muon_Numberofvalidtrackerhits.clear();
    Muon_innerTrack_highPurity.clear();
    
    Muon_outerTrack_p.clear();
    Muon_outerTrack_eta.clear();
    Muon_outerTrack_phi.clear();
    Muon_outerTrack_normalizedChi2.clear();
    Muon_outerTrack_muonStationsWithValidHits.clear();
    Muon_innerTrack_p.clear();
    Muon_innerTrack_eta.clear();
    Muon_innerTrack_phi.clear();
    Muon_innerTrack_normalizedChi2.clear();
    Muon_QInnerOuter.clear();
    
    Muon_combinedQuality_updatedSta.clear();
    Muon_combinedQuality_trkKink.clear();
    Muon_combinedQuality_glbKink.clear();
    Muon_combinedQuality_trkRelChi2.clear();
    Muon_combinedQuality_staRelChi2.clear();
    Muon_combinedQuality_chi2LocalPosition.clear();
    Muon_combinedQuality_chi2LocalMomentum.clear();
    Muon_combinedQuality_localDistance.clear();
    Muon_combinedQuality_globalDeltaEtaPhi.clear();
    Muon_combinedQuality_tightMatch.clear();
    Muon_combinedQuality_glbTrackProbability.clear();

    Muon_combinedQuality_match1_dX.clear();
    Muon_combinedQuality_match1_pullX.clear();
    Muon_combinedQuality_match1_pullDxDz.clear();
    Muon_combinedQuality_match1_dY.clear();
    Muon_combinedQuality_match1_pullY.clear();
    Muon_combinedQuality_match1_pullDyDz.clear();
        
    Muon_combinedQuality_match2_dX.clear();
    Muon_combinedQuality_match2_pullX.clear();
    Muon_combinedQuality_match2_pullDxDz.clear();
    Muon_combinedQuality_match2_dY.clear();
    Muon_combinedQuality_match2_pullY.clear();
    Muon_combinedQuality_match2_pullDyDz.clear();

    Muon_calEnergy_em.clear();
    Muon_calEnergy_emS9.clear();
    Muon_calEnergy_emS25.clear();
    Muon_calEnergy_had.clear();
    Muon_calEnergy_hadS9.clear();
    
    Muon_segmentCompatibility.clear();
    Muon_caloCompatibility.clear();
    
    Muon_ptErrOverPt.clear();
    Muon_BestTrackPt.clear();
    Muon_BestTrackPtErr.clear();
    
    Muon_BestTrackEta.clear();
    Muon_BestTrackEtaErr.clear();
    
    Muon_BestTrackPhi.clear();
    Muon_BestTrackPhiErr.clear();
    
    Muon_emEt03.clear();
    Muon_hadEt03.clear();
    Muon_nJets03.clear();
    Muon_nTracks03.clear();
    Muon_sumPt03.clear();
    Muon_hadVetoEt03.clear();
    Muon_emVetoEt03.clear();
    Muon_trackerVetoPt03.clear();
    
    Muon_emEt05.clear();
    Muon_hadEt05.clear();
    Muon_nJets05.clear();
    Muon_nTracks05.clear();
    Muon_sumPt05.clear();
    Muon_hadVetoEt05.clear();
    Muon_emVetoEt05.clear();
    Muon_trackerVetoPt05.clear();
    
    Track_pt.clear();
    Track_eta.clear();
    Track_phi.clear();
    Track_normalizedChi2.clear();
    Track_numberOfValidHits.clear();
    Track_charge.clear();
    Track_dxy.clear();
    Track_dz.clear();
    Track_dxyError.clear();
    Track_dzError.clear();
    Track_vx.clear();
    Track_vy.clear();
    Track_vz.clear();

    PV_x.clear();
    PV_y.clear();
    PV_z.clear();
    PV_NTracks.clear();

    BS_x.clear();
    BS_y.clear();
    BS_z.clear();
    
    Vtx12_x.clear();
    Vtx23_x.clear();
    Vtx13_x.clear();
    Vtx12_y.clear();
    Vtx23_y.clear();
    Vtx13_y.clear();
    Vtx12_z.clear();
    Vtx23_z.clear();
    Vtx13_z.clear();
    Vtx12_Chi2.clear();
    Vtx23_Chi2.clear();
    Vtx13_Chi2.clear();
    Vtx12_nDOF.clear();
    Vtx23_nDOF.clear();
    Vtx13_nDOF.clear();
    
    Mu01_Pt.clear();
    Mu01_Eta.clear();
    Mu01_Phi.clear();
    Mu1_NTracks03iso.clear();
    
    Mu02_Pt.clear();
    Mu02_Eta.clear();
    Mu02_Phi.clear();
    Mu2_NTracks03iso.clear();
    
    Tr_Pt.clear();
    Tr_Eta.clear();
    Tr_Phi.clear();
    Mu3_NTracks03iso.clear();
    
    Mu01_TripletIndex.clear();
    Mu02_TripletIndex.clear();
    Tr_TripletIndex.clear();

    RefTrack1_Pt.clear();
    RefTrack1_Eta.clear();
    RefTrack1_Phi.clear();
    RefTrack1_TripletIndex.clear();

    RefTrack2_Pt.clear();
    RefTrack2_Eta.clear();
    RefTrack2_Phi.clear();
    RefTrack2_TripletIndex.clear();

    RefTrack3_Pt.clear();
    RefTrack3_Eta.clear();
    RefTrack3_Phi.clear();
    RefTrack3_TripletIndex.clear();

    RefittedSV_Chi2.clear();
    RefittedSV_nDOF.clear();
    RefittedSV_Mass.clear();
   
    IsoTrackMu1_Pt.clear();
    IsoTrackMu1_Eta.clear();
    IsoTrackMu1_Phi.clear();

    IsoTrackMu2_Pt.clear();
    IsoTrackMu2_Eta.clear();
    IsoTrackMu2_Phi.clear();

    IsoTrackMu3_Pt.clear();
    IsoTrackMu3_Eta.clear();
    IsoTrackMu3_Phi.clear();
 
    Mu01_dRtriggerMatch.clear();
    Mu02_dRtriggerMatch.clear();
    Tr_dRtriggerMatch.clear();
    
    Trigger_l1name.clear();
    Trigger_l1decision.clear();
    Trigger_l1prescale.clear();

    Trigger_hltname.clear();
    Trigger_hltdecision.clear();
    
    Mu1_dRtriggerMatch_Mu8_IP5.clear();
    Mu1_dRtriggerMatch_Mu8_IP6.clear();
    Mu1_dRtriggerMatch_Mu9_IP0.clear();
    Mu1_dRtriggerMatch_Mu9_IP3.clear();
    Mu1_dRtriggerMatch_Mu9_IP4.clear();
    Mu1_dRtriggerMatch_Mu9_IP5.clear();
    Mu1_dRtriggerMatch_Mu9_IP6.clear();
    Mu1_dRtriggerMatch_Mu12_IP6.clear();

    Mu1_dRtriggerMatch_Mu7.clear();
    Mu1_dRtriggerMatch_Mu8.clear();
    Mu2_dRtriggerMatch_Mu7.clear();
    Mu2_dRtriggerMatch_Mu8.clear();
    Mu3_dRtriggerMatch_Mu7.clear();
    Mu3_dRtriggerMatch_Mu8.clear();

    selectedTripletsIndex.clear();
    GenMatchMu01_SimPhi.clear();
    GenMatchMu02_SimPhi.clear();
    
    GenMatchMu01_SimPt.clear();
    GenMatchMu02_SimPt.clear();
    
    GenMatchMu01_SimEta.clear();
    GenMatchMu02_SimEta.clear();
    
    GenMatchMu01_Pt.clear();
    GenMatchMu02_Pt.clear();
    
    GenMatchMu01_Eta.clear();
    GenMatchMu02_Eta.clear();
    
    GenMatchMu01_Phi.clear();
    GenMatchMu02_Phi.clear();

    Triplet_mindca_iso.clear();
    Triplet_relativeiso.clear();
    Triplet_relativeiso2.clear();
 
    TripletCollectionSize2 = -99;
    SelectedTripletsSize = -99;
    TripletVtx2_x.clear();
    TripletVtx2_y.clear();
    TripletVtx2_z.clear();
    
    TripletVtx2_Chi2.clear();
    TripletVtx2_NDOF.clear();
    
    Triplet2_Mass.clear();
    Triplet2_Pt.clear();
    Triplet2_Eta.clear();
    Triplet2_Phi.clear();
    Triplet2_Charge.clear();
    dxy_mu1.clear();
    dxy_mu2.clear();
    dxy_mu3.clear();
    dxyErr_mu1.clear();
    dxyErr_mu2.clear();
    dxyErr_mu3.clear();
    RefittedPV2_x.clear();
    RefittedPV2_y.clear();
    RefittedPV2_z.clear();
    RefittedPV2_NTracks.clear();
    RefittedPV2_isValid.clear();
    //RefittedPV2_Chi2.push_back(PVertex.);
    RefittedPV_Chi2.clear();
    RefittedPV_nDOF.clear();
    PV_bis_Chi2.clear();
    PV_bis_nDOF.clear();
    
    FlightDistPVSV2.clear();
    FlightDistPVSV2_Err.clear();
    FlightDistPVSV2_Significance.clear();
    FlightDistPVSV2_chi2.clear();
    PVCollection_Size =0;
    
    DistXY_PVSV.clear();
    DistXY_significance_PVSV.clear();
    Triplet_IsoMu1.clear();
    Triplet_IsoMu2.clear();
    Triplet_IsoMu3.clear();
    FlightDistBS_SV.clear();
    FlightDistBS_SV_Err.clear();
    FlightDistBS_SV_Significance.clear();


    Mu1_dRtriggerMatch_2017.clear();
    Mu2_dRtriggerMatch_2017.clear();
    Mu3_dRtriggerMatch_2017.clear();

    MuonPt_HLT.clear();
    MuonEta_HLT.clear();
    MuonPhi_HLT.clear();
    MuonPt_HLT2017.clear();
    MuonEta_HLT2017.clear();
    MuonPhi_HLT2017.clear();
    MuonPt_HLT_Dimuon.clear();
    MuonEta_HLT_Dimuon.clear();
    MuonPhi_HLT_Dimuon.clear();
    
    MuonPt_HLT_DiMu_Incl.clear();
    MuonEta_HLT_DiMu_Incl.clear();
    MuonPhi_HLT_DiMu_Incl.clear();
    MuonPt_HLT_DiMu_Incl_displ.clear();
    MuonEta_HLT_DiMu_Incl_displ.clear();
    MuonPhi_HLT_DiMu_Incl_displ.clear();
    
    MuonPt_HLT_BPMu7.clear();
    MuonEta_HLT_BPMu7.clear();
    MuonPhi_HLT_BPMu7.clear();
    MuonPt_HLT_BPMu8.clear();
    MuonEta_HLT_BPMu8.clear();
    MuonPhi_HLT_BPMu8.clear();
    MuonPt_HLT_BPMu8_IP6.clear();
    MuonEta_HLT_BPMu8_IP6.clear();
    MuonPhi_HLT_BPMu8_IP6.clear();
    MuonPt_HLT_BPMu8_IP5.clear();
    MuonEta_HLT_BPMu8_IP5.clear();
    MuonPhi_HLT_BPMu8_IP5.clear();
    MuonPt_HLT_BPMu9_IP0.clear();
    MuonEta_HLT_BPMu9_IP0.clear();
    MuonPhi_HLT_BPMu9_IP0.clear();
    MuonPt_HLT_BPMu9_IP3.clear();
    MuonEta_HLT_BPMu9_IP3.clear();
    MuonPhi_HLT_BPMu9_IP3.clear();
    MuonPt_HLT_BPMu9_IP4.clear();
    MuonEta_HLT_BPMu9_IP4.clear();
    MuonPhi_HLT_BPMu9_IP4.clear();
    MuonPt_HLT_BPMu9_IP5.clear();
    MuonEta_HLT_BPMu9_IP5.clear();
    MuonPhi_HLT_BPMu9_IP5.clear();
    MuonPt_HLT_BPMu9_IP6.clear();
    MuonEta_HLT_BPMu9_IP6.clear();
    MuonPhi_HLT_BPMu9_IP6.clear();
    MuonPt_HLT_BPMu12_IP6.clear();
    MuonPhi_HLT_BPMu12_IP6.clear();
    Track_pdgId.clear();
    
    L1Muon_Pt.clear();
    L1Muon_Eta.clear();
    L1Muon_Phi.clear();
    L1Muon_EtaAtVtx.clear();
    L1Muon_PhiAtVtx.clear();
    L1Muon_BX.clear();
    L1Muon_Quality.clear();
    L1Muon_ChargeValid.clear();
    L1Muon_Charge.clear();
    L1Muon_TfMuonIndex.clear();
    L1Muon_rank.clear();
    L1Muon_isoSum.clear();

}
    
// ------------ method called once each job just before starting event loop  ------------
void DsPhiPiTreeMakerMINI::beginJob() {

    hEvents = fs->make<TH1F>("hEvents","hEvents",10,0,10);
    hEventsAfterGoodCand= fs->make<TH1F>("hEventsAfterGoodCand","hEventsAfterGoodCand",10,0,10);
    tree_ = fs->make<TTree>("ntuple","LFVTau ntuple");
    
    tree_->Branch("evt", &evt);
    tree_->Branch("run", &run);
    tree_->Branch("lumi", &lumi);
    tree_->Branch("NGoodTriplets", &NGoodTriplets);
    tree_->Branch("nPileUpInt", &puN);
    
    tree_->Branch("Trigger_l1name", &Trigger_l1name);
    tree_->Branch("Trigger_l1decision",&Trigger_l1decision);
    tree_->Branch("Trigger_l1prescale",&Trigger_l1prescale);
    
    tree_->Branch("Trigger_hltname",&Trigger_hltname);
    tree_->Branch("Trigger_hltdecision",&Trigger_hltdecision);
    
    tree_->Branch("GenParticle_PdgId", &GenParticle_PdgId);
    tree_->Branch("GenParticle_Pt", &GenParticle_Pt);
    tree_->Branch("GenParticle_Eta", &GenParticle_Eta);
    tree_->Branch("GenParticle_Phi", &GenParticle_Phi);
    tree_->Branch("GenParticle_isDs_mother", &GenParticle_isDs_mother);
    tree_->Branch("GenParticle_isDs_daughters", &GenParticle_isDs_daughters);
    tree_->Branch("GenParticle_MotherPdgId", &GenParticle_MotherPdgId);
    tree_->Branch("evt_isPrompt", &evt_isPrompt);
    
    tree_->Branch("MuonCollectionSize",&MuonCollectionSize);
    tree_->Branch("MuonPt",&MuonPt);
    tree_->Branch("MuonEnergy", &MuonEnergy);
    tree_->Branch("MuonCharge", &MuonCharge);
    tree_->Branch("MuonEta",&MuonEta);
    tree_->Branch("MuonPhi",&MuonPhi);
    tree_->Branch("Muon_PdgId", &Muon_PdgId);
    tree_->Branch("Muon_MotherPdgId", &Muon_MotherPdgId);
    tree_->Branch("Muon_simFlavour", &Muon_simFlavour);
    
    //Vtx position
    tree_->Branch("Muon_vx", &Muon_vx);
    tree_->Branch("Muon_vy", &Muon_vy);
    tree_->Branch("Muon_vz", &Muon_vz);
    
    //MuonID
    tree_->Branch("Muon_isGlobal", &Muon_isGlobal);
    //tree_->Branch("Muon_isTracker", &Muon_isTracker);
    tree_->Branch("Muon_isSoft", &Muon_isSoft);
    tree_->Branch("Muon_isLoose", &Muon_isLoose);
    tree_->Branch("Muon_isMedium", &Muon_isMedium);
    tree_->Branch("Muon_isPF", &Muon_isPF);
    tree_->Branch("Muon_isRPCMuon", &Muon_isRPCMuon);
    tree_->Branch("Muon_isStandAloneMuon", &Muon_isStandAloneMuon);
    tree_->Branch("Muon_isTrackerMuon", &Muon_isTrackerMuon);
    tree_->Branch("Muon_isCaloMuon", &Muon_isCaloMuon);
    tree_->Branch("Muon_isQualityValid", &Muon_isQualityValid);
    tree_->Branch("Muon_isTimeValid", &Muon_isTimeValid);
    tree_->Branch("Muon_isIsolationValid", &Muon_isIsolationValid);
    tree_->Branch("Muon_numberOfMatchedStations", &Muon_numberOfMatchedStations);
    tree_->Branch("Muon_numberOfMatches", &Muon_numberOfMatches);
    tree_->Branch("Muon_SoftMVA_Val", &Muon_SoftMVA_Val);
    tree_->Branch("Muon_MVA", &Muon_MVA);

    tree_->Branch("Muon_timeAtIpInOut",&Muon_timeAtIpInOut);
    tree_->Branch("Muon_timeAtIpInOutErr",&Muon_timeAtIpInOutErr);
    //Muon inner + outer track
    tree_->Branch("Muon_GLnormChi2", &Muon_GLnormChi2);
    tree_->Branch("Muon_GLhitPattern_numberOfValidMuonHits", &Muon_GLhitPattern_numberOfValidMuonHits);
    
    tree_->Branch("Muon_trackerLayersWithMeasurement", &Muon_trackerLayersWithMeasurement);
    tree_->Branch("Muon_Numberofvalidpixelhits", &Muon_Numberofvalidpixelhits);
    
    tree_->Branch("Muon_outerTrack_p", &Muon_outerTrack_p);
    tree_->Branch("Muon_outerTrack_eta", &Muon_outerTrack_eta);
    tree_->Branch("Muon_outerTrack_phi", &Muon_outerTrack_phi);
    tree_->Branch("Muon_outerTrack_normalizedChi2", &Muon_outerTrack_normalizedChi2);
    tree_->Branch("Muon_outerTrack_muonStationsWithValidHits", &Muon_outerTrack_muonStationsWithValidHits);
    tree_->Branch("Muon_innerTrack_p", &Muon_innerTrack_p);
    tree_->Branch("Muon_innerTrack_eta", &Muon_innerTrack_eta);
    
    tree_->Branch("Muon_innerTrack_phi", &Muon_innerTrack_phi);
    tree_->Branch("Muon_innerTrack_normalizedChi2", &Muon_innerTrack_normalizedChi2);
    tree_->Branch("Muon_QInnerOuter", &Muon_QInnerOuter);
    
    tree_->Branch("Muon_combinedQuality_updatedSta", &Muon_combinedQuality_updatedSta);
    tree_->Branch("Muon_combinedQuality_trkKink", &Muon_combinedQuality_trkKink);
    tree_->Branch("Muon_combinedQuality_glbKink", &Muon_combinedQuality_glbKink);
    tree_->Branch("Muon_combinedQuality_trkRelChi2", &Muon_combinedQuality_trkRelChi2);
    tree_->Branch("Muon_combinedQuality_staRelChi2", &Muon_combinedQuality_staRelChi2);
    tree_->Branch("Muon_combinedQuality_chi2LocalPosition", &Muon_combinedQuality_chi2LocalPosition);
    tree_->Branch("Muon_combinedQuality_chi2LocalMomentum", &Muon_combinedQuality_chi2LocalMomentum);
    tree_->Branch("Muon_combinedQuality_localDistance", &Muon_combinedQuality_localDistance);
    tree_->Branch("Muon_combinedQuality_globalDeltaEtaPhi", &Muon_combinedQuality_globalDeltaEtaPhi);
    tree_->Branch("Muon_combinedQuality_tightMatch", &Muon_combinedQuality_tightMatch);
    tree_->Branch("Muon_combinedQuality_glbTrackProbability", &Muon_combinedQuality_glbTrackProbability);

    tree_->Branch("Muon_combinedQuality_match1_dX", &Muon_combinedQuality_match1_dX);
    tree_->Branch("Muon_combinedQuality_match1_pullX", &Muon_combinedQuality_match1_pullX);
    tree_->Branch("Muon_combinedQuality_match1_pullDxDz", &Muon_combinedQuality_match1_pullDxDz);
    tree_->Branch("Muon_combinedQuality_match1_dY", &Muon_combinedQuality_match1_dY);
    tree_->Branch("Muon_combinedQuality_match1_pullY", &Muon_combinedQuality_match1_pullY);
    tree_->Branch("Muon_combinedQuality_match1_pullDyDz", &Muon_combinedQuality_match1_pullDyDz);

    tree_->Branch("Muon_combinedQuality_match2_dX", &Muon_combinedQuality_match2_dX);
    tree_->Branch("Muon_combinedQuality_match2_pullX", &Muon_combinedQuality_match2_pullX);
    tree_->Branch("Muon_combinedQuality_match2_pullDxDz", &Muon_combinedQuality_match2_pullDxDz);
    tree_->Branch("Muon_combinedQuality_match2_dY", &Muon_combinedQuality_match2_dY);
    tree_->Branch("Muon_combinedQuality_match2_pullY", &Muon_combinedQuality_match2_pullY);
    tree_->Branch("Muon_combinedQuality_match2_pullDyDz", &Muon_combinedQuality_match2_pullDyDz);
    
    tree_->Branch("Muon_calEnergy_em", &Muon_calEnergy_em);
    tree_->Branch("Muon_calEnergy_emS9", &Muon_calEnergy_emS9);
    tree_->Branch("Muon_calEnergy_emS25", &Muon_calEnergy_emS25);
    tree_->Branch("Muon_calEnergy_had", &Muon_calEnergy_had);
    tree_->Branch("Muon_calEnergy_hadS9", &Muon_calEnergy_hadS9);
    
    tree_->Branch("Muon_segmentCompatibility", &Muon_segmentCompatibility);
    tree_->Branch("Muon_caloCompatibility", &Muon_caloCompatibility);
    
    tree_->Branch("Muon_ptErrOverPt", &Muon_ptErrOverPt);
    tree_->Branch("Muon_BestTrackPt", &Muon_BestTrackPt);
    tree_->Branch("Muon_BestTrackPtErr", &Muon_BestTrackPtErr);
    tree_->Branch("Muon_BestTrackEta", &Muon_BestTrackEta);
    tree_->Branch("Muon_BestTrackEtaErr", &Muon_BestTrackEtaErr);
    tree_->Branch("Muon_BestTrackPhi", &Muon_BestTrackPhi);
    tree_->Branch("Muon_BestTrackPhiErr", &Muon_BestTrackPhiErr);
    
    tree_->Branch("Muon_emEt03", &Muon_emEt03);
    tree_->Branch("Muon_hadEt03", &Muon_hadEt03);
    tree_->Branch("Muon_nJets03", &Muon_nJets03);
    tree_->Branch("Muon_nTracks03", &Muon_nTracks03);
    tree_->Branch("Muon_sumPt03", &Muon_sumPt03);
    tree_->Branch("Muon_hadVetoEt03", &Muon_hadVetoEt03);
    tree_->Branch("Muon_emVetoEt03", &Muon_emVetoEt03);
    tree_->Branch("Muon_trackerVetoPt03", &Muon_trackerVetoPt03);

    tree_->Branch("Muon_emEt05", &Muon_emEt05);
    tree_->Branch("Muon_hadEt05", &Muon_hadEt05);
    tree_->Branch("Muon_nJets05", &Muon_nJets05);
    tree_->Branch("Muon_nTracks05", &Muon_nTracks05);
    tree_->Branch("Muon_sumPt05", &Muon_sumPt05);
    tree_->Branch("Muon_hadVetoEt05", &Muon_hadVetoEt05);
    tree_->Branch("Muon_emVetoEt05", &Muon_emVetoEt05);
    tree_->Branch("Muon_trackerVetoPt05", &Muon_trackerVetoPt05);
    
    tree_->Branch("Track_pt", &Track_pt);
    tree_->Branch("Track_eta", &Track_eta);
    tree_->Branch("Track_phi", &Track_phi);
    tree_->Branch("Track_normalizedChi2", &Track_normalizedChi2);
    tree_->Branch("Track_numberOfValidHits", &Track_numberOfValidHits);
    tree_->Branch("Track_charge", &Track_charge);
    tree_->Branch("Track_dxy", &Track_dxy);
    tree_->Branch("Track_dxyError", &Track_dxyError);
    tree_->Branch("Track_dz", &Track_dz);
    tree_->Branch("Track_dzError", &Track_dzError);
    tree_->Branch("Track_vx", &Track_vx);
    tree_->Branch("Track_vy", &Track_vy);
    tree_->Branch("Track_vz", &Track_vz);
    
    tree_->Branch("Muon_validMuonHitComb", &Muon_validMuonHitComb);
    tree_->Branch("Muon_innerTrack_ValidFraction", &Muon_innerTrack_ValidFraction);
    tree_->Branch("Muon_Numberofvalidtrackerhits", &Muon_Numberofvalidtrackerhits);
    tree_->Branch("Muon_innerTrack_highPurity", &Muon_innerTrack_highPurity);

    tree_->Branch("Track_pdgId", &Track_pdgId);
    tree_->Branch("TripletCollectionSize2", &TripletCollectionSize2);
    tree_->Branch("PVCollection_Size", &PVCollection_Size);
    tree_->Branch("PV_x", &PV_x);
    tree_->Branch("PV_y", &PV_y);
    tree_->Branch("PV_z", &PV_z);
    tree_->Branch("PV_NTracks", &PV_NTracks);

    tree_->Branch("BS_x", &BS_x);
    tree_->Branch("BS_y", &BS_y);
    tree_->Branch("BS_z", &BS_z);

    tree_->Branch("Vtx12_x", &Vtx12_x);
    tree_->Branch("Vtx23_x", &Vtx23_x);
    tree_->Branch("Vtx13_x", &Vtx13_x);
    tree_->Branch("Vtx12_y", &Vtx12_y);
    tree_->Branch("Vtx23_y", &Vtx23_y);
    tree_->Branch("Vtx13_y", &Vtx13_y);
    tree_->Branch("Vtx12_z", &Vtx12_z);
    tree_->Branch("Vtx23_z", &Vtx23_z);
    tree_->Branch("Vtx13_z", &Vtx13_z);
    tree_->Branch("Vtx12_Chi2", &Vtx12_Chi2);
    tree_->Branch("Vtx23_Chi2", &Vtx23_Chi2);
    tree_->Branch("Vtx13_Chi2", &Vtx13_Chi2);
    tree_->Branch("Vtx12_nDOF", &Vtx12_nDOF);
    tree_->Branch("Vtx23_nDOF", &Vtx23_nDOF);
    tree_->Branch("Vtx13_nDOF", &Vtx13_nDOF);
    
    tree_->Branch("SelectedTripletsSize", &SelectedTripletsSize);
    tree_->Branch("Mu01_Pt",&Mu01_Pt);
    tree_->Branch("Mu01_Eta", &Mu01_Eta);
    tree_->Branch("Mu01_Phi", &Mu01_Phi);
    tree_->Branch("Mu01_dRtriggerMatch", &Mu01_dRtriggerMatch);
    tree_->Branch("Mu01_TripletIndex", &Mu01_TripletIndex);
    tree_->Branch("Mu1_NTracks03iso", &Mu1_NTracks03iso);
    
    tree_->Branch("Mu02_Pt", &Mu02_Pt);
    tree_->Branch("Mu02_Eta", &Mu02_Eta);
    tree_->Branch("Mu02_Phi", &Mu02_Phi);
    tree_->Branch("Mu02_dRtriggerMatch", &Mu02_dRtriggerMatch);
    tree_->Branch("Mu02_TripletIndex", &Mu02_TripletIndex);
    tree_->Branch("Mu2_NTracks03iso", &Mu2_NTracks03iso);
    
    tree_->Branch("Tr_Pt", &Tr_Pt);
    tree_->Branch("Tr_Eta", &Tr_Eta);
    tree_->Branch("Tr_Phi", &Tr_Phi);
    tree_->Branch("Tr_dRtriggerMatch", &Tr_dRtriggerMatch);
    tree_->Branch("Tr_TripletIndex", &Tr_TripletIndex);
    tree_->Branch("Tr_NTracks03iso", &Mu3_NTracks03iso);
    
    tree_->Branch("selectedTripletsIndex", &selectedTripletsIndex);
 
    tree_->Branch("GenMatchMu01_SimPt", &GenMatchMu01_SimPt);
    tree_->Branch("GenMatchMu02_SimPt", &GenMatchMu02_SimPt);
    
    tree_->Branch("GenMatchMu01_SimEta", &GenMatchMu01_SimEta);
    tree_->Branch("GenMatchMu02_SimEta", &GenMatchMu02_SimEta);
    
    tree_->Branch("GenMatchMu01_SimPhi", &GenMatchMu01_SimPhi);
    tree_->Branch("GenMatchMu02_SimPhi", &GenMatchMu02_SimPhi);
    
    tree_->Branch("GenMatchMu01_Pt", &GenMatchMu01_Pt);
    tree_->Branch("GenMatchMu02_Pt", &GenMatchMu02_Pt);
    
    tree_->Branch("GenMatchMu01_Eta", &GenMatchMu01_Eta);
    tree_->Branch("GenMatchMu02_Eta", &GenMatchMu02_Eta);
    
    tree_->Branch("GenMatchMu01_Phi", &GenMatchMu01_Phi);
    tree_->Branch("GenMatchMu02_Phi", &GenMatchMu02_Phi);
   
    tree_->Branch("Triplet_mindca_iso", &Triplet_mindca_iso);
    tree_->Branch("Triplet_relativeiso", &Triplet_relativeiso);
    tree_->Branch("Triplet_relativeiso2", &Triplet_relativeiso2);

    tree_->Branch("TripletVtx2_x", &TripletVtx2_x);
    tree_->Branch("TripletVtx2_y", &TripletVtx2_y);
    tree_->Branch("TripletVtx2_z", &TripletVtx2_z);
    
    tree_->Branch("TripletVtx2_Chi2", &TripletVtx2_Chi2);
    tree_->Branch("TripletVtx2_NDOF", &TripletVtx2_NDOF);
    
    tree_->Branch("Triplet2_Mass", &Triplet2_Mass);
    tree_->Branch("Triplet2_Pt", &Triplet2_Pt);
    tree_->Branch("Triplet2_Eta", &Triplet2_Eta);
    tree_->Branch("Triplet2_Phi", &Triplet2_Phi);
    tree_->Branch("Triplet2_Charge", &Triplet2_Charge);
    
    tree_->Branch("RefittedPV2_x", &RefittedPV2_x);
    tree_->Branch("RefittedPV2_y", &RefittedPV2_y);
    tree_->Branch("RefittedPV2_z", &RefittedPV2_z);
    tree_->Branch("RefittedPV2_NTracks", &RefittedPV2_NTracks);
    tree_->Branch("RefittedPV2_isValid", &RefittedPV2_isValid);
    //RefittedPV2_Chi2.push_back(PVertex2.);
    tree_->Branch("RefittedPV_Chi2", &RefittedPV_Chi2);
    tree_->Branch("RefittedPV_nDOF", &RefittedPV_nDOF);
    tree_->Branch("PV_bis_Chi2", &PV_bis_Chi2);
    tree_->Branch("PV_bis_nDOF", &PV_bis_nDOF);
    
    tree_->Branch("FlightDistPVSV2", &FlightDistPVSV2);
    tree_->Branch("FlightDistPVSV2_Err", &FlightDistPVSV2_Err);
    tree_->Branch("FlightDistPVSV2_Significance", &FlightDistPVSV2_Significance);
    tree_->Branch("FlightDistPVSV2_chi2", &FlightDistPVSV2_chi2);

    tree_->Branch("dxy_mu1", &dxy_mu1);
    tree_->Branch("dxy_mu2", &dxy_mu2);
    tree_->Branch("dxy_mu3", &dxy_mu3);
    tree_->Branch("dxyErr_mu1", &dxyErr_mu1);
    tree_->Branch("dxyErr_mu2", &dxyErr_mu2);
    tree_->Branch("dxyErr_mu3", &dxyErr_mu3);
    
    tree_->Branch("DistXY_PVSV", &DistXY_PVSV);
    tree_->Branch("DistXY_significance_PVSV", &DistXY_significance_PVSV);
    tree_->Branch("Triplet_IsoMu1", &Triplet_IsoMu1);
    tree_->Branch("Triplet_IsoMu2", &Triplet_IsoMu2);
    tree_->Branch("Triplet_IsoMu3", &Triplet_IsoMu3);
    tree_->Branch("FlightDistBS_SV", &FlightDistBS_SV);
    tree_->Branch("FlightDistBS_SV_Err", &FlightDistBS_SV_Err);
    tree_->Branch("FlightDistBS_SV_Significance", &FlightDistBS_SV_Significance);

    tree_->Branch("RefTrack1_Pt",           &RefTrack1_Pt);
    tree_->Branch("RefTrack1_Eta",          &RefTrack1_Eta);
    tree_->Branch("RefTrack1_Phi",          &RefTrack1_Phi);
    tree_->Branch("RefTrack1_TripletIndex", &RefTrack1_TripletIndex);
    tree_->Branch("RefTrack2_Pt",           &RefTrack2_Pt);
    tree_->Branch("RefTrack2_Eta",          &RefTrack2_Eta);
    tree_->Branch("RefTrack2_Phi",          &RefTrack2_Phi);
    tree_->Branch("RefTrack2_TripletIndex", &RefTrack2_TripletIndex);
    tree_->Branch("RefTrack3_Pt",           &RefTrack3_Pt);
    tree_->Branch("RefTrack3_Eta",          &RefTrack3_Eta);
    tree_->Branch("RefTrack3_Phi",          &RefTrack3_Phi);
    tree_->Branch("RefTrack3_TripletIndex", &RefTrack3_TripletIndex);

    tree_->Branch("RefittedSV_Chi2", &RefittedSV_Chi2);
    tree_->Branch("RefittedSV_nDOF", &RefittedSV_nDOF);
    tree_->Branch("RefittedSV_Mass", &RefittedSV_Mass);

    tree_->Branch("IsoTrackMu1_Pt",         &IsoTrackMu1_Pt);
    tree_->Branch("IsoTrackMu1_Eta",        &IsoTrackMu1_Eta);
    tree_->Branch("IsoTrackMu1_Phi",        &IsoTrackMu1_Phi);
    tree_->Branch("IsoTrackMu2_Pt",         &IsoTrackMu2_Pt);
    tree_->Branch("IsoTrackMu2_Eta",        &IsoTrackMu2_Eta);
    tree_->Branch("IsoTrackMu2_Phi",        &IsoTrackMu2_Phi);
    tree_->Branch("IsoTrackMu3_Pt",         &IsoTrackMu3_Pt);
    tree_->Branch("IsoTrackMu3_Eta",        &IsoTrackMu3_Eta);
    tree_->Branch("IsoTrackMu3_Phi",        &IsoTrackMu3_Phi);

    tree_->Branch("Mu1_dRtriggerMatch_Mu7", &Mu1_dRtriggerMatch_Mu7);
    tree_->Branch("Mu1_dRtriggerMatch_Mu8", &Mu1_dRtriggerMatch_Mu8);
    tree_->Branch("Mu2_dRtriggerMatch_Mu7", &Mu2_dRtriggerMatch_Mu7);
    tree_->Branch("Mu2_dRtriggerMatch_Mu8", &Mu2_dRtriggerMatch_Mu8);
    tree_->Branch("Mu3_dRtriggerMatch_Mu7", &Mu3_dRtriggerMatch_Mu7);
    tree_->Branch("Mu3_dRtriggerMatch_Mu8", &Mu3_dRtriggerMatch_Mu8);

    tree_->Branch("Mu1_dRtriggerMatch_Mu8_IP5", &Mu1_dRtriggerMatch_Mu8_IP5);
    tree_->Branch("Mu1_dRtriggerMatch_Mu8_IP6", &Mu1_dRtriggerMatch_Mu8_IP6);
    tree_->Branch("Mu1_dRtriggerMatch_Mu9_IP0", &Mu1_dRtriggerMatch_Mu9_IP0);
    tree_->Branch("Mu1_dRtriggerMatch_Mu9_IP3", &Mu1_dRtriggerMatch_Mu9_IP3);
    tree_->Branch("Mu1_dRtriggerMatch_Mu9_IP4", &Mu1_dRtriggerMatch_Mu9_IP4);
    tree_->Branch("Mu1_dRtriggerMatch_Mu9_IP5", &Mu1_dRtriggerMatch_Mu9_IP5);
    tree_->Branch("Mu1_dRtriggerMatch_Mu9_IP6", &Mu1_dRtriggerMatch_Mu9_IP6);
    tree_->Branch("Mu1_dRtriggerMatch_Mu12_IP6", &Mu1_dRtriggerMatch_Mu12_IP6);

    tree_->Branch("Mu1_dRtriggerMatch_2017", &Mu1_dRtriggerMatch_2017);
    tree_->Branch("Mu2_dRtriggerMatch_2017", &Mu2_dRtriggerMatch_2017);
    tree_->Branch("Mu3_dRtriggerMatch_2017", &Mu3_dRtriggerMatch_2017);
    
    tree_->Branch("MuonPt_HLT2017", &MuonPt_HLT2017);
    tree_->Branch("MuonEta_HLT2017", &MuonEta_HLT2017);
    tree_->Branch("MuonPhi_HLT2017", &MuonPhi_HLT2017);
    tree_->Branch( "MuonPt_HLT_Dimuon",  &MuonPt_HLT_Dimuon);
    tree_->Branch("MuonEta_HLT_Dimuon", &MuonEta_HLT_Dimuon);
    tree_->Branch("MuonPhi_HLT_Dimuon", &MuonPhi_HLT_Dimuon);
    
    tree_->Branch("MuonPt_HLT_DiMu_Incl", &MuonPt_HLT_DiMu_Incl);
    tree_->Branch("MuonEta_HLT_DiMu_Incl", &MuonEta_HLT_DiMu_Incl);
    tree_->Branch("MuonPhi_HLT_DiMu_Incl", &MuonPhi_HLT_DiMu_Incl);
    tree_->Branch("MuonPt_HLT_DiMu_Incl_displ", &MuonPt_HLT_DiMu_Incl_displ);
    tree_->Branch("MuonEta_HLT_DiMu_Incl_displ", &MuonEta_HLT_DiMu_Incl_displ);
    tree_->Branch("MuonPhi_HLT_DiMu_Incl_displ", &MuonPhi_HLT_DiMu_Incl_displ);
    
    tree_->Branch("MuonPt_HLT", &MuonPt_HLT);
    tree_->Branch("MuonEta_HLT", &MuonEta_HLT);
    tree_->Branch("MuonPhi_HLT", &MuonPhi_HLT);
    
    if( isBParking){
        tree_->Branch("MuonPt_HLT_BPMu7", &MuonPt_HLT_BPMu7);
        tree_->Branch("MuonEta_HLT_BPMu7", &MuonEta_HLT_BPMu7);
        tree_->Branch("MuonPhi_HLT_BPMu7", &MuonPhi_HLT_BPMu7);
        tree_->Branch("MuonPt_HLT_BPMu8", &MuonPt_HLT_BPMu8);
        tree_->Branch("MuonEta_HLT_BPMu8", &MuonEta_HLT_BPMu8);
        tree_->Branch("MuonPhi_HLT_BPMu8", &MuonPhi_HLT_BPMu8);
        tree_->Branch("MuonPt_HLT_BPMu8_IP6", &MuonPt_HLT_BPMu8_IP6);
        tree_->Branch("MuonEta_HLT_BPMu8_IP6", &MuonEta_HLT_BPMu8_IP6);
        tree_->Branch("MuonPhi_HLT_BPMu8_IP6", & MuonPhi_HLT_BPMu8_IP6);
        tree_->Branch("MuonPt_HLT_BPMu8_IP5", &MuonPt_HLT_BPMu8_IP5);
        tree_->Branch("MuonEta_HLT_BPMu8_IP5", &MuonEta_HLT_BPMu8_IP5);
        tree_->Branch("MuonPhi_HLT_BPMu8_IP5", &MuonPhi_HLT_BPMu8_IP5);
        tree_->Branch("MuonPt_HLT_BPMu9_IP0", &MuonPt_HLT_BPMu9_IP0);
        tree_->Branch("MuonEta_HLT_BPMu9_IP0", &MuonEta_HLT_BPMu9_IP0);
        tree_->Branch("MuonPhi_HLT_BPMu9_IP0", &MuonPhi_HLT_BPMu9_IP0);
        tree_->Branch("MuonPt_HLT_BPMu9_IP3", &MuonPt_HLT_BPMu9_IP3);
        tree_->Branch("MuonEta_HLT_BPMu9_IP3", &MuonEta_HLT_BPMu9_IP3);
        tree_->Branch("MuonPhi_HLT_BPMu9_IP3", &MuonPhi_HLT_BPMu9_IP3);
        tree_->Branch("MuonPt_HLT_BPMu9_IP4", &MuonPt_HLT_BPMu9_IP4);
        tree_->Branch("MuonEta_HLT_BPMu9_IP4", &MuonEta_HLT_BPMu9_IP4);
        tree_->Branch("MuonPhi_HLT_BPMu9_IP4", &MuonPhi_HLT_BPMu9_IP4);
        tree_->Branch("MuonPt_HLT_BPMu9_IP5", &MuonPt_HLT_BPMu9_IP5);
        tree_->Branch("MuonEta_HLT_BPMu9_IP5", &MuonEta_HLT_BPMu9_IP5);
        tree_->Branch("MuonPhi_HLT_BPMu9_IP5", &MuonPhi_HLT_BPMu9_IP5);
        tree_->Branch("MuonPt_HLT_BPMu9_IP6", &MuonPt_HLT_BPMu9_IP6);
        tree_->Branch("MuonEta_HLT_BPMu9_IP6", &MuonEta_HLT_BPMu9_IP6);
        tree_->Branch("MuonPhi_HLT_BPMu9_IP6", &MuonPhi_HLT_BPMu9_IP6);
        tree_->Branch("MuonPt_HLT_BPMu12_IP6", &MuonPt_HLT_BPMu12_IP6);
        tree_->Branch("MuonEta_HLT_BPMu12_IP6", &MuonEta_HLT_BPMu12_IP6);
        tree_->Branch("MuonPhi_HLT_BPMu12_IP6", &MuonPhi_HLT_BPMu12_IP6);
    }
    
    tree_->Branch("L1Muon_Pt", &L1Muon_Pt);
    tree_->Branch("L1Muon_Eta", &L1Muon_Eta);
    tree_->Branch("L1Muon_Phi", &L1Muon_Phi);
    tree_->Branch("L1Muon_EtaAtVtx", &L1Muon_EtaAtVtx);
    tree_->Branch("L1Muon_PhiAtVtx", &L1Muon_PhiAtVtx);
    tree_->Branch("L1Muon_BX", &L1Muon_BX);
    tree_->Branch("L1Muon_Quality", &L1Muon_Quality);
    tree_->Branch("L1Muon_Charge", &L1Muon_Charge);
    tree_->Branch("L1Muon_ChargeValid", &L1Muon_ChargeValid);
    tree_->Branch("L1Muon_TfMuonIndex", &L1Muon_TfMuonIndex);
    tree_->Branch("L1Muon_rank", &L1Muon_rank);
    tree_->Branch("L1Muon_isoSum", &L1Muon_isoSum);
    
    /*
    SyncTree_ = fs->make<TTree>("t","Sync ntuple");
    SyncTree_ ->Branch("allmuons_pt",&allmuons_pt);
    SyncTree_->Branch("leadmuon_pt",&leadmuon_pt);
    SyncTree_->Branch("leadmuon_phi",&leadmuon_phi);
    SyncTree_->Branch("leadmuon_eta",&leadmuon_eta);
    SyncTree_->Branch("nmuons",&nmuons);
    SyncTree_->Branch("nprimevtxs",&nprimevtxs);
    
    SyncTree_->Branch("leadtrack_pt", &leadtrack_pt);
    SyncTree_->Branch("leadtrack_eta", &leadtrack_eta);
    SyncTree_->Branch("leadtrack_phi", &leadtrack_phi);
    SyncTree_->Branch("alltracks_pt", &alltracks_pt);
    SyncTree_->Branch("evt", &evt);
    SyncTree_->Branch("run", &run);
    SyncTree_->Branch("lumi", &lumi);
    */
}
    
    
// ------------ method called once each job just after ending the event loop  ------------
void DsPhiPiTreeMakerMINI::endJob() {
    tree_->GetDirectory()->cd();
    tree_->Write();
    //  SyncTree_->GetDirectory()->cd();
    //  SyncTree_->Write();
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void DsPhiPiTreeMakerMINI::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
    //The following says we do not know what parameters are allowed so do no validation
    // Please change this to state exactly what you do use, even if it is no parameters
    edm::ParameterSetDescription desc;
    desc.setUnknown();
    //desc.add<edm::InputTag>("algInputTag", edm::InputTag("gtStage2Digis"));
    //desc.add<edm::InputTag>("extInputTag", edm::InputTag("gtStage2Digis"));
    descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(DsPhiPiTreeMakerMINI);
