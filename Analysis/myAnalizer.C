 #define myAnalizer_cxx

#define NCUTS 9
#define NMU 3
#define mumass 0.1056583715
#define PhiMass 1.019461 // Phi mass in GeV
#define OmegaMass 0.78265 // Omega mass in GeV
#define ptmin 2.0

#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TRandom.h>
#include "myAnalizer.h"
#include "Utilities.C"
#include <stdio.h>
#include <iostream>

using namespace std;

void myAnalizer::Loop_Tau3mu(TString type, TString datasetName)
{
    if (fChain == 0) return;
    Long64_t nentries = fChain->GetEntries();
    // Variables definition & init
    int cutevt[NCUTS] = {0};
    TString listCut[NCUTS];
    Fill_CutName(listCut);
    
    double isMC = -99;
    int L1seed = -99; int HLTpath = -99;
    double run_n = 0, lumi_n = 0, evt_n = 0, category = 0, L1 = 0, nHLT = 0, deltaR_max = 0, deltaZ_max = 0, Pmu3 = 0, cLP = 0, tKink = 0, segmComp = 0, tripletMass = 0, tripletMassReso = 0, fv_nC = 0, fv_dphi3D = 0, fv_d3D = 0, fv_d3Dsig = 0, bs_d2D = 0, bs_d2Dsig = 0, d0 = 0, MVA1=0, MVA2=0, MVA3=0, MVASoft1=0, MVASoft2=0, MVASoft3=0, nVtx=0, d0sig = 0, d0sig_max = 0,  mindca_iso = 0, trkRel = 0, Pmu1 = 0, Ptmu1 = 0, etamu1 = 0, phimu1 = 0, Pmu2 = 0, Ptmu2 = 0, etamu2 = 0, phimu2 = 0, Ptmu3 = 0, etamu3 = 0, phimu3 = 0, dispMu1=0, dispMu2=0, dispMu3=0, xydispMu1=0, xydispMu2=0, xydispMu3=0, P_trip = 0, Pt_trip = 0, eta_trip = 0, nStationsMu1 = 0, nStationsMu2 = 0, nStationsMu3 = 0, Iso03Mu1 = 0, Iso03Mu2 = 0, Iso03Mu3 = 0, Iso05Mu1 = 0, Iso05Mu2 = 0, Iso05Mu3 = 0, nMatchesMu1 = 0, nMatchesMu2 = 0, nMatchesMu3 = 0, timeAtIpInOutMu_sig1 = 0, timeAtIpInOutMu_sig2 = 0, timeAtIpInOutMu_sig3 = 0, cQ_uS = 0, cQ_tK, cQ_gK = 0, cQ_tRChi2 = 0, cQ_sRChi2 = 0, cQ_Chi2LP = 0, cQ_Chi2LM = 0, cQ_lD = 0, cQ_gDEP = 0, cQ_tM = 0, cQ_gTP = 0, calEn_emMu1 = 0, calEn_emMu2 = 0, calEn_emMu3 = 0, calEn_hadMu1 = 0, calEn_hadMu2 = 0, calEn_hadMu3 = 0, caloComp = 0, fliDistPVSV_Chi2 = 0, isGlb1 = 0, isMedium1 = 0, isTracker1 = 0, isLoose1 = 0,  isSoft1 = 0, SoftMVA1 = 0, isPF1 = 0, isRPC1 = 0, isSA1 = 0, isCalo1 = 0, isGlb2 = 0, isMedium2 = 0, isTracker2 = 0, isLoose2 = 0,  isSoft2 = 0, SoftMVA2 = 0, isPF2 = 0, isRPC2 = 0, isSA2 = 0, isCalo2 = 0, isGlb3 = 0, isMedium3 = 0, isTracker3 = 0, isLoose3 = 0, isSoft3 = 0, SoftMVA3 = 0, isPF3 = 0, isRPC3 = 0, isSA3 = 0, isCalo3 = 0, vx1 = 0, vx2 = 0, vx3 = 0, vy1 = 0, vy2 = 0, vy3 = 0, vz1 = 0, vz2 = 0, vz3 = 0, Refvx1 = 0, Refvx2 = 0, Refvx3 = 0, Refvy1 = 0, Refvy2 = 0, Refvy3 = 0, Refvz1 = 0, Refvz2 = 0, Refvz3 = 0, SVx = 0, SVy = 0, SVz = 0, had03 = 0, had05 = 0, nJets03 = 0, nJets05 = 0, nTracks03_mu1 = 0, nTracks03_mu2 = 0, nTracks03_mu3 = 0, nTracks05_mu1 = 0, nTracks05_mu2 = 0, nTracks05_mu3 = 0, sumPt03_mu1 = 0, sumPt03_mu2 = 0, sumPt03_mu3 = 0, sumPt05_mu1 = 0, sumPt05_mu2 = 0, sumPt05_mu3 = 0, hadVeto03 = 0, hadVeto05 = 0, emVeto03 = 0, emVeto05 = 0, trVeto03 = 0, trVeto05 = 0, EnMu1 = 0, EnMu2 = 0, EnMu3 = 0, ChargeMu1 = 0, ChargeMu2 = 0, ChargeMu3 = 0, isQValid1 = 0, isTValid1 = 0, isIsoValid1 = 0, GLnormChi2_mu1 = 0, GL_nValidMuHits1 = 0, trkLayersWMeas1 = 0, nValidPixelHits1 = 0, outerTrk_P_1 = 0, outerTrk_Eta_1 = 0, outerTrk_normChi2_1 = 0, outerTrk_muStValidHits_1 = 0, innerTrk_P_1 = 0, innerTrk_Eta_1 = 0, innerTrk_normChi2_1 = 0, QInnerOuter_1 = 0, cQ_uS_1 = 0, cQ_tK_1 = 0, cQ_gK_1 = 0, cQ_tRChi2_1 = 0, cQ_sRChi2_1 = 0, cQ_Chi2LP_1 = 0, cQ_Chi2LM_1 = 0, cQ_lD_1 = 0, cQ_gDEP_1 = 0, cQ_tM_1 = 0, cQ_gTP_1 = 0, segmComp_1 = 0, caloComp_1 = 0, isQValid2 = 0, isTValid2 = 0, isIsoValid2 = 0, GLnormChi2_mu2 = 0, GL_nValidMuHits2 = 0, trkLayersWMeas2 = 0, nValidPixelHits2 = 0, outerTrk_P_2 = 0, outerTrk_Eta_2 = 0, outerTrk_normChi2_2 = 0, outerTrk_muStValidHits_2 = 0, innerTrk_P_2 = 0, innerTrk_Eta_2 = 0, innerTrk_normChi2_2 = 0, QInnerOuter_2 = 0, cQ_uS_2 = 0, cQ_tK_2 = 0, cQ_gK_2 = 0, cQ_tRChi2_2 = 0, cQ_sRChi2_2 = 0, cQ_Chi2LP_2 = 0, cQ_Chi2LM_2 = 0, cQ_lD_2 = 0, cQ_gDEP_2 = 0, cQ_tM_2 = 0, cQ_gTP_2 = 0, segmComp_2 = 0, caloComp_2 = 0, isQValid3 = 0, isTValid3 = 0, isIsoValid3 = 0, GLnormChi2_mu3 = 0, GL_nValidMuHits3 = 0, trkLayersWMeas3 = 0, nValidPixelHits3 = 0, outerTrk_P_3 = 0, outerTrk_Eta_3 = 0, outerTrk_normChi2_3 = 0, outerTrk_muStValidHits_3 = 0, innerTrk_P_3 = 0, innerTrk_Eta_3 = 0, innerTrk_normChi2_3 = 0, QInnerOuter_3 = 0, cQ_uS_3 = 0, cQ_tK_3 = 0, cQ_gK_3 = 0, cQ_tRChi2_3 = 0, cQ_sRChi2_3 = 0, cQ_Chi2LP_3 = 0, cQ_Chi2LM_3 = 0, cQ_lD_3 = 0, cQ_gDEP_3 = 0, cQ_tM_3 = 0, cQ_gTP_3 = 0, segmComp_3 = 0, caloComp_3 = 0, inTrk_highPurity_1 = 0, inTrk_ValidFraction_1 = 0, NvalidTrkHits_1 = 0, validMuHitComb_1 = 0, IP2D_BS_1 = 0, IP3D_BS_1 = 0, IP2D_PV_1 = 0, IP3D_PV_1 = 0, inTrk_highPurity_2 = 0, inTrk_ValidFraction_2 = 0, NvalidTrkHits_2 = 0, validMuHitComb_2 = 0, IP2D_BS_2 = 0, IP3D_BS_2 = 0, IP2D_PV_2 = 0, IP3D_PV_2 = 0, inTrk_highPurity_3 = 0, inTrk_ValidFraction_3 = 0, NvalidTrkHits_3 = 0, validMuHitComb_3 = 0, IP2D_BS_3 = 0, IP3D_BS_3 = 0, IP2D_PV_3 = 0, IP3D_PV_3 = 0, inTrk_highPurity_max = 0, inTrk_ValidFraction_max = 0, NvalidTrkHits_max = 0, validMuHitComb_max = 0, IP2D_BS_max = 0, IP3D_BS_max = 0, IP2D_PV_max = 0, IP3D_PV_max = 0, inTrk_highPurity_min = 0, inTrk_ValidFraction_min = 0, NvalidTrkHits_min = 0, validMuHitComb_min = 0, IP2D_BS_min = 0, IP3D_BS_min = 0, IP2D_PV_min = 0, IP3D_PV_min = 0, tripl_IsoMu1 = 0, tripl_IsoMu2 = 0, tripl_IsoMu3 = 0, DistXYPVSV = 0, DistXY_PVSV_sig = 0, FlightDistBSSV = 0, FlightDistBS_SV_sig = 0, diMu12_mass = 0, diMu23_mass = 0, diMu13_mass = 0, cTau = 0, cTau2 = 0, NMu_TrMatch = 0, IP1 = 0, IP2 = 0, IP3 = 0, IP1_sig = 0, IP2_sig = 0, IP3_sig = 0, muSimPdgId_1 = 0, muSimMotherPdgId_1 = 0, muSimPdgId_2 = 0, muSimMotherPdgId_2 = 0, muSimPdgId_3 = 0, muSimMotherPdgId_3 = 0, NTrk_RefittedPV = 0, RefittedPV_Chi2norm = 0, diMuVtx_dist_max = 0, diMuVtx_dist_min = 0, Chi2IP_max = 0, dimu_OS1=0, dimu_OS2=0;
    int L1_DoubleMu0_er1p5 = 0, L1_DoubleMu0_er1p4 = 0, L1_DoubleMu4_dR1p2 = 0, L1_DoubleMu4p5_dR1p2 = 0, L1_DoubleMu0_er2p0 = 0, L1_DoubleMu0_er2p0_bk = 0, L1_TripleMu_5SQ_3SQ_0 = 0, L1_TripleMu_5SQ_3SQ_0OQ = 0, L1_TripleMu_3SQ_2p5SQ_0OQ_Mass_Max12 = 0, L1_TripleMu_2SQ_1p5SQ_0OQ_Mass_Max12 = 0;

    double match1_dX_1=0, match1_pullX_1=0, match1_pullDxDz_1=0, match1_dY_1=0, match1_pullY_1=0, match1_pullDyDz_1=0; 
    double match1_dX_2=0, match1_pullX_2=0, match1_pullDxDz_2=0, match1_dY_2=0, match1_pullY_2=0, match1_pullDyDz_2=0; 
    double match1_dX_3=0, match1_pullX_3=0, match1_pullDxDz_3=0, match1_dY_3=0, match1_pullY_3=0, match1_pullDyDz_3=0; 
    double match2_dX_1=0, match2_pullX_1=0, match2_pullDxDz_1=0, match2_dY_1=0, match2_pullY_1=0, match2_pullDyDz_1=0; 
    double match2_dX_2=0, match2_pullX_2=0, match2_pullDxDz_2=0, match2_dY_2=0, match2_pullY_2=0, match2_pullDyDz_2=0; 
    double match2_dX_3=0, match2_pullX_3=0, match2_pullDxDz_3=0, match2_dY_3=0, match2_pullY_3=0, match2_pullDyDz_3=0; 

    double validMuonHitComb1=0, validMuonHitComb2=0, validMuonHitComb3=0, nValidTrackerHits1=0, nValidTrackerHits2=0, nValidTrackerHits3=0;
    double innerTrk_ValidFraction_1=0, innerTrk_ValidFraction_2=0, innerTrk_ValidFraction_3=0, innerTrk_highPurity_1=0, innerTrk_highPurity_2=0, innerTrk_highPurity_3=0;

    // Creation of the output file
        TString root_fileName = fileName;
        TFile *fout = new TFile(root_fileName, "RECREATE");
        fout->cd();
        TTree *tree = new TTree("FinalTree","FinalTree");
        TreeFin_Init(tree, isMC, lumi_n, run_n, evt_n, pileupFactor, category, L1_DoubleMu0_er1p5, L1_DoubleMu0_er1p4, L1_DoubleMu4_dR1p2, L1_DoubleMu4p5_dR1p2, L1_DoubleMu0_er2p0, L1_DoubleMu0_er2p0_bk, L1_TripleMu_5SQ_3SQ_0, L1_TripleMu_5SQ_3SQ_0OQ, L1_TripleMu_3SQ_2p5SQ_0OQ_Mass_Max12, L1_TripleMu_2SQ_1p5SQ_0OQ_Mass_Max12, L1seed, HLTpath, deltaR_max, deltaZ_max, Pmu3, cLP, tKink, segmComp, tripletMass, tripletMassReso, fv_nC, fv_dphi3D, fv_d3D, fv_d3Dsig, bs_d2D, bs_d2Dsig, d0, nVtx, d0sig, MVA1, MVA2, MVA3, MVASoft1, MVASoft2, MVASoft3, d0sig_max, mindca_iso, trkRel, Pmu1, Ptmu1, etamu1, phimu1, Pmu2, Ptmu2, etamu2, phimu2, Ptmu3, etamu3, phimu3, dispMu1, dispMu2, dispMu3, xydispMu1, xydispMu2, xydispMu3, P_trip, Pt_trip, eta_trip, nStationsMu1, nStationsMu2, nStationsMu3, Iso03Mu1, Iso03Mu2, Iso03Mu3, Iso05Mu1, Iso05Mu2, Iso05Mu3, nMatchesMu1, nMatchesMu2, nMatchesMu3, timeAtIpInOutMu_sig1, timeAtIpInOutMu_sig2, timeAtIpInOutMu_sig3, cQ_uS, cQ_tK, cQ_gK, cQ_tRChi2, cQ_sRChi2, cQ_Chi2LP, cQ_Chi2LM, cQ_lD, cQ_gDEP, cQ_tM, cQ_gTP, calEn_emMu1, calEn_emMu2, calEn_emMu3, calEn_hadMu1, calEn_hadMu2, calEn_hadMu3, caloComp, fliDistPVSV_Chi2, isMedium1, isMedium2, isMedium3, isGlb1, isTracker1, isLoose1,  isSoft1, isPF1, isRPC1, isSA1, isCalo1, isGlb2, isTracker2, isLoose2,  isSoft2, isPF2, isRPC2, isSA2, isCalo2, isGlb3, isTracker3, isLoose3,  isSoft3, isPF3, isRPC3, isSA3, isCalo3, vx1, vx2, vx3, vy1, vy2, vy3, vz1, vz2, vz3, Refvx1, Refvx2, Refvx3, Refvy1, Refvy2, Refvy3, Refvz1, Refvz2, Refvz3, SVx, SVy, SVz, had03, had05, nJets03, nJets05, nTracks03_mu1, nTracks03_mu2, nTracks03_mu3, nTracks05_mu1, nTracks05_mu2, nTracks05_mu3, sumPt03_mu1, sumPt03_mu2, sumPt03_mu3, sumPt05_mu1, sumPt05_mu2, sumPt05_mu3, hadVeto03, hadVeto05, emVeto03, emVeto05, trVeto03, trVeto05, EnMu1, EnMu2, EnMu3, ChargeMu1, ChargeMu2, ChargeMu3, isQValid1, isTValid1, isIsoValid1, GLnormChi2_mu1, GL_nValidMuHits1, trkLayersWMeas1, nValidPixelHits1, outerTrk_P_1, outerTrk_Eta_1, outerTrk_normChi2_1, outerTrk_muStValidHits_1, innerTrk_P_1, innerTrk_Eta_1, innerTrk_normChi2_1, QInnerOuter_1, cQ_uS_1, cQ_tK_1, cQ_gK_1, cQ_tRChi2_1, cQ_sRChi2_1, cQ_Chi2LP_1, cQ_Chi2LM_1, cQ_lD_1, cQ_gDEP_1, cQ_tM_1, cQ_gTP_1, segmComp_1, caloComp_1, isQValid2, isTValid2, isIsoValid2, GLnormChi2_mu2, GL_nValidMuHits2, trkLayersWMeas2, nValidPixelHits2, outerTrk_P_2, outerTrk_Eta_2, outerTrk_normChi2_2, outerTrk_muStValidHits_2, innerTrk_P_2, innerTrk_Eta_2, innerTrk_normChi2_2, QInnerOuter_2, cQ_uS_2, cQ_tK_2, cQ_gK_2, cQ_tRChi2_2, cQ_sRChi2_2, cQ_Chi2LP_2, cQ_Chi2LM_2, cQ_lD_2, cQ_gDEP_2, cQ_tM_2, cQ_gTP_2, segmComp_2, caloComp_2, isQValid3, isTValid3, isIsoValid3, GLnormChi2_mu3, GL_nValidMuHits3, trkLayersWMeas3, nValidPixelHits3, outerTrk_P_3, outerTrk_Eta_3, outerTrk_normChi2_3, outerTrk_muStValidHits_3, innerTrk_P_3, innerTrk_Eta_3, innerTrk_normChi2_3, QInnerOuter_3, cQ_uS_3, cQ_tK_3, cQ_gK_3, cQ_tRChi2_3, cQ_sRChi2_3, cQ_Chi2LP_3, cQ_Chi2LM_3, cQ_lD_3, cQ_gDEP_3, cQ_tM_3, cQ_gTP_3, segmComp_3, caloComp_3, dimu_OS1, dimu_OS2, match1_dX_1, match1_pullX_1, match1_pullDxDz_1, match1_dY_1, match1_pullY_1, match1_pullDyDz_1, match2_dX_1, match2_pullX_1, match2_pullDxDz_1, match2_dY_1, match2_pullY_1, match2_pullDyDz_1, match1_dX_2, match1_pullX_2, match1_pullDxDz_2, match1_dY_2, match1_pullY_2, match1_pullDyDz_2, match2_dX_2, match2_pullX_2, match2_pullDxDz_2, match2_dY_2, match2_pullY_2, match2_pullDyDz_2, match1_dX_3, match1_pullX_3, match1_pullDxDz_3, match1_dY_3, match1_pullY_3, match1_pullDyDz_3, match2_dX_3, match2_pullX_3, match2_pullDxDz_3, match2_dY_3, match2_pullY_3, match2_pullDyDz_3, innerTrk_highPurity_1, innerTrk_highPurity_2, innerTrk_highPurity_3, innerTrk_ValidFraction_1, innerTrk_ValidFraction_2, innerTrk_ValidFraction_3, nValidTrackerHits1, nValidTrackerHits2, nValidTrackerHits3, validMuonHitComb1, validMuonHitComb2, validMuonHitComb3);

    TH1I *hCutEffEvt = new TH1I("CutEff_NEvents", "CutEff_NEvents", NCUTS, 0.5, (NCUTS+0.5));
    cout<< "datasetName: " << datasetName << endl;
    if(datasetName.Contains("2022") || datasetName.Contains("2023")) isMC=0;
    else{
        if(datasetName.Contains("Ds")) isMC=1;
        if(datasetName.Contains("Bp")) isMC=2;
        if(datasetName.Contains("B0")) isMC=3;
    }
    
    for (Long64_t jentry=0; jentry<nentries;jentry++) {
        Long64_t ientry = fChain->LoadTree(jentry);
        if (ientry < 0) break;
        fChain->GetTree()->GetEntry(ientry);
        // if (Cut(ientry) < 0) continue;
        //cout << endl << "Event n. " << jentry << endl;
        bool triplEff_counter[NCUTS] = {false};
        run_n = run; lumi_n = lumi; evt_n = evt;
        
        //Ncut = 0; cutevt[Ncut]++;
        triplEff_counter[0] = true;
        int mu_good[NMU] = {-99}; int mu_Ind_good[NMU] = {-99}; int ind_good = -99;
        vector<int> goodTriplInd;
      
        //CUT 0 : Before cuts - skip event if no good triplets
        if(NGoodTriplets->at(0) < 1) {cutevt[0]++; continue;}

        // CUT 1 : Check L1 & HLT decision
        bool L1_passed = false; bool HLT_passed = false; L1seed = 0; HLTpath = 0;
        L1_DoubleMu0_er1p5 = -99, L1_DoubleMu0_er1p4 = -99, L1_DoubleMu4_dR1p2 = -99, L1_DoubleMu4p5_dR1p2 = -99, L1_DoubleMu0_er2p0 = -99, L1_DoubleMu0_er2p0_bk = -99, L1_TripleMu_5SQ_3SQ_0 = -99, L1_TripleMu_5SQ_3SQ_0OQ = -99, L1_TripleMu_3SQ_2p5SQ_0OQ_Mass_Max12 = -99, L1_TripleMu_2SQ_1p5SQ_0OQ_Mass_Max12 = -99;
        for(int h=0; h<Trigger_l1name->size(); h++){
            TString l1Name = Trigger_l1name->at(h);
            if( (l1Name.Contains("L1_TripleMu_5SQ_3SQ_0_DoubleMu_5_3_SQ_OS_Mass_Max9") || l1Name.Contains("L1_TripleMu_5SQ_3SQ_0OQ_DoubleMu_5_3_SQ_OS_Mass_Max9") ||
                 l1Name.Contains("L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4") || l1Name.Contains("L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4") || l1Name.Contains("L1_DoubleMu4_SQ_OS_dR_Max1p2") || l1Name.Contains("L1_DoubleMu4p5_SQ_OS_dR_Max1p2") || l1Name.Contains("L1_TripleMu_2SQ_1p5SQ_0OQ_Mass_Max12") || l1Name.Contains("L1_TripleMu_3SQ_2p5SQ_0OQ_Mass_Max12") || l1Name.Contains("L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p6") || l1Name.Contains("L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p5") ) && Trigger_l1Finaldecision->at(h) == 1){
	       L1_passed = true; //cout << "L1 passed" << endl;
                if(l1Name.Contains("L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4") && Trigger_l1Finaldecision->at(h) == 1) {L1seed+=1; L1_DoubleMu0_er1p5 = 1;}
                if(l1Name.Contains("L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4") && Trigger_l1Finaldecision->at(h) == 1) L1_DoubleMu0_er1p4 = 1;
                if(l1Name.Contains("L1_DoubleMu4_SQ_OS_dR_Max1p2") && Trigger_l1Finaldecision->at(h) == 1) {L1seed+=10; L1_DoubleMu4_dR1p2=1;}
                if(l1Name.Contains("L1_DoubleMu4p5_SQ_OS_dR_Max1p2") && Trigger_l1Finaldecision->at(h) == 1) L1_DoubleMu4p5_dR1p2=1;
                if(l1Name.Contains("L1_TripleMu_5SQ_3SQ_0OQ_DoubleMu_5_3_SQ_OS_Mass_Max9") && Trigger_l1Finaldecision->at(h) == 1) { L1seed+=100; L1_TripleMu_5SQ_3SQ_0OQ=1;}
                if(l1Name.Contains("L1_TripleMu_5SQ_3SQ_0_DoubleMu_5_3_SQ_OS_Mass_Max9") && Trigger_l1Finaldecision->at(h) == 1) L1_TripleMu_5SQ_3SQ_0=1;
                if(l1Name.Contains("L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p6") && Trigger_l1Finaldecision->at(h) == 1) {L1seed+=1000; L1_DoubleMu0_er2p0=1;}
                if(l1Name.Contains("L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p5") && Trigger_l1Finaldecision->at(h) == 1) L1_DoubleMu0_er2p0_bk=1;
                if(l1Name.Contains("L1_TripleMu_2SQ_1p5SQ_0OQ_Mass_Max12") && Trigger_l1Finaldecision->at(h) == 1) {L1seed+=10000; L1_TripleMu_2SQ_1p5SQ_0OQ_Mass_Max12 = 1;}
                if(l1Name.Contains("L1_TripleMu_3SQ_2p5SQ_0OQ_Mass_Max12") && Trigger_l1Finaldecision->at(h) == 1) L1_TripleMu_3SQ_2p5SQ_0OQ_Mass_Max12 = 1;
            }
        }
        
        if(L1_passed) triplEff_counter[1] = true;
        else{
            cutevt[0]++;
            continue;
        }

        for(int h=0; h<Trigger_hltname->size(); h++){
            TString hltName = Trigger_hltname->at(h);
	    //cout << "HLT path: "<< hltName << " | decision: " << Trigger_hltdecision->at(h) << endl;
            if( hltName.Contains("HLT_DoubleMu3_TkMu_DsTau3Mu_v") && Trigger_hltdecision->at(h) == 1){
            //if( (hltName.Contains("HLT_DoubleMu3_TkMu_DsTau3Mu_v") || hltName.Contains("HLT_DoubleMu4_3_LowMass_v") || hltName.Contains("HLT_DoubleMu4_LowMass_Displaced_v")) && Trigger_hltdecision->at(h) == 1){
                HLT_passed = true;// cout << "HLT passed" << endl;
		if(hltName.Contains("HLT_DoubleMu3_TkMu_DsTau3Mu_v") && Trigger_hltdecision->at(h) == 1) HLTpath +=1;
		if(hltName.Contains("HLT_DoubleMu4_3_LowMass") && Trigger_hltdecision->at(h) == 1) HLTpath +=10;
        if(hltName.Contains("HLT_DoubleMu4_LowMass_Displaced") && Trigger_hltdecision->at(h) == 1) HLTpath +=100;
            }
        }

        if(HLT_passed) triplEff_counter[2] = true;

        if(!HLT_passed){
	     for(int i=0; i<2; i++){
            //cout << "triplEff_counter["<<i<<"] = "<< triplEff_counter[i] << endl;
             if(triplEff_counter[i] == true) cutevt[i]++;
                //cout << "It's true!"<< endl;
            }
            continue;
        }

      
        //Loop over the TRIPLETS
        bool goodTripl = false;
        for (int j=0; j<TripletVtx_Chi2->size(); j++){
            //cout << endl <<  "Triplet n. " << j << " | Triplet Chi2: " << TripletVtx_Chi2->at(j) << endl;
            double pt[NMU] = {0}, eta[NMU] = {0}, phi[NMU] = {0};
            int mu[NMU] = {0}; int mu_Ind[NMU] = {0};
            MatchIndex("ID", j, mu_Ind, mu);
            Get_MuonVariables(mu_Ind, pt, eta, phi);
            
            // Check duplicates
            if( abs(pt[0]-pt[1])<0.0001 || abs(eta[0]-eta[1])<0.0001 || abs(phi[0]-phi[1])<0.0001) continue;
            if( abs(pt[0]-pt[2])<0.0001 || abs(eta[0]-eta[2])<0.0001 || abs(phi[0]-phi[2])<0.0001) continue;
            if( abs(pt[2]-pt[1])<0.0001 || abs(eta[2]-eta[1])<0.0001 || abs(phi[2]-phi[1])<0.0001) continue;

            // CUT 2 : 3 Glb & Medium mu
            bool good_muonID = false;
            //if(Muon_isGlobal->at(mu[0]) == 1 && Muon_isPF->at(mu[0]) == 1 && Muon_isGlobal->at(mu[1]) == 1 && Muon_isPF->at(mu[1]) == 1 && (Muon_isGlobal->at(mu[2]) == 1 || Muon_isTrackerMuon->at(mu[2]) == 1) && Muon_isPF->at(mu[2]) == 1){
            if(Muon_isGlobal->at(mu[0]) == 1 && Muon_isMedium->at(mu[0]) == 1 && Muon_isGlobal->at(mu[1]) == 1 && Muon_isMedium->at(mu[1]) == 1 && Muon_isGlobal->at(mu[2]) == 1 && Muon_isMedium->at(mu[2]) == 1 && Mu1_Pt->at(j)>=2 && Mu2_Pt->at(j)>=2  && Mu3_Pt->at(j)>=2 && abs(Mu1_Eta->at(j))<=2.4 && abs(Mu2_Eta->at(j))<=2.4 && abs(Mu3_Eta->at(j))<=2.4){
            //if(Muon_isMedium->at(mu[0]) == 1 && Muon_isMedium->at(mu[1]) == 1 && Muon_isMedium->at(mu[2]) == 1 && Mu1_Pt->at(j)>=2 && Mu2_Pt->at(j)>=2  && Mu3_Pt->at(j)>=2 && abs(Mu1_Eta->at(j))<=2.4 && abs(Mu2_Eta->at(j))<=2.4 && abs(Mu3_Eta->at(j))<=2.4){
                 good_muonID = true; //cout << "goodMuonID" << endl;
            }
            if(!good_muonID) continue;
            else triplEff_counter[3] = true;
            
            // CUT 3: Sign BS-SV>=3.5 && deltaR<0.6 && |deltaZ|<2.5
            if( FlightDistBS_SV_Significance->at(j) < 3.5 ) continue;
            if( !(isPairDeltaRGood(j, 0.6)) ) continue;
            double vz1 = Muon_vz->at(mu[0]);
            double vz2 = Muon_vz->at(mu[1]);
            double vz3 = Muon_vz->at(mu[2]);
            if( !(isPairDeltaZGood(vz1, vz2, vz3, 2.5) )) continue;
            
            triplEff_counter[4] = true;
            
            
            // CUT 4 : TripletMass in [1.62-2] GeV
            bool good_triMuMass = false;
            if(Triplet_Mass->at(j)<=2 && Triplet_Mass->at(j)>=1.62){
                good_triMuMass = true; //cout << "goodTriMuMass" << endl;
            }
            if(!good_triMuMass) continue;
            else triplEff_counter[5] = true;
            
            // CUT 5 : HLT Trigger Matching
            bool triggerMatch[3] = {false, false, false};
            vector<double> HLT_obj_pt, HLT_obj_eta, HLT_obj_phi;
            
            if(HLTpath==1 || HLTpath==11 || HLTpath==101 || HLTpath==111){
                for(int i=0; i<MuonPt_HLT->size(); i++){
                    HLT_obj_pt.push_back(MuonPt_HLT->at(i));
                    HLT_obj_eta.push_back(MuonEta_HLT->at(i));
                    HLT_obj_phi.push_back(MuonPhi_HLT->at(i));
                }
                for(int f=0; f<NMU; f++){
                    for(int i=0; i<HLT_obj_pt.size(); i++){
                    double dphi = abs(phi[f] - HLT_obj_phi.at(i));
                    double deta = abs(eta[f] - HLT_obj_eta.at(i));
                    if(dphi > double(M_PI)) dphi -= double(2*M_PI);
                    double dR = TMath::Sqrt(dphi*dphi + deta*deta);
                    double dpt = abs(pt[f] - HLT_obj_pt.at(i))/pt[f];
                    // cout << "dR mu "<<f+1<<": " << dR << endl;
                    // cout << "dpt mu "<<f+1<<": " << dpt << endl;
                    if(dR<0.03 && dpt<0.1) triggerMatch[f] = true;
                    }
                }
	    }
            else{
                if(HLTpath>=100){
                    for(int i=0; i<MuonPt_HLT_DiMu_Incl_displ->size(); i++){
                        HLT_obj_pt.push_back(MuonPt_HLT_DiMu_Incl_displ->at(i));
                        HLT_obj_eta.push_back(MuonEta_HLT_DiMu_Incl_displ->at(i));
                        HLT_obj_phi.push_back(MuonPhi_HLT_DiMu_Incl_displ->at(i));
                    }
                }
                else{
                    for(int i=0; i<MuonPt_HLT_DiMu_Incl->size(); i++){
                        HLT_obj_pt.push_back(MuonPt_HLT_DiMu_Incl->at(i));
                        HLT_obj_eta.push_back(MuonEta_HLT_DiMu_Incl->at(i));
                        HLT_obj_phi.push_back(MuonPhi_HLT_DiMu_Incl->at(i));
                    }
                }
                for(int f=0; f<2; f++){
                    for(int i=0; i<HLT_obj_pt.size(); i++){
                    double dphi = abs(phi[f] - HLT_obj_phi.at(i));
                    double deta = abs(eta[f] - HLT_obj_eta.at(i));
                    if(dphi > double(M_PI)) dphi -= double(2*M_PI);
                    double dR = TMath::Sqrt(dphi*dphi + deta*deta);
                    double dpt = abs(pt[f] - HLT_obj_pt.at(i))/pt[f];
	            if(dR<0.03 && dpt<0.1) triggerMatch[f] = true;
                    }
                }
            if(triggerMatch[0] == true && triggerMatch[1] == true) triggerMatch[2] = true;
            }
            
            if(triggerMatch[0] == true) triplEff_counter[6] = true;
            if(triggerMatch[0] == true && triggerMatch[1] == true) triplEff_counter[7] = true;
            if(triggerMatch[0] == true && triggerMatch[1] == true && triggerMatch[2] == true) triplEff_counter[8] = true;
            
            if(triggerMatch[0] != true || triggerMatch[1] != true || triggerMatch[2] != true) continue;
            //else cout << "Good trigger Matching" << endl;
            
            if(triplEff_counter[0] == true){
                goodTripl = true; //cout << "Questo tripletto è buono!!!" << endl;
                goodTriplInd.push_back(j);
                //ind_good = j;
                for(int i=0; i<NMU; i++){
                    mu_Ind_good[i] = mu_Ind[i];
                    mu_good[i] = mu[i];
                }
            }
            else
                cout << "C'è un baco!!!" << endl;
        } // end loop on triplet
      
        for(int i=0; i<NCUTS; i++){
            if(triplEff_counter[i] == true)
                cutevt[i]++;
        }
        
        if(goodTripl){
            ind_good = BestTripletFinder(goodTriplInd);
            MatchIndex("ID", ind_good, mu_Ind_good, mu_good);
            TreeFin_Fill(tree, isMC, ind_good, mu_Ind_good, mu_good, lumi_n, run_n, evt_n, pileupFactor, category, L1_DoubleMu0_er1p5, L1_DoubleMu0_er1p4, L1_DoubleMu4_dR1p2, L1_DoubleMu4p5_dR1p2, L1_DoubleMu0_er2p0, L1_DoubleMu0_er2p0_bk, L1_TripleMu_5SQ_3SQ_0, L1_TripleMu_5SQ_3SQ_0OQ, L1_TripleMu_3SQ_2p5SQ_0OQ_Mass_Max12, L1_TripleMu_2SQ_1p5SQ_0OQ_Mass_Max12, L1seed, HLTpath, deltaR_max, deltaZ_max, Pmu3, cLP, tKink, segmComp, tripletMass, tripletMassReso, fv_nC, fv_dphi3D, fv_d3D, fv_d3Dsig, bs_d2D, bs_d2Dsig, d0, nVtx, d0sig, MVA1, MVA2, MVA3, MVASoft1, MVASoft2, MVASoft3, d0sig_max, mindca_iso, trkRel, Pmu1, Ptmu1, etamu1, phimu1, Pmu2, Ptmu2, etamu2, phimu2, Ptmu3, etamu3, phimu3, dispMu1, dispMu2, dispMu3, xydispMu1, xydispMu2, xydispMu3, P_trip, Pt_trip, eta_trip, nStationsMu1, nStationsMu2, nStationsMu3, Iso03Mu1, Iso03Mu2, Iso03Mu3, Iso05Mu1, Iso05Mu2, Iso05Mu3, nMatchesMu1, nMatchesMu2, nMatchesMu3, timeAtIpInOutMu_sig1, timeAtIpInOutMu_sig2, timeAtIpInOutMu_sig3, cQ_uS, cQ_tK, cQ_gK, cQ_tRChi2, cQ_sRChi2, cQ_Chi2LP, cQ_Chi2LM, cQ_lD, cQ_gDEP, cQ_tM, cQ_gTP, calEn_emMu1, calEn_emMu2, calEn_emMu3, calEn_hadMu1, calEn_hadMu2, calEn_hadMu3, caloComp, fliDistPVSV_Chi2, isMedium1, isMedium2, isMedium3, isGlb1, isTracker1, isLoose1,  isSoft1, isPF1, isRPC1, isSA1, isCalo1, isGlb2, isTracker2, isLoose2,  isSoft2, isPF2, isRPC2, isSA2, isCalo2, isGlb3, isTracker3, isLoose3,  isSoft3, isPF3, isRPC3, isSA3, isCalo3, vx1, vx2, vx3, vy1, vy2, vy3, vz1, vz2, vz3, Refvx1, Refvx2, Refvx3, Refvy1, Refvy2, Refvy3, Refvz1, Refvz2, Refvz3, SVx, SVy, SVz, had03, had05, nJets03, nJets05, nTracks03_mu1, nTracks03_mu2, nTracks03_mu3, nTracks05_mu1, nTracks05_mu2, nTracks05_mu3, sumPt03_mu1, sumPt03_mu2, sumPt03_mu3, sumPt05_mu1, sumPt05_mu2, sumPt05_mu3, hadVeto03, hadVeto05, emVeto03, emVeto05, trVeto03, trVeto05, EnMu1, EnMu2, EnMu3, ChargeMu1, ChargeMu2, ChargeMu3, isQValid1, isTValid1, isIsoValid1, GLnormChi2_mu1, GL_nValidMuHits1, trkLayersWMeas1, nValidPixelHits1, outerTrk_P_1, outerTrk_Eta_1, outerTrk_normChi2_1, outerTrk_muStValidHits_1, innerTrk_P_1, innerTrk_Eta_1, innerTrk_normChi2_1, QInnerOuter_1, cQ_uS_1, cQ_tK_1, cQ_gK_1, cQ_tRChi2_1, cQ_sRChi2_1, cQ_Chi2LP_1, cQ_Chi2LM_1, cQ_lD_1, cQ_gDEP_1, cQ_tM_1, cQ_gTP_1, segmComp_1, caloComp_1, isQValid2, isTValid2, isIsoValid2, GLnormChi2_mu2, GL_nValidMuHits2, trkLayersWMeas2, nValidPixelHits2, outerTrk_P_2, outerTrk_Eta_2, outerTrk_normChi2_2, outerTrk_muStValidHits_2, innerTrk_P_2, innerTrk_Eta_2, innerTrk_normChi2_2, QInnerOuter_2, cQ_uS_2, cQ_tK_2, cQ_gK_2, cQ_tRChi2_2, cQ_sRChi2_2, cQ_Chi2LP_2, cQ_Chi2LM_2, cQ_lD_2, cQ_gDEP_2, cQ_tM_2, cQ_gTP_2, segmComp_2, caloComp_2, isQValid3, isTValid3, isIsoValid3, GLnormChi2_mu3, GL_nValidMuHits3, trkLayersWMeas3, nValidPixelHits3, outerTrk_P_3, outerTrk_Eta_3, outerTrk_normChi2_3, outerTrk_muStValidHits_3, innerTrk_P_3, innerTrk_Eta_3, innerTrk_normChi2_3, QInnerOuter_3, cQ_uS_3, cQ_tK_3, cQ_gK_3, cQ_tRChi2_3, cQ_sRChi2_3, cQ_Chi2LP_3, cQ_Chi2LM_3, cQ_lD_3, cQ_gDEP_3, cQ_tM_3, cQ_gTP_3, segmComp_3, caloComp_3, dimu_OS1, dimu_OS2, match1_dX_1, match1_pullX_1, match1_pullDxDz_1, match1_dY_1, match1_pullY_1, match1_pullDyDz_1, match2_dX_1, match2_pullX_1, match2_pullDxDz_1, match2_dY_1, match2_pullY_1, match2_pullDyDz_1, match1_dX_2, match1_pullX_2, match1_pullDxDz_2, match1_dY_2, match1_pullY_2, match1_pullDyDz_2, match2_dX_2, match2_pullX_2, match2_pullDxDz_2, match2_dY_2, match2_pullY_2, match2_pullDyDz_2, match1_dX_3, match1_pullX_3, match1_pullDxDz_3, match1_dY_3, match1_pullY_3, match1_pullDyDz_3, match2_dX_3, match2_pullX_3, match2_pullDxDz_3, match2_dY_3, match2_pullY_3, match2_pullDyDz_3, innerTrk_highPurity_1, innerTrk_highPurity_2, innerTrk_highPurity_3, innerTrk_ValidFraction_1, innerTrk_ValidFraction_2, innerTrk_ValidFraction_3, nValidTrackerHits1, nValidTrackerHits2, nValidTrackerHits3, validMuonHitComb1, validMuonHitComb2, validMuonHitComb3);
        }
        
    } // end loop on events
    
    //Histo of cuts Efficiency
    TCanvas *canvEvt = new TCanvas("CutEfficiency_Nevents", "CutEfficiency_Nevents", 0, 0, 1200, 1000);
    Draw_CutEffCanvas(canvEvt, hCutEffEvt, cutevt, listCut);
    
    //Write and close the file
    fout->Write();
    fout->Close();
}

